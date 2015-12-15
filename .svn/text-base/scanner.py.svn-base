#!/usr/bin/python
# coding=utf8
# Copyright 2014 LeTV Inc. All Rights Reserved.
# author: gaoqiang@letv.com (Qiang Gao)

import time

from pymongo import MongoClient, UpdateOne

from le_crawler.base.logutil import Log


class Scanner(object):
  def __init__(self, logger):
    self.logger_ = logger
    self.exit_ = False


  def _init_schedule_db(self):
    client = MongoClient('10.180.91.115:9211,10.180.91.125:9211,10.180.91.41:9211')
    client.admin.authenticate('admin', 'MzU3ZmU4YmFhZDg')
    self.logger_.info('successfully connect to MongoDB.')
    return client.admin


  def _gen_next_schedule_time(self, schedule_info):
    self.logger_.debug('calculating schedule time')
    crawl_history = schedule_info.get('crawl_history', {}).get('crawl_history')
    now = time.time()
    if not crawl_history:
      return None
    content_timestamp = schedule_info.get('content_timestamp')
    if not content_timestamp:
      return None
    if content_timestamp < time.time() - 604800:  # 60 * 60 * 24 * 7
      return None
    if len(crawl_history) == 1:
      if crawl_history[0] > 1000:
        return {'url': schedule_info['url'],
                'next_schedule_time': now + 10 * 60}
    incr_count_hourly = ((crawl_history[0].get('play_count') or 0) - (crawl_history[1].get('play_count') or 0)) * 60 * 60 \
                      / ((crawl_history[0].get('crawl_time') or 0) - (crawl_history[1].get('crawl_time') or 0) or 1)
    schedule_interval = crawl_history[0]['crawl_interval'] / 2 if incr_count_hourly > 1000 \
                   else crawl_history[0]['crawl_interval'] * 2
    # self.logger_.info('finish calculating schedule time')
    return {'url': schedule_info['url'],
            'next_schedule_time': now + schedule_interval}


  def _scan_schedule_info(self):
    self.logger_.info('start to scan schedule info')
    db = self._init_schedule_db()
    schedule_table = db.schedule_info
    update_time = None
    while not self.exit_:
      self.logger_.info('scanning schedule_info...')
      cursor = schedule_table.find({'update_time': {'$gt': update_time}, 'next_schedule_time': None}) if update_time else schedule_table.find()
      update_time = time.time()
      items = []
      for item in cursor:
        item = self._gen_next_schedule_time(item)
        if item:
          items.append(UpdateOne({'url': item['url']}, {'$set': item}, upsert=True))
          self.logger_.debug('schedule item: %s, %s', item['url'], item['next_schedule_time'])
      self.logger_.info('finished calculating schedule time.')
      if items:
        schedule_table.bulk_write(items, ordered=False)
      self.logger_.info('finished writing back into schedule database, total: [%s]', len(items))
      time.sleep(60 * 60)
    db.logout()


  def scan(self):
    self._scan_schedule_info()


if __name__ == '__main__':
  scanner = Scanner(Log('scanner.log', 'log/scanner.log').log)
  scanner.scan()

