#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import sys
import MySQLdb
import time
import md5
import traceback

reload(sys)
sys.setdefaultencoding('utf8')

from scrapy import log
from scrapy.utils.project import get_project_settings

from extend_map_handler import ExtendMapHandler
from ..base.utils import *
from ..base.url_filter import UrlFilter
from ..core.page_writer import PageWriterWithBuff


class TodayTvWriter(PageWriterWithBuff):
  def __init__(self, spider):
    super(TodayTvWriter, self).__init__(spider)
    self.set_name('TodayTvWriter')
    self.connect_ = None
    self.debug_ = get_project_settings()['DEBUG_MODEL']
    if self.debug_: # local test
      self.mysql_host_ = '10.200.91.74'
      self.mysql_port_ = 3306
      self.mysql_passwd_ = 'search@letv'
      self.mysql_usr_ = 'search'
      self.mysql_db_ = 'crawler_tmp'
    else: # on line
      #TODO(xiaohe): add secondary host select
      self.mysql_host_ = '10.181.155.116'
      #self.mysql_host_ = '10.181.155.117'
      self.mysql_port_ = 3306
      self.mysql_usr_ = 'reptile_wr'
      self.mysql_passwd_ = 'X0pJjIE4'
      self.mysql_db_ = 'headline_video'

    self.store_pages_ = 0
    self.extend_map_handler_ = ExtendMapHandler.get_instance()

  @property
  def conn(self):
    while not self.exit_sig:
      try:
        if not self.connect_:
          self.connect_ = MySQLdb.connect(host = self.mysql_host_, user =
              self.mysql_usr_, passwd = self.mysql_passwd_, db = self.mysql_db_,
              charset = 'utf8', port = self.mysql_port_)
          self.spider_.log('Success connect to mysql!', log.INFO)
        return self.connect_
      except Exception, e:
        self.spider_.log('Error connect to mysqldb[%s]:[%s, %s, %s, %s]' % (e,
          self.mysql_host_, self.mysql_port_, self.mysql_db_,
          self.mysql_usr_), log.ERROR)
        self.release_connect()
        time.sleep(4)
        continue

  def release_connect(self):
    if self.connect_:
      self.connect_.cursor().close()
      self.connect_.close()
      self.connect_ = None

  # base reg match
  # judgment the url is accept to crawl
  def _get_store_key(self, url):
    return md5.new(url).hexdigest()
  # return [(url, {property:value})]

  def finalize(self):
    super(PageWriterWithBuff, self).finalize()
    time.sleep(10)
    self.release_connect()

  def writer(self, item):
    self.__write_mysql_internal(item)

  def get_connect(self):
    while not self.exit_:
      try:
        if not self.connect_:
          self.connect_ = MySQLdb.connect(host = self.mysql_host_, user =
              self.mysql_usr_, passwd = self.mysql_passwd_, db = self.mysql_db_,
              charset = 'utf8', port = self.mysql_port_)
          self.spider_.log('Success connect to mysql!', log.INFO)
        return self.connect_
      except Exception, e:
        self.spider_.log('Error connect to mysqldb[%s]:[%s, %s, %s, %s]' % (e,
          self.mysql_host_, self.mysql_port_, self.mysql_db_,
          self.mysql_usr_), log.ERROR)
        self.release_connect()
        time.sleep(4)
        continue

  def __write_mysql_internal(self, item):
    if not item:
      return
    try:
      sql_str = ''
      url = UrlFilter.get_base_url(item['url']).encode('utf8').strip()
      if not url or not self.extend_map_handler_.settings.accept_url(url):
        self.spider_.log('ignore url:[%s]' % (url), log.INFO)
        return
      page = item['page'].decode(item['page_encoding']).encode('utf8')
      refer_url = None
      if item.has_key('referer'):
        refer_url = item['referer'] or url
      mapid = self.extend_map_handler_.settings.get_id_from_referer(refer_url)
      (refer_url)
      if not mapid:
        self.spider_.log('Failed Got Id:[%s] for [%s]' % (url, refer_url), log.INFO)
        return
      tbl_n = self.extend_map_handler_.settings.get_table_name(id = mapid)
      if not tbl_n:
        self.spider_.log('Failed Found Table name [%s]' % (url), log.ERROR)
        return
      #self.spider_.log('Finished parser[%s]' % (url), log.INFO)
      idstr = self._get_store_key(url) 
      conn = self.get_connect()
      conn.ping(True)
      cursor = conn.cursor()
      if cursor.execute("""select id from %s where id='%s'""" % (tbl_n, idstr)) > 0:
        self.spider_.log('skip store, dupe [%s],[%s]' % (idstr, url), log.INFO)
        return
      sql_str = 'insert into %s' % (tbl_n)
      sql_str += "(id, url, html, parse_state, category, fetch_time, extend_map) values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')"
      cpage = str_gzip(page)
      tmp_ext = '{}'
      location_str = \
          self.extend_map_handler_.settings.get_location_from_referer(refer_url) or ''
      tmp_ext = self.extend_map_handler_.lookup_extend_map(url)
      if not tmp_ext:
        tmp_ext = '{}'
        self.spider_.log('Failed lookup extend map for %s' % (url), log.ERROR)
        return
      ac_category = self.extend_map_handler_.settings.get_category_name(refer_url)
      if ac_category:
        category = str.split(ac_category, '_')[0]
      else:
        category = ''
      cursor.execute("""insert into %s 
      (id, url, parse_state, category, fetch_time, extend_map, html, inlink_location) values
      (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)""" % (tbl_n), (idstr, url, 0, category,
        int(time.time()) * 1000, str(tmp_ext), cpage, location_str))
      conn.commit()
      #cursor.close()
      self.store_pages_ += 1
      self.spider_.log('Store [%d] pages [%s]' % (self.store_pages_, url), log.INFO)
    except Exception, e:
      #print e
      #print traceback.format_exc()
      self.spider_.log('store to mysql error [%s] [%s] with coding [%s]' %(sql_str,
        traceback.format_exc(), item['page_encoding']), log.ERROR)
      #self.release_connect()
