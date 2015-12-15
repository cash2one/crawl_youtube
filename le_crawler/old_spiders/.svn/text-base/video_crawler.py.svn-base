#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for test module.

A detailed description of test.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.spiders import CrawlSpider, Rule

#from le_crawler.common.items import CrawlerLoader
from ..base.url_filter import UrlFilter
from ..core.le_sgml import LeSgmlLinkExtract
from ..core.items import CrawlerItem, fill_base_item
from le_spiders import RedisMixin


class VideoCrawler(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'video_crawler'
    redis_key = 'video_crawler:start_urls'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    print allowed_domains
    start_urls = []

    rules = (
        # follow all links
        Rule(LeSgmlLinkExtract(), callback='parse_page', follow=True),
    )

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse_page(self, response):
      try:
        item = CrawlerItem()
        fill_base_item(response, item)
        return item
      except Exception, e:
        print e
        return None
