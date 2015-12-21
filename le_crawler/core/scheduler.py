#!/usr/bin/python
#coding=utf-8
#author=gaoqiang@letv.com
#
# Copyright 2015 LeTV Inc. All Rights Reserved.

import Queue
import time
try:
  import cPickle as pickle
except:
  import pickle
from threading import Thread
from random import choice

# from scrapy.utils.misc import load_object
from scrapy.utils.reqser import request_to_dict, request_from_dict

from ..common import thrift_util
from ..proto.crawl_doc.ttypes import CrawlDoc
from ..proto.crawl.ttypes import Request, CrawlStatus, ScheduleDocType, CrawlDocType, PageType
from ..proto.scheduler.ttypes import CrawlDocSlim
from scheduler_client import SchedulerClient
from ..common.domain_parser import query_domain_from_url
from ..common.parse_youtube import parse_channel_id


class CrawlDocScheduler(object):
  """ thrift-rpc based scheduler """
  def __init__(self, thrift_client, idle_before_close, crawler):
    self.boot = True
    self.exit_sig_ = False
    self.crawler = crawler
    self.stats_ = self.crawler.stats
    self.scheduler_client_ = thrift_client
    self.idle_before_close = idle_before_close
    self.cache_input_max_ = 20
    self.cache_upload_max_ = 20
    self.cache_input_ = Queue.Queue(2)
    self.cache_upload_ = Queue.Queue(2)
    # self.crawler.signals.connect(self.close_test, signal = signals.engine_stopped)
    # self.crawler.signals.connect(self.close_test, signal = signals.spider_closed)
    self.max_idle_times_ = 50
    self.scheduler_count_ = 0
    self.valid_request_ = 0
    self.idle_times_ = 0
    self.flush_request_thread_ = Thread(target=self._flush_request)
    self.flush_request_thread_.start()


  def open(self, spider):
    self.spider_ = spider
    self.logger_ = spider.logger_
    self.len_start_urls_ = self.spider_.start_size
    self.logger_.info('amount of start urls: %s', self.len_start_urls_)
    self.scheduler_client_.open(self.logger_)
    if self.idle_before_close < 0:
      self.idle_before_close = None


  @classmethod
  def from_settings(cls, settings, crawler):
    idle_before_close = settings.get('SCHEDULER_IDLE_BEFORE_CLOSE', 4)
    debug_mode = settings.get('DEBUG_MODE', True)
    client_host = settings.get('DEBUG_HOST' if debug_mode else 'CRAWLDOC_SCHEDULER_HOST', 'localhost')
    client_port = settings.get('CRAWLDOC_SCHEDULER_PORT', 8088)
    client = SchedulerClient(client_host, client_port)
    return cls(client, idle_before_close, crawler)


  @classmethod
  def from_crawler(cls, crawler):
    return cls.from_settings(crawler.settings, crawler)


  def _encode_request(self, request):
    """Encode a request object"""
    request_dict = request_to_dict(request, self.spider_)
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
      if not crawl_doc or not crawl_doc.request or not crawl_doc.request.meta:
        self.logger_.info('recalled request: %s', crawl_doc.url)
        return self.spider_._create_request(url=crawl_doc.url,
                                            page_type=crawl_doc.page_type,
                                            doc_type=crawl_doc.doc_type,
                                            schedule_doc_type=ScheduleDocType.RECRAWL_PLAY,
                                            dont_filter=True)
      red_dict = pickle.loads(crawl_doc.request.meta)
      request = request_from_dict(red_dict, self.spider_)
      request.meta['crawl_doc'] = crawl_doc
      return request
    except:
      self.logger_.exception('failed decode request: %s', crawl_doc)
      return None


  def close(self, reason):
    self.exit_sig_ = True
    while self.flush_request_thread_.isAlive():
      self.logger_.info('wait for scheduler request push thread exit')
      time.sleep(1)
    self.scheduler_client_.close()


  def enqueue_request(self, request):
    if not request:
      self.logger_.error('invalid request, skip.')
      return
    self.logger_.info('<<<< enqueue request, %s', request.url)
    doc = self._encode_request(request)
    if not doc.url:
      return
    while 1:
      try:
        self.cache_upload_.put(doc, timeout=1)
        if self.stats_:
          self.stats_.inc_value('scheduler/enqueued/service', spider=self.spider_)
        break
      except:
        self.logger_.exception('failed to put request to queue.')
        self._flush_queue()
        if self.cache_upload_.maxsize < self.cache_upload_max_:
          self.cache_upload_ = Queue.Queue(self.cache_upload_.maxsize + 2)
          self.logger_.info('cache upload size updated to [%s]', self.cache_upload_.maxsize)
        if self.exit_sig_:
          break


  def _cal_priority(self, doc):
    return doc.doc_type


  def _flush_queue(self):
    if self.cache_upload_.empty():
      return
    flush_docs = []
    while not self.cache_upload_.empty():
      try:
        doc = self.cache_upload_.get(timeout=1)
        self.spider_.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.SCHEDULING))
        crawl_doc_slim = CrawlDocSlim(url=doc.url,
                                      crawl_doc=thrift_util.thrift_to_str(doc),
                                      priority=self._cal_priority(doc))
        #if not doc.domain_id:
        #  self.logger_.error('no domain_id, url: %s, in_link: %s', doc.url, doc.in_links[0].url if doc.in_links else None)
        flush_docs.append(crawl_doc_slim)
        now = int(time.time())
        if CrawlDocType.PAGE_PLAY < crawl_doc_slim.priority < CrawlDocType.HUB_FRESH_MAX:
          self.spider_.update_recrawl_info(url=doc.url,
                                           data={'next_schedule_time': now + 60 * 30,
                                                 'retry_times': 0,
                                                 'crawl_doc_slim': pickle.dumps(crawl_doc_slim)})
        if doc.page_type == PageType.CHANNEL:
          channel_id = parse_channel_id(doc.url)
          if not channel_id:
            self.logger_.info('failed parse_channel_id, url: %s', doc.url)
          else:
            channel_dict = self.spider_.get_channel_info(channel_id)
            if not channel_dict or not channel_dict.get('crawl_doc_slim', None):
              schedule_interval = 1 * 60 * 60
              #schedule_interval = 1 * 60
              channel_dict = {'channel_id': channel_id,
                              'next_schedule_time': now + schedule_interval,
                              'schedule_interval': schedule_interval,
                              'update_time': now,
                              'crawl_doc_slim': pickle.dumps(crawl_doc_slim)}
              self.spider_.upsert_channel_info(channel_dict)
      except:
        self.logger_.exception('failed to get flush doc from cache.')
    if flush_docs:
      self.logger_.info('<<<< pushing requests to scheduler service, requests amount: %s', len(flush_docs))
      self.scheduler_client_.set_crawldocs_local(flush_docs)
      self.idle_times_ = 0


  def _flush_request(self):
    while not self.exit_sig_:
      if self.idle_times_ >= self.max_idle_times_:
        self._flush_queue()
      else:
        self.idle_times_ += 1
      time.sleep(2)
    self._flush_queue()


  def _mixin_list(self, data):
    # data为list，其元素也是list
    # 首先按照元素长度降序排列
    # 对于各个list，根据步长step逆序插入结果list中
    # 输出为list
    if not data:
      return data
    data.sort(cmp=lambda x, y: len(y) - len(x))
    result = data[0]
    step = 1
    for item in data[1:]:
      index = len(result)
      for i in item:
        result.insert(index, i)
        index -= step
      if item:
        step += 1
    self.logger_.debug('end mixin')
    return result


  def next_request(self):
    """
    if self.len_start_urls_:
      self.len_start_urls_ -= 1
      return None
    """
    if self.cache_input_.empty():
      self.logger_.info('fetching requests from scheduler service...')
      docs = self.scheduler_client_.get_crawldocs_local(self.cache_input_.maxsize) or []
      if not docs:
        self.logger_.info('no docs from scheduler service')
        self._flush_queue()
        time.sleep(2)
        return None
      docs = self._mixin_list(docs)
      docs_len = len(docs)
      if self.cache_input_.maxsize < self.cache_input_max_:
        self.cache_input_ = Queue.Queue(self.cache_input_.maxsize + 2)
        self.logger_.info('cache input size updated to [%s]', self.cache_input_.maxsize)
      for doc_str in docs:
        doc = CrawlDoc()
        thrift_util.str_to_thrift(doc_str, doc)
        self.spider_.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.SCHEDULED))
        self.cache_input_.put(doc, timeout=3)
      self.scheduler_count_ += docs_len
      self.logger_.info('>>>> fetched request: %s' % docs_len)
      self.logger_.info('current requests: %s, total requests: %s' % (docs_len, self.scheduler_count_))
    crawl_doc = self.cache_input_.get(timeout=1)
    request = self._decode_request(crawl_doc)
    if not request:
      self.logger_.error('decoded request empty, crawl_doc: %s', crawl_doc)
      return None
    if self.stats_:
      self.stats_.inc_value('scheduler/dequeued/service', spider=self.spider_)
    self.logger_.info('>>>> next request: %s', request.url)
    self.valid_request_ += 1
    self.spider_.update_status(crawl_doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADING))
    return request


  def __len__(self):
    return self.cache_input_.qsize()


  def has_pending_requests(self):
    return len(self) > 0


class SchedulerYoutube(CrawlDocScheduler):
  def __init__(self, thrift_client, idle_before_close, crawler):
    CrawlDocScheduler.__init__(self, thrift_client, idle_before_close, crawler)
    self._keys = ['AIzaSyADAw1LV8-DmiqJNvYD7qxTRn7VclazxAE',
                  'AIzaSyDR82r3LDFYgXAnio126YwtkWWcOfwrcDM',
                  'AIzaSyAAvUAixwoB2XtPsuX-i6aq64QStKczcag',
                  'AIzaSyDNW5VmzjLzzsxOWcLhse8zXZWAyHcbggM',
                  'AIzaSyDklVqYGpjE3nOUDIOuc5fNRrdFr-t7T9g',
                  'AIzaSyCLiSdR3CBH2AcgnwPEovag88BrPCfyhPA',
                  'AIzaSyCObEV-VM_xecAQGROfi8RA9qB5eLqxFWc']
    self.cache_input_max_ = 50
    self.cache_upload_max_ = 50


  def _add_key(self, url):
    if not url:
      return None

    if query_domain_from_url(url) != 'googleapis.com':
      return url

    if 'key=' in url:
      self.logger_.error('url already has key, url: [%s]', url)
      return url
    key = choice(self._keys)
    return '%s&key=%s' % (url, key)

  def next_request(self):
    request = super(SchedulerYoutube, self).next_request()
    if request:
      replace_url = self._add_key(request.url)
      #print 'replace_url:', replace_url
      request = request.replace(url=replace_url)
    return request

