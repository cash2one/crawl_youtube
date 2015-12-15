#coding: utf-8

import re
import time

try:
  import cPickle as pickle
except:
  import pickle

from pymongo import MongoClient, UpdateOne


from le_crawler.common.logutil import Log
from le_crawler.proto.crawl.ttypes import CrawlStatus, CrawlDocType
from le_crawler.core.scheduler_client import SchedulerClient

black_regs = ['http://list.iqiyi.com/www/13/',
              'http://list.iqiyi.com/www/21/',
              'http://list.iqiyi.com/www/8/',
              'http://list.iqiyi.com/www/20',
              'http://list.iqiyi.com/www/29/',
              'http://list.iqiyi.com/www/5/',
              'http://list.iqiyi.com/www/16/',
              'http://list.iqiyi.com/www/\d+/\d*-\d*-\d{4}.*.html',
              'http://v.qq.com/mvlist',
              'http://v.qq.com/fashion',
              'http://v.qq.com/baby',
              ]

class Recrawler(object):
  def __init__(self):
    self.logger_ = Log('recrawl_failed', 'log/recrawl_failed.log').log
    self.client_ = SchedulerClient('10.150.140.84', 8088)
    self.client_.open(self.logger_)
    self.exit_ = False
    self._init_client()

  def _init_client(self):
    client = MongoClient('10.180.91.41:9224,10.180.91.115:9224,10.180.91.125:9224')
    self._db = client.admin
    self._db.authenticate('admin', 'NjlmNTdkNGQ4OWY')
    self._collection = client.crawl.recrawl_failed_info

  def run(self):
    while not self.exit_:
      update_items = []
      docs = []
      self.logger_.info('begin to scan.')
      try:
        for item in self._collection.find({'next_schedule_time': {'$lt': int(time.time())}}):
          doc = item.get('crawl_doc_slim', None)
          if not doc:
            continue
          doc = pickle.loads(doc.encode('utf-8'))
          if isinstance(doc.url, unicode):
            try:
              doc.url = doc.url.encode('utf-8', errors='ignore')
            except:
              self.logger_.exception('failed encode url: %s', doc.url)
              continue
          retry_times = item.get('retry_times', 0) + 1
          skip = any(re.search(reg, item['url']) for reg in black_regs)
          if retry_times > 10 or CrawlDocType.PAGE_PLAY >= doc.priority or doc.priority >= CrawlDocType.HUB_FRESH_MAX or skip:
            self.logger_.info('retry times: %s, priority: %s, remove url: %s , skip: %s',
                              retry_times, doc.priority, item['url'], skip)
            self._collection.remove({'url': item['url']})
            continue
          docs.append(doc)
          next_schedule_time = int(time.time()) + 600 * retry_times
          update_items.append(UpdateOne({'url': item['url']}, 
                                        {'$set': {'next_schedule_time': next_schedule_time,
                                                  'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.SCHEDULING), 
                                                  'retry_times': retry_times}}, 
                                        upsert=True))
          self.logger_.info('recrawl url: [ %s ], retry_times: [%s], next_schedule_time: [%s]',
                            item['url'], retry_times, next_schedule_time)
          if len(docs) >= 20:
            self.logger_.info('recawl docs, [%s]', len(docs))
            self.client_.set_crawldocs_local(docs)
            self._collection.bulk_write(update_items, ordered=False)
            update_items = []
            docs = []
        if docs:
          self.logger_.info('recrawl docs, [%s]', len(docs))
          self.client_.set_crawldocs_local(docs)
        if update_items:
          self._collection.bulk_write(update_items, ordered=False)
        self.logger_.info('finish recrawl.')
      except:
        self.logger_.exception('failed query mongo.')
      time.sleep(5 * 60)
    self._db.logout()


if __name__ == '__main__':
  Recrawler().run()

