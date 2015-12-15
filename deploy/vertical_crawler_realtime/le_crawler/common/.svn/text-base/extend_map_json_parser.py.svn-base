#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import sys, os
import re
import json
import traceback

from ..base.singleton import Singleton
from ..base.utils import *
from ..base.logutil import Log
from ..base.url_filter import UrlFilter
from ..common.extend_map_handler import ExtendMapHandler

reload(sys)
sys.setdefaultencoding('utf8')

class ExtendMapJsonParser():
  def __init__(self):
    print '--------------extend map json running as %r------------' % os.getpid()
    self.loger = Log('extend_map_json_log', '../log/extend_map_json.log')
    self.loger.log.info('extend map json service is running... [%d]' % os.getpid())
    self.extend_map_ = {}
    self.__init_setting()
    self.extend_map_h_ = ExtendMapHandler()

# 
  def __init_setting(self):
    pass

  def extract_extend_map(self, body, pageurl = None):
    if not body:
      return None, None
    try:
      if 'SOHU_GIRL' == self.extend_map_h_.settings.get_id_from_url(pageurl):
        return self.__parse_souhu_json(body)
      else:
        self.loger.error('un-support input parse %s' % (jsonob['status']))
        return None, None
    except Exception, e:
      print e
      print traceback.format_exc()
      return None, None

  def __parse_souhu_json(self, json_str):
    jsonob = json.loads(json_str)
    if not jsonob.has_key('status'):
      self.loger.error('Json String Not Ok: %s' % (json_str))
      return None, None
    if 200 != jsonob['status']:
      self.loger.error('Json String status error: %s' % (jsonob['status']))
      return None, None
    if not jsonob.has_key('data'):
      self.loger.error('Json String Not Contail data: %s' % (json_str))
      return None, None
    dataj = jsonob['data']
    max_id = None
    min_id = None
    if dataj.has_key('max_id'):
      max_id = dataj['max_id']
    if dataj.has_key('min_id'):
      min_id = dataj['min_id']
    if not min_id or not max_id:
      self.loger.error('Failed Get max(in) id')
      return None, None
    if not dataj.has_key('videos'):
      self.loger.error('Failed Get videos:%s' % (dataj))
      return None, None
    nrurl = "http://api.tv.sohu.com/v4/search/stream/2.json?channeled=1000130005&pull_down=1&api_key=695fe827ffeb7d74260a813025970bd5&plat=3&partner=1&sver=4.2&poid=1&page_size=50&max_id=%s&min_id=%s" % (max_id, min_id)
    return [nrurl], dataj['videos']
