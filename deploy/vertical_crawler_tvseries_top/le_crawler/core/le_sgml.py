#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class LeSgmlLinkExtract(SgmlLinkExtractor):

  def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(),
                 tags=('a', 'area'), attrs=('href'), canonicalize=True, unique=True, process_value=None,
                 deny_extensions=None):
    SgmlLinkExtractor.__init__(self, allow = allow,
        deny = deny,
        allow_domains = allow_domains,
        deny_domains = deny_domains,
        restrict_xpaths = restrict_xpaths,
        tags = tags,
        attrs = attrs,
        canonicalize = canonicalize,
        unique = unique,
        process_value = self.process_value,
        deny_extensions = deny_extensions
        )

  def handle_data(self, data):
    try:
      if self.current_link:
        tmp_text = self.current_link.text + data.strip()
        self.current_link.text = tmp_text
        return
    except Exception, e:
      print 'extract linked text error, belong decoding error'
      return 

  def process_value(self, value):
    if value:
      return value.strip()

  def _process_links(self, links):
    links = SgmlLinkExtractor._process_links(self, links)
    return links
