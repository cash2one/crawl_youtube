#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
"""
this pipeline using for fetch content from html
"""
from le_crawler.base.extract_content import ContentExtractor

class ContentExtractorPipeline(object):
  def __init__(self):
    self.spider_ = None
    self.content_extractor = ContentExtractor()

  def initialize(self):
    pass

  def finalize(self):
    pass

  def open_spider(self, spider):
    self.spider_ = spider

  def close_spider(self, spider):
    pass

  def process_item(self, item, spider):
    if item.has_key('page'):
      res = \
            self.content_extractor.extract_with_paragraph(item['page'],
                encode_type = 'utf8')
      if res[-1]:
        item['content_body'] = res[-1]
      if res[0]:
        item['content_imgs'] = res[0]
      if res[1]:
        item['content_links'] = res[1]
      if not item.has_key('title') and res[2]:
        item['title'] = res[2]
    return item
