#!/usr/bin/python
#coding=utf-8
# Copyright 2015 LeTV Inc. All Rights Reserved.

__author__ = 'zhaojincheng@letv.com'

import time
import traceback
import logging

from scrapy.http import Request
from scrapy.spiders import Spider

#from scrapy.exceptions import IgnoreRequest
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from ..base.url_filter import UrlFilter
from ..base.start_url_loads import StartUrlsLoader
from ..base.logutil import Log
from ..common.extend_map_handler import ExtendMapHandler
from ..core.items import CrawlerItem, fill_base_item
from ..proto.crawl.ttypes import CrawlDoc, CrawlDocType, PageType, Location, Anchor




class LejianCrawler(Spider):
    name = 'lejian_home'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/', random_sort = True)
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(LejianCrawler, self).__init__(*a, **kw)
      self._logger = Log('', log_path='../log/spider.log', log_level=logging.INFO).log
      self.extend_map_h_ = ExtendMapHandler.get_instance(LejianCrawler.start_url_loader,
                                                         module_path='le_crawler.common.lejian_home_settings', loger=self._logger)
      self.finished_count = 0
      self.start_size = len(LejianCrawler.start_urls)
      self.callback_map_ = {PageType.HOME:        self.parse_home,
                            PageType.CHANNEL:     self.parse_channel,
                            PageType.LIST:        self.parse_list,
                            PageType.PLAY:        self.parse_page}



    def _create_request(self, url, page_type, doc_type, meta=None, headers=None, dont_filter=True):
      crawl_doc = CrawlDoc()
      crawl_doc.url = url
      crawl_doc.discover_time = int(time.time())
      crawl_doc.page_type = page_type
      crawl_doc.doc_type = CrawlDocType.HOME

      meta = meta or {}
      headers = headers or {}
      referer = headers.get('Referer')
      if referer:
        inlink_anchor = Anchor()
        inlink_anchor.url = referer
        inlink_anchor.doc_type = CrawlDocType.HOME
        inlink_anchor.location = Location()
        inlink_anchor.location.position = meta.get('position', 0)
        inlink_anchor.location.page_index = meta.get('page_index', 0)
        crawl_doc.in_links = [inlink_anchor]

      meta['crawl_doc'] = crawl_doc

      return Request(url,
                     callback=self.callback_map_[page_type],
                     meta=meta,
                     dont_filter=dont_filter)


    def start_requests(self):
      for url in LejianCrawler.start_urls:
        type = self.start_url_loader.get_property(url, 'type', 'list')
        if type == 'home':
          yield self._create_request(url, PageType.HOME, CrawlDocType.HOME)
        elif type == 'channel':
          yield self._create_request(url, PageType.CHANNEL, CrawlDocType.HOME)
        elif type == 'list':
          yield self._create_request(url, PageType.LIST, CrawlDocType.HOME)


    def parse_home(self, response):
      try:
        url = response.url.strip()
        self._logger.info('parse_home url: %s' % url)
        page = response.body.decode(response.encoding)
        sta, channel_links_map = self.extend_map_h_.extract_channel_links_map(body = page, pageurl = url)
        if not sta:
          #TODO log
          print 'parse_home failed sta:%s, url:%s' % (sta, url)
          return
        for link, link_map in channel_links_map.items():
          yield self._create_request(link, PageType.CHANNEL, CrawlDocType.HOME)
      except:
        msg = traceback.format_exc()
        print msg
        self._logger.error('Failed parse_home: %s, url: %s' % (msg, url))
        return


    def parse_channel(self, response):
      try:
        url = response.url.strip()
        self._logger.info('parse_channel url: %s' % url)
        page = response.body.decode(response.encoding)
        # use block_url_list for dupefilter key
        # status, extend_url = self.extend_map_h_.extract_extend_map(body = page, pageurl = url, ignore_empty_property=True)

        sub_category_num = response.meta.get('sub_category_num', 0)
        sta, has_sub_category, links_list = self.extend_map_h_.extract_sub_links_list(body = page, pageurl = url,sub_category_num=sub_category_num)
        if not sta:
          #print 'parse_channel url failed, url: [%s]' % url
          yield self._create_request(url, PageType.LIST, CrawlDocType.HOME)
          #return
        else:
          if not links_list:
            yield self._create_request(url, PageType.LIST, CrawlDocType.HOME)
            links_list = []
          sub_category_num += 1
          for link in links_list:
            if has_sub_category:
              yield self._create_request(link,
                                         PageType.CHANNEL,
                                         CrawlDocType.HOME,
                                         meta={'sub_category_num':sub_category_num})
            else:
              yield self._create_request(link, PageType.LIST, CrawlDocType.HOME)
      except:
        msg = traceback.format_exc()
        print msg
        self._logger.error('Failed parse_channel: %s, url: %s' % (msg, url))
        return



    def parse_list(self, response):
      try:
        url = response.url.strip()
        self._logger.info('parse_list url: %s' % url)
        page = response.body.decode(response.encoding, 'ignore')
        page_index = response.meta.get('page_index', 1)

        # use block_url_list for dupefilter key
        status, extend_url = self.extend_map_h_.extract_urls(body = page, pageurl = url)
        if not status:
          self.log('parse list failed,  listurl:%s' %  url)
          return
        #print 'len extend_url: ', len(extend_url)
        crawl_item = CrawlerItem()
        for position, link in enumerate(extend_url):
          yield self._create_request(link,
                                     PageType.PLAY,
                                     CrawlDocType.HOME,
                                     meta={'doc_type': CrawlDocType.HOME,
                                           'page_index': page_index,
                                           'position': position +1},
                                     headers={'Referer': url},
                                     dont_filter=False)
        fill_base_item(response, crawl_item)
        yield crawl_item
      except:
        msg = traceback.format_exc()
        print msg
        self._logger.error('Failed parse list: %s, url:%s' % (msg, url))
        return


    def parse_page(self, response):
      url = response.url.strip()
      self._logger.info('parse_page url: %s referer--> %s' % (url, response.meta['crawl_doc'].in_links[0].url if response.meta['crawl_doc'].in_links else None))
      page = response.body.decode(response.encoding)
      crawl_item = CrawlerItem()
      fill_base_item(response, crawl_item)
      if not self.extend_map_h_.filter_by_page(body = page, pageurl = url):
        yield crawl_item

