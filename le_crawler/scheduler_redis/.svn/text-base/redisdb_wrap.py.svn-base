#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe 
__author__ = 'guoxiaohe@letv.com'

import time

from base.logutil import Log

# move requests from in-redis to leveldb
class RequestGetterWriter(object):
  # redis, redis server
  # timeout
  def __init__(self, redis, key, id_str = None, loger = None):
    self.redis_ = redis
    self.key_ = key
    self.exit_ = False
    self.id_ = id_str
    # if request queue is not meet reqiret nums, will be return None under force is False
    # but is allways failed for fore_feed_times_threshlod times(seconds) will be return results
    self.up_meet_times_ = 0
    self.force_feed_times_threshold_ = 60 * 10
    if loger:
      self.log_ = loger
    else:
      self.log_ = Log()
    self.log_.log.info('using key:[%s]' %(self.key_))

  def exit(self):
    self.exit_ = True

  # batch_num: batch requests get
  # timeout: if requirt num is not
  def get_requests(self, batch_num = 1024, force = False):
    try:
      remote_len = 0
      rets = []
      remote_len = self.redis_.zcard(self.key_)
      #print 'nowlen [%d] for key [%s], batch_num[%d]' %(remote_len, self.key_,
      #    batch_num)
      if remote_len <= 0:
        return []
      nowt = int(time.time())
      if remote_len >= batch_num:
        remote_len = batch_num
      elif remote_len < batch_num and not force:
        difft = nowt - self.up_meet_times_ 
        if difft < self.force_feed_times_threshold_:
          return []
        else:
          self.log_.log.info('Not meet reqiret len for[%d]s from key[%s]' % (difft, self.key_))
      self.up_meet_times_ = nowt
      pipe = self.redis_.pipeline(transaction = True)
      #pipe.ltrim(self.key_, remote_len, -1)
      #self.log_.log.info('begin get key[%s]' % (self.key_))
      pipe.zrange(self.key_, 0, remote_len - 1)
      pipe.zremrangebyrank(self.key_, 0, remote_len - 1)
      rets, trs = pipe.execute()
      if not trs:
        self.log_.log.error('Failed remove request from request queue')
      self.log_.log.info('get key[%s] len[%s]' % (self.key_, len(rets)))
      return rets
    except Exception, e:
      self.log_.log.error('get request error from [%s] with [%s]' % (self.key_, e.message))
      return []

# requests: request list, blocked
  def writer_request(self,requests, remote_que_size = 4096):
    try:
      self.log_.log.debug('begin Upload request to: [%s]' % (self.key_))
      rlen = self.redis_.llen(self.key_)
      #print '1011: get len[%d] with key[%s]' %(len, self.key_)
      if rlen > remote_que_size:
        self.log_.log.debug('Dest queue [%s]is full[%d], under[%d]'
            %(self.key_, rlen, remote_que_size))
        return False
      reqlen = len(requests)
      #self.log_.log.info('Upload request:[%d] to [%s]' % (reqlen, self.key_))
      p = self.redis_.pipeline()
      p.rpush(self.key_, *requests)
      if not p.execute():
        self.log_.error('Failed push:[%s] to [%s]' %(requests, self.key_))
      #self.log_.log.debug('Upload request:[%d]' % len(requests))
      self.log_.log.info('Finished Upload request:[%d] to [%s]' % (reqlen, self.key_))
      return True
    except Exception, e:
      self.log_.log.error('Error writer to:[%s] with error[%s]' % (self.key_, e.message))
      return False


