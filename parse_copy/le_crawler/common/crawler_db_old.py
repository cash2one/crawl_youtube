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
from url_domain_parser import query_domain_from_url
from le_crawler.proto.crawl.ttypes import CrawlDocType, PageType
from le_crawler.proto.crawl_doc.ttypes import CrawlDoc
from le_crawler.proto.scheduler.ttypes import CrawlDocSlim


#fresh_docs = set(range(CrawlDocType.HUB_FRESH_MIN, CrawlDocType.HUB_FRESH_MAX))
fresh_docs = set([CrawlDocType.HUB_HOME])

doc_type_map = {CrawlDocType.HOME: 21,
                CrawlDocType.HUB_HOME: 22,
                CrawlDocType.HUB_CATEGORY: 23}

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


class CrawlerDBManger(object):
  STOP_READ = 1
  STOP_WRITE = (1 << 1)

  def __init__(self, db_path, logger=None):
    self.logger_ = logger or Log('crawlerdb_log', 'crawler_sch_db.log').log
    self._list_logger = Log('list_logger', 'log/list_recrawler.log').log
    self.db_base_path_ = db_path
    self.db_dict_ = {}
    self._load_dbs(self.db_base_path_)
    self.exit_sig_ = False
    self.max_schedule_delay_ = 0
    self.min_schedule_delay_ = 24 * 60 * 60  # 1 day
    self.mongo_client_ = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')
    self.mongo_client_.admin.authenticate('admin', 'NzU3ZmU4YmFhZDg')
    #self._load_from_mongo()
    self.docs_pool_ = {}
    Thread(target=self._recall_hub_docs).start()
    self.db_create_lock_ = threading.Lock()


  def _load_from_mongo(self):
    self.logger_.info('loading data from mongo...')
    self.docs_pool_ = {}
    for data in self.mongo_client_.crawl.hot_urls.find():
      url = data['url']
      key = self._get_store_key(url, CrawlDocType.PAGE_HOT + 1)
      crawl_doc = CrawlDoc(url=url,
                           doc_type=CrawlDocType.HUB_TIME_HOME,
                           page_type=PageType.HUB)
      doc = CrawlDocSlim(url=url,
                         crawl_doc=thrift_util.thrift_to_str(crawl_doc),
                         priority=CrawlDocType.PAGE_HOT + 1)
      self.docs_pool_[url] = (key, doc)
    self.logger_.info('load data from mongo finished.')


  def _recall_hub_docs(self):
    def put_into_db(item):
      key, doc = item
      for reg in black_regs:
        if re.search(reg, doc.url):
          return False
      doc.discover_time = int(time.time())
      """
      self.mongo_client_.admin.hot_urls.update(
          {'url': doc.url},
          {'$set': {'url': doc.url, 'update_time': time.strftime('%Y%m%d_%H%M%S')}},
          upsert=True)
      """
      db = self._get_db(doc.url)
      if db:
        db.put(key, doc.crawl_doc)
        self._list_logger.info('recalling list url: [%s]' % doc.url)
        return True

    while not self.exit_sig_:
      try:
        if not self.docs_pool_:
          time.sleep(1 * 60)
          continue
        counter = 0
        for doc in self.docs_pool_.values():
          if put_into_db(doc):
            counter += 1
        self.logger_.info('finished recalling [%s] hub docs into scheduler.' % counter)
        # self._gather_info()
        time.sleep(2 * 60 * 60)
      except:
        self.logger_.exception('failed recall docs.')


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
      if doc.priority in fresh_docs and doc.url not in self.docs_pool_:
        key = self._get_store_key(doc.url, CrawlDocType.PAGE_HOT + 1)
        self.docs_pool_[doc.url] = (key, doc)
      else:
        key = self._get_store_key(doc.url, doc_type_map.get(doc.priority, doc.priority))
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

  def _gather_info(self):
    databases = self.db_dict_.copy()
    statistic = 'Scheduler details:'
    for domain, database in databases.iteritems():
      statistic += '\n\t%16s: %s' % (domain, database.size())
    self.logger_.info(statistic)

  def stop(self):
    self.logger_.info('stopping crawler database manager...')
    self.exit_sig_ = True
    self.logger_.info('stop crawler database manager finished.')

  def _load_from_file(self):
    self.logger_.info('loading data from cache file...')
    if not os.path.isfile('data/refresh_pool.data'):
      self.logger_.error('refresh pool file not found, create one instead.')
      self.docs_pool_ = {}
    else:
      with open('data/refresh_pool.data', 'r') as f:
        self.docs_pool_ = pickle.load(f)
    self.logger_.info('load data from cache file finished.')

  def _dump_to_file(self):
    self.logger_.info('dumping data...')
    if not os.path.isdir('data'):
      os.mkdir('data')
    docs = self.docs_pool_.copy()
    with open('data/refresh_pool.data', 'w') as f:
      pickle.dump(docs, f, 2)
    self.logger_.info('dump data finished.')

