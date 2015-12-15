#!/usr/bin/python
#
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for spider picture from some mobile site
for cdesktop project templore
"""
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
import traceback
import re
import time
import urlparse

from le_crawler.core.items import CrawlerItem
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.core.links_extractor import LinksExtractor
from le_crawler.core.items import fill_base_item

#global var 

class YoutubeAlbumSpider(Spider):
  name = 'youtube_album_spider'
  start_url_loads = StartUrlsLoader.get_instance('../start_urls/')
  start_urls = start_url_loads.get_start_urls()

  def __init__(self, *a, **kw):
    super(YoutubeAlbumSpider, self).__init__(*a, **kw)
    self.finished_count = 0
    self.start_size = len(YoutubeAlbumSpider.start_urls)
    self.new_links_extract = \
    LinksExtractor('le_crawler.common.page_info_settings',
        start_url_loader = YoutubeAlbumSpider.start_url_loader)

    # mock_start_urls = []
    self.search_result_page = re.compile(r'www\.youtube\.com\/result')
    self.user_page_url = re.compile(r'www\.youtube\.com\/user\/(\w+)')
    self.user_album_list_url = re.compile(r'www\.youtube\.com\/user\/(.+)\/playlists')
    self.user_album_v_list_url = re.compile(r'www\.youtube\.com\/playlist\?list=(.+)')
    # share object
    self.album_info_cache = {}
    self.album_v_info_cache = {}

  def _get_user_id(self, url):
    tmp = self.user_page_url.findall(url)
    return tmp[0] if tmp else None

  def _build_v_list_url(user_id):
    if not user_id:
      return None
    else:
      return 'https://www.youtube.com/user/%s/playlists?flow=grid&view=1' % (user_id)

  def _get_album_id(self, url):
    tmp = self.user_v_list_url.findall(url)
    return tmp[0] if tmp else None

  def _build_local_album_id(self, id):
    return '%s_%s' % ('youtube.com', id)

  def __file_crawler_items(self, condict):
    if not condict:
      return None
    item = CrawlerItem()
    item['down_time'] = int(time.time())
    for k, v in condict.items():
      item[k] = v
    return item

  def _parser_response_url(self, url):
    if self.search_result_page.search(url):
      return ('result_page', None)
    album_reg = self.user_album_list_url.findall(url)
    if album_reg:
      return ('album_list_page', album_reg)
    album_v_reg = self.user_album_v_list_url.findall(url)
    if album_v_reg:
      return ('album_v_list_page', album_v_reg)
    return (None, None)

  def _parse_album_id_from_url(self, url):
    up = urlparse.urlparse(url)
    qs = urlparse.parse_qs(up.query)
    if 'list' in qs:
      return qs['list'][0]
    return None



  def parse(self, response):
    try:
      item = CrawlerItem()
      fill_base_item(response, item)
      status, links_map = self.new_links_extract.extract_block_links(item['url'],
            body = item['page'], bd_type = LinksExtractor.HTML_EXTRA)

      url_type, data = self._parser_response_url(item['url'])
      if url_type == 'result_page':
        #generator user album list url request 
        for l in links_map:
          album_list_url = self._build_v_list_url(self._get_user_id(l))
          if not album_list_url:
            self.log('Failed build album list url:%s, %s' %(item['url'], l),
                log.ERROR)
            continue
          request = Request(album_list_url, header = {'Referer' : '%s' %
          (item['url'])}, callback = self.parse)
          yield request
      elif url_type == 'album_list_page':
        for l in links_map:
          request = Request(l.url, header = {'Referer' : '%s' %
          (item['url'])}, callback = self.parse)
          yield request
      elif url_type == 'album_v_list_page':
        #  generator v url request
        status, link = self.new_links_extract.extract_custom_links(item['url'],
            body = item['page'], bd_type = LinksExtractor.HTML_EXTRA)
        if status:
          #self.album_info_cache[data] = link.extend_map
          album_item = CrawlerItem()
          album_item['item_type'] = 'album_info'
          album_item['url'] = self._build_local_album_id(data)
          album_item['extend_map'] = link.extend_map
          yield album_item
          for l in links_map:
            self.album_v_info_cache[l.url] = dict(l.extend_map)
            request = Request(l.url, header = {'Referer' : '%s' %
              (item['url'])}, callback = self.parse_page)
            yield request
    except Exception, e:
      self.log('%s, %s' % (e.message, traceback.format_exc()), log.ERROR)

  def _fill_item_from_album_info(self, album_info, item):
    if not album_info:
      return
    if 'title' in album_info:
      item['title'] = album_info.pop('title', '')
    item['extend_map'] = dict(album_info)

  def parse_page(self, response):
    url = response.url
    status, page_l = self.new_links_extract.extract_custom_links(url, body =
        response.body, bd_type = LinksExtractor.HTML_EXTRA)
    if not status:
      self.log('Failed parse video page :%s' % (url), log.ERROR)
      return
    album_id = self._parse_album_id_from_url(url)
    if not album_id:
      self.log('Failed found album id from url:%s' % (url), log.ERROR)
    item = CrawlerItem()
    item['url'] = url
    item['referer'] = album_id
    item['extend_map'] = page_l.extend_map
    yield item

  def closed(self, reason):
    self.log('Spider items: %s' %(self.album_pages_count), log.INFO)
