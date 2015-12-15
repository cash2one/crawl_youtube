#coding: utf-8

import time

try:
  import cPickle as pickle
except:
  import pickle

from pymongo import MongoClient, UpdateOne


from le_crawler.common.logutil import Log
from le_crawler.proto.crawl.ttypes import CrawlStatus
from le_crawler.core.scheduler_client import SchedulerClient

class Recrawler(object):
  def __init__(self):
    self.logger_ = Log('recrawl_failed', 'log/recrawl_failed.log').log
    self.client_ = SchedulerClient('65.255.32.210', 8088)
    self.client_.open(self.logger_)
    self.exit_ = False
    self._init_client()

  
  def _init_client(self):
    try:
      client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')
      self._db = client.admin
      self._db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
      self._collection = self._db.recrawl_failed_info
    except Exception, e:
      self._collection = None
      self._logger.exception('failed to connect to mongodb...')

  
  def run(self):
    while not self.exit_:
      now = int(time.time())
      update_items = []
      docs = []
      self.logger_.info('begin to scan.')
      #print 'begin to scan.....'
      for item in self._collection.find({'next_schedule_time': {'$lt': now}}):
      #for item in self._collection.find({}):
        time_now = int(time.time())
        retry_times = item.get('retry_times', 0) + 1
        if retry_times > 10:
          self.logger_.info('retry max_times: %s, remove url: %s' % (retry_times, item['url']))
          try:
            self._collection.remove({'url': item['url']})
          except:
            self.logger_.info('failed remove url: %s' % item['url'])
          continue
        doc_slim = item.get('crawl_doc_slim', None)
        if not doc_slim:
          continue
        docs.append(pickle.loads(doc_slim.encode('utf-8')))
        schedule_delta_time = 3600 * (retry_times + 3)
        next_schedule_time = time_now + schedule_delta_time
        update_item = UpdateOne({'url': item['url']},{'$set': {'next_schedule_time': next_schedule_time,'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.SCHEDULING), 'retry_times': retry_times}}, upsert=True)
        update_items.append(update_item)
        self.logger_.info('recrawl url: %s, retry_times: [%s], next_schedule_time: [%s]' % (item['url'], retry_times, next_schedule_time))
        if len(docs) >= 50:
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
      self.logger_.info('finish recrawl.....')
      #print 'finish recrawl.....'
      time.sleep(5 * 60)
    self._db.logout()


if __name__ == '__main__':
  recrawler = Recrawler()
  recrawler.run()
