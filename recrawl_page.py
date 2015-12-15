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
    self.logger_ = Log('reschedule', 'log/reschedule.log').log
    self.client_ = SchedulerClient('127.0.0.1', 8088)
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
      self._logger.exception('failed to connect to mongodb...')


  def run(self):
    now = time.time()
    while not self.exit_:
      docs = []
      self.logger_.info('begin to reschedule page.')
      #for item in self._collection.find({'next_schedule_time': {'$lt': now}}):
      for item in self._collection.find({}):
        doc = CrawlDoc()
        doc.doc_type = CrawlDocType._NAMES_TO_VALUES.get(item['doc_type']) if item.get('doc_type', None) else CrawlDocType.PAGE_PLAY
        doc.schedule_doc_type = ScheduleDocType.RECRAWL_PLAY
        doc.url = item['url']
        crawl_doc_slim = CrawlDocSlim(url=doc.url,
                                      crawl_doc=thrift_util.thrift_to_str(doc),
                                      priority=doc.doc_type)
        docs.append(crawl_doc_slim)
        self._collection.remove({'url': item['url']})
        self.logger_.info('recall url: %s', item['url'])
        if len(docs) >= 50:
          self.logger_.info('recalling docs, [%s]', len(docs))
          self.client_.set_crawldocs_local(docs)
          docs = []
      if docs:
        self.logger_.info('recrawl docs, [%s]', len(docs))
        self.client_.set_crawldocs_local(docs)
      self.logger_.info('finish reschedule.')
      time.sleep(5 * 60)
    db.logout()



if __name__ == '__main__':
  recawler = RecrawlPage()
  recawler.run()

