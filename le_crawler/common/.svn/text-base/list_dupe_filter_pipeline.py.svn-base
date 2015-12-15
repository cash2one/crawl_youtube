#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
for item level dupe, for some case:
  responses extract from one request, can not dupe from
  request
"""
import os
import hashlib

from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from le_crawler.core import connection_redis


def item_fingerprint(page):
  return hashlib.md5(page).hexdigest()


class ListDupFilterPipeline(object):
  def __init__(self):
    self._init_redis()
    self.spider = None

  def _init_redis(self):
    settings = get_project_settings()
    self.server = connection_redis.from_settings(settings)
    self.key = settings.get('LIST_DUPEFILTER_KEY', 'list_dupefilter_key')

  def open_spider(self, spider):
    self.spider = spider

  def __item_seen(self, url, block_urls=''):
    if not url:
      return True
    fp = item_fingerprint(url + '\t' + block_urls)
    added = self.server.sadd(self.key, fp)
    #print 'key============================,', self.key
    #print 'value============================,', fp
    #print 'added=========================%s' % added
    return not added

  def process_item(self, item, spider):
    #print 'process_item list url ====================', item.get('url', None)
    block_urls = ''
    block_url_list = []
    extend_map = item.get('extend_map', None)
    if extend_map:
      block_url_list = extend_map.get('block_url_list', '')
    if block_url_list:
      block_urls = ';'.join(block_url_list)
    if not item.get('dont_filter', False) and self.__item_seen(item.get('url', None), block_urls):
      #raise DropItem('Drop item:%s' % (item.get('url')))
      spider.log('Drop item:%s' % item.get('url'))
      return None
    else:
      return item

  def close_spider(self, spider):
    self.server.delete(self.key)
