#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for content desktop spider
"""

import os
import re
import datetime
import traceback
from scrapy.spider import Spider
from scrapy import log
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient

from ..core.items import CrawlerItem
from ..core.items import fill_base_item
from ..base.start_url_loads import StartUrlsLoader
from ..core.links_extractor import LinksExtractor


class XiamiSpider(Spider):
  name = 'xiami_spider'

  def __init__(self, *kargs, **kwargs):
    super(XiamiSpider, self).__init__(*kargs, **kwargs)
    self._finished_count = 0
    self._start_size = len(XiamiSpider.start_urls)
    setting_path = get_project_settings().get('EXTRACT_SETTING_PATH', '')
    if not setting_path:
      self.log('Failed found links extract setting_path moudle', log.ERROR)
    self._new_links_extract = LinksExtractor(setting_path)
    self._share_cache = {}
    self._need_links_extra = get_project_settings().get('NEED_LINKS_EXTR', True)
    self._need_custom_extra = get_project_settings().get('NEED_CUSTOM_EXTR', True)
    self._machine_amount = get_project_settings()['MACHINE_AMOUNT']
    self._machine_num = get_project_settings()['MACHINE_NUM']
    self._jobdir = get_project_settings().get('JOBDIR', '../data/')
    self._song_id_file = os.path.join(self._jobdir, 'song_id.data')
    self._album_id_file = os.path.join(self._jobdir, 'album_id.data')
    self._timestamp_file = os.path.join(self._jobdir, 'timestamp.data')
    print 'machine_amount: %s, machine_num: %s' % (self._machine_amount, self._machine_num)
    self._mogo_read_client = MongoClient('10.180.92.202:27017,10.180.92.203:27017,10.180.92.215:27017')
    self._song_table = self._mogo_read_client.lemusic.songs
    self._album_table = self._mogo_read_client.lemusic.albums
    self.log('Begin prepare xiami ids', log.INFO)
    if get_project_settings().get('DEBUG_MODEL', False):
      XiamiSpider.start_urls = ['http://www.xiami.com/song/2068460',
                                'http://www.xiami.com/album/4574']
    else:
      XiamiSpider.start_urls = self._load_local() or self._reload()
    self.log('Finished load start song/album ids:%s' % (len(XiamiSpider.start_urls)), log.INFO)
    self._id_re = re.compile(r'\d+')

  def _load_local(self):
    print 'start to load start urls from local disk'
    timestamp = datetime.datetime.now()
    if not os.path.isfile(self._song_id_file) or not os.path.isfile(self._album_id_file) \
      or not os.path.isfile(self._timestamp_file):
      return None
    local_stamp = open(self._timestamp_file).readline().strip()
    if not local_stamp:
      return None
    update_time = datetime.datetime.strptime(local_stamp, '%Y-%m-%d')
    if datetime.datetime.now() - update_time > datetime.timedelta(1):  # 1 day
      return None
    urls = ['http://www.xiami.com/song/%s' % song_id.strip() for song_id in open(self._song_id_file) if song_id]
    urls.extend(['http://www.xiami.com/album/%s' % album_id.strip()
                 for album_id in open(self._album_id_file) if album_id])
    print 'load start urls completed, time spent: %s' % (datetime.datetime.now() - timestamp)
    return urls

  def _reload(self):
    print 'start to reload start urls'
    timestamp = datetime.datetime.now()
    if not os.path.exists(self._jobdir):
      os.makedirs(self._jobdir)
    songid_list = [int(song.get('song_id', 0)) for song in self._song_table.find()]
    songid_list = [song_id for song_id in songid_list
                   if song_id and song_id % self._machine_amount == self._machine_num]
    albumid_list = [int(album.get('album_id', 0)) for album in self._album_table.find()]
    albumid_list = [album_id for album_id in albumid_list
                    if album_id and album_id % self._machine_amount == self._machine_num]
    with open(self._song_id_file, 'w') as f:
      map(lambda x: f.write('%s\n' % x), songid_list)
    with open(self._album_id_file, 'w') as f:
      map(lambda x: f.write('%s\n' % x), albumid_list)
    urls = ['http://www.xiami.com/song/%s' % xid for xid in songid_list]
    urls.extend(['http://www.xiami.com/album/%s' % xid for xid in albumid_list])
    with open(self._timestamp_file, 'w') as f:
      f.write(datetime.datetime.now().strftime('%Y-%m-%d'))
    print 'reload start urls completed, time spent: %s' % (datetime.datetime.now() - timestamp)
    return urls

  def parse(self, response):
    try:
      item = CrawlerItem()
      fill_base_item(response, item)
      sta, links = self._new_links_extract.extract_custom_links(
        item['url'], item['page'], LinksExtractor.HTML_EXTRA)
      if sta:
        item['extend_map'] = links.extend_map
        item['cate_id'] = self._parse_id_from_url(item['url'])
        yield item
      else:
        self.log('Failed custom extra:%s' % (item['url']), log.ERROR)
    except Exception, e:
      err_msg = traceback.format_exc() + e.message
      print err_msg
      self.log(err_msg, log.ERROR)

  def _parse_id_from_url(self, url):
    se = self._id_re.search(url)
    if se:
      return se.group()
    return None
