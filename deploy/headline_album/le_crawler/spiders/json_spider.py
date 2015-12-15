#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
this spider only crawl json apid and then parse_page
"""
import traceback
import sys
import json
#from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.spider import Spider
#from scrapy.exceptions import IgnoreRequest 
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from ..core.items import CrawlerItem
from ..base.url_filter import UrlFilter 
from ..base.url_extend import load_lines_with_extend
#from ..core.le_sgml import LeSgmlLinkExtract
#from ..common.extend_map_handler import ExtendMapHandler
from ..common.extend_map_json_parser import ExtendMapJsonParser


reload(sys)
sys.setdefaultencoding('utf8')
#global var 
class ApiSpider(Spider):
    name = 'api_crawler'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_urls = [line.split(' ')[0] for line in
        load_lines_with_extend('../start_urls/start_urls_api.cfg', random_sort = True)]

    def __init__(self, *a, **kw):
      super(ApiSpider, self).__init__(*a, **kw)
      self.api_parser_ = ExtendMapJsonParser()
      self.start_size = len(ApiSpider.start_urls)
      self.request_num = 0

    def parse(self, response):
      try:
        url = response.url.strip()
        page = response.body.decode(response.encoding).encode('utf8')
        nrurl, items = self.api_parser_.extract_extend_map(body = page, pageurl = url)
        size = 0
        self.request_num += 1
        if items:
          size = len(items)
        print 'Ok[%d]:%s, parsed: %d' % (self.request_num, url, size)
        if items:
          for i in items:
            re_item = CrawlerItem()
            re_item['url'] = i['url_html5']
            tmppage = json.dumps(i)
            re_item['page'] = tmppage.encode('utf8')
            #print re_item['page']
            re_item['http_header'] = ''
            re_item['page_encoding'] = 'utf8'
            re_item['referer'] =  url
            yield re_item
        if nrurl:
          for r in nrurl:
            yield Request(r, callback = self.parse)
      except Exception, e:
        print 'spider try catch error:', e
        print traceback.format_exc()
        return
