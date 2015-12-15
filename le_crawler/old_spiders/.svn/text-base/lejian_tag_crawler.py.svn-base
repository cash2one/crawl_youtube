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
import json
import time
from copy import deepcopy
#from scrapy.exceptions import IgnoreRequest
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from ..core.items import CrawlerItem, fill_base_item
from ..base.time_parser import TimeParser
from ..base.url_filter import UrlFilter
from ..common.extend_map_handler import ExtendMapHandler
from le_crawler.base.start_url_loads import StartUrlsLoader

def parserTimestr(timestr):
  calc_ts_obj = TimestrParser()
  timestr = timestr.replace(' ', ' ')
  time_temp = calc_ts_obj.timestamp(timestr)
  if time_temp < 0:
    return None
  timeArray = time.localtime(time_temp)
  otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
  return otherStyleTime



#global var
class LejianCrawler(Spider):
    name = 'lejian_tag'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/', random_sort = True)
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(LejianCrawler, self).__init__(*a, **kw)
      self.extend_map_h_ = ExtendMapHandler.get_instance(LejianCrawler.start_url_loader,
          module_path='le_crawler.common.lejian_video_settings')
      self.finished_count = 0
      self.start_size = len(LejianCrawler.start_urls)

    def start_requests(self):
      items = []
      for url in LejianCrawler.start_urls:
        type = self.start_url_loader.get_property(url, 'type', 'list')
        extend_map = self.start_url_loader.get_property(url, 'extend_map', {})
        if type == 'home':
          items.append(Request(url, meta = {'extend_map' : extend_map}, callback = self.parse_home, dont_filter = True))
        elif type == 'channel':
          items.append(Request(url, meta = {'extend_map' : extend_map}, callback = self.parse_channel, dont_filter = True))
        elif type == 'list':
          items.append(Request(url, meta = {'extend_map' : extend_map}, callback = self.parse_list, dont_filter = True))
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
          items.append(Request(link, meta = {'extend_map' : link_map}, callback = self.parse_channel, dont_filter = True))
        el = CrawlerItem()
        el['extend_map'] = response.meta.get('extend_map', {})
        fill_base_item(response, el)
        items.append(el)
        return items
      except Exception, e:
        msg = e.message
        msg += traceback.format_exc()
        print msg
        self.log('Failed parse_home: %s, url:%s' % (msg, url), log.ERROR)
        return

    def parse_channel(self, response):
      try:
        items = []
        url = response.url.strip()
        #print 'parse_channel url: %s' % url
        page = response.body.decode(response.encoding)
        extend_map = response.meta.get('extend_map', {})
        sub_category_num = response.meta.get('sub_category_num', 0)
        sta, has_sub_category, links_map = self.extend_map_h_.extract_sub_links_map(body = page, pageurl = url,sub_category_num=sub_category_num)
        if not sta:
          print 'parse_channel url failed, url: [%s]' % url
          return
        else:
          sub_category_num += 1
          for link, link_map in links_map.items():
            tag_item = link_map.pop('tags',None)
            link_map.update(extend_map)
            tag_list = deepcopy(extend_map.get('tags',[]))
            if tag_item:
              tag_list.append(tag_item)
            link_map['tags'] = tag_list
            if has_sub_category:
              items.append(Request(link, meta = {'extend_map':link_map, 'sub_category_num':sub_category_num}, 
                callback = self.parse_channel,dont_filter = True))
            else:
              items.append(Request(link, meta = {'extend_map':link_map, 'need_asyc_load':True}, callback = self.parse_list, dont_filter = True))
        el = CrawlerItem()
        el['extend_map'] = response.meta.get('extend_map', {})
        fill_base_item(response, el)
        items.append(el)
        return items
      except Exception, e:
        msg = e.message
        msg += traceback.format_exc()
        print msg
        self.log('Failed parse_channel: %s, url: %s' % (msg, url), log.ERROR)
        return

    def parse_list(self, response):
      try:
        items = []
        url = response.url.strip()
        page = response.body.decode(response.encoding)
        extend_map = response.meta.get('extend_map', {})
        #print 'parse_list url: %s, extend_map: %s' % (url, extend_map)
        sta, next_link = self.extend_map_h_.extract_next_url(body=page, pageurl=url)
        if sta:
          #print 'get next link: [%s]' % next_link
          next_extend_map = deepcopy(extend_map)
          items.append(Request(next_link, meta = {'extend_map': next_extend_map}, callback = self.parse_list, dont_filter = True))
        status, extend_url = self.extend_map_h_.extract_extend_map(body = page, pageurl = url)
        if not status:
          self.log('parse list failed,  listurl:%s' %  url)
          return
        extend_map['tags'] = ';'.join(extend_map.get('tags',[]))
        ignore_crawl = self.extend_map_h_.setting_handler_.ignore_link_to_crawler(url)
        if not ignore_crawl:
          for i in extend_url:
            exmap = self.extend_map_h_.lookup_extend_map(i, re_type='dict')
            if exmap.has_key('showtime'):
              try:
                exmap['showtime'] = parserTimestr(exmap['showtime'])
              except:
                self.log('parse timestr failed, videourl: %s, listurl:%s' % (i, url))
                exmap['showtime'] = None
                print 'parse timestr failed, videourl: %s, listurl:%s' % (i, url)
            exmap.update(extend_map)
            items.append(Request(i, meta = {'extend_map': exmap}, headers={'Referer': '%s' % (url)}, callback = self.parse_page, dont_filter = False))
        el = CrawlerItem()
        el['extend_map'] = response.meta.get('extend_map', {})
        fill_base_item(response, el)
        items.append(el)
        return items
      except Exception, e:
        msg = e.message
        msg += traceback.format_exc()
        print msg
        self.log('Failed parse_list: %s, url:%s' % (msg, url), log.ERROR)
        return

    def parse_page(self, response):
      items = []
      el = CrawlerItem()
      el['extend_map'] = response.meta.get('extend_map', {})
      fill_base_item(response, el)
      #print 'parse_page <%s> --> <%s>' % (response.url, response.request.headers.get('Referer'))
      items.append(el)
      return items

if __name__ == '__main__':
  print parserTimestr('2012')
