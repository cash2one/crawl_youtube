#-*-coding:utf-8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import json
import pika

from thrift.transport  import  TSocket
from thrift.transport  import  TTransport
from thrift.protocol import  TBinaryProtocol

from scrapy import log

from le_crawler.core.page_writer import PageWriterWithBuff
from le_crawler.genpy.video_media.ttypes import MediaVideo
from le_crawler.genpy.hbase import Hbase
from le_crawler.genpy.hbase.ttypes import Mutation
from le_crawler.common.extend_map_handler import ExtendMapHandler
from le_crawler.base.thrift_util import thrift_to_str
from le_crawler.base.thrift_util import SERIALIZE_TYPE_FAST
from le_crawler.core.docid_generator import gen_docid


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
  elif 'tv.cntv.com' in url:
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
    self.extend_map_handler_ = ExtendMapHandler()
    # rabittmq 
    self.ips_ = ['10.150.140.78', '10.150.140.77', '10.150.140.79']
    self.port_ = 5672
    self.exchange = 'hbase.exchange'
    self.queue = 'hbase.search2.realtime.queue'
    self.channel = self._get_channel()
    assert self.channel
    # hbase writer
    self.hbase_host = '10.100.91.36'
    self.hbase_port = 9090
    self.hbase_tbname = 'search_video'
    self.hbase_client = self._get_hbase_client()
    assert self.hbase_client
    # othres 
    self.total_send = 0

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

  def _get_hbase_client(self):
    try:
      self.tsp =  TSocket.TSocket(self.hbase_host, self.hbase_port)
      self.tsp.setTimeout(3000)
      prot = TBinaryProtocol.TBinaryProtocol(self.tsp)
      client = Hbase.Client(prot)
      self.tsp.open()
      self.spider.log('Success connect to hbase!', log.INFO)
      return client
    except Exception, e:
      print "Failed Connection To Hbase",e
      self.spider.log('Faild connect to hbase!', log.ERROR)
      return None

  def close_hbase(self):
    if self.tsp:
      self.tsp.close()

  def close_rabitt(self):
    if self.rabitt_:
      import time
      time.sleep(1)
      self.rabitt_.close()

  def _get_value(self, item, key, default_value = None):
    if not item:
      return default_value
    if item.has_key(key):
      return item[key]

  def _convert_to_video_media(self, item):
    if not item:
      return None
    tmp_ext = self.extend_map_handler_.lookup_extend_map(item['url'])
    if not tmp_ext:
      return None
    media_video = MediaVideo()
    import ctypes
    # cause fingerprint is singed value
    media_video.id = 'crawler_%s' % ctypes.c_uint64(gen_docid(item['url'])).value
    # extend map
    tmp_ext_json = json.loads(tmp_ext)
    if tmp_ext_json.has_key('title'):
      media_video.title = tmp_ext_json['title'].encode('utf8')
    else:
      self.spider.log('Failed Found Title, %s' % item['url'], log.ERROR)
      return None
    if tmp_ext_json.has_key('length'):
      media_video.duration = tmp_ext_json['length']
    else:
      media_video.duration = '--:--'

    if tmp_ext_json.has_key('cover'):
      media_video.poster = tmp_ext_json['cover']
    sourid = get_source_and_id(item['url'])
    if sourid:
      media_video.source, media_video.source_id = sourid[0], sourid[1]
    else:
      return None
    # extend map
    if item.has_key('referer'):
      catid = self.extend_map_handler_.settings.get_category_name(url =
        item['referer'])
    else:
      catid = self.extend_map_handler_.settings.get_category_name(url =
        item['url'])
    if catid:
      catnid = get_category_name_id(catid)
      media_video.category, media_video.category_id = catnid[0], catnid[1]
    else:
      return None
    media_video.play_url = item['url']
    return media_video

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
      import traceback
      print traceback.format_exc()
      print e
      return None
    redict = {}
    import base64
    redict['object'] = base64.b64encode(media_str)
    redict['type'] = 3
    redict['operation'] = 1
    redict['object_id'] = media_video.id
    #return json.dumps(redict, ensure_ascii = False).encode('utf8') 
    return media_str, redict

  def writer(self, item):
    if not item:
      return False
    media_video = self._convert_to_video_media(item)
    if not media_video:
      self.spider.log("Failed convert item to MediaVideo", log.ERROR)
      return False
    #print media_video
    media_str, redict =  self._wrap_result(media_video)
    try:
      self.channel.basic_publish(exchange = self.exchange, routing_key = '',
          body = json.dumps(redict))
      self.total_send += 1
      self.spider.log('Store:[%s] [%s] [%s] to rabittmq'% (self.total_send,
        media_video.id,
        item['url']), log.INFO)
      mutation = Mutation(False, 'v:v', media_str)
      self.hbase_client.mutateRow(self.hbase_tbname, media_video.id, [mutation],
          {})
      self.spider.log('Store:[%s] [%s] [%s] to hbase'% (self.total_send,
        media_video.id,
        item['url']), log.INFO)
      return True
    except Exception, e:
      import traceback
      print traceback.format_exc()
      print e
      self.spider.log('Failed writer realtime doc\n' + str(traceback.format_exc()), log.ERROR)

  def finalize(self):
    super(PageWriterWithBuff, self).finalize()
    self.close_rabitt()
    self.close_hbase()

