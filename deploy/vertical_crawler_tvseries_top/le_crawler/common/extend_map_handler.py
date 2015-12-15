#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import sys, os
import threading
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy import log

from le_crawler.base.utils import *
from le_crawler.base.logutil import Log
from le_crawler.core.extra_extend_map_engine import ExtraExtendMapEngine

#from le_crawler.common.get_children_text import get_children_text

class ExtendMapHandler(object):
  _instance = None
  _instance_lock = threading.Lock()
  # must ensure call initialize avoid multi thread call
  @staticmethod
  def get_instance(start_url_loader,
      module_path = 'le_crawler.common.headline_video_settings'):
    ExtendMapHandler._instance_lock.acquire()
    if not ExtendMapHandler._instance:
      ExtendMapHandler._instance = ExtendMapHandler(start_url_loader, module_path)
    ExtendMapHandler._instance_lock.release()
    return ExtendMapHandler._instance

  def __init__(self, start_url_loader, module_path):
    self.loger = Log('extend_map_log', '../log/extend_map.log')
    self.loger.log.info('extend service is running... [%d]' % os.getpid())
    self.extend_map_ = {}
    self.inlink_location_ = {}
    self.setting_handler_ = ExtraExtendMapEngine(
        start_url_loader,
        module_path = module_path,
        loger = self.loger)
    self.loger.log.info('finished initialize')

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
      self.loger.log.error('Failed Got Url From[%s]' % (url))
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
      self.loger.log.debug('put extend url [%s]' % url)
      tmpurl = self.settings.url_normalizer.get_unique_url(url)
      if not tmpurl or not self.settings.accept_url(tmpurl):
        self.loger.log.info('droped Url[%s]' % (url), log.INFO)
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
        self.loger.log.debug('new extend:[%s] for [%s] [%d]' % (tmpurl, exs,
          len(exs)))

  def lookup_extend_map(self, url, type = "json"):
    from le_crawler.base.url_normalize import UrlNormalize
    tmpurl = UrlNormalize.get_instance().get_unique_url(url)
    if not tmpurl:
      self.loger.log.error('Failed Got Url From[%s]' % (url))
      return None
    if self.extend_map_.has_key(url):
      if "json" == type:
        return self.settings._gen_json_result(self.extend_map_[tmpurl])
      elif "dict" == type:
        return self.extend_map_[tmpurl]
      else:
        self.loger.log.error('Unkown return type:%s' % type)
        return None
    else:
      self.loger.log.error('Failed lookup extend map for [%s]'% (url))
    return None

  def batch_update_inlink_location(self, referer_url, extend_urls):
    if not referer_url or not extend_urls:
      return None
    locstr = self.settings.get_location_from_referer(referer_url)
    if not locstr:
      return None
    for u in extend_urls:
      self.put_inlink_location(u, locstr)

  def extract_extend_map(self, body = None, id = None, pageurl = None,
      ignore_empty_property = False, bd_type = 'html'):
    sta, urls, extmd = self.settings.extract_extend_map(body = body,
        id = id, pageurl = pageurl, ignore_empty_property = ignore_empty_property,
        bd_type = bd_type)
    self.batch_update_inlink_location(pageurl, urls)
    self.put_extend_map(extmd)
    return sta, urls
