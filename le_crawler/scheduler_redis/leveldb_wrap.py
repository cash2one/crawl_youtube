#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe 
__author__ = 'guoxiaohe@letv.com'

import pickle
import traceback

import leveldb
from base.logutil import Log
#from leveldbClient import database

class LeveldbWrap(object):
  def __init__(self, data_dir = '../database/crawler_request.db'):
    #leveldbh = 'tcp://127.0.0.1:1547'
    #setting.get('LEVELDB_HOST', 'tcp://127.0.0.1:1547')
    #db =  database.leveldb()
    self.db_ =  leveldb.LevelDB(data_dir)
  def put(self, key, value):
    try:
      self.db_.Put(key, value)
    except Exception, e:
      print e
      print traceback.format_exc()
      return False
    return True

  def get(self, key):
    try:
      value = self.db_.Get(key)
    except Exception, e:
      #print e
      #print traceback.format_exc()
      value = None
    return value


class RemoteLock(object):
  def lock(self, nonblock):
    pass

  def unlock(self):
    pass

  def test_locked(self):
    pass

class KeyOperWrap(object):
  def __init__(self, org_key, db, revers = False, loger = None):
    self.db_ = db
    self.store_key_ =  org_key
    self.revers_ =  revers
    self.seek_pos_key_ = '%s:seek_pos' % self.store_key_
    self.store_pos_key_ = '%s:last_pos' %  self.store_key_
    self.total_request_num_key_ = '%s:total_request' %  self.store_key_
    self.start_key_ = 0
    self.in_key_step_ = 1
    self.in_max_key_ = 0x7ffffffffffffff7
    if not loger:
      self.log_ = Log()
    else:
      self.log_ = loger

    if self.revers_:
      self.start_k_ey_ = self.in_max_key_
      self.in_key_step_ = -1

  def __key_gen(self, key_pos):
    return '%s:%d' %(self.store_key_, key_pos)
  # next_pos, next_key
  def update_request_num(self, num):
    nownum = int(self.db_.get(self.total_request_num_key_) or 0)
    nownum += num
    self.db_.put(self.total_request_num_key_, str(nownum))

  def get_requests_num(self):
    return self.db_.get(self.total_request_num_key_)

  def __next_key(self, cur_pos):
    if cur_pos < 0 or cur_pos >= self.in_max_key_:
      raise 'key out of range:[%d]' %(cur_pos)
      return -1, None
    next_pos = cur_pos + self.in_key_step_
    return next_pos, self.__key_gen(next_pos)

  def __update_key(self, key, value):
    try:
      return self.db_.put(key, '%s' %(value))
      self.log_.get_log.debub('Update:[%s] with [%s]' %(key, value))
      return True
    except Exception, e:
      self.log_.log.error(e)
      self.log_.log.error(traceback.format_exc())
      self.log_.log.error('ERROR while try to update seek postion value')
      return False

  # query key value from db
  def __get_pos(self, key):
    try:
    #  print 'begin query leveldb [%s]' % key
      cur_pos = self.db_.get(key)
    #  print 'finished query leveldb'
    except Exception, e:
      self.log_.log.error(e)
      self.log_.log.error(traceback.format_exc())
      self.log_.log.error('Failed Get Position Key:[%s]' % key)
      return -1
    if not cur_pos:
      cur_pos = self.start_key_
      self.log_.log.info('[%s], using start key[%s]'
          %(key, cur_pos))
    return int(cur_pos)

  def update_seek_key(self, new_pos):
    return self.__update_key(self.seek_pos_key_, new_pos)

  def update_store_key(self, new_pos):
    return self.__update_key(self.store_pos_key_, new_pos)

  # return next_pos, key_str
  def next_seek_key(self):
    cur_sk = self.__get_pos(self.seek_pos_key_)
    #print 'seek position key is[%s], cur seek is [%d]' % (self.seek_pos_key_, cur_sk)
    last_stp = self.__get_pos(self.store_pos_key_)
    if cur_sk >= last_stp:
      #print 'Last pos:[%d], seek pos[%d]' %(last_stp, cur_sk)
      return -1, None
    if cur_sk >= 0:
      np, key = self.__next_key(cur_sk)
      #print '+++++++++++++++++++++++%d, %s' %(np, key)
      return np, key
    return -1, None

  def next_store_key(self):
    cur_st = self.__get_pos(self.store_pos_key_)
    if cur_st >= 0:
      np, key = self.__next_key(cur_st)
      #print '+++++++++++++++++++++++%d, %s' %(np, key)
      return np, key
    return None, None
    
    
class LeveldbGetterSetter(object):
  def __init__(self, key, loger = None):
    self.request_store_batch_num_ = 512
    self.request_output_multiple_ = 50
    self.db_ =  LeveldbWrap('../database/crawler_request.db')
    self.keyops_ = KeyOperWrap(key, self.db_, False, loger)
    self.key_ = key
    if not loger:
      self.log_ = Log()
    else:
      self.log_ = loger

  # pickle list
  def join_request_to_str(self, requests):
    return pickle.dumps(requests, 1)

  def get_status(self):
    rets = []
    rets.append('leveldb status:')
    rets.append(self.keyops_.get_requests_num())
    ns, nsk = self.keyops_.next_seek_key()
    nst, nstk = self.keyops_.next_store_key()
    rets.append([ns, nsk])
    rets.append([nst, nstk])
    return rets

  # return list
  def split_request_from_str(self, requeststr):
    if not requeststr or len(requeststr) <= 0:
      return None
    try:
      rets = pickle.loads(requeststr)
      return rets
    except Exception, e:
      self.log_.log.error('error unpack[%s]'% requeststr)
      self.log_.log.error(e)
      return None

  # requests is list, control store batch num
  def writer_request(self, requests):
    if not requests or len(requests) <= 0:
      return
    sidx = 0
    while sidx < len(requests):
      self.__writer_request(requests[sidx : (sidx +
        self.request_store_batch_num_)])
      sidx += self.request_store_batch_num_

  def __writer_request(self, requests):
    if not requests or len(requests) <= 0:
      return True
    st_ps, stk = self.keyops_.next_store_key()
    #print 'next store key is :%s %s' %(st_ps, stk)
    if not stk or st_ps < 0:
      self.log_.log.error('Failed Got store key for:[%s]' % requests)
      return False
    store_str = self.join_request_to_str(requests)
    self.log_.log.debug('Store new request[%d] with key[%s]' % (len(store_str), stk))
    rets = self.db_.put(stk, store_str)
    self.keyops_.update_request_num(len(requests))
    if not rets:
      self.log_.log.error('Error while try store requst to leveldb')
      return False
    return self.keyops_.update_store_key(st_ps)

  def get_requests(self):
    rets = []
    for i in range(0, self.request_output_multiple_):
      rets.extend(self._get_requests())
    return rets
    
  def _get_requests(self):
    np, sek = self.keyops_.next_seek_key()
    rets = []
    if np < 0 or not sek:
      self.log_.log.error('Failed Got seek key for:[%s]' % self.key_)
      return []
    try:
      self.log_.log.debug('++++++Get next seek key:[%s, %d]' %(sek, np))
      rets = self.db_.get(sek)
      #print '-------------------get request [%s] len=[%d] from [%s]' % (rets,
      #    len(rets), sek)
    except Exception, e:
      self.log_.log.error(e.message)
      self.log_.log.error(traceback.format_exc())
      self.log_.log.error('Error while get key[%s]' %(sek))
      return []
    if not rets:
      self.log_.log.info('Empty result with[%s]' %(sek))
      return []
    reqs = self.split_request_from_str(rets)
    if not reqs or len(reqs) < 0:
      self.log_.log.error('Failed pickle result with[%s]' %(sek))
    self.keyops_.update_seek_key(np)
    return reqs

