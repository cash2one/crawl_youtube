#!/usr/bin/python
#-*-coding:utf8-*-
#
# Copyright 2015 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
"""
this pipeline using for fetch content from html
"""
from scrapy.exceptions import DropItem

from le_crawler.common.cdesktop_writer import CDesktopWriter

class CDHotwordsWriter(CDesktopWriter):
  def __init__(self, spider):
    super(CDHotwordsWriter, self).__init__(spider)
    self.set_name('CDesktopHotwordsWriter')
    self.data_reciver_ip = '10.180.92.206'

  def initialize(self):
    pass

  def finalize(self):
    pass

  def open_spider(self, spider):
    self.spider_ = spider

  def close_spider(self, spider):
    pass

  def cd_item_normalize(self, item):
    if 'item_type' in item:
      item['item_type'] = item['item_type'].replace(u'榜单首页', '')
    if 'cate_id' in item:
      item['cate_id'] = item['cate_id'].replace(u'搜索排行榜', '')
    if 'cate_id' in item:
      item['cate_id'] = item['cate_id'].replace(u'排行榜', '')
    if 'cate_id' in item:
      item['cate_id'] = item['cate_id'].replace(u'今日', '')
    if 'cate_id' in item:
      item['cate_id'] = item['cate_id'].replace(u'七日', '')

  def process_item(self, item, spider):
    self.cd_item_normalize(item)
    if 'item_type' in item and item.get('item_type') not in (u'热搜', u'人物',
        u'热点', u'娱乐'):
      raise DropItem('%s' % (item['url']))
    return item
