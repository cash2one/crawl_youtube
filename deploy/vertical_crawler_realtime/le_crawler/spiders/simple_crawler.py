#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""One-line documentation for test module.
A detailed description of test.
"""
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.utils.project import get_project_settings
import traceback
#from scrapy.exceptions import IgnoreRequest 
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from ..core.items import CrawlerItem
from ..base.url_filter import UrlFilter 
from ..base.url_extend import load_lines_with_extend
#from ..core.le_sgml import LeSgmlLinkExtract
from ..common.extend_map_handler import ExtendMapHandler


#global var 
class SimpleSpider(Spider):
    name = 'hdv_crawler'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    if get_project_settings()['DEBUG_MODEL']:
      start_urls = [line.split(' ')[0] for line in
        load_lines_with_extend('../start_urls/headline_urls_test.cfg', random_sort = True)]
    else:
      start_urls = [line.split(' ')[0] for line in
        load_lines_with_extend('../start_urls/headline_urls.cfg', random_sort = True)]

    def __init__(self, *a, **kw):
      super(SimpleSpider, self).__init__(*a, **kw)
      self.extend_map_h_ = ExtendMapHandler()
      if get_project_settings()['DEBUG_MODEL']:
        self.extend_map_h_.initialize(start_urls_path =
          '../start_urls/headline_urls_test.cfg')
      else:
        self.extend_map_h_.initialize(start_urls_path =
          '../start_urls/headline_urls.cfg')

      #print 'simple_crawler ---->%s' %self.extend_map_h_
      self.finished_count = 0
      self.start_size = len(SimpleSpider.start_urls)
      self.use_sys_extract_link = False 

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
        if not self.use_sys_extract_link:
          for i in extend_url:
            yield Request(i, headers={'Referer': '%s' % (url)}, callback =
                self.parse_page)
        #return self.parse_page(response)
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
