#coding: utf-8

import time

try:
  import cPickle as pickle
except:
  import pickle

from pymongo import MongoClient, UpdateOne


from le_crawler.common.logutil import Log
from le_crawler.proto.crawl.ttypes import CrawlStatus

class Recrawler(object):
  def __init__(self):
    self.logger_ = Log('recrawl', 'recrawl.log').log
    self.exit_ = False
    self._init_client()

  
  def _init_client(self):
    try:
      client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')
      self._db = client.admin
      self._db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
      self._collection = self._db.debug_recrawl_info
    except Exception, e:
      self._collection = None
      self._logger.exception('failed to connect to mongodb...')

  
  def run(self):
    now = int(time.time())
    update_items = []
    docs = []
    self.logger_.info('begin to scan.')
    #for item in self._collection.find({'next_schedule_time': {'$lt': now}}):
    for item in self._collection.find({}):
      print item
      url = item.get('url', None)
      next_schedule_time = item.get('next_schedule_time', None)
      print 'url: %s, next_schedule_time: %s' % (url, next_schedule_time)
      if not next_schedule_time:
        self.logger_.info('not next_schedule_time, url: %s' % url)
      #self.logger_.info('item: %s' % item)
      #print pickle.loads(item['crawl_doc_slim'].encode('utf-8'))
      break
    print self._collection.count()


if __name__ == '__main__':
  recrawler = Recrawler()
  recrawler.run()
