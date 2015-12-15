#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
"""
this pipeline using simple item, remove not used item

"""
from scrapy.utils.project import get_project_settings

class ItemExpressPipeline(object):
  def __init__(self):
    self.spider = None
    self.express_key = get_project_settings().getlist('ITEM_EXPRESS_KEYS', [])
  def open_spider(self, spider):
    self.spider = spider

  def __load_express_words(self):
    pass

  def close_spider(self, spider):
    pass
  def process_item(self, item, spider):
    for k in self.express_key:
      item.pop(k, None)
    return item



