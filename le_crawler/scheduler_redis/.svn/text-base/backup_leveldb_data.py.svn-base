#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe 
__author__ = 'guoxiaohe@letv.com'

import pickle
import traceback

import leveldb

from crawler_sch_db import CrawlerDBManger
from leveldb_wrap import LeveldbGetterSetter
from base.logutil import Log

class DataMove(object):
  def __init__(self):
    self.loger_ = Log('data_move_id', '../log/data_move.log')
    self.org_db_oper_ = LeveldbGetterSetter('video_crawler', self.loger_)
    self.new_db_oper_ = CrawlerDBManger('../database/', self.loger_)
    self.loger_.log.info('db data moving is running')

  def move_data(self):
    while True:
      tmplist = self.org_db_oper_.get_requests()
      self.loger_.log.info('got request size: %d' % (len(tmplist)))
      self.loger_.log.info(self.org_db_oper_.get_status())
      self.new_db_oper_.writer_request(tmplist)

if __name__ == '__main__':
  datam = DataMove()
  print 'begin move data'
  datam.move_data()
  print 'end move data'



