#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import time
from scrapy import log

from url_filter import UrlFilter
from page_writer_manager import PageWriterManager


class PageWriterPipeline(object):
  def __init__(self):
    self.spider_ = None
    self.url_filter_ = UrlFilter.get_instance()
    self.pwmgr_ = None
    self.exit_ = False
    self.crawled_items_ = 0
    self.up_log_time_ = 0

  def initialize(self):
    pass

  def finalize(self):
    pass

  def open_spider(self, spider):
    if not spider:
      raise Exception('failed load spider instance')
    self.spider_ = spider
    self.spider_.log("Page writer pipeline is ready", log.INFO)
    self.pwmgr_ = PageWriterManager(queue_max_size=10240, spider=self.spider_)
    self.pwmgr_.start()

  def close_spider(self, spider):
    print 'call pipeline close spider'
    spider.log('Pipeline close called...', log.INFO)
    self.pwmgr_.exit()

  def filter_url(self, item):
    if not self.url_filter_.is_interesting_url(item['crawl_doc'].url):
      self.spider_.log("uninteresting url %s" % item['crawl_doc'].url, log.INFO)
      return True
    return False

  def process_item(self, item, spider):
    if not item or self.filter_url(item):
      return None
    self.pwmgr_.add_item(item)
    self.crawled_items_ += 1
    spider.crawler.stats.inc_value('pipeline/write_pages', spider=spider)

    now = int(time.time())
    if (now - self.up_log_time_) >= 60:
      self.spider_.log('crawled pages num[%d]' % self.crawled_items_)
      self.up_log_time_ = now
    return item

