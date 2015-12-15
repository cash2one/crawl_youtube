#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""One-line documentation for test module.
A detailed description of test.
"""
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy import log
import traceback
import json
#from scrapy.exceptions import IgnoreRequest
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from ..core.items import CrawlerItem
from ..base.url_filter import UrlFilter
from ..common.extend_map_handler import ExtendMapHandler
from le_crawler.common.headline_location_updater import HeadlineLocationUpdater
from le_crawler.base.start_url_loads import StartUrlsLoader
from ..common.extend_map_json_parser import ExtendMapJsonParser


#global var
class HeadlineCrawler(Spider):
    name = 'hdv_crawler'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/',
        random_sort = True)
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(HeadlineCrawler, self).__init__(*a, **kw)
      self.extend_map_h_ =\
          ExtendMapHandler.get_instance(HeadlineCrawler.start_url_loader)
      self.finished_count = 0
      self.start_size = len(HeadlineCrawler.start_urls)
      self.location_update = HeadlineLocationUpdater(self)
      self.api_parser_ = ExtendMapJsonParser()
      import re
      self.json_parser_reg = \
      re.compile(r'api\.tv\.sohu\.com\/v4\/search\/stream\/2\.json\?channeled=1000130005')

    def parse(self, response):
      try:
        url = response.url.strip()
        page = response.body.decode(response.encoding)
        self.finished_count += 1
        extend_url = []
        status = True
        size = 0
        if self.json_parser_reg.search(url):
          nrurl, items = self.api_parser_.extract_extend_map(
              body = page, pageurl = url)
          if nrurl:
            for i in nrurl:
              yield Request(i, headers={'Referer': '%s' % (url)}, callback =
                self.parse)
          if items:
            size = len(items)
            for i in items:
              re_item = CrawlerItem()
              re_item['url'] = i.get('url_html5', '')
              tmppage = json.dumps(i)
              re_item['page'] = tmppage.encode('utf8')
              #print re_item['page']
              re_item['page_encoding'] = 'utf8'
              re_item['referer'] =  url
              yield re_item
        else:
          status, extend_url =\
            self.extend_map_h_.extract_extend_map(body = page, pageurl = url)
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
        if not ignore_crawl:
          for i in extend_url:
            yield Request(i, headers={'Referer': '%s' % (url)}, callback =
                self.parse_page)
        else:
          self.log('ignore crawl: %s' % (url), log.INFO)
      except Exception, e:
        msg = e.message
        msg += traceback.format_exc()
        print msg
        self.log('Failed parse response: %s' % (msg), log.ERROR)
        return

      pass
    def parse_page(self, response):
      el = CrawlerItem()
      el['url'] = response.url.strip()
      el['redirect_urls'] = response.meta.get('redirect_urls', [])
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
