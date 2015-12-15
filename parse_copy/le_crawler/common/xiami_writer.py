#!/usr/bin/python
# encoding=utf8
# Copyright 2014 LeTV Inc. All Rights Reserved.

__author__ = 'guoxiaohe@letv.com'

import traceback
from pymongo import MongoClient
from scrapy import log

from html_utils import remove_tags
from ..core.page_writer import PageWriterWithBuff


class XiaMiWriter(PageWriterWithBuff):
  def __init__(self, spider):
    super(XiaMiWriter, self).__init__(spider)
    self.set_name('XiaMiWriter')
    # self.update_db = MongoClient('mongodb://admin:76f4473ed098b43@10.150.130.30:9031').lemusic
    # self.update_db = MongoClient(host='10.140.60.82', port=27017).lemusic
    self.client = MongoClient('10.180.92.202:27017,10.180.92.203:27017,10.180.92.215:27017').lemusic
    self.song_tbl_w = self.client.songs_extend
    self.album_tbl_w = self.client.albums_extend
    self.total_send_count = 0
    self.failed_send_count = 0
    self.retry_time_max = 10
    self.remove_tags = ['div', 'tr', 'td', 'a', 'tbody', 'table']

  def _prepare_data(self, item):
    try:
      if 'extend_map' in item:
        redict = {}
        if 'album_info' in item['extend_map']:
          alist = remove_tags(self.remove_tags, item['extend_map']['album_info'],
                              '</tr>')
          alist = [x.replace('\t', '').replace('\r\n', '').replace('\n', '') for x
                   in alist if u'专辑风格' in x]
          if alist:
            kv = alist[0].split(u'：')
            if len(kv) >= 2:
              redict['album_style'] = ''.join(kv[1:])
              redict['album_id'] = item['cate_id']
              redict['type'] = 'album'
        elif 'song_info' in item['extend_map']:
          alist = remove_tags(self.remove_tags, item['extend_map']['song_info'],
                              '</tr>')
          alist = [x.replace('\t', '').replace('\r\n', '').replace(' ', '')
                   for x in alist if x]
          for i in alist:
            kv = i.split(u'：')
            if len(kv) >= 2:
              if u'作词' in kv[0]:
                redict['lyricist'] = ''.join(kv[1:])
              elif u'作曲' in kv[0]:
                redict['composer'] = ''.join(kv[1:])
              elif u'编曲' in kv[0]:
                redict['arranger'] = ''.join(kv[1:])
          if redict:
            redict['song_id'] = item['cate_id']
            redict['type'] = 'song'
        return redict
    except Exception, e:
      self.spider.log('Failed send data:%s, %s, %s' % (item, traceback.format_exc(), e.message), log.ERROR)
      return None

  def status(self):
    return 'suc:%s, fai: %s, %s' % (self.total_send_count,
                                    self.failed_send_count,
                                    super(XiaMiWriter, self).status())

  def _send_data(self, res, tlb_type):
    try:
      if res:
        if tlb_type == 'song':
          self.spider.log('song: %s' % res, log.ERROR)
          self.song_tbl_w.save(res)
        elif tlb_type == 'album':
          self.spider.log('album: %s' % res, log.ERROR)
          self.album_tbl_w.save(res)
      return True
    except Exception, e:
      self.spider.log('Failed send data:%s, %s, %s' %
                      (res, traceback.format_exc(), e.message), log.ERROR)
      return False

  def writer(self, item):
    try_time = 0
    # will retry 10 times, if not drop
    res = self._prepare_data(item)
    if res:
      tbl_type = res.pop('type')
      while try_time < self.retry_time_max:
        if not self._send_data(res, tbl_type):
          try_time += 1
          continue
        break
      self.total_send_count += 1
    else:
      self.failed_send_count += 1
      self.spider.log('Failed convert item data:%s' % item, log.ERROR)
