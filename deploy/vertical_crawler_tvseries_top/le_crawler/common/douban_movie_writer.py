#!/usr/bin/python
#-*-coding:utf-8-*-
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'zhaoguozhu@letv.com'

import json
import MySQLdb
import time
import md5
import traceback

from scrapy import log

from ..base.utils import *
from ..core.page_writer import PageWriterWithBuff
from ..base.url_normalize import UrlNormalize

class DouBanMovieWriter(PageWriterWithBuff):
  def __init__(self, spider):
    super(DouBanMovieWriter, self).__init__(spider)
    self.set_name('DouBanMovieWriter')
    self.connect_ = None
    self.mysql_host_ = '10.181.155.117'
    self.mysql_port_ = 3307
    self.mysql_passwd_ = 'search@letv'
    self.mysql_usr_ = 'search'
    self.mysql_db_ = 'crawler_moviepic'
    self.tbl_n_ = 'DoubanMovieWebDb'

    self.store_pages_ = 0

  def release_connect(self):
    if self.connect_:
      self.connect_.cursor().close()
      self.connect_.close()
      self.connect_ = None

  def _get_store_key(self, url):
    return md5.new(url).hexdigest()

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

  def __write_mysql_moviejson(self, item ,idstr, url, cursor):
    item_frmjson = json.loads(item['page'])
    item_frmjson_subject= item_frmjson[u'subject']
    title = item_frmjson_subject[u'title'].encode('utf-8')
    directors = ','.join(item_frmjson_subject[u'directors']).encode('utf-8')
    actors = ','.join(item_frmjson_subject[u'actors']).encode('utf-8')
    release_year = item_frmjson_subject[u'release_year'].encode('utf-8')
    region = item_frmjson_subject[u'region'].encode('utf-8')
    types = ','.join(item_frmjson_subject[u'types']).encode('utf-8')
    rate = item_frmjson_subject[u'rate']
    duration = item_frmjson_subject[u'duration'].encode('utf-8')
    movie_id = item_frmjson_subject[u'id']
    cpage = str_gzip(item['page'].encode('utf-8'))

    if cursor.execute("""select id from %s where id='%s'""" % (self.tbl_n_, idstr)) > 0:
        cursor.execute("""update %s set url = %%s,\
                    movie_id = %%s, title = %%s,\
                    directors = %%s, actors = %%s,\
                    release_year = %%s, region = %%s, types = %%s,\
                    rate = %%s, duration = %%s, page_json = %%s,\
                    update_time = %%s where id= %%s"""
                    %(self.tbl_n_), (url, movie_id, title, directors, actors,
                    release_year, region, types, rate, duration, cpage, int(time.time()) * 1000, idstr))
    else:
        cursor.execute("""insert into %s
        (id, url, movie_id, title, directors, actors,
        release_year, region, types, rate, duration, page_json, update_time) values
        (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)"""
        % (self.tbl_n_), (idstr, url, movie_id, title, directors, actors,
        release_year, region, types, rate, duration, cpage,
        int(time.time()) * 1000))

  def __write_mysql_moviemisc(self, item, idstr, url, cursor):
    item_frmjson = item['page']
    description = str_gzip(item_frmjson.get(u'desc','').encode('utf-8'))
    tags =  json.dumps(item_frmjson.get(u'tags','')).encode('utf-8')
    trailer = json.dumps(item_frmjson.get(u'trailer','')).encode('utf-8')
    award = item_frmjson.get(u'award','').encode('utf-8')
    item_frmjson_additional= item_frmjson[u'additional']
    language = item_frmjson_additional.get(u'语言','').encode('utf-8')
    screenwriter = item_frmjson_additional.get(u'编剧','').encode('utf-8')
    another_title = item_frmjson_additional.get(u'又名','').encode('utf-8')
    imdblink = item_frmjson_additional.get(u'IMDb链接','')
    cpage = str_gzip(json.dumps(item['page']).encode('utf-8'))

    if cursor.execute("""select id from %s where id='%s'""" % (self.tbl_n_, idstr)) > 0:
      cursor.execute("""update %s set url = %%s,
                     another_title = %%s, language = %%s, screenwriter =
                     %%s, tags = %%s,
                     imdblink = %%s, description = %%s, trailer = %%s,
                     award = %%s, page_misc = %%s, update_time = %%s where
                     id= %%s """
                     % (self.tbl_n_), (url, another_title, language, screenwriter, tags,
                     imdblink, description, trailer, award, cpage,
                     int(time.time()) * 1000, idstr))
    else:
      cursor.execute("""insert into %s
      (id, url, another_title, language, screenwriter, tags, imdblink, description, trailer, award,
      page_misc, update_time) values
      (%%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s, %%s)"""
      % (self.tbl_n_), (idstr, url, another_title, language, screenwriter, tags, imdblink, description, trailer, award,
      cpage, int(time.time()) * 1000))


  def __write_mysql_pic(self, item, idstr, url, cursor):
      pic_list = []
      pic_list = item['content_imgs']
      pic_urlstr = str_gzip(json.dumps(pic_list))

      if cursor.execute("""select id from %s where id='%s'""" % (self.tbl_n_, idstr)) > 0:
        cursor.execute("""select pic from %s where id='%s'""" % (self.tbl_n_, idstr))
        recd_fetched = cursor.fetchone()
        if recd_fetched[0]:
          pic_urlstr = recd_fetched[0]
          pic_urlstr_unzip = str_unzip(pic_urlstr)
          pic_list_unzip = json.loads(pic_urlstr_unzip)
        else:
          pic_list_unzip = ""

        pic_urlset = set(pic_list_unzip)
        pic_urlset.union(pic_list)
        pic_urlstr = str_gzip(json.dumps(list(pic_urlset)))
        cursor.execute("""update %s set url = %%s, pic = %%s, update_time =
                          %%s where id= %%s"""
                       % (self.tbl_n_),(url, pic_urlstr, int(time.time()) * 1000, idstr))
      else:
        cursor.execute("""insert into %s
        (id, url, pic, update_time) values
        (%%s, %%s, %%s, %%s)"""
        % (self.tbl_n_), (idstr, url, pic_urlstr, int(time.time()) * 1000))


  def __write_mysql_internal(self, item):
    if not item:
      return
    try:
      url = UrlNormalize.get_instance().get_unique_url(item['url']).encode('utf8').strip()
      if not url:
        self.spider_.log('ignore url:[%s]' % (url), log.INFO)
        return
      idstr = self._get_store_key(url)

      conn = self.get_connect()
      conn.ping(True)
      cursor = conn.cursor()
      if item['item_type'] == 'MOVIES_JSON':
        self.__write_mysql_moviejson(item, idstr, url, cursor)
      elif item['item_type'] == 'MOVIES_MISC':
        self.__write_mysql_moviemisc(item, idstr, url, cursor)
      elif item['item_type'] == 'PIC':
        self.__write_mysql_pic(item, idstr, url, cursor)

      conn.commit()

    except Exception, e:
      print e
      print traceback.format_exc()
      self.spider_.log('store to mysql error [%s] [%s] with coding' %(sql_str,
        traceback.format_exc()), log.ERROR)
      #self.release_connect()
