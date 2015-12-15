#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for content desktop spider
"""
import traceback
import re
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy import log

from le_crawler.core.items import CrawlerItem
from le_crawler.core.items import fill_base_item
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.core.links_extractor import LinksExtractor

class HotWordsCrawler(Spider):
    name = 'hotwords_crawler'
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/')
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(HotWordsCrawler, self).__init__(*a, **kw)
      self.finished_count = 0
      self.start_size = len(HotWordsCrawler.start_urls)
      self.collect_nums = 0
      self.new_links_extract = \
      LinksExtractor('le_crawler.common.hotwords_settings',
          start_url_loader = HotWordsCrawler.start_url_loader)
      self.share_cache = {}
      self.item_reg = re.compile(r'top\.baidu\.com\/buzz')
      self.detail_reg = re.compile(r'top\.baidu\.com\/detail')

    def parse(self, response):
      try:
        url = response.url.strip()
        page = response.body.decode(response.encoding)
        self.finished_count += 1
        # first jugy json parser
        size = 0
        status = True
        refer_url = response.request.headers.get('Referer', None)
        status, links_map = self.new_links_extract.extract_block_links(url,
              body = page, bd_type = LinksExtractor.HTML_EXTRA)
        if status:
          size = len(links_map)
          print 'Ok:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
        else:
          print 'Failed:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
          return
        item_yield = self.accept_item(url)
        if item_yield:
          item = CrawlerItem()
          sta, links = self.new_links_extract.extract_custom_links(url, page,
                LinksExtractor.HTML_EXTRA)
          if sta:
            item.update(links.extend_map)
          else:
            self.log('Failed extract custome property:%s' % (url), log.ERROR)
        hotwords = []
        for i in links_map:
          if not self.ignore_crawl(i.url):
            yield Request(i.url, headers={'Referer': '%s' % (refer_url or url)},
              callback = self.parse, dont_filter = True)
          if item_yield and i.extend_map and 'title' in i.extend_map:
            hotwords.append(i.extend_map.get('title'))
          #return self.parse_page(response)
        if item_yield and hotwords:
          item['extend_map'] = hotwords
          item['url'] = url
          yield item
      except Exception, e:
        print 'spider try catch error:', e
        print traceback.format_exc()
        return

    def accept_item(self, url):
      return bool(self.item_reg.search(url))

    def ignore_crawl(self, url):
      return bool(self.detail_reg.search(url))

