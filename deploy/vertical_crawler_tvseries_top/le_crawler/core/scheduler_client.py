#!python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.cn'

import Queue
import time
import pickle
import base64
from threading import Thread
import threading
from thrift import Thrift
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from scrapy.utils.misc import load_object
from scrapy import log, signals
from scrapy.utils.reqser import request_to_dict, request_from_dict

from le_crawler.genpy.crawl.scheduler.ttypes import *
from le_crawler.genpy.crawl.scheduler import *
from le_crawler.genpy.crawl.ttypes import *
from le_crawler.base.thrift_util import str_to_thrift
from le_crawler.base.thrift_util import thrift_to_str
from le_crawler.base.url_normalize import UrlNormalize
from le_crawler.core.dupefilter import RFPDupeFilter
from request_compress import RequestDeCompress
from le_crawler.genpy.crawl.ttypes import CrawlDoc, CrawlDocType, CrawlDocAttachment, Request, Response, RedirectInfo

"""
this sheduler is using for thrift rpc, read more about:
  search2/crawler_ver2/proto/scheduler_service.thrift
"""

class SchedulerClient(object):
  def __init__(self, server_ip = "localhost", server_port = "8088", spider = None):
    self.__server_ip = server_ip
    self.__server_port = server_port
    self.__spider = spider
    self.__exit_sig = False
    self.__client = None
    self.__lock = threading.Lock()

  def open_connection(self):
    if not self.__create_scheduler_client(self.__server_ip,
        self.__server_port,
        864000):
      if self.__spider:
        self.__spider.log('can not create client for scheduler', log.ERROR)
      assert False, 'can not create client for scheduler'
      import sys
      sys.exit(1)

  def set_spider(self, spider = None):
    self.__spider = spider

  def __create_scheduler_client(self, host, port, try_num):
    self.__lock.acquire()
    if self.__client:
      try:
        if self.__client.ping():
          self.__lock.release()
          return True
      except:
        pass
    for i in range(1, try_num):
      try:
        if self.__spider:
          self.__spider.log('try connect to scheduler times[%s], exit signals [%s]'
              % (i, self.__exit_sig), log.INFO)
        if self.__exit_sig:
          print 'quit retry create connection for exit commond'
          return False
        tmptrsp = TSocket.TSocket(host, port)
        tmptrsp.setTimeout(6000)
        self.trsp = TTransport.TBufferedTransport(tmptrsp)
        self.proto = TBinaryProtocol.TBinaryProtocol(self.trsp)
        self.__client = SchedulerService.Client(self.proto)
        if self.__spider:
          self.__spider.log('create scheduler client: %s' % self.__client,
              log.INFO)
        self.trsp.open()
        self.__lock.release()
        if self.__spider:
          self.__spider.log('success connection to:%s, %s' % (host, port), log.INFO)
        return True
      except:
        time.sleep(5)
        print 'try connect times:[%s]' % i
        continue
    if self.__spider:
      self.__spider.log('Failed try connect for times[%s], quit' % try_num,
           log.ERROR)
    self.__lock.release()
    return False


  def close(self):
    self.__spider.log('client recive exit signals, closing', log.INFO)
    self.trsp.close()
    self.__exit_sig = True
    del self.__client
    self.__client = None

  # this ping_local should call before other api
  def ping_local(self, reconnect = False):
    try:
      return self.__client.ping()
    except:
      if reconnect:
        try:
          assert self.__create_scheduler_client(
              self.__server_ip,
              self.__server_port,
              864000
              ), 'Failed create connect to thrift server'
          return self.__client.ping()
        except Thrift.TException, e:
          print 'ping_local failed', e
      return False

  def get_crawldocs_local(self, requiret_num = 128, force = False):
    try:
      if self.ping_local(True):
        rets = self.__client.get_crawldocs(requiret_num, force)
        return rets
    except Exception, e:
      print e
      return []

  # return bool
  def set_crawldocs_local(self, docs):
    try:
      if not self.ping_local(True):
        return False
      self.__client.set_crawldocs(docs)
      return True
    except Exception, e:
      import traceback
      print traceback.format_exc()
      print e
      return False


class CrawlDocScheduler(object):
  """ thrift-rpc based scheduler """
  def __init__(self, thrift_client, dupefilter, persist, idle_before_close, crawler):
    self.crawler = crawler
    self.__client = thrift_client
    self.df = dupefilter
    self.idle_before_close = idle_before_close
    self.__cache_input = Queue.Queue(2048) # will be crawl item
    self.__cache_output = Queue.Queue(2048) # extract link crawl item
    self.__flush_request_thread = Thread(target = self.__flush_request,
        args = ())
    self.__exit_sig = False
    self.url_normalize = UrlNormalize.get_instance()
    self.persist = persist
    self.__flush_request_thread.start()
    #self.crawler.signals.connect(self.close_test, signal = signals.engine_stopped)
    #self.crawler.signals.connect(self.close_test, signal = signals.spider_closed)
    from scrapy.http import Request
    self.__mock_request = Request('http://www.example.com')
    self.__scheduler_count = 0
    self.__valid_request = 0

  def __len__(self):
    return self.__cache_input.qsize()

  @classmethod
  def from_settings(cls, settings, crawler):
    persist = settings.get('SCHEDULER_PERSIST', True)
    idle_before_close = settings.get('SCHEDULER_IDLE_BEFORE_CLOSE', 4)
    client_host = settings.get('CRAWLDOC_SCHEDULER_HOST', 'localhost')
    client_port = settings.get('CRAWLDOC_SCHEDULER_PORT', 8088)
    client = SchedulerClient(client_host, client_port)
    dupefilter_ins = load_object(
            settings['DUPEFILTER_CLASS']).from_settings(settings)
    return cls(client, dupefilter_ins, persist, idle_before_close, crawler)

  @classmethod
  def from_crawler(cls, crawler):
    instance = cls.from_settings(crawler.settings, crawler)
    instance.stats = crawler.stats
    return instance

  def _encode_request(self, request):
    """Encode a request object"""
    org_dict = request_to_dict(request, self.spider)
    red_dict = RequestDeCompress.reduce_request_dict(org_dict)
    return pickle.dumps(red_dict, protocol=1)
    #return zlib.compress(request.url)

  def _decode_request(self, encoded_request):
    """Decode an request previously encoded"""
    try:
      red_dict = pickle.loads(encoded_request)
      org_dict = RequestDeCompress.restore_request_dict(red_dict)
      return request_from_dict(org_dict, self.spider)
    except Exception, e:
      #import traceback
      #print 'Failed decode reqeust'
      #print traceback.format_exc()
      self.spider.log('Failed decode request:%s, %s' % (e.message, encoded_request))
      return None
    #return zlib.decompress(encoded_request)

  def __get_requests(self):
    if self.__cache_input.empty():
      reqs = self.__client.get_crawldocs_local()
      self.__scheduler_count += len(reqs)
      self.spider.log('Scheduler Counter:%s, Valid:%s' %
          (self.__scheduler_count, self.__valid_request), log.INFO)
      for i in reqs:
        self.__cache_input.put(i, timeout = 1)

  def __persistan_push(self, crawldocs):
    while not self.__client.set_crawldocs_local(crawldocs):
      str1 = 'Failed push crawldoc to scheduler: %s' % len(crawldocs)
      print str1
      self.spider.log(str1, log.ERROR)
      if not self.__exit_sig:
        time.sleep(4)
      else:
        break

  def __flush_request(self):
    flush_list = []
    max_idel_times = 3600 * 2
    idel_time = 0
    while not self.__exit_sig:
      try:
        req = self.__cache_output.get(timeout = 1)
        # make crawldoc
        crawldoc = CrawlDoc()
        crawldoc.docid = 4000300104
        crawldoc.content = req
        crawldoc.doctype = CrawlDocType.SCHEDULERMOCKDOC
        flush_list.append(crawldoc)
      except Queue.Empty, e:
        pass
      if len(flush_list) > 512 or idel_time >= max_idel_times:
        self.__persistan_push(flush_list)
        flush_list = []
        idel_time = 0
      else:
        idel_time += 1
    self.__persistan_push(flush_list)

  def open(self, spider):
    self.spider = spider
    self.__client.set_spider(spider)
    self.__client.open_connection()
    if self.idle_before_close < 0:
      self.idle_before_close = None
    if isinstance(self.df, RFPDupeFilter):
      self.df.set_spider(spider)

  def close(self, reason):
    if not self.persist:
      self.df.clear()
    self.__exit_sig = True
    while self.__flush_request_thread.isAlive():
      self.spider.log('wait for scheduler request push thread exit', log.INFO)
      time.sleep(1)
    self.__client.close()

  def __ignore_request(self, request, rawrequest = None):
    if not request.dont_filter:
      if not rawrequest:
        return self.df.request_seen(request)
      else:
        return self.df.request_seen(request) or self.df.request_seen(rawrequest)
    return False

  def enqueue_request(self, request):
    if not request:
        return
      # TODO(Xiaohe): move url normalize to some better place, for example
      # download middlewares
      # process request, url normalize
      # some place we dont need normalize url in process request or response
    tmpurl = self.url_normalize.get_unique_url(request.url)
    if not tmpurl:
      raise Exception('Bad request url:%s' % (request.url))
      return
    new_meta = request.meta.copy() or {}
    new_meta['Rawurl'] = request.url
    nrequest = request.replace(url = tmpurl, meta = new_meta)
    if self.__ignore_request(nrequest, request):
      return
    #if not request.dont_filter and self.df.request_seen(request):
    #  return
    encode_req = self._encode_request(nrequest)
    if not encode_req:
      self.spider.log('encode request error:%s' % request, log.ERROR)
      return
    if self.stats:
        self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
    while True:
      try:
        self.__cache_output.put(encode_req, timeout = 3)
        break
      except:
        self.spider.log('Failed put request to queue, %s' % e.message, log.ERROR)
        if self.__exit_sig:
          break

  def __next_request(self):
    try:
      encode_req = self.__cache_input.get(timeout = self.idle_before_close)
      request = None
      if encode_req:
        if encode_req.doctype == CrawlDocType.SCHEDULERMOCKDOC:
          request = self._decode_request(encode_req.content)
        else:
          self.spider.log('Un-supported doctype:%s'% encode_req.doctype, log.ERROR)
          return None
      else:
        return None
      if request and self.stats:
        self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
      if request and not request.meta.has_key('Rawurl'):
        tmpurl = self.url_normalize.get_unique_url(request.url)
        if not tmpurl:
          raise Exception('Bad request url:%s' % (request.url))
        nrequest = request.replace(url = tmpurl)
        return nrequest
      return request
    except Queue.Empty, e:
      self.__get_requests()
      return None
    except Exception, e:
      self.spider.log('Error while call __next_request:%s' % e.message, log.ERROR)
      return None

  def next_request(self):
    #TODO(xiaohe): solve scheduler loop for ever even recive shutdown signals,
    # when yremote db no more requests can be get
    req = None
    while not self.__exit_sig:
      req = self.__next_request()
      if req and not self.__ignore_request(req):
        self.spider.log('next request:%s' % req, log.DEBUG)
        self.__valid_request += 1
        return req
      else:
        time.sleep(2)
  def has_pending_requests(self):
    return self.__cache_input.qsize()
