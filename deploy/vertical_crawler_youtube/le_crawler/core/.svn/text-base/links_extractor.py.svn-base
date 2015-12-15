#!/usr/bin/env python
#-*-coding:utf8-*-
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import sys

from scrapy.settings import CrawlerSettings 

from le_crawler.base.logutil import Log
from le_crawler.core.html_extract import HtmlExtractor
from le_crawler.core.json_extract import JsonExtractor

class LinksExtractor(object):
  XML_EXTRA =  'XML'
  HTML_EXTRA =  'HTML'
  JSON_EXTRA =  'JSON'
  def __init__(self, setting_path, *kargs, **kwargs):
    __import__(setting_path)
    self.settings = CrawlerSettings(settings_module = sys.modules[setting_path])
    self.loger = Log('links_extractor_log', '../log/links_extractor.log')
    self.xml_extract = None  # the same as html
    self.html_extract= HtmlExtractor(self.settings, self.loger, *kargs, **kwargs) 
    self.json_extract = JsonExtractor(self.settings, self.loger, *kargs, **kwargs)

  def extract_links(self, body, url):
    pass

  # return list of extractlinks
  def extract_block_links(self, url, body, bd_type, filter = True):
    if bd_type == LinksExtractor.HTML_EXTRA:
      return self.html_extract.extract_block_links(url, body, bd_type = 'html',
          filter_url= filter)
    elif bd_type == LinksExtractor.XML_EXTRA:
      return self.html_extract.extract_block_links(url, body, bd_type = 'xml',
          filter_url= filter)
    elif bd_type == LinksExtractor.JSON_EXTRA:
      return self.json_extract.extract_block_links(url, body, bd_type = 'json',
          filter_url= filter)
    else:
      raise Exception('Bad extract type: %s' % (bd_type))

  def extract_custom_links(self, url, body, bd_type):
    if bd_type == LinksExtractor.HTML_EXTRA:
      return self.html_extract.extract_custom_links(url, body, bd_type = 'html')
    elif bd_type == LinksExtractor.XML_EXTRA:
      return self.html_extract.extract_custom_links(url, body, bd_type = 'xml')
    elif bd_type == LinksExtractor.JSON_EXTRA:
      return self.json_extract.extract_custom_links(url, body, bd_type = 'json')
    else:
      raise Exception('Bad extract type: %s' % (bd_type))
