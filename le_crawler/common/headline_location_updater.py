#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import time
import MySQLdb
import md5
import re

from scrapy.utils.project import get_project_settings
from scrapy import log

class HeadlineUpdater(object):
  def __init__(self, spider):
    self.spider = spider
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
    self.connect_ = self.get_connect()
    self.num_reg = re.compile(r'(\d+)')
    print 'Got Connect:', self.connect_

  def set_table_name(self, tlb_name):
    self.tlb_name = tlb_name

  def get_connect(self):
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

  def close(self):
    self.connect_.cursor().close()
    self.connect_.close()
    self.connect_ = None

class HeadlineLocationUpdater(HeadlineUpdater):
  def __init__(self,
      spider,
      updatef = '../data/location_update.data',
      update_inv = 3600 * 4
      ):
    HeadlineUpdater.__init__(self, spider)
    self.update_timef = updatef
    self.spider = spider
    self.update_location_interval = update_inv

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

  def _get_store_key(self, url):
    return md5.new(url).hexdigest()

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
        update_time = now() where id="%s" and
        inlink_location != "%s" """ % (
            self.tlb_name,
            location_str,
            idstr, location_str)
        cursor.execute(sql_str)
      except Exception, e:
        print e
    self.connect_.commit()
    self.spider.log('end update location string', log.DEBUG)

class HeadlineAlbumUpdater(HeadlineLocationUpdater):
  NOEXISTS = 1
  TIMEOUT = 2
  IGNORE = 0
  def __init__(self, spider):
    HeadlineLocationUpdater.__init__(self, spider,
        '../data/update_old_album.data',
        86400 * 7)
    self.set_table_name('tbl_today_album_info')

  def need_update_album_info(self, albumid):
    try:
      sql_str = """select col_id from %s where col_zid = "%s" """ % (self.tlb_name,
          albumid)
      cursor = self.connect_.cursor()
      if cursor.execute(sql_str) <= 0:
        return HeadlineAlbumUpdater.NOEXISTS
    except Exception, e:
      print e
      return HeadlineAlbumUpdater.IGNORE
    return HeadlineAlbumUpdater.TIMEOUT if self.need_update() else HeadlineAlbumUpdater.IGNORE

  def __update_album_info(self, albumid, album_info, reason):
    sql_str = ''
    try:
      if not album_info:
        return
      newdict = sorted(album_info['album_vids'].iteritems(), key = lambda
            d:d[0])
      newlist = []
      for i in newdict:
        newlist.extend(i[1])
      vids = '-'.join(newlist)
      if reason == HeadlineAlbumUpdater.NOEXISTS:
        sql_str = '''insert into %s(
        col_zid,
        col_title,
        col_description,
        col_url,
        col_pic,
        col_vids,
        col_cid1,
        col_count,
        col_organizetype,
        col_deleted,
        col_add_type,
        col_create_time,
        col_update_time) values
        ("%s",
        "%s",
        "%s",
        "%s",
        "%s",
        "%s",
        "%s",
        %d,
        %d,
        %d,
        %d,
        now(), now())''' % (
          self.tlb_name,
          album_info['album_id'],
          album_info['album_name'],
          album_info['album_desc'],
          album_info['album_url'],
          album_info['album_pic'],
          vids,
          int(album_info['album_cid']),
          self.__data_convert(album_info['album_video_nums']),
          1,
          0,
          0
          )
      else:
        sql_str = """
        update %s set col_title = "%s",
        col_description = "%s",
        col_pic = "%s",
        col_vids = "%s",
        col_count = "%d",
        col_update_time = now()
        where col_zid=%d and col_vids != "%s"
        """ % (
            self.tlb_name,
            album_info['album_name'],
            album_info['album_desc'],
            album_info['album_pic'],
            vids,
            self.__data_convert(album_info['album_video_nums']),
            album_info['album_id'],
            vids
            )
      self.connect_.cursor().execute(sql_str)
      self.connect_.commit()
      self.spider.log('update album ids: %s' % (vids), log.INFO)
    except Exception, e:
      import traceback
      print traceback.format_exc()
      self.spider.log('Error update album info:%s' % album_info, log.ERROR)
      print e, sql_str
      return False

  def __get_decimals(self, intstr):
    if '千' in intstr:
      return 1000
    elif '万' in intstr:
      return 10000
    elif '十万' in intstr:
      return 100000
    elif '百万' in intstr:
      return 1000000
    elif '千万' in intstr:
      return 10000000
    else:
      return 1

  def __data_convert(self, intstr):
    nums = self.num_reg.findall(intstr)
    if not nums:
      return 0
    numi = int(''.join(nums))
    return numi * self.__get_decimals(intstr)

  def update_album_info(self, album_infos):
    count = 0
    for k, v in album_infos.items():
      reason = self.need_update_album_info(k)
      if reason != HeadlineAlbumUpdater.IGNORE:
        self.__update_album_info(k, v, reason)
        count += 1
    self.spider.log('Update album info:%s' % count, log.INFO)
