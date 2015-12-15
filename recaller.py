#!/usr/bin/python
# coding=utf8
# Copyright 2014 LeTV Inc. All Rights Reserved.
# author: gaoqiang@letv.com (Qiang Gao)

import time

from pymongo import MongoClient, UpdateOne

from le_crawler.base.logutil import Log
from le_crawler.proto.crawl.ttypes import CrawlDocType, CrawlDoc, ScheduleDocType
from le_crawler.core.scheduler_client import SchedulerClient


class Recaller(object):
  def __init__(self, logger):
    self.logger_ = logger
    self.exit_ = False
    self.client_ = SchedulerClient('10.150.140.84', 8088)
    self.client_.open(self.logger_)


  def _init_schedule_db(self):
    client = MongoClient('10.180.91.115:9211,10.180.91.125:9211,10.180.91.41:9211')
    client.admin.authenticate('admin', 'MzU3ZmU4YmFhZDg')
    return client.admin


  def _recall_pages(self):
    db = self._init_schedule_db()
    schedule_table = db.schedule_info
    now = time.time()
    while not self.exit_:
      docs = []
      update_items = []
      self.logger_.info('begin to scan.')
      for item in schedule_table.find({'next_schedule_time': {'$lt': now}}):
        doc = CrawlDoc()
        doc.doc_type = CrawlDocType.PAGE_PLAY
        doc.schedule_doc_type = ScheduleDocType.RECRAWL_PLAY
        doc.url = item['url']
        docs.append(doc)
        update_items.append(UpdateOne({'url': item['url']}, {'$set': {'next_schedule_time': None}}, upsert=True))
        self.logger_.info('recall url: %s', item['url'])
        if len(docs) >= 1024:
          self.logger_.info('recalling docs, [%s]', len(docs))
          self.client_.set_crawldocs_local(docs)
          schedule_table.bulk_write(update_items, ordered=False)
          update_items = []
          docs = []
      self.logger_.info('recalling docs, [%s]', len(docs))
      self.client_.set_crawldocs_local(docs)
      if update_items:
        schedule_table.bulk_write(update_items, ordered=False)
      self.logger_.info('finish scanning.')
      # self.logger_.info('no docs with correct scheduling time found.')
      time.sleep(5 * 60)
    db.logout()


  def run(self):
    self._recall_pages()


if __name__ == '__main__':
  recaller = Recaller(Log('recaller.log', 'log/recaller.log').log)
  recaller.run()

