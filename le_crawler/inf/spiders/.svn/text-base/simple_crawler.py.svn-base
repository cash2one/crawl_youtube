#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""One-line documentation for test module.
A detailed description of test.
"""
from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.exceptions import IgnoreRequest 
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from ..core.items import CrawlerLoader 
from ..base.url_filter import UrlFilter 
from ..core.le_sgml import LeSgmlLinkExtract
from ..common.extend_map_handler import ExtendMapHandler


#global var 
class SimpleSpider(CrawlSpider):
    name = 'sle_crawler'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_urls = [line.split(' ')[0] for line in UrlFilter.load_domains('../conf/start_urls.cfg')]
    print '--------start url-------:\n%s ' % start_urls

    rules = (
        Rule(LeSgmlLinkExtract(allow=('', )),
             callback='parse_page', follow = True),
    )

    def __init__(self, *a, **kw):
      super(SimpleSpider, self).__init__(*a, **kw)
      self.extend_map_h_ = ExtendMapHandler.get_instance()
      #print 'simple_crawler ---->%s' %self.extend_map_h_

    def parse_page(self, response):
      el = CrawlerLoader(response=response)
      el.add_value('url', response.url.strip())
      el.add_value('page', response.body)
      el.add_value('http_header', response.headers.to_string())
      el.add_value('page_encoding', response.encoding)
      # this hock using for compute category
      el.add_value('referer', response.request.headers.get('Referer'))
      #print '<%s> --> <%s>' % (response.url, response.request.headers.get('Referer'))
      return el.load_item()

    def parse_start_url(self, response):
      try:
        url = response.url.strip()
        print 'begin extract start_urls: %s' % (url)
        page = response.body.decode(response.encoding).encode('utf8')
        self.extend_map_h_.extract_extend_map(body = page, pageurl = url)
        print 'end extract start_urls: %s' % (url)
        return self.parse_page(response)
      except Exception, e:
        print e
        return None
      #raise IgnoreRequest('ignore start url: %s' % url)
