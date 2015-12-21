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

class ChannelRecrawler(object):
  def __init__(self):
    self.logger_ = Log('recrawl_channel', 'log/recrawl_channel.log').log
    self.client_ = SchedulerClient('65.255.32.210', 8088)
    self.client_.open(self.logger_)
    self.exit_ = False
    self._init_client()

  
  def _init_client(self):
    try:
      client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')
      self._db = client.admin
      self._db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
      self._collection = self._db.channel_info
    except Exception, e:
      self._collection = None
      self._logger.exception('failed to connect to mongodb...')


  def _timestamp2string(self, stamp):
    if not stamp:
      return
    return time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(stamp))


  def gen_schedule_interval(self, channel_dict):
    schedule_interval = item.get('schedule_interval', None)
    if not schedule_interval:
      self.logger_.info('failed to get schedule_interval, channel: [%s]', item['channel_id'])
      return 1 * 60 * 60

    is_parse = channel_dict.get('is_parse', False)
    if not is_parse:
      return schedule_interval * 3 / 2

    video_num = item.get('video_num', 0)
    if not video_num:
      return schedule_interval * 3 / 2

    fans_num = item.get('fans_num', 0)
    if fans_num > 1000000:
      return 10 * 60
    elif fans_num > 100000:
      return 1 * 60 * 60

    video_follow_time = item.get('video_follow_time', None)
    if not video_follow_time:
      return schedule_interval * 3 / 2
    else:
      time_now = int(time.time())
      video_interval = (time_now - video_follow_time[-1])
      interval = video_interval / 2
      interval = min(24 * 60 * 60, interval)
      interval = max(10 * 60, interval)
      return interval


  def run(self):
    while not self.exit_:
      now = int(time.time())
      update_items = []
      docs = []
      self.logger_.info('begin to recrawl channel.')
      #print 'begin to scan.....'
      for item in self._collection.find({'next_schedule_time': {'$lt': now}}):
        time_now = int(time.time())
        if not item.get('channel_id'):
          continue
        doc_slim = item.get('crawl_doc_slim', None)
        if not doc_slim:
          #self.logger_.info('failed to get crawl_doc_slim ..., channel_id: %s', item['channel_id'])
          continue
        docs.append(pickle.loads(doc_slim.encode('utf-8')))
        schedule_interval = self.gen_schedule_interval(item)
        update_item = UpdateOne({'channel_id': item['channel_id']},{'$set': {'next_schedule_time': time_now + schedule_interval,'schedule_interval': schedule_interval}}, upsert=True)
        update_items.append(update_item)
        self.logger_.info('recrawl channel: [%s], schedule_interval: [%s], next_schedule_time: [%s]' % (item['channel_id'], schedule_interval, self._timestamp2string(next_schedule_time)))
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
      self.logger_.info('finish recrawl channel')
      #print 'finish recrawl.....'
      time.sleep(5 * 60)
    self._db.logout()


if __name__ == '__main__':
  channel_recrawler = ChannelRecrawler()
  channel_recrawler.run()
