#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""One-line documentation for test module.
A detailed description of test.
"""
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
import traceback
#from scrapy.exceptions import IgnoreRequest 
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from ..core.items import CrawlerItem
from ..base.url_filter import UrlFilter 
from ..base.url_extend import load_lines_with_extend
#from ..core.le_sgml import LeSgmlLinkExtract
from le_crawler.common.headline_location_updater import HeadlineAlbumUpdater 
from le_crawler.common.headline_album_extractor import HeadLineAlbumExtractor 


#global var 
class HeadlineAlbumCrawler(Spider):
    name = 'hdv_album_crawler'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_urls = [line.split(' ')[0] for line in
        load_lines_with_extend('../start_urls/', random_sort = True)]

    def __init__(self, *a, **kw):
      super(HeadlineAlbumCrawler, self).__init__(*a, **kw)
      self.finished_count = 0
      self.start_size = len(HeadlineAlbumCrawler.start_urls)
      self.use_sys_extract_link = False 
      self.album_update = HeadlineAlbumUpdater(self)
      self.album_extractor = \
      HeadLineAlbumExtractor.get_instance()
      # mock_start_urls = []
      self.mock_start_urls = set()
      self.album_pages_count = 0

    def parse(self, response):
      try:
        url = response.url.strip()
        if response.encoding != 'utf8' and response.encoding != 'utf-8':
          page = response.body.decode(response.encoding).encode('utf8')
        else:
          page = response.body
        retre = self.album_extractor.parser_enter(url, page)
        self.finished_count += 1
        print 'Ok:(%5d/%d)Finished ParserEnterUrl: %s, %d' % (self.finished_count,
            self.start_size, url, len(retre))
        album_start_urls = [ i.split(' ')[0] for i in retre ]
        # add album video list page to start urls
        #self.extend_map_h_.settings.add_start_urls(retre)
        self.mock_start_urls.union(album_start_urls)
        for i in album_start_urls:
          yield Request(i.split(' ')[0], headers={'Referer': '%s' % (url)},
              callback = self.parse_album_list_page,
              dont_filter = True)
        # update location string
        #location_str = self.extend_map_h_.setting_handler_.get_location_from_referer(url)
        #self.location_update.update_headlinedb(extend_url, location_str)
      except Exception, e:
        print 'spider try catch error:', e
        print traceback.format_exc()
        return

    def parse_album_list_page(self, response):
      try:
        url = response.url.strip()
        if response.encoding != 'utf8' and response.encoding != 'utf-8':
          page = response.body.decode(response.encoding).encode('utf8')
        else:
          page = response.body
        self.album_pages_count += 1
        size = 0
         
        extend_url =  self.album_extractor.parser_album_info_pages(body = page,
            url = url, refer_url = response.request.headers.get('Referer'))
        if extend_url:
          size = len(extend_url)
        print 'Done:(%s,%s)AlbumListPageExtend: %s' % (
            size,
            self.album_pages_count,
            url)
        if extend_url and not self.use_sys_extract_link:
          for i in extend_url:
            yield Request(i,
                headers={'Referer': '%s' % (url)},
                callback = self.parse_page)
      except Exception, e:
        import traceback
        print traceback.format_exc()
        print 'error while parser_album_info_pags', e
        return

    def parse_page(self, response):
      el = CrawlerItem()
      el['url'] = response.url.strip()
      el['page'] = response.body
      el['http_header'] = response.headers.to_string()
      el['page_encoding'] = response.encoding
      # this hock using for compute category
      el['referer'] = response.request.headers.get('Referer')
      #print '<%s> --> <%s>' % (response.url, response.request.headers.get('Referer'))
      return el

    def closed(self, reason):
      try:
        self.album_update.update_album_info(self.album_extractor.get_album_infos())
      except Exception, e:
        import traceback
        print traceback.format_exc()
        self.log('Failed: %s' % e.message, log.ERROR)
