#!/usr/bin/python
#coding=utf-8
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'zhaojincheng@letv.com'

"""One-line documentation for test module.
A detailed description of test.
"""
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
import traceback
import time
#from scrapy.exceptions import IgnoreRequest
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from ..core.rank_item import RankItem
from ..common.url_filter import UrlFilter
from ..common.extend_map_handler import ExtendMapHandler
from ..common.start_url_loads import StartUrlsLoader




#global var
class BaiduHotCrawler(Spider):
    name = 'baiduhot'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/', random_sort = True)
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(BaiduHotCrawler, self).__init__(*a, **kw)
      self.extend_map_h_ = ExtendMapHandler.get_instance(BaiduHotCrawler.start_url_loader,
          module_path='le_crawler.common.baidu_hot_settings')
      self.finished_count = 0
      self.start_size = len(BaiduHotCrawler.start_urls)

    def start_requests(self):
      items = []
      for url in BaiduHotCrawler.start_urls:
        type = self.start_url_loader.get_property(url, 'type', 'list')
        extend_map = self.start_url_loader.get_property(url, 'extend_map', {})
        if type == 'home':
          items.append(Request(url, meta = {'extend_map' : extend_map}, callback = self.parse_home, dont_filter = True))
        elif type == 'channel':
          items.append(Request(url, meta = {'need_asyc_load':True, 'extend_map' : extend_map}, callback = self.parse_channel, dont_filter = True))
        elif type == 'list':
          items.append(Request(url, meta = {'need_asyc_load':True, 'extend_map' : extend_map}, callback = self.parse_list, dont_filter = True))
      return items

    def parse_home(self, response):
      try:
        items = []
        url = response.url.strip()
        #print 'parse_home url:', url
        page = response.body.decode(response.encoding)
        extend_map = response.meta.get('extend_map', {})
        sta, channel_links_map = self.extend_map_h_.extract_channel_links_map(body = page, pageurl = url)
        if not sta:
          #TODO log
          print 'parse_home failed sta:%s, url:%s' % (sta, url)
          return
        for link, link_map in channel_links_map.items():
          link_map.update(extend_map)
          items.append(Request(link, meta = {'extend_map':link_map}, callback = self.parse_list, dont_filter = True))
        #el = CrawlerItem()
        #fill_base_item(response, el)
        #el['dont_filter'] = False
        #items.append(el)
        return items
      except Exception, e:
        msg = e.message
        msg += traceback.format_exc()
        print msg
        self.log('Failed parse_home: %s, url:%s' % (msg, url), log.ERROR)
        return

    def parse_list(self, response):
      try:
        items = []
        url = response.url.strip()
        #print 'parse_list url:', url
        page = response.body.decode(response.encoding)
        extend_map = response.meta.get('extend_map', {})
        status, extmd = self.extend_map_h_.extract_listurl_map(body = page, pageurl = url, ignore_empty_property=True, unique=False)
        if not status or not extmd:
          return
        for (i, exmap) in extmd:
          exmap.update(extend_map)
          #print 'page url:%s, exmap:%s ' % (i, exmap)
          items.append(Request(i, meta = {'extend_map': exmap}, headers={'Referer': '%s' % (url)}, callback = self.parse_page, dont_filter = True))
        #el = CrawlerItem()
        #fill_base_item(response, el)
        #el['dont_filter'] = False
        #el['extend_map'] = extend_map
        #items.append(el)
        return items
      except Exception, e:
        msg = e.message
        msg += traceback.format_exc()
        print msg
        self.log('Failed parse_list: %s, url:%s' % (msg, url), log.ERROR)
        return

    def parse_page(self, response):
      items = []
      url = response.url.strip()
      page = response.body.decode(response.encoding)
      extend_map = response.meta.get('extend_map', {})
      sta, exmap = self.extend_map_h_.extract_custom_map(body=page, pageurl=url)
      if sta:
        exmap.update(extend_map)
      else:
        exmap = extend_map
      ri = RankItem()
      ri['extend_map'] = exmap
      ri['url'] = url
      ri['referer'] = response.request.headers.get('Referer')
      ri['down_time'] = int(time.time())
      #el['dont_filter'] = True
      #print 'parse_page <%s> --> <%s>' % (response.url, response.request.headers.get('Referer'))
      items.append(ri)
      return items

