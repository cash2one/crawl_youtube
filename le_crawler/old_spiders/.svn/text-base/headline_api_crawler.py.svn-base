#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
this spider using for api json parser
"""
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy import log
import traceback

from ..core.items import CrawlerItem
from ..base.url_filter import UrlFilter 
from le_crawler.common.headline_location_updater import HeadlineLocationUpdater
from ..common.extend_map_handler import ExtendMapHandler
from le_crawler.base.start_url_loads import StartUrlsLoader

class HeadlineApiCrawler(Spider):
    name = 'hdv_api_crawler'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loader =\
    StartUrlsLoader.get_instance('../start_urls/headline_api_url.cfg',
        random_sort = True)
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(HeadlineApiCrawler, self).__init__(*a, **kw)
      self.extend_map_h_ = ExtendMapHandler.get_instance(
          HeadlineApiCrawler.start_url_loader)
      self.finished_count = 0
      self.start_size = len(HeadlineApiCrawler.start_urls)
      self.location_update = HeadlineLocationUpdater(self)

    def parse(self, response):
      try:
        url = response.url.strip()
        if response.encoding != 'utf8' and response.encoding != 'utf-8':
          page = response.body.decode(response.encoding).encode('utf8')
        else:
          page = response.body
        self.finished_count += 1
        status, extend_url = self.extend_map_h_.extract_extend_map(body = page, pageurl = url)
        size = 0
        if extend_url:
          size = len(extend_url)
        if status:
          print 'Ok:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
        else:
          print 'Failed:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
          return
        ignore_crawl = self.extend_map_h_.setting_handler_.ignore_link_to_crawler(url)
        if not ignore_crawl and not self.use_sys_extract_link:
          for i in extend_url:
            yield Request(i, headers={'Referer': '%s' % (url)}, callback =
                self.parse_page)
        else:
          self.log('ignore crawl: %s' % (url), log.INFO)
        #return self.parse_page(response)
        # update location string
        #location_str = self.extend_map_h_.setting_handler_.get_location_from_referer(url)
        #self.location_update.update_headlinedb(extend_url, location_str)
      except Exception, e:
        print 'spider try catch error:', e
        print traceback.format_exc()
        return

      pass
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
        if self.location_update.need_update():
          locationd = self.extend_map_h_.get_inlink_location_dict()
          self.log('update location size: %d' %  len(locationd), log.INFO)
          for (k, v) in locationd.items():
            self.location_update.update_headlinedb(k, v)
          self.location_update.update_timestamp()
        self.location_update.close()
      except Exception, e:
        import traceback
        print traceback.format_exc()
        self.log('Failed: %s' % e.message, log.ERROR)
