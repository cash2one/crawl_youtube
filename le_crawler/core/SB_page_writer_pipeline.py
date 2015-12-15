#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

from scrapy import log

from ..base.url_filter import UrlFilter

from page_writer_pipeline import PageWriterPipeLine


class SBPageWriterPipeLine(PageWriterPipeLine):
  def filter_url(self, item):
    if not self.url_filter_.is_interesting_url(item['url']):
      self.spider_.log("uninteresting url %s" % item['url'], log.INFO)
      return True
    return False
