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

# TODO(xiaohe): consider collect dupe logic here with scheduler
# using db is better than local disk and memory

def item_fingerprint(url):
  return hashlib.md5(url).hexdigest()


class ItemDupFilterPipeline(object):
  def __init__(self):
    self.file = None
    self.fingerprints = set()
    self.logdupes = True
    path = get_project_settings()['JOBDIR']

    if path:
      if not os.path.exists(path):
        os.makedirs(path)
      assert os.path.isdir(path), '%s is not dir' % path
      self.file = open(os.path.join(path, 'items.seen'), 'a+')
      self.fingerprints.update(x.rstrip() for x in self.file)
    self.spider = None

  def open_spider(self, spider):
    self.spider = spider

  def __item_seen(self, url, *kargs):
    if not url:
      return True

    fp = item_fingerprint(url + ''.join(kargs))
    if fp in self.fingerprints:
      return True
    self.fingerprints.add(fp)
    if self.file:
      self.file.write(fp + os.linesep)

  def process_item(self, item, spider):
    if not item.get('dont_filter', False) and \
      self.__item_seen(item.get('url', None), '%s' % item.get('item_type', '')):
      raise DropItem('Drop item:%s' % (item.get('url')))
    else:
      return item

  def close_spider(self, spider):
    if self.file:
      self.file.close()
