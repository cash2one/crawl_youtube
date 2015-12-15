#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

from scrapy.exceptions import DropItem
from scrapy import log
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.settings import Settings


from le_crawler.base.url_filter import UrlFilter
from le_crawler.core.page_writer import PageWriterManager 

class PageWriterPipeLine(object):
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
      raise Exception('faild load spider instance')
    self.spider_ = spider
    self.spider_.log("Page writer pipeline is ready", log.INFO)
    self.pwmgr_ = PageWriterManager(queue_max_size = 10240, spider = self.spider_)
    self.pwmgr_.start()

  def close_spider(self, spider):
    print 'call pipeline close spider'
    spider.log('Pipeline close called...', log.INFO)
    self.pwmgr_.exit()

  def process_item(self, item, spider):
    if not item:
      return None
    if not self.url_filter_.is_interesting_url(item['url']):
      msg = "unintresting url %s" % item['url']
      self.spider_.log(msg, log.INFO)
      return None
      #raise DropItem(msg)
    self.pwmgr_.add_item(item)
    self.crawled_items_ += 1
    spider.crawler.stats.inc_value('pipeline/write_pages', spider = spider)
    import time
    nowt = int(time.time())
    if (nowt - self.up_log_time_) >= 60:
      self.spider_.log('crawled pages num[%d]' % self.crawled_items_)
      self.up_log_time_ = nowt
    return item

