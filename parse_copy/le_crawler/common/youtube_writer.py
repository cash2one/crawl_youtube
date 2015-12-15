#!/usr/bin/python
# coding=utf8
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'zhaojincheng'

import traceback
from pymongo import MongoClient
import json
import time
import copy
import base64
import logging

from scrapy.utils.project import get_project_settings

from ..core.page_writer import PageWriterWithBuff
from logutil import Log
from utils import gen_next_schedule_time


class YoutubeWriter(PageWriterWithBuff):
  def __init__(self, spider):
    super(YoutubeWriter, self).__init__(spider)
    self.total_save_count = 0
    self.failed_save_count = 0
    self.total_update_count = 0
    self.failed_updata_count = 0
    self.retry_time_max = 10
    self.logger_ = Log('youtubewriter', log_path='../log/mongo_w.log', log_level=logging.INFO).log
    self._init_client()

  def _init_client(self):
    try:
      client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')
      self._db = client.admin
      self._db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
      if get_project_settings()['DEBUG_MODE']:
        self._collection = self._db.debug_doc_info
        self._collection_reschedule = self._db.debug_recrawl_page_info
      else:
        self._collection = self._db.doc_info
        self._collection_reschedule = self._db.recrawl_page_info
      self._ensure_indexs()
    except Exception, e:
      self._collection = None
      self.logger_.exception('failed to connect to mongodb...')

  def _ensure_indexs(self):
    #index_info = self._collection.index_information()
    #if not index_info or 'url_1' not in index_info or 'create_time_-1' not in index_info \
    #  or 'update_time_-1' not in index_info:
    from pymongo import IndexModel, ASCENDING, DESCENDING
    self._collection.create_index('url', unique=True)
    self._collection.create_index([('update_time', DESCENDING)])
    self._collection.create_index([('create_time', DESCENDING)])
    self._collection_reschedule.create_index('url', unique=True)
    self._collection_reschedule.create_index([('next_schedule_time', DESCENDING)])


  def _get_data(self, url):
    try:
      if not self._collection:
        self._init_client()
      doc = self._collection.find({'url':url})
      doc = [obj for obj in doc]
      if doc:
      	self.logger_.error('exist data:[%s]' % url)
        return doc[0]
      else:
        return []
    except:
      self.logger_.error('Failed get data:[%s], %s, %s' % (url, traceback.format_exc(), e.message))
      raise

  def _update_data(self, data):
    try:
      if not self._collection:
        self._init_client()
      if not data:
        return False
      data['update_time'] = int(time.time())
      self._collection.update({'url': data['url']}, {'$set': data})
      self.logger_.error('success update data:%s' % data['url'])
      return True
    except:
      self.logger_.exception('Failed update data:%s' % data['url'])
      return False


  def _save_data(self, data):
    try:
      if not self._collection:
        self._init_client()
      if data:
        data['create_time'] = int(time.time())
        data['update_time'] = int(time.time())
        self._collection.save(data)
        self.logger_.error('success save data:%s' % data['url'])
      return True
    except:
      self.logger_.exception('Failed save data:%s', data)
      return False


  def status(self):
    return 'total_save:%s, total_update:%s, %s' % (self.total_save_count, self.total_update_count, super(YoutubeWriter, self).status())


  def writer(self, item):
    if not item or not item['url']:
      return
    db_data = self._get_data(item['url'])
    if not db_data:
      data = item.convert_item()
      try_time = 0
      while try_time < self.retry_time_max:
        if not self._save_data(data):
          try_time += 1
          continue
        break
      self.total_save_count += 1
    else:
      item.merge_video(db_data.get('video', None))
      data = item.convert_item()
      self._update_data(data)
      self.total_update_count += 1
    self._save_reschedule_info(item)

  def _save_reschedule_info(self, item):
    if not item or not item['request_url']:
      return
    try:
      content_timestamp = item.get('content_timestamp', None)
      if not content_timestamp or (content_timestamp < int(time.time() - 604800)):
        return
      next_schedule_time = gen_next_schedule_time(item['crawl_history'].get('crawl_history', None))
      if not next_schedule_time:
        return
      if not self._collection_reschedule:
        self._init_client()
      update_dict = {'content_timestamp': content_timestamp,
                     'next_schedule_time': next_schedule_time,
                     'doc_type': item['doc_type'],
                     'page_type': item['page_type']}
      self._collection_reschedule.update({'url': item['request_url']}, {'$set': update_dict}, upsert=True)
      self.logger_.error('success update item:%s' % item['request_url'])
      return True
    except:
      self.logger_.exception('Failed update item:%s' % item['url'])
      return False

