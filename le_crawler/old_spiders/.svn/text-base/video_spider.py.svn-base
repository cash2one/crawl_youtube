#!/usr/bin/python
# encoding:utf8
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import CrawlSpider, Rule

from ..core.items import CrawlerItem, fill_base_item
from ..base.url_filter import UrlFilter
from ..core.le_sgml import LeSgmlLinkExtract
from ..base.start_url_loads import StartUrlsLoader


class VideoCrawler(CrawlSpider):
  name = 'le_spider'
  allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
  start_url_loader = StartUrlsLoader.get_instance('../start_urls/')
  start_urls = start_url_loader.get_start_urls()
  rules = (
        # follow all links
        Rule(LeSgmlLinkExtract(), callback='parse_page', follow=True),
    )

  def set_crawler(self, crawler):
    print 'call set_crawler'
    CrawlSpider.set_crawler(self, crawler)

  def parse_page(self, response):
      try:
        item = CrawlerItem()
        fill_base_item(response, item)
        return item
      except Exception, e:
        print e
        return None

  def next_request(self):
    print 'call spider next_request'
    pass
    #"""Returns a request to be scheduled or none."""
    #url = self.server.lpop(self.redis_key)
    #if url:
    #    return self.make_requests_from_url(url)

  def schedule_next_request(self):
    """Schedules a request if available"""
    #req = self.next_request()
    #if req:
    #    self.crawler.engine.crawl(req, spider=self)

  def spider_idle(self):
    """Schedules a request if available, otherwise waits."""
    #self.schedule_next_request()
    print 'call spider spider_idle'
    raise DontCloseSpider

  def item_scraped(self, *args, **kwargs):
    """Avoids waiting for the spider to  idle before scheduling the next request"""
    #self.schedule_next_request()
    pass
