##!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
Extension for filter request by domain
"""

from scrapy.exceptions import IgnoreRequest

from le_crawler.base.url_filter import UrlFilter

class DomainFilterMiddleware(object):
  def __init__(self, settings, stats):
    self.url_filter_ = UrlFilter.get_instance()
    self.stats_ = stats

  @classmethod
  def from_crawler(cls, crawler):
    o = cls(crawler.settings, crawler.stats)
    return o

  #all url if url domain is disallowed will be ignore
  def process_request(self, request, spider):
    if not self.url_filter_.is_interesting_url(request.url):
      if self.stats_:
        self.stats_.inc_value('downloader/droped_request', spider = spider)
      raise IgnoreRequest('Un interesting request %s' % request.url)


