# -*-coding:utf-8-*-
# !/usr/bin/python
#
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import time

from scrapy import log

from ..genpy.video_media.ttypes import MediaVideo
from ..core.docid_generator import gen_docid
import realtime_video_writer as realtime_writer


"""
for video search realtime video search
"""

class WebSearchDBWriter(realtime_writer.RealtimeVideoWriter):
  def _convert_to_video_media(self, item):
    if not item:
      return None
    media_video = MediaVideo()
    import ctypes
    # cause fingerprint is singed value
    media_video.id = 'crawler_%s' % ctypes.c_uint64(gen_docid(item['url'])).value
    # extend map
    if 'title' in item:
      media_video.title = item['title'].encode('utf8')
    else:
      self.spider.log('title not found, %s' % item['url'], log.ERROR)
      return None
    if 'duration' in item:
      media_video.duration = item['duration']
    else:
      media_video.duration = '00:00'
      self.spider_.log('duration not found, %s' % item['url'], log.ERROR)
    if 'play_count' in item:
      media_video.play_total = item['play_count']
    if 'cover' in item:
      media_video.poster = item['cover']
    if 'article_time' in item:
      media_video.showtime = time.strftime('%Y-%m-%d %H:%M:%S',
                                           time.localtime(item['article_time']))
    sourid = realtime_writer.get_source_and_id(item['url'])
    if sourid:
      media_video.source, media_video.source_id = sourid[0], sourid[1]
    else:
      return None
    # extend map
    if 'item_type' in item:
      catnid = realtime_writer.get_category_name_id(item['item_type'])
      media_video.category, media_video.category_id = catnid[0], catnid[1]
    else:
      return None
    media_video.play_url = item['url']
    media_video.create_time = item['down_time']
    return media_video


  def writer(self, item):
    if not item:
      return False
    media_video = self._convert_to_video_media(item)
    if not media_video:
      self.spider.log("Failed convert item to MediaVideo", log.ERROR)
      return False
    media_str, redict = self._wrap_result(media_video)
    self._mq_writer(redict)
    self._mysql_writer(redict)
    self.total_send += 1
