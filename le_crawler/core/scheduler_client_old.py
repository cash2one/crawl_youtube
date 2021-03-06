#
# Copyright 2015 LeTV Inc. All Rights Reserved.

import Queue
import time
try:
  import cPickle as pickle
except:
  import pickle
from threading import Thread
import threading
from random import choice

import scrapy
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol
# from scrapy.utils.misc import load_object
from scrapy.utils.reqser import request_to_dict, request_from_dict

from ..proto.crawl.ttypes import Request, CrawlStatus
from ..proto.scheduler import SchedulerService
from ..proto.scheduler.ttypes import CrawlDocSlim
# from request_compress import RequestDeCompress


"""
this sheduler is using for thrift rpc, read more about:
  search2/crawler_ver2/le_crawler/proto/scheduler_service.thrift
"""


class SchedulerClient(object):
  def __init__(self, server_ip="localhost", server_port=8088):
    self.server_ip_ = server_ip
    self.server_port_ = server_port
    self.exit_sig_ = False
    self.client_ = None
    self.lock_ = threading.Lock()


  def open(self, logger):
    self._logger = logger
    self._create_scheduler_client(self.server_ip_, self.server_port_)


  def _create_scheduler_client(self, host, port, try_num=5):
    self.lock_.acquire()
    for i in range(1, try_num):
      try:
        tsocket = TSocket.TSocket(host, port)
        tsocket.setTimeout(10000)
        self.transport = TTransport.TBufferedTransport(tsocket)
        self.client_ = SchedulerService.Client(TCompactProtocol.TCompactProtocol(self.transport))
        self.transport.open()
        self._logger.info('create scheduler client: %s' % self.client_)
        break
      except:
        self._logger.exception('failed create scheduler client [%s/%s].', i, try_num)
        time.sleep(1)
        continue
    self.lock_.release()


  def close(self):
    self._logger.info('client receive exit signals, closing')
    self.transport.close()
    self.exit_sig_ = True


  def ping_local(self):
    try:
      return self.client_.ping()
    except:
      self._logger.exception('failed ping local.')
      time.sleep(1)
      try:
        self._create_scheduler_client(self.server_ip_, self.server_port_)
        return self.client_.ping()
      except:
        self._logger.exception('failed ping local again after recreate client.')
      return False


  def get_crawldocs_local(self, requiret_num=40):
    while 1:
      try:
        return self.client_.get_crawldocs(requiret_num)
      except:
        self._logger.exception('failed get crawl_docs.')
        self._create_scheduler_client(self.server_ip_, self.server_port_)
      time.sleep(1)


  # return bool
  def set_crawldocs_local(self, docs):
    while 1:
      try:
        self.client_.set_crawldocs(docs)
        self._logger.info('pushed crawl_doc to scheduler: %s', len(docs))
        return True
      except:
        self._logger.exception('failed set crawl_docs.')
        self._create_scheduler_client(self.server_ip_, self.server_port_)
      time.sleep(1)


class CrawlDocScheduler(object):
  """ thrift-rpc based scheduler """

  def __init__(self, thrift_client, persist, idle_before_close, crawler, request_pool_size):
    self.dedup_lock_ = threading.Lock()
    # self.dedup_client_ = BloomRedisClient('10.150.140.84', 8099)
    self.crawler = crawler
    self.stats = self.crawler.stats
    self.client_ = thrift_client
    self.idle_before_close = idle_before_close
    self.cache_input_ = Queue.Queue(request_pool_size)
    self.cache_upload_ = Queue.Queue(2048)
    self.flush_request_thread_ = Thread(target=self._flush_request)
    self.exit_sig_ = False
    self.persist = persist
    self.flush_request_thread_.start()
    # self.crawler.signals.connect(self.close_test, signal = signals.engine_stopped)
    # self.crawler.signals.connect(self.close_test, signal = signals.spider_closed)
    self.scheduler_count_ = 0
    self.valid_request_ = 0


  @classmethod
  def from_settings(cls, settings, crawler):
    persist = settings.get('SCHEDULER_PERSIST', True)
    idle_before_close = settings.get('SCHEDULER_IDLE_BEFORE_CLOSE', 4)
    request_pool_size = settings.get('SCHEDULER_REQUEST_POOL_SIZE', 50)
    client_host = settings.get('CRAWLDOC_SCHEDULER_HOST', 'localhost')
    client_port = settings.get('CRAWLDOC_SCHEDULER_PORT', 8088)
    client = SchedulerClient(client_host, client_port)
    # dupefilter_ins = load_object(settings['DUPEFILTER_CLASS']).from_settings(settings)
    return cls(client, persist, idle_before_close, crawler, request_pool_size)


  @classmethod
  def from_crawler(cls, crawler):
    return cls.from_settings(crawler.settings, crawler)


  def _encode_request(self, request):
    """Encode a request object"""
    request_dict = request_to_dict(request, self.spider_)
    # red_dict = RequestDeCompress.reduce_request_dict(request_dict)
    return self._request_to_crawldoc(request_dict, pickle.dumps(request_dict, protocol=1))


  def _request_to_crawldoc(self, request_dict, request_str):
    doc = request_dict['meta']['crawl_doc']
    doc.request = Request()
    doc.request.meta = request_str
    doc.request.dont_filter = request_dict.get('dont_filter', False)
    return doc


  def _decode_request(self, crawl_doc):
    """Decode an request previously encoded"""
    try:
      if not crawl_doc or not crawl_doc.request:
        self._logger.info('not crawl_doc request ')
        return None
      if not crawl_doc.request.meta:
        self._logger.info('got recalled request from scheduler service')
        return scrapy.http.Request(crawl_doc.url,
                                   callback=self.spider_.parse_page,
                                   meta={'crawl_doc': crawl_doc},
                                   dont_filter=True)
      red_dict = pickle.loads(crawl_doc.request.meta)
      # org_dict = RequestDeCompress.restore_request_dict(red_dict)
      return request_from_dict(red_dict, self.spider_)
    except:
      self._logger.exception('failed decode request: %s', crawl_doc.request.meta)
      return None


  def open(self, spider):
    self.spider_ = spider
    self._logger = spider._logger
    # self.len_start_urls_ = len(self.spider_.start_urls)
    # self._logger.info('Amount of start urls: %s', self.len_start_urls_)
    self.client_.open(self._logger)
    if self.idle_before_close < 0:
      self.idle_before_close = None
    # if isinstance(self.df, RFPDupeFilter):
    #   self.df.set_spider(spider)


  def close(self, reason):
    # if not self.persist:
    #   self.df.clear()
    self.exit_sig_ = True
    while self.flush_request_thread_.isAlive():
      self._logger.info('wait for scheduler request push thread exit')
      time.sleep(1)
    self.client_.close()


  def enqueue_request(self, request):
    self._logger.debug('<<<< enqueue request, %s' % request.url)
    if not request:
      self._logger.error('invalid request, skip.')
      return
    doc = self._encode_request(request)
    while 1:
      try:
        if self.cache_upload_.full():
          self._flush_queue()
        self.cache_upload_.put(doc, timeout=1)
        if self.stats:
          self.stats.inc_value('scheduler/enqueued/service', spider=self.spider_)
        break
      except:
        self._logger.exception('failed to put request to queue.')
        if self.exit_sig_:
          break


  def _persistan_push(self, crawldocs):
    if not crawldocs:
      self._logger.error('crawldocs empty, skip pushing.')
      return
    self._logger.debug('<<<< pushing requests to scheduler service, request num: %s' % len(crawldocs))
    return self.client_.set_crawldocs_local(crawldocs)


  def _cal_priority(self, doc):
    return doc.doc_type


  def _flush_queue(self):
    flush_list = []
    max_idle_times = 50  # 30 wait before persist push
    idle_times = 0
    doc = None
    while not self.cache_upload_.empty():
      try:
        doc = self.cache_upload_.get(timeout=1)
      except:
        doc = None
      if doc:
        self.spider_.update_status(doc.url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.SCHEDULING)})
        crawl_doc_slim = CrawlDocSlim(url=doc.url,
                                      crawl_doc=pickle.dumps(doc, protocol=2),
                                      priority=self._cal_priority(doc))
        flush_list.append(crawl_doc_slim)
        self.spider_.update_recrawl_info(url=doc.url,
                                         data={'next_schedule_time': int(time.time()) + 7200,
                                               'retry_times': 0,
                                               'crawl_doc_slim': pickle.dumps(crawl_doc_slim)})
      if idle_times >= max_idle_times:
        if self._persistan_push(flush_list):
          flush_list = []
          idle_times = 0
      else:
        idle_times += 1
    if flush_list:
      self._persistan_push(flush_list)


  def _flush_request(self):
    while not self.exit_sig_:
      self._flush_queue()
      time.sleep(1)
    self._flush_queue()


  def next_request(self):
    # TODO: solve scheduler loop for ever even receive shutdown signals, when remote db no more requests can be get
    # if self.len_start_urls_:
    #   self.len_start_urls_ -= 1
    #   return None
    docs = []
    # while self.cache_input_.empty():
    if self.cache_input_.empty():
      self._logger.info('local requests empty, fetch from scheduler service...')
      docs = self.client_.get_crawldocs_local(self.cache_input_.maxsize) or []
      if not docs:
        self._logger.info('no docs from scheduler service.')
      #   time.sleep(2)
      #   continue
        return None
      len_valid_docs = 0
      for doc_str in docs:
        if doc_str:
          doc = pickle.loads(doc_str)
          self.spider_.update_status(doc.url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.SCHEDULED)})
          len_valid_docs += 1
          self.cache_input_.put(doc, timeout=3)
      # if not self.cache_input_.empty():
      #   break
      if self.cache_input_.empty():
        self._logger.error('docs of scheduler invalid.')
        return None
      self.scheduler_count_ += len_valid_docs
      self._logger.info('current requests: %s, total requests: %s' % (len_valid_docs, self.scheduler_count_))
    crawl_doc = self.cache_input_.get(timeout=1)
    request = self._decode_request(crawl_doc)
    if not request:
      self._logger.error('decoded request empty, crawl_doc: %s', crawl_doc)
      return None
    if self.stats:
      self.stats.inc_value('scheduler/dequeued/service', spider=self.spider_)
    self._logger.info('>>>> next request: %s' % request.url)
    self.valid_request_ += 1
    self.spider_.update_status(crawl_doc.url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADING)})
    return request


  def __len__(self):
    return self.cache_input_.qsize() + self.cache_upload_.qsize()


  def has_pending_requests(self):
    return not self.exit_sig_ and len(self) > 0

class SchedulerYoutube(CrawlDocScheduler):
  def __init__(self, thrift_client, persist, idle_before_close, crawler, request_pool_size):
    CrawlDocScheduler.__init__(self, thrift_client, persist, idle_before_close, crawler, request_pool_size)
    self._keys = ['AIzaSyADAw1LV8-DmiqJNvYD7qxTRn7VclazxAE',
                  'AIzaSyDR82r3LDFYgXAnio126YwtkWWcOfwrcDM',
                  'AIzaSyAAvUAixwoB2XtPsuX-i6aq64QStKczcag',
                  'AIzaSyDNW5VmzjLzzsxOWcLhse8zXZWAyHcbggM',
                  'AIzaSyDklVqYGpjE3nOUDIOuc5fNRrdFr-t7T9g',
                  'AIzaSyCLiSdR3CBH2AcgnwPEovag88BrPCfyhPA',
                  'AIzaSyCObEV-VM_xecAQGROfi8RA9qB5eLqxFWc']


  def _add_key(self, url):
    if not url:
      return None
    if 'key=' in url:
      self._logger.error('url already has key')
      return url
    key = choice(self._keys)
    return '%s&key=%s' % (url, key)


  def __len__(self):
    return self.cache_input_.qsize()


  def has_pending_requests(self):
    return len(self) > 0


  def next_request(self):
    request = super(SchedulerYoutube, self).next_request()
    if request:
      replace_url = self._add_key(request.url)
      #print 'replace_url:', replace_url
      request = request.replace(url=replace_url)
    return request


