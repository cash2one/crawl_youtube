#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for spider picture from some mobile site
for cdesktop project templore
"""
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
import traceback


from le_crawler.core.items import CrawlerItem
from le_crawler.base.url_filter import UrlFilter 
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.common.cd_pictures_album_extractor import CdPicturesAlbumExtractor 
from le_crawler.common.cd_cateid_getter import get_cd_cateid_name


#global var 
class CDesktopPicturesAlbumCrawler(Spider):
    name = 'cd_pics_crawler'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loads = StartUrlsLoader.get_instance('../start_urls/')
    start_urls = start_url_loads.get_start_urls()

    def __init__(self, *a, **kw):
      super(CDesktopPicturesAlbumCrawler, self).__init__(*a, **kw)
      self.finished_count = 0
      self.start_size = len(CDesktopPicturesAlbumCrawler.start_urls)
      self.album_extractor = \
          CdPicturesAlbumExtractor(self, start_url_loader =
              CDesktopPicturesAlbumCrawler.start_url_loads)
      # mock_start_urls = []
      self.mock_start_urls = set()
      self.album_pages_count = 0

    def __file_crawler_items(self, condict):
      if not condict:
        return None
      item = CrawlerItem()
      import time
      item['down_time'] = int(time.time())
      for k, v in condict.items():
        item[k] = v
      return item

    def parse(self, response):
      try:
        url = response.url.strip()
        page = response.body.decode(response.encoding)
        retre = self.album_extractor.parser_album_list_page(url, page)
        self.finished_count += 1
        item_count = 0
        request_count = 0
        refer_url = response.request.headers.get('Referer', url)
        if 'items' in retre:
          item_count = len(retre['items'])
          self.album_pages_count += item_count 
          for i in retre['items']:
            item = self.__file_crawler_items(i)
            item['item_type'] = CDesktopPicturesAlbumCrawler.\
                start_url_loads.get_property(refer_url, 'category', '')
            yield item
          self.log('Got items size(1) %s' % (len(retre['items'])), log.DEBUG)
        if 'requests' in retre:
          request_count = len(retre['requests'])
          for r in retre['requests']:
            yield Request(r.split(' ')[0], headers={'Referer': '%s' % (url)},
              callback = self.parse_page)
        print 'Stage1: (%s/%s)%s, item:%s, request:%s' % (self.finished_count,
            self.start_size, url, item_count, request_count)

      except Exception, e:
        debug_msg = 'spider try catch error: %s' % e
        debug_msg += traceback.format_exc()
        print debug_msg
        self.log(debug_msg, log.ERROR)
        return 

    def parse_page(self, response):
      url = response.url.strip()
      if response.status == 404:
        nrequrl = self.album_extractor.refactory_qq_request_url(url)
        if nrequrl:
          yield Request(nrequrl, headers = response.request.headers,
              callback = self.parse_page)
      else:
        page = response.body
        if response.encoding != 'utf8' and response.encoding != 'utf-8':
          page = response.body.decode(response.encoding).encode('utf8')
        else:
          page = response.body
        content_type = response.headers.get('Content-Type')
        res = self.album_extractor.parser_album_info_pages(url, page, content_type)
        if 'items' in res:
          tmpcount = len(res['items'])
          self.album_pages_count += tmpcount
          for i in res['items']:
            item = self.__file_crawler_items(i)
            item['item_type'] = CDesktopPicturesAlbumCrawler.\
                start_url_loads.get_property(response.request.headers.get('Referer'),
                    'category', '')
            assert item['item_type'], 'bad item type'
            subid = CDesktopPicturesAlbumCrawler.\
                start_url_loads.get_property(response.request.headers.get('Referer'),
                    'subcategory', '10')
            item['cate_id'] = get_cd_cateid_name(subid, '体育')
            yield item
          self.log('Got item size(2) %s' % (len(res['items'])), log.DEBUG)
        if 'requests' in res:
          for r in res['requests']:
            yield Request(r.split(' ')[0], headers={'Referer': '%s' % (url)},
              callback = self.parse_page)

    def closed(self, reason):
      self.log('Spid)er items: %s' %(self.album_pages_count), log.INFO)
