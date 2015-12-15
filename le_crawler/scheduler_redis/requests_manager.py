#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe 
__author__ = 'guoxiaohe@letv.com'

import threading
import time
import thread
import redis
import signal
import os

from base.logutil import Log

from crawler_sch_db import CrawlerDBManger
from redisdb_wrap import RequestGetterWriter


# request get and feed manager
class RequestsManage(threading.Thread):
  def __init__(self, db, linredis, loutredis, inredis_qsize = 1024,
      outredis_qsize = 86400, loger = None):
    threading.Thread.__init__(self)
    self.exit_ = False
    self.inredis_qsize_ = inredis_qsize
    self.outredis_qsize_ = outredis_qsize
    self.db_ = db
    self.req_prods_ =  linredis
    self.req_custs_ = loutredis
    if loger:
      self.log_ =  loger
    else:
      self.log_ = Log()
    
  @classmethod
  def from_settings(cls, settings, loger):
    #setting.get('REDIS_SERVER_LIST')
    #redishs = [('10.150.140.87', 6379)]
    redishs = [
        ('10.150.140.82', 6379),
        ('10.150.140.83', 6379),
        ('10.150.140.84', 6379),
        ('10.150.140.85', 6379),
        ('10.150.140.86', 6379),
        ('10.150.140.87', 6379),
        ('10.180.155.135', 6379),
        ('10.180.155.136', 6379),
        ('10.180.155.137', 6379),
        ('10.180.155.138', 6379),
        ('10.180.155.139', 6379),
        ('10.130.208.60', 6379),
        ('10.130.208.64', 6379),
        ('10.130.208.65', 6379),
        ('10.130.208.66', 6379),
        ('10.130.208.67', 6379),
        ]
    reqps = []
    reqcs = []
    shid = 0
    for i in redishs:
      reqps.append(
          RequestGetterWriter(redis.Redis(host = i[0], port = i[1], socket_timeout = 1),
            'video_crawler:input_requests_%d' % (shid), loger = loger))
      reqcs.append(
          RequestGetterWriter(redis.Redis(host = i[0], port = i[1], socket_timeout = 1),
            'video_crawler:output_requests_%d' % (shid), loger = loger))
      shid += 1
    print 'Load redis in queue:[%d]' % len(reqps)
    print 'Load redis out queue:[%d]' % len(reqcs)
    # move leveldb instances to leveldb_wrap
    lgeter = CrawlerDBManger('../database/', loger)
    return cls(lgeter, reqps, reqcs, 10240, 4096, loger)

  def exit(self, signalNum, currentStackFrame):
    msg = 'reciver: exit[%d]' % (signalNum)
    print msg
    self.log_.log.info(msg)
    self.exit_ = True

  # fetcher request form redis to leveldb
  def run_fetch_req(self):
    self.log_.log.info('Running fetcher request thread')
    while not self.exit_:
      lentmp = 0
      for iredis in self.req_prods_:
        tmpreqs = iredis.get_requests(self.inredis_qsize_, False)
        if not tmpreqs or len(tmpreqs) < 0:
          continue
        self.db_.writer_request(tmpreqs)
        lentmp += len(tmpreqs)
      if lentmp > 0:
     	  self.log_.log.info('Collect request size[%d]' % (lentmp))
      else:
        time.sleep(1)
      #FIXME(xiaohe):if fetch is the n
      time.sleep(0.1)
    self.log_.log.info('exit fetcher request thread')

  def get_db_status(self):
    return self.db_.get_status()
  # upload request from leveldb to redis
  def run_upload_req(self):
    self.log_.log.info('Running upload request thread')
    reciver_idx = 0
    ideal_num = 0
    while not self.exit_:
      #rets = self.db_.get_requests()
      for rets in self.db_.get_requests_iter(self.outredis_qsize_):
        if not rets or len(rets) < 0:
          ideal_num += 1
          if ideal_num % 100 == 0:
            self.log_.log.info('Nothin got from DB for [%d]'
                %(ideal_num * 5))
          time.sleep(1)
          continue
      # will be block if not meet
        ideal_num = 0
        failed_num = 0
        redis_num = len(self.req_custs_)
        while True:
          if reciver_idx >= redis_num:
            reciver_idx = 0
          req_cus = self.req_custs_[reciver_idx]
          # if remote queue size little than 23 will upload
          if req_cus.writer_request(rets, 23):
            self.log_.log.debug('Success upload [%d] with [%s]' %(len(rets),
              req_cus.key_))
            reciver_idx += 1
            break
          else:
            failed_num += 1
            self.log_.log.debug('Failed upload size[%d] with [%s], one loop' %(len(rets), req_cus.key_))
            if failed_num == redis_num:
              self.log_.log.error('All output queue is Failed upload[%d]'
                  %(len(rets)))
              time.sleep(1)
            reciver_idx += 1
    self.log_.log.info('exit upload request thread')

  def run(self):
    thread.start_new_thread(self.run_fetch_req, ())
    thread.start_new_thread(self.run_upload_req, ())
    while not self.exit_:
      time.sleep(10)
    for i in self.req_prods_:
      i.exit()
    for j in self.req_custs_:
      j.exit()
    self.log_.log.info('Request manager exit normal')
 
 # main 


def sig_handler(num, frame):
  global system_exit_sig
  system_exit_sig = False
  print 'reciver: %d' % (num)
  print frame

loger = Log('request_mgr_log', '../log/crawler_db.log')
manager = RequestsManage.from_settings(None, loger)
signal.signal(signal.SIGINT, manager.exit)
signal.signal(signal.SIGTERM, manager.exit)

if __name__ == '__main__':
  manager.setDaemon(True)
  manager.start()
  fp = open('dbservice.pid', 'w')
  fp.write(str('%d' % (os.getpid())))
  fp.close()
  count = 0
  while manager.isAlive():
    if count > 300:
      loger.log.info(manager.get_db_status())
      count = 0
    time.sleep(5)
    count += 1
  fp = open('dbservice.pid', 'w')
  fp.write(str('%d' % (-1)))
  fp.close()
