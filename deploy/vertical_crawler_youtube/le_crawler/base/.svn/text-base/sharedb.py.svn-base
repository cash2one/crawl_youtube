#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe 
__author__ = 'guoxiaohe@letv.com'

import traceback

import leveldb
import threading
# shareddb is wrap for leveldb, 
# otherwise may change for future

class DBOption(object):
  def __init__(self):
    self.create_if_missing = True
    self.error_if_exists = False
    self.paranoid_checks = False
    self.block_cache_size = 8 * (2 << 20)
    self.write_buffer_size = 8 * (2 << 20)
    self.block_size = 4096 * 4
    self.max_open_files = 9000

class ShareDB(object):
  def __init__(self, db_name, dboption = None):
    assert db_name, 'db_name must not be null'
    self.__db = None
    self.__default_op = DBOption()
    self.__db_name = db_name
    self.__inner_total_keys = 'store_total_key'
    self.__lock = threading.Lock()
    if not dboption:
      self.__db = leveldb.LevelDB(self.__db_name,
          create_if_missing = self.__default_op.create_if_missing,
          error_if_exists = self.__default_op.error_if_exists,
          paranoid_checks = self.__default_op.paranoid_checks,
          block_cache_size = self.__default_op.block_cache_size,
          write_buffer_size = self.__default_op.write_buffer_size,
          block_size = self.__default_op.block_size,
          max_open_files = self.__default_op.max_open_files
          )
    else: # using the lib default parameters
      self.__db = leveldb.LevelDB(self.__db_name)
    assert self.__db, 'Can not alloc shareddb'

  @property
  def db_id(self):
    return self.__db_name

  def put(self, key, value):
    try:
      self.__db.Put(key, value)
      self.__update_status()
    except Exception, e:
      print e
      print traceback.format_exc()
      return False
    return True

  def get_total_num(self):
    return -1

  def get(self, key):
    try:
      value = self.__db.Get(key)
    except Exception, e:
      #print e
      #print traceback.format_exc()
      value = None
    return value

  def __update_status(self, count = 1):
    pass
  # get batch value [(k, v)]
  def batch_get(self, batch_num = 1024):
    rets = []
    try:
      iter = self.__db.RangeIter()
      while len(rets) < batch_num:
        rets.append(iter.next())
    except Exception, e:
      pass
    return rets

  def delete(self, key):
    self.wb.Delete(key)

  # batch delete keys
  def batch_delete(self, keys):
    wb = leveldb.WriteBatch()
    for key in keys:
      if key != self.__inner_total_keys:
        wb.Delete(key)
    try:
      self.__db.Write(wb)
      return True
    except Exception, e:
      print e
      print traceback.format_exc()
      return False

  # batch writer
  def batch_put(self, kvs):
    if not kvs or len(kvs) <= 0:
      return True
    wb = leveldb.WriteBatch()
    for (k, v) in kvs:
      if k and v:
        wb.Put(k, v)
    try:
      self.__db.Write(wb)
      self.__update_status(count = len(kvs))
    except Exception, e:
      print e
      print traceback.format_exc()
      return False

  def status(self):
    return self.__db.GetStats()
