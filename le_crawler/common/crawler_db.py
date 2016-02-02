#!/usr/bin/python
# coding=utf8
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe

__author__ = 'guoxiaohe@letv.com'

# this cls is using for crawler backgroud request
# store db, store by domain


import re
import os
import time
import random
import string
import hashlib
import threading
from threading import Thread
# import traceback
try:
  import cPickle as pickle
except:
  import pickle
from pymongo import MongoClient

import thrift_util
from logutil import Log
from sharedb import ShareDB, DBOption
from domain_parser import query_domain_from_url
from le_crawler.proto.crawl.ttypes import CrawlDocType, PageType
from le_crawler.proto.crawl_doc.ttypes import CrawlDoc
from le_crawler.proto.scheduler.ttypes import CrawlDocSlim




class CrawlerDBManger(object):
  STOP_READ = 1
  STOP_WRITE = (1 << 1)

  def __init__(self, db_path, logger=None):
    self.logger_ = logger or Log('crawlerdb_log', 'crawler_sch_db.log').log
    self.db_base_path_ = db_path
    self.db_dict_ = {}
    self._load_dbs(self.db_base_path_)
    self.db_create_lock_ = threading.Lock()


  def _load_dbs(self, db_path):
    if not os.path.isdir(db_path):
      os.mkdir(db_path)
    dbids = os.listdir(db_path)
    for dbid in dbids:
      tmpdb = self._create_db(dbid)
      if tmpdb:
        self.db_dict_[dbid] = tmpdb
        self.logger_.info('Load db [%s]' % dbid)
      else:
        self.logger_.error('Load db [%s] failed' % dbid)
    self.logger_.info('db loaded: [%d]' % len(self.db_dict_))
    return True

  def _create_db(self, dbid):
    db_path = os.path.join(self.db_base_path_, dbid)
    op = DBOption()
    domain_db = ShareDB(db_path, self.logger_, dboption=op)
    self.logger_.info('created db [%s] to [%s] ' % (dbid, db_path))
    return domain_db

  def _get_db(self, url):
    dbid = query_domain_from_url(url)
    if dbid == 'googleapis.com':
      dbid = 'youtube.com'
    if not dbid:
      self.logger_.error('failed parse domain from url, %s', url)
      return None
    if dbid in self.db_dict_:
      return self.db_dict_[dbid]
    else:
      self.db_create_lock_.acquire()
      if dbid in self.db_dict_:
        self.db_create_lock_.release()
        return self.db_dict_[dbid]
      self.db_dict_[dbid] = self._create_db(dbid)
      self.db_create_lock_.release()
      # assert self.db_dict_[dbid], 'Create db [%s] failed' % dbid
      return self.db_dict_[dbid]


  def _get_store_key(self, url, priority=6):
    return '%s_%s' % (string.zfill(priority, 6), hashlib.md5(url).hexdigest())


  def get_crawldocs(self, batch_num=1024):
    self.logger_.info('getting requests: [%s]', batch_num)
    data = []
    if not batch_num or not self.db_dict_:
      return data
    db_amount = len(self.db_dict_)
    average = batch_num / db_amount or 1
    last_spare = total = 0
    spare = batch_num
    db_len = len(self.db_dict_)
    db_keys = self.db_dict_.keys()
    db_idx = random.choice(range(db_len))
    idx_0 = db_idx
    while 1:
      db = self.db_dict_[db_keys[db_idx]]
      actual_num = average + last_spare
      batch_data = db.batch_get(actual_num)
      if batch_data:
        cur_len = len(batch_data)
        last_spare = actual_num - cur_len
        db.batch_delete([k for (k, v) in batch_data])
        total += cur_len
        data.append([v for (k, v) in batch_data])
        spare -= cur_len
        if spare <= 0:
          break
      db_idx = (db_idx + 1) % db_len
      if db_idx == idx_0:
        break
    self.logger_.info('batch num actual: %s' % total)
    return data


  def put(self, doc):
    if not doc or not doc.url:
      return True
    try:
      db = self._get_db(doc.url)
      if not db:
        self.logger_.error('failed get db id, url: %s', doc.url)
        return False
      key = self._get_store_key(doc.url, doc.priority)
      db.put(key, doc.crawl_doc)
      self.logger_.debug('put into db, key: [%s], %s' % (key, doc.url))
    except:
      self.logger_.exception('failed to put request')
      return False


  # write the request to db the api for request_manger
  # input: request is [requests, request,]
  def set_crawldocs(self, crawldocs):
    try:
      self.logger_.info('writing requests: [%s]', len(crawldocs))
      for doc in crawldocs:
        self.put(doc)
        self.logger_.debug('url added, %s', doc.url)
      self.logger_.info('finished writing requests: [%s]', len(crawldocs))
    except:
      self.logger_.exception('failed to write requests')


  # return all the db status
  def get_status(self):
    pass



