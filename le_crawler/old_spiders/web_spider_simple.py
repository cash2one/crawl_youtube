#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright 2015 LeTV Inc. All Rights Reserved.

__author__ = 'guoxiaohe@letv.com'

import time
import traceback

from scrapy.spider import Spider

from ..core.items import CrawlerItem
from ..base.start_url_loads import StartUrlsLoader
from ..core.links_extractor import LinksExtractor
from ..base.number_convert import get_number
from ..base.time_parser import TimeParser


class WebSpiderSimple(Spider):
  name = 'web_simple_spider'
  start_url_loader = StartUrlsLoader.get_instance('../start_urls/')
  start_urls = start_url_loader.get_start_urls()

  def __init__(self, *kargs, **kwargs):
    self.collect_nums = 0
    self.finished_count = 0
    self.time_parser_ = TimestrParser()
    self.start_size = len(WebSpiderSimple.start_urls)
    super(WebSpiderSimple, self).__init__(*kargs, **kwargs)
    self.new_links_extract = LinksExtractor('le_crawler.common.headline_video_settings',
                                            start_url_loader=WebSpiderSimple.start_url_loader)

  def parse(self, response):
    try:
      url = response.url.strip()
      page = response.body.decode(response.encoding)
      self.finished_count += 1
      # first jugy json parser
      size = 0
      refer_url = response.request.headers.get('Referer', None)
      status, links_map = self.new_links_extract.extract_block_links(url, body=page, bd_type=LinksExtractor.HTML_EXTRA)
      if status:
        size = len(links_map)
        print 'OK: (%5d/%d) Finished Extend: %s, %d' % (self.finished_count, self.start_size, url, size)
        for i in links_map:
          item = CrawlerItem()
          item['url'] = i.url
          item['item_type'] = WebSpiderSimple.start_url_loader.get_property(refer_url, 'category', None) or 'news'
          self._post_item_process(i.extend_map)
          item.update(i.extend_map)
          item['down_time'] = int(time.time())
          yield item
      else:
        print 'Failed: (%5d/%d) Finished Extend: %s, %d' % (self.finished_count, self.start_size, url, size)
        return
        # return self.parse_page(response)
    except Exception, e:
      print 'spider try catch error:', e
      print traceback.format_exc()
      return

  def _post_item_process(self, item):
    if not item:
      return
    item.pop('sid', None)
    if 'download_count' in item:
      counter = item.pop('download_count', 0)
      counter = get_number(counter)
      if counter:
        item['play_count'] = counter
    if 'length' in item:
      counter = item.pop('length', '')
      item['duration'] = counter
    item['article_time'] = int(time.time())
    if 'article_time_raw' in item:
      ts = self.time_parser_.timestamp(item['article_time_raw'])
      if ts > 0:
        item['article_time'] = ts
