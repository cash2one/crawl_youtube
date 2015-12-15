#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy import log
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.settings import Settings

from url_filter import UrlFilter
from page_local_writer import PageDataWriter

class CrawlerPipeline(object):
  def __init__(self):
    self.spider_ = None
    self.url_filter_ = UrlFilter()
    dispatcher.connect(self.initialize, signals.engine_started)
    dispatcher.connect(self.finalize, signals.engine_stopped)
    self.data_dir = Settings().get('DATA_DIR', '/letv/crawler_delta/')
    self.crawled_items_ = 0
    self.up_log_time_ = 0

  def initialize(self):
    pass

  def finalize(self):
    pass

  def open_spider(self, spider):
    if not spider:
      raise Exception('faild load spider instance')
    self.spider_ = spider
    self.spider_.log("Crawler pipeline is ready", log.INFO)
    self.file_writer_ = PageDataWriter(self.spider_, 1800, 4000, self.data_dir)

  def close_spider(self, spider):
    print 'call pipeline close spider'
    spider.log('Pipeline close called...', log.INFO)
    self.file_writer_.finalize()

  def process_item(self, item, spider):
    if not item:
      return None
    self.file_writer_.add_item(item)
    self.crawled_items_ += 1
    spider.crawler.stats.inc_value('pipeline/write_pages', spider = spider)
    import time
    nowt = time.time()
    if nowt - self.up_log_time_ >= 60:
      self.spider_.log('crawled pages num[%d]' % self.crawled_items_)
      self.up_log_time_ = nowt
    return item

