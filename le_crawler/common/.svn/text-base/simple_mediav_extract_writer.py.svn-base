#-*-coding:utf-8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import json
import pika
import MySQLdb
import time
import md5
import traceback
import re

from thrift.transport  import  TSocket
from thrift.transport  import  TTransport
from thrift.protocol import  TBinaryProtocol

from scrapy import log
from scrapy.utils.project import get_project_settings

from le_crawler.core.page_writer import PageWriterWithBuff
from le_crawler.genpy.video_media.ttypes import MediaVideo
from le_crawler.common.extend_map_handler import ExtendMapHandler
from le_crawler.base.thrift_util import thrift_to_str
from le_crawler.base.thrift_util import SERIALIZE_TYPE_FAST
from le_crawler.core.docid_generator import gen_docid
from le_crawler.core.links_extractor import LinksExtractor
from le_crawler.core.base_extract import ExtractLinks

"""
for video search realtime video search
"""

def get_source_and_id(url):
  if 'letv.com' in url:
    return 'letv', 1
  elif 'sohu.com' in url:
    return 'sohu', 2
  elif 'iqiyi.com' in url:
    return 'iqiyi', 3
  elif 'youku.com' in url:
    return 'youku', 4
  elif 'baomihua.com' in url:
    return 'baomihua', 5
  elif 'v.ifeng.com' in url:
    return 'ifeng', 6
  elif 'v.qq.com' in url:
    return 'qq', 7
  elif 'ku6.com' in url:
    return 'ku6', 8
  elif 'tudou.com' in url:
    return 'tudou', 9
  elif 'video.sina.com.cn' in url:
    return 'sina', 10
  elif 'v.163.com' in url:
    return '163', 11
  elif 'pptv.com' in url:
    return 'pptv', 15
  elif 'tv.cntv.com' in url or 'news.cntv.cn' in url:
    return 'cntv', 16
  elif 'imgo.tv' in url:
    return 'imgo', 17
  elif 'm1905.com' in url:
    return 'm1905', 18
  elif 'wasu.cn' in url:
    return 'wasu', 19
  elif 'baofeng.com' in url:
    return 'baofeng', 20
  elif 'kumi.cn' in url:
    return 'kumi', 21
  elif 'bt.ktxp.com' in url:
    return 'ktxp', 22
  elif 'v.61.com' in url:
    return '61', 23
  elif '56.com' in url:
    return '56', 24
  elif 'tangdou.com' in url:
    return 'tangdou', 25
  elif 'joy.cn' in url:
    return 'joy', 26
  elif '370kan.com' in url:
    return '370kan', 27
  elif '100pd.com' in url:
    return '100pd', 28
  elif 'aipai.com' in url:
    return 'aipai', 29
  elif 'people.com.cn' in url:
    return 'people', 30
  else:
    return None

def get_category_name_id(nickname):
  if not nickname:
    return None
  if 'movie' == nickname:
    return '电影', 1
  elif 'ent' == nickname:
    return '娱乐', 3
  if 'sport' == nickname:
    return '体育', 4
  if 'animation' == nickname:
    return '动漫', 5
  if 'finance' == nickname:
    return '财经', 22
  if 'joke' == nickname:
    return '搞笑', 10
  if 'fashion' == nickname:
    return '风尚', 20
  else:
    return '资讯', 6

class RealtimeVideoWriter(PageWriterWithBuff):
  def __init__(self, spider, bufsize = 4096):
    super(RealtimeVideoWriter, self).__init__(spider, bufsize)
    self.set_name('RealtimeVideoWriter')
    from le_crawler.base.start_url_loads import StartUrlsLoader
    self.extend_map_handler_ = ExtendMapHandler.get_instance(
        StartUrlsLoader.get_instance('../start_urls/'))
    self.new_links_extract = \
      LinksExtractor('le_crawler.common.simple_webcrawler_settings')

    # rabittmq
    self.ips_ = ['10.150.140.78', '10.150.140.77', '10.150.140.79']
    self.port_ = 5672
    self.exchange = 'hbase.exchange'
    self.queue = 'hbase.search2.realtime.queue'
    self.channel = self._get_channel()
    assert self.channel
    # othres
    self.total_send = 0
    self.debug = get_project_settings()['DEBUG_MODEL']
    self.using_links_extract_ = get_project_settings().get('USING_EXTRACT_LINKS',
        False)

    self.tbl_n = 'crawler_video'
    self.connect_ = None
    self.mysql_host_ = '10.150.140.80'
    self.mysql_port_ = 3306
    self.mysql_passwd_ = 'search@letv'
    self.mysql_usr_ = 'search'
    self.mysql_db_ = 'crawler'
    self.mysql_tbl_num_ = 32


  def _get_channel(self):
    for ip in self.ips_:
      try:
        self.rabitt_ = pika.BlockingConnection(pika.ConnectionParameters(
                         host = ip, port = self.port_))
        channel = self.rabitt_.channel()
        channel.exchange_declare(exchange =self.exchange,
            durable = True,
            auto_delete = False,
            exchange_type='fanout')
        #channel.queue_declare(queue = self.queue, exchange)
        self.spider.log('Success connect to rabittmq!', log.INFO)
        return channel
      except Exception, e:
        print e
        continue
    return None

  def _gen_table_name(self, prefix, docid):
    id = int(docid) % self.mysql_tbl_num_
    return '%s_%s' % (prefix, id)

  def close_rabitt(self):
    if self.rabitt_:
      import time
      time.sleep(1)
      self.rabitt_.close()

  def get_connect_mysql(self):
    while not self.exit_:
      try:
         if not self.connect_:
            self.connect_ = MySQLdb.connect(host = self.mysql_host_, user =
                self.mysql_usr_, passwd = self.mysql_passwd_, db = self.mysql_db_,
                charset = 'utf8', port = self.mysql_port_)
            self.spider_.log('RealtimeVideoWriter Success connect to mysql!', log.INFO)
         return self.connect_
      except Exception, e:
         self.spider_.log('Error connect to mysqldb[%s]:[%s, %s, %s, %s]' % (e,
                          self.mysql_host_, self.mysql_port_, self.mysql_db_,
            self.mysql_usr_), log.ERROR)
         self.release_connect()
         time.sleep(4)
         continue


  def release_connect_mysql(self):
    self.spider_.log('RealtimeVideoWriter release_connect_mysql', log.INFO)
    if self.connect_:
      self.connect_.cursor().close()
      self.connect_.close()
      self.connect_ = None


  def _get_value(self, item, key, default_value = None):
    if not item:
      return default_value
    if item.has_key(key):
      return item[key]

  def _batch_fill_items(self, item):
    if not item:
      return None
    retlist = []
    sta, links = self.new_links_extract.extract_block_links(item['url'], body =
        item['page'], bd_type = LinksExtractor.HTML_EXTRA)
    if not sta or not links:
      self.spider.log('Failed extract page:%s' % (item['url'],
        log.ERROR))
      return retlist    
    cate_id = self._extract_pg_category_id(item)
    for i in links:
      if not i.extend_map:
        continue
      i.extend_map['category_id'] = cate_id
      video_m = self._fill_video_media_from_extend_map(i.extend_map, i.url,
          item.get('referer', None))
      if video_m:
        retlist.append(video_m)
      else:
        self.spider.log("Failed convert item to MediaVideo:%s refer:%s" %
            (item.get('url'), item.get('referer', None)), log.ERROR)
    return retlist
    
  def _fill_video_media_from_extend_map(self, extend_map, url, ref_url):
    media_video = MediaVideo()
    import ctypes
    # cause fingerprint is singed value
    media_video.id = 'crawler_%s' % ctypes.c_uint64(gen_docid(url)).value
    # extend map
    tmp_ext_json = extend_map 
    if tmp_ext_json.has_key('title'):
      media_video.title = tmp_ext_json['title'].encode('utf8')
    else:
      self.spider.log('Failed Found Title, %s, %s' % (url, ref_url), log.ERROR)
      return None
    if tmp_ext_json.has_key('length'):
      media_video.duration = tmp_ext_json['length']
    else:
      media_video.duration = '--:--'

    if tmp_ext_json.has_key('cover'):
      media_video.poster = tmp_ext_json['cover']
    sourid = get_source_and_id(url)
    if sourid:
      media_video.source, media_video.source_id = sourid[0], sourid[1]
    else:
      self.spider.log('Failed Found sourceid, %s, %s' % (url, ref_url), log.ERROR)
      return None
    # extend map
    catnid = extend_map['category_id'] if 'category_id' in extend_map else None
    if catnid:
      media_video.category, media_video.category_id = catnid[0], catnid[1]
    else:
      self.spider.log('Failed Found catnid, %s, %s' % (url, ref_url), log.ERROR)
      return None
    media_video.play_url = url
    return media_video

  def _convert_to_video_media(self, item):
    if not item:
      return None
    tmp_ext = self.extend_map_handler_.lookup_extend_map(item['url'])
    if not tmp_ext:
      return None

  def _wrap_result(self, media_video):
    if not media_video:
      return None
    media_str = thrift_to_str(media_video, SERIALIZE_TYPE_FAST)
    if not media_str:
      return None
    try:
      #media_str.encode('ISO-8859-1')
      pass
    except Exception, e:
      msg = e.message + traceback.format_exc()
      self.spider_.log(msg, log.ERROR)
      return None
    redict = {}
    import base64
    redict['object'] = base64.b64encode(media_str)
    redict['url'] = media_video.play_url
    redict['type'] = 3
    redict['operation'] = 1
    redict['object_id'] = media_video.id
    #return json.dumps(redict, ensure_ascii = False).encode('utf8')
    return media_str, redict

  def _mq_writer(self, redict):
    try:
      self.channel.basic_publish(exchange = self.exchange, routing_key = '',
          body = json.dumps(redict))
      self.spider.log('Store:[%s] [%s]to rabittmq'% (
        redict.get('object_id', ''),
        redict.get('url', '')), log.INFO)
    except Exception, e:
      msg = 'Failed wroter to rabittmq:' + e.message + traceback.format_exc()
      self.spider_.log(msg, log.ERROR)

  def _mysql_writer(self, redict):
    try:
      conn = self.get_connect_mysql()
      conn.ping(True)
      cursor = conn.cursor()
      idstr = redict.get('object_id', '').replace('crawler_', '')
      if cursor.execute("""select id from %s where id='%s'""" % (self.tbl_n, idstr)) > 0:
        self.spider_.log('realtime skip store, dupe [%s]' % (idstr), log.INFO)
        self.release_connect_mysql()
        return
      cursor.execute("""insert into %s
               (id, base64_thrift) values
               (%%s, %%s)""" % (self._gen_table_name(self.tbl_n, idstr)), (idstr, redict['object']))
      conn.commit()
      self.spider.log('Store:[%s] [%s] to mysql'% (
        redict.get('object_id', ''),
        redict.get('url', '')), log.INFO)
    except Exception, e:
      msg = 'RealtimeVideoWriter Failed wroter to Mysql:' + e.message + traceback.format_exc()
      self.spider_.log(msg, log.ERROR)

  def _extract_pg_category_id(self, item):
    sta, link_ext = self.new_links_extract.extract_custom_links(item['url'],
        item['page'], LinksExtractor.HTML_EXTRA)
    if not sta or 'category_name' not in link_ext.extend_map:
      self.spider_.log('Failed extract item category:%s' % (item['url']), log.ERROR)
      return get_category_name_id('mock')
    # process extend map
    return get_category_name_id(link_ext.extend_map)

  def writer(self, item):
    if not item:
      return False
    # extract html category
    for v in self._batch_fill_items(item):
      media_str, redict =  self._wrap_result(v)
      self._mq_writer(redict)
      self._mysql_writer(redict)
      self.total_send += 1
    
  def finalize(self):
    self.spider_.log('RealtimeVideoWriter has wrote:%s' % self.total_send,
        log.INFO)
    super(PageWriterWithBuff, self).finalize()
    self.close_rabitt()
    self.release_connect_mysql()
