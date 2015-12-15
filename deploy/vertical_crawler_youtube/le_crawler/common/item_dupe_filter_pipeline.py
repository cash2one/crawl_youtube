#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
for item level dupe, for some case:
  responses extract from one request, can not dupe from
  request
"""
import md5
import os

from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
#TODO(xiaohe): consider collect dupe logic here with scheduler
# using db is better than localdisk and memory
class ItemDupFilterPipeline(object):
  def __init__(self):
    self.file = None
    self.fingerprints = set()
    self.logdupes = True
    path = get_project_settings()['JOBDIR']
    if path:
        self.file = open(os.path.join(path, 'items.seen'), 'a+')
        self.fingerprints.update(x.rstrip() for x in self.file)
    self.spider = None
 
  def open_spider(self, spider):
    self.spider = spider

  def __item_seen(self, url, *kargs):
    if not url:
      return True

    fp = self.__item_fingerprint(url + ''.join(kargs))
    if fp in self.fingerprints:
      return True
    self.fingerprints.add(fp)
    if self.file:
        self.file.write(fp + os.linesep)

  def __item_fingerprint(self, url):
    return md5.new(url).hexdigest()

  def process_item(self, item, spider):
    if not item.get('dont_filter', False) \
        and self.__item_seen(item.get('url', None), '%s' % item.get('item_type', '')):
      raise DropItem('Drop item:%s' %(item.get('url')))
    else:
      return item

  def close_spider(self, reason):
    if self.file:
          self.file.close()
