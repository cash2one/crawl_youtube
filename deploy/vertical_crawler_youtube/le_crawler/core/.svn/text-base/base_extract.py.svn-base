#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import re


from le_crawler.base.url_normalize import UrlNormalize
from le_crawler.base.url_domain_parser import query_domain_from_url
from le_crawler.base.url_filter import UrlFilter

class ExtractLinks(object):
  ITEM_REQUEST = 1 # request once and send to parse_page callback
  LIST_REQUEST = 2 # request agin for the item the respon
  ITEM_ITEM = 3
  
  def __init__(self):
    self.url = ''
    self.text = ''
    self.extend_map = None
    self.item_type = ExtractLinks.ITEM_REQUEST
    self.dont_filter = False

  def __str__(self):
    return '<%s><%s><%s><%s>' % ('request'
        if self.item_type == ExtractLinks.LIST_REQUEST else 'item', self.url,
        self.extend_map, self.dont_filter)

class BaseExtractor(object):
  def __init__(self, settings, loger, *kargs, **kwargs):
    self.loger = loger
    self.settings = settings
    self.url_normalize = UrlNormalize.get_instance()
    self.localid_share_dict = self.settings.getdict('LOCAL_ID_SHARE', {})
    self.accept_url_regs = self._convert_map_regs(self.settings.getdict('ACCEPT_URL_REG', {}))
    if 'start_url_loader' in kwargs:
      self.start_url_loader = kwargs['start_url_loader']
    else:
      self.start_url_loader = None
    self.property_path = self.settings.getdict('PROPERTY_PATH', {})
    self.json_property_path = self.settings.getdict('JSON_PROPERTY_PATH', {})
    self.custom_property_path = self.settings.getdict('CUSTOM_PATH', {})
    self.json_custom_property_path = self.settings.getdict('JSON_CUSTOM_PATH', {})
    self.url_filter = UrlFilter.get_instance()

  def _get_link_type(self, item_type):
    if item_type == 'item':
      return  ExtractLinks.ITEM_ITEM
    elif item_type == 'list_request':
      return ExtractLinks.LIST_REQUEST
    elif item_type == 'item_request':
      return ExtractLinks.ITEM_REQUEST
    return None

  def accept_url(self, url):
    localid = self.get_localid(url)
    if self.accept_url_regs.has_key(localid):
      for r in self.accept_url_regs[localid]:
        if r.search(url):
          return True
    return False
  def _convert_map_regs(self, regmap):
    if not regmap:
      return {}
    tmpres = {}
    for (id, reglist) in regmap.items():
      regstmp = []
      for r in reglist:
        regstmp.append(re.compile(r, re.IGNORECASE))
      if regstmp:
        tmpres[id] = regstmp
    return tmpres

  def get_localid(self, url):
    #domain = self.url_filter.get_domain_from_url(url)
    domain = query_domain_from_url(url) or\
        self.url_filter.get_domain_from_url(url)
    return self.localid_share_dict[domain] if\
        self.localid_share_dict.has_key(domain) else domain

  def add_start_urls(self, surl_json, random_sort = False):
    self.start_url_loader.add_start_urls(surl_json, random_sort = random_sort)

  def get_request_type_from_start_url(self, start_url):
    if not self.start_url_loader:
      return None
    else:
      return self._get_link_type(self.start_url_loader.get_property(
        start_url, 'request_type', 'item_request'))

  # return this list of ExtractLinks
  def extract_block_links(self, url, body, bd_type):
    pass

  def extract_custom_links(self, url, body, bd_type):
    pass
