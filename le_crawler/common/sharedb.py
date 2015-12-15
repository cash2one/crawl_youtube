#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe
__author__ = 'guoxiaohe@letv.com'

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
  def __init__(self, db_name, logger, dboption=None):
    assert db_name, 'db_name must not be null'
    self.db_name_ = db_name
    self.__inner_total_keys = 'store_total_key'
    self.__lock = threading.Lock()
    self.logger_ = logger
    if not dboption:
      self.db_ = leveldb.LevelDB(self.db_name_)
      return
    self.db_ = leveldb.LevelDB(self.db_name_,
                               create_if_missing = dboption.create_if_missing,
                               error_if_exists = dboption.error_if_exists,
                               paranoid_checks = dboption.paranoid_checks,
                               block_cache_size = dboption.block_cache_size,
                               write_buffer_size = dboption.write_buffer_size,
                               block_size = dboption.block_size,
                               max_open_files = dboption.max_open_files)

  @property
  def db_id(self):
    return self.db_name_

  def put(self, key, value):
    try:
      self.db_.Put(key, value)
      self.__update_status()
    except:
      self.logger_.exception('failed put.')
      return False
    return True

  def get(self, key):
    try:
      value = self.db_.Get(key)
    except StopIteration:
      value = None
    return value

  def delete(self, key):
    self.db_.Delete(key)

  def __update_status(self, count = 1):
    pass

  # get batch value [(k, v)]
  def batch_get(self, batch_num=1024):
    rets = []
    if batch_num <= 0:
      return rets
    try:
      iter = self.db_.RangeIter()
      while len(rets) < batch_num:
        rets.append(iter.next())
    except StopIteration:
      pass
    return rets

  # batch delete keys
  def batch_delete(self, keys):
    if not keys:
      return True
    wb = leveldb.WriteBatch()
    for key in keys:
      if key != self.__inner_total_keys:
        wb.Delete(key)
    try:
      self.db_.Write(wb)
      return True
    except:
      self.logger_.exception('failed batch delete.')
      return False

  # batch writer
  def batch_put(self, kvs):
    if not kvs:
      return True
    wb = leveldb.WriteBatch()
    for (k, v) in kvs:
      if k and v:
        wb.Put(k, v)
    try:
      self.db_.Write(wb)
      self.__update_status(count = len(kvs))
    except:
      self.logger_.exception('failed batch put.')
      return False

  def status(self):
    return self.db_.GetStats()

  def size(self):
    s = 0
    for i in self.db_.RangeIter():
      s += 1
    return s

