#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe

__author__ = 'guoxiaohe@letv.com'

# this cls is using for crawler backgroud request
# store db, store by domain

import os
import traceback
import hashlib
import string
import threading
try:
  import cPickle as pickle
except ImportError:
  import pickle

from ..base.sharedb import ShareDB, DBOption
from ..base.url_filter import UrlFilter
from ..base.logutil import Log


class CrawlerDBManger(object):
  STOP_READ = 1
  STOP_WRITER = (1 << 1)

  def __init__(self, db_path, loger=None):
    self.loger = loger or Log('crawlerdb_log', '../log/crawler_sch_db.log')
    self.__db_base_path = db_path
    self.__db_dict = {}
    self.__load_dbs(self.__db_base_path)
    self.__db_mark_dict = {}
    self.__url_filter = UrlFilter.get_instance()
    self.store_by_priority = True
    self.set_stop_mark()
    self.__db_keys = self.__db_dict.keys()
    self.__db_seek = 0
    # db lock
    # FIXME(xiaohe): add read and writer lock
    # one thread process delete request
    self.__db_lock = threading.Lock()

  # FIXME(xiaohe): resolve youku crawled problem
  def set_stop_mark(self):
    # self.__mark(dbid = 'youku.com', flag = CrawlerDBManger.STOP_READ)
    self.__mark(dbid='letv.com', flag=CrawlerDBManger.STOP_WRITER)
    self.__mark(dbid='letv.com', flag=CrawlerDBManger.STOP_READ)

  def test_stop_write(self, dbid):
    return self.__test_mark(dbid=dbid, mark=CrawlerDBManger.STOP_WRITER)

  def test_stop_read(self, dbid):
    return self.__test_mark(dbid=dbid, mark=CrawlerDBManger.STOP_READ)

  # this fun call url filter allowed host
  def __test_mark(self, dbid, mark):
    return mark & self.__get_mark(dbid)

  def __mark(self, dbid, flag):
    if not self.__db_mark_dict.has_key(dbid):
      self.__db_mark_dict[dbid] = 0
    self.__db_mark_dict[dbid] |= flag

  def __get_mark(self, dbid):
    if self.__db_mark_dict.has_key(dbid):
      return self.__db_mark_dict[dbid]
    return 0

  def __get_db_id_from_url(self, url):
    # self.loger.log.info('put %s' % url)
    return self.__url_filter.get_flag(url)

  def __load_dbs(self, db_path):
    if not os.path.isdir(db_path):
      os.makedirs(db_path)
    #FIXME: get url auto
    dbids = os.listdir(db_path)
    for dbid in dbids:
      tmpdb = self.__create_db(dbid)
      if tmpdb:
        self.__db_dict[dbid] = tmpdb
        self.loger.log.info('Load db [%s]', dbid)
      else:
        self.loger.log.error('Load db [%s]', dbid)

    self.loger.log.info('Load dbs [%d]', len(self.__db_dict))
    return True

  def __create_db(self, dbid):
    db_path = os.path.join(self.__db_base_path, dbid)
    op = DBOption()
    domain_db = ShareDB(db_path, dboption=op)
    self.loger.log.info('created db [%s] to [%s] ' % (dbid, db_path))
    self.loger.log.info('db [%s] status [%s] ' % (dbid, domain_db.get_total_num()))
    return domain_db

  def __get_db(self, url=None, id=None):
    dbid = id or self.__get_db_id_from_url(url)
    if not dbid:
      return None
    if self.__db_dict.has_key(dbid):
      return self.__db_dict[dbid]
    else:
      # create db for domain
      self.__db_dict[dbid] = self.__create_db(dbid)
      assert self.__db_dict[dbid], 'Create db [%s] error' % dbid
      return self.__db_dict[dbid]

  def __get_store_key(self, url, priority=0):
    if self.store_by_priority:
      return '%s_%s' % (string.zfill(priority, 6), hashlib.md5(url).hexdigest())
    else:
      return hashlib.md5(url).hexdigest()

  # input request pickle's value
  def put(self, reqv):
    if not reqv:
      return True
    try:
      req_dict = pickle.loads(reqv)
      url = None
      if 'u' in req_dict:
        url = req_dict['u']
      elif 'url' in req_dict:
        url = req_dict['url']
      if not url:
        self.loger.log.error('value is not contails url: %s' % reqv)
        return False
      # get priority from request
      priority = 0
      if self.store_by_priority:
        metadic = None
        if req_dict.has_key('me'):
          metadic = req_dict['me']
        elif req_dict.has_key('meta'):
          metadic = req_dict['meta']
        if metadic and metadic.has_key('depth'):
          priority = metadic['depth']
      dbid = self.__get_db_id_from_url(url)
      if self.test_stop_write(dbid):
        self.loger.log.error('stop writer for stop mark flag for %s' % dbid)
        return False
      db = self.__get_db(id=dbid)
      # print db
      db.put(self.__get_store_key(url, priority), reqv)
    except Exception, e:
      self.loger.log.error('%s, %s : %s ' % (e.message, traceback.format_exc(),
                                             reqv))
      return False

  # thread safe, add lock
  def get_requests(self, batch_num=1024):
    dbkl = len(self.__db_keys)
    if dbkl <= 0:
      return []
    # operater to db seek, lock
    self.__db_lock.acquire()
    if self.__db_seek >= dbkl:
      self.__db_seek = 0
    id = self.__db_keys[self.__db_seek]
    self.__db_seek += 1
    self.__db_lock.release()
    if self.test_stop_read(id):
      self.loger.log.debug('stop read for stop mark flag for %s' % id)
      return []
    db = self.__db_dict[id]
    batch_res = db.batch_get(batch_num)
    self.loger.log.debug('Got request from [%s] [%d]' % (id, len(batch_res)))
    # delete the keys in db
    # FIXME(xiaohe): delete keys in db after rpc finished,
    # let remote caller to delete the fetcher keys
    db.batch_delete([k for (k, v) in batch_res])
    return batch_res

  # FIXME(xiaohe): load policy fetcher from each db
  # return iterator able value
  def get_requests_iter(self, batch_num=1024):
    for item_id, db in self.__db_dict.items():
      if self.test_stop_read(item_id):
        self.loger.log.error('stop read for stop mark flag for %s' % item_id)
        continue
      batch_res = db.batch_get(batch_num)
      self.loger.log.debug('Got request from [%s] [%d]' % (item_id, len(batch_res)))
      if not batch_res or len(batch_res) <= 0:
        continue
      db.batch_delete([k for (k, v) in batch_res])
      yield [v for (k, v) in batch_res]

  # return all the db status
  def get_status(self):
    total_num = 0
    rets = []
    for item_id, db in self.__db_dict.items():
      tmpnum = int(db.get_total_num())
      total_num += tmpnum
      rets.append('%s db status[%d]\n' % (item_id, tmpnum))
      # rets.append(db.status())
    rets.append('Total Num:%d' % total_num)
    return rets

  # writer the request to db
  # the api for request_manger ,
  # input: request is [requests, request,]
  def writer_request(self, requests):
    for req in requests:
      self.put(req)
