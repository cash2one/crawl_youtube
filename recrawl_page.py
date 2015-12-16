#!/usr/bin/python
# coding=utf8
# Copyright 2014 LeTV Inc. All Rights Reserved.
# author: gaoqiang@letv.com (Qiang Gao)

import time

from pymongo import MongoClient, UpdateOne

from le_crawler.common.logutil import Log
from le_crawler.proto.crawl.ttypes import CrawlDocType, ScheduleDocType, PageType
from le_crawler.proto.crawl_doc.ttypes import CrawlDoc
from le_crawler.proto.scheduler.ttypes import CrawlDocSlim
from le_crawler.core.scheduler_client import SchedulerClient
from le_crawler.common import thrift_util


class RecrawlPage(object):
  def __init__(self):
    self.logger_ = Log('reschedule', 'log/recrawl_page_info.log').log
    self.client_ = SchedulerClient('65.255.32.210', 8088)
    self.client_.open(self.logger_)
    self.exit_ = False
    self._init_client()

  def _init_client(self):
    try:
      client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')
      self._db = client.admin
      self._db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
      self._collection = self._db.recrawl_page_info
    except Exception, e:
      self._collection = None
      self.logger_.exception('failed to connect to mongodb...')

  def _timestamp2string(self, stamp):
    if not stamp:
      return
    return time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(stamp))

  def _recrawl(self):
    now = time.time()
    try:
      docs = []
      for item in self._collection.find({'next_schedule_time': {'$lt': now}}):
        doc = CrawlDoc()
        doc.doc_type = CrawlDocType._NAMES_TO_VALUES.get(item['doc_type']) if item.get('doc_type', None) else CrawlDocType.PAGE_PLAY
        #doc.doc_type = CrawlDocType._NAMES_TO_VALUES.get(item['doc_type'])
        doc.page_type = PageType._NAMES_TO_VALUES.get(item['page_type']) if item.get('page_type', None) else PageType.PLAY
        #doc.page_type = PageType._NAMES_TO_VALUES.get(item['page_type'])
        doc.schedule_doc_type = ScheduleDocType.RECRAWL_PLAY
        doc.url = item['url']
        crawl_doc_slim = CrawlDocSlim(url=doc.url,
                                      crawl_doc=thrift_util.thrift_to_str(doc),
                                      priority=doc.doc_type)
        docs.append(crawl_doc_slim)
        self._collection.remove({'url': item['url']})
        showtime = self._timestamp2string(item.get('content_timestamp', None))
        play_total = item.get('play_total', None)
        next_time_str = self._timestamp2string(item.get('next_schedule_time', None))

        self.logger_.info('recall url: %s, showtime: %s, next_time: %s, play_total: %s', item['url'], showtime, next_time_str, play_total)
        if len(docs) >= 50:
          self.logger_.info('recalling docs, [%s]', len(docs))
          self.client_.set_crawldocs_local(docs)
          docs = []
      if docs:
        self.logger_.info('recrawl docs, [%s]', len(docs))
        self.client_.set_crawldocs_local(docs)
    except:
      self.logger_.exception('failed to recrawl ...')



  def run(self):
    while not self.exit_:
      docs = []
      self.logger_.info('begin to reschedule page.')
      self._recrawl()
      self.logger_.info('finish reschedule.')
      time.sleep(5 * 60)
    db.logout()



if __name__ == '__main__':
  recawler = RecrawlPage()
  recawler.run()

