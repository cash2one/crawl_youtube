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


from le_crawler.le_spiders import RedisMixin

from scrapy.contrib.spiders import CrawlSpider, Rule

from le_crawler.common.items import CrawlerLoader
from le_crawler.common.url_filter import UrlFilter
from le_crawler.core.le_sgml import LeSgmlLinkExtract


class VideoCrawler(RedisMixin, CrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'video_crawler'
    redis_key = 'video_crawler:start_urls'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    #print allowed_domains
    start_urls = []

    rules = (
        # follow all links
        Rule(LeSgmlLinkExtract(), callback='parse_page', follow=True),
    )

    def set_crawler(self, crawler):
        CrawlSpider.set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse_page(self, response):
        el = CrawlerLoader(response=response)
        el.add_value('url', response.url)
        el.add_value('page', response.body)
        el.add_value('http_header', response.headers.to_string())
        el.add_value('page_encoding', response.encoding)
        return el.load_item()
