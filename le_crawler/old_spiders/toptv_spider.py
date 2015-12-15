#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""One-line documentation for test module.
A detailed description of test.
"""
import sys

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
import traceback
import json

from le_crawler.base.url_filter import UrlFilter
from le_crawler.core.items import CrawlerItem
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.core.extra_extend_map_engine import ExtraExtendMapEngine

class TopListSpider(Spider):
  name = 'toptv_spider'
  allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
  start_url_loader = StartUrlsLoader.get_instance('../start_urls/',
  random_sort = True)
  start_urls = start_url_loader.get_start_urls()

  def __init__(self, *a, **kw):
    super(TopListSpider, self).__init__(*a, **kw)
    self.extend_map_h_ = ExtraExtendMapEngine(TopListSpider.start_url_loader,
        'le_crawler.common.tvtoplist_settings')
    self.finished_count = 0
    self.start_size = len(TopListSpider.start_urls)
    self.url_filter = UrlFilter.get_instance()

  def __get_source_type(self, url):
    if 'cntv.cn' in url:
      return 'cntv'
    elif 'fun.tv' in url:
      return 'funshion'
    elif 'hunantv.com' in url:
      return 'imgo'
    elif 'iqiyi.com' in url:
      return 'iqiyi'
    elif 'm1905.com' in url:
      return 'm1905'
    elif 'pptv.com' in url:
      return 'pptv'
    elif 'qq.com' in url:
      return 'qq'
    elif 'sohu.com' in url:
      return 'sohu'
    elif 'tudou.com' in url:
      return 'tudou'
    elif 'youku.com' in url:
      return 'youku'
    elif 'zjstv.com' in url:
      return 'zjstv'


  def parse(self, response):
    self.finished_count += 1
    body = response.body.decode(response.encoding)
    url = response.url
    refer_url = response.request.headers.get('Referer', url)
    status, extend_urls, extend_map_l = \
        self.extend_map_h_.extract_extend_map(body, pageurl = url)
    if status:
      print 'OK(%d/%d, %d) %s' % (self.finished_count,
          self.start_size,
          len(extend_urls), url)
      i = 0
      for (u, d) in extend_map_l:
        i += 1
        item = CrawlerItem()
        item['url'] = u
        item['title'] = d.get('title', '')
        item['source_type'] = self.__get_source_type(refer_url)
        item['comment_num'] = d.get('number', i)
        item['item_type'] = self.extend_map_h_.get_category_name(refer_url or url)
        if item['item_type'] is None:
          print item['item_type'], refer_url, url
        yield item
    else:
      print 'Failed(%d/%d, %d) %s' % (self.finished_count,
          self.start_size,
          0, url)

  def closed(self, reason):
    pass

