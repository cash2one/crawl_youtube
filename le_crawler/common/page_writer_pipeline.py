#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import time
from page_writer_manager import PageWriterManager

class PageWriterPipeline(object):
  def __init__(self):
    self.spider_ = None
    self.pwmgr_ = None
    self.exit_ = False
    self.crawled_items_ = 0
    self.up_log_time_ = 0

  def initialize(self):
    pass

  def finalize(self):
    pass

  def open_spider(self, spider):
    self.spider_ = spider
    self.logger_ = spider.logger_
    self.pwmgr_ = PageWriterManager(queue_max_size=10240, spider=self.spider_)
    self.pwmgr_.start()
    self.logger_.info("page writer pipeline started")

  def close_spider(self, spider):
    self.logger_.info('page writer pipeline closing')
    self.pwmgr_.exit()

  def process_item(self, item, spider):
    if not item:
      return None
    self.pwmgr_.add_item(item)
    self.crawled_items_ += 1
    spider.crawler.stats.inc_value('pipeline/write_pages', spider=spider)
    now = int(time.time())
    if (now - self.up_log_time_) >= 60:
      self.spider_.log('crawled page amount [%d]', self.crawled_items_)
      self.up_log_time_ = now
    return item

