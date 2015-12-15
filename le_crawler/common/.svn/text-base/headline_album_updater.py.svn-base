#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import time
import MySQLdb
import hashlib

from scrapy.utils.project import get_project_settings
from scrapy import log

class HeadlineLocationUpdater(object):
  def __init__(self, spider):
    self.update_timef = '../data/album_update.data'
    self.spider = spider
    self.update_location_interval = 3600 * 4
    self.debug_ = get_project_settings()['DEBUG_MODEL']
    if self.debug_: # local test
      self.mysql_host_ = '10.200.91.74'
      self.mysql_port_ = 3306
      self.mysql_passwd_ = 'search@letv'
      self.mysql_usr_ = 'search'
      self.mysql_db_ = 'crawler_tmp'
    else: # on line
      self.mysql_host_ = '10.181.155.117'
      #self.mysql_host_ = '10.181.155.116'
      self.mysql_port_ = 3306
      self.mysql_usr_ = 'reptile_wr'
      self.mysql_passwd_ = 'X0pJjIE4'
      self.mysql_db_ = 'headline_video'
    self.tlb_name = 'HeadLineExtractDB'
    self.connect_ = self._get_connect()
    print 'Got Connect:', self.connect_

  def read_lastupdate_timestamp(self):
    import os
    if not os.path.exists(self.update_timef):
      return 0
    f = open(self.update_timef, 'r')
    lines = f.readlines(1)
    f.close()
    if not lines or lines[0] == '':
      return 0
    try:
      return int(lines[0])
    except Exception, e:
      return 0

  def update_timestamp(self):
    f = open(self.update_timef, 'w')
    f.write('%s' % int(time.time()))
    f.close()

  def need_update(self):
    nt = int(time.time()) - self.read_lastupdate_timestamp()
    return nt >= self.update_location_interval

  def _get_connect(self):
    for i in range(5):
      try:
        connect = MySQLdb.connect(host = self.mysql_host_, user =
              self.mysql_usr_, passwd = self.mysql_passwd_, db = self.mysql_db_,
              charset = 'utf8', port = self.mysql_port_)
        self.spider.log('Success connect to mysql!', log.INFO)
        return connect
      except Exception, e:
        self.spider.log('Failed connect to mysql! %s' % e.message, log.ERROR)
        time.sleep(5)
    assert 'Failed connect to mysql: %s %s' %(self.mysql_host_, self.mysql_port_)

  def _get_store_key(self, url):
    return hashlib.md5(url).hexdigest()

  def update_headlinedb(self, urls, location_str):
    if location_str is None or not urls:
      return
    self.connect_.ping(True)
    cursor = self.connect_.cursor()
    self.spider.log('begin update location string', log.DEBUG)
    if type(urls) is list:
      tmpurls = urls
    else:
      tmpurls = [urls]
    for u in tmpurls:
      idstr = self._get_store_key(u)
      try:
        sql_str = """update %s set inlink_location = "%s",
        update_time = %s where id="%s" and
        inlink_location != "%s" """ % (
            self.tlb_name,
            location_str,
            int(time.time()),
            idstr, location_str)
        cursor.execute(sql_str)
      except Exception, e:
        print e
    self.connect_.commit()
    self.spider.log('end update location string', log.DEBUG)

  def close(self):
    self.connect_.cursor().close()
    self.connect_.close()
