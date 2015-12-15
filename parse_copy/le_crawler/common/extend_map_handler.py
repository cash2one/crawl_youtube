#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import sys, os
import threading

reload(sys)
sys.setdefaultencoding('utf8')

from logutil import Log
from url_normalize import UrlNormalize
from ..core.extra_extend_map_engine import ExtraExtendMapEngine


class ExtendMapHandler(object):
  _instance = None
  _instance_lock = threading.Lock()
  # must ensure call initialize avoid multi thread call

  @staticmethod
  def get_instance(start_url_loader,
                   module_path='le_crawler.common.headline_video_settings', loger=None):
    ExtendMapHandler._instance_lock.acquire()
    if not ExtendMapHandler._instance:
      ExtendMapHandler._instance = ExtendMapHandler(start_url_loader, module_path, loger)
    ExtendMapHandler._instance_lock.release()
    return ExtendMapHandler._instance

  def __init__(self, start_url_loader, module_path, loger=None):
    if loger:
      self.loger = loger
    else:
      self.loger = Log('extend_map_log', '../log/extend_map.log').log
    self.loger.info('extend service is running... [%d]' % os.getpid())
    self.extend_map_ = {}
    self.inlink_location_ = {}
    self.setting_handler_ = ExtraExtendMapEngine(
      start_url_loader,
      module_path=module_path,
      logger=self.loger)
    self.loger.info('finished initialize')

  @property
  def settings(self):
    return self.setting_handler_

  def put_inlink_location(self, base_url, location_str):
    if self.inlink_location_.has_key(base_url):
      if location_str < self.inlink_location_[base_url]:
        self.inlink_location_[base_url] = location_str
      else:
        return
    else:
      self.inlink_location_[base_url] = location_str

  def lookup_inlink_location(self, url):
    if self.inlink_location_.has_key(url):
      return self.inlink_location_[url]
    tmpurl = self.settings.url_normalizer.get_unique_url(url)
    if not tmpurl:
      self.loger.error('Failed Got Url From[%s]' % (url))
      return None
    if self.inlink_location_.has_key(tmpurl):
      return self.inlink_location_[tmpurl]

  def get_inlink_location_dict(self):
    return self.inlink_location_

  # url_extrdict: [(url, exted_dict)]
  def put_extend_map(self, url_extrdict):
    if not url_extrdict:
      return
    for (url, exs) in url_extrdict:
      self.loger.debug('put extend url [%s]' % url)
      tmpurl = self.settings.url_normalizer.get_unique_url(url)
      if not tmpurl or not self.settings.accept_url(tmpurl):
        self.loger.info('droped Url[%s]' % (url))
        continue
      if self.extend_map_.has_key(tmpurl):
        tmpti = None
        if self.extend_map_[tmpurl].has_key('title'):
          tmpti = self.extend_map_[tmpurl]['title']
        self.extend_map_[tmpurl].update(exs)
        if tmpti and len(self.extend_map_[tmpurl]['title']) < len(tmpti):
          self.extend_map_[tmpurl]['title'] = tmpti
      else:
        self.extend_map_[tmpurl] = exs
        self.loger.debug('new extend:[%s] for [%s] [%d]' % (tmpurl, exs,
                                                                len(exs)))

  def lookup_extend_map(self, url, re_type="json", pop=False):
    tmpurl = UrlNormalize.get_instance().get_unique_url(url)
    if not tmpurl:
      self.loger.error('Failed Got Url From[%s]' % (url))
      return None
    if self.extend_map_.has_key(url):
      retdict = None
      retdict = self.extend_map_.pop(url) if pop else self.extend_map_.get(url)
      if "json" == re_type:
        return self.settings._gen_json_result(retdict)
      elif "dict" == re_type:
        return retdict
      else:
        self.loger.error('Unkown return type:%s' % re_type)
        return None
    elif self.settings.ignore_extend_map_miss(tmpurl):
      if 'json' == re_type:
        return '{}'
      elif 'dict' == re_type:
        return {}
      else:
        return None
    else:
      self.loger.error('Failed lookup extend map for [%s]' % (url))
    return None

  def batch_update_inlink_location(self, referer_url, extend_urls):
    if not referer_url or not extend_urls:
      return None
    locstr = self.settings.get_location_from_referer(referer_url)
    if not locstr:
      return None
    for u in extend_urls:
      self.put_inlink_location(u, locstr)

  def extract_extend_map(self, body=None, id=None, pageurl=None,
                         ignore_empty_property=False, bd_type='html'):
    sta, urls, extmd = self.settings.extract_extend_map(body=body,
                                                        id=id, pageurl=pageurl,
                                                        ignore_empty_property=ignore_empty_property,
                                                        bd_type=bd_type)
    self.batch_update_inlink_location(pageurl, urls)
    self.put_extend_map(extmd)
    return sta, urls

  def extract_listurl_map(self, body=None, id=None, pageurl=None,
                         ignore_empty_property=False, bd_type='html', unique=True):
    sta, urls, extmd = self.settings.extract_extend_map(body=body,
                                                        id=id, pageurl=pageurl,
                                                        ignore_empty_property=ignore_empty_property,
                                                        bd_type=bd_type, unique=unique)
    return sta, extmd

  def extract_channel_links_map(self, body=None, id=None, pageurl=None, prefix=''):
    sta, links_map = self.settings.extract_channel_links_map(body=body, id=id, pageurl=pageurl, prefix=prefix)
    return sta, links_map

  def extract_sub_links_list(self, body=None, id=None, pageurl=None, sub_category_num=0):
    sta, has_sub_category, link_maps = self.settings.extract_sub_links_list(body=body, id=id, pageurl=pageurl,sub_category_num=sub_category_num)
    return sta, has_sub_category, link_maps

  def extract_next_url(self, body=None, id=None, pageurl=None):
    sta, next_url = self.settings.extract_next_url(body=body, id=id, pageurl=pageurl)
    return sta, next_url

  def filter_by_page(self, body=None, id=None, pageurl=None):
    return self.settings.filter_by_page(body=body, id=id, pageurl=pageurl)

  def extract_orderlist_map(self, body=None, id=None, pageurl=None):
    sta, order_select, url_map = self.settings.extract_orderlist_map(body=body, id=id, pageurl=pageurl)
    return sta, order_select, url_map

  def extract_custom_map(self, body, localid=None, pageurl=None):
    sta, retdicts = self.settings.extract_custom_map(body, localid, pageurl)
    return sta, retdicts

  def extract_urls(self, body, id=None, pageurl=None, extract_relative=True):
    sta, ret_urls = self.settings.extract_urls(body=body, id=id,
        pageurl=pageurl, extract_relative=extract_relative)
    return sta, ret_urls

  def parse_api(self, body, pageurl, list_page=False):
    sta, results = self.settings.parse_api(body=body, pageurl=pageurl, list_page=list_page)
    return sta, results

  def accept_url(self, url):
    return self.settings.accept_url(url)

  def extract_users(self, pageurl, body=None):
    sta, results = self.settings.extract_users(pageurl=pageurl, body=body)
    return sta, results

  def assemble_html(self, pageurl, response=None):
    return self.settings.assemble_html(pageurl=pageurl, response=response)
