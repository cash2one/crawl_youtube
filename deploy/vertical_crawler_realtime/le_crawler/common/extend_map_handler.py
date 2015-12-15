#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import sys, os
import re
import json
import traceback

reload(sys)
sys.setdefaultencoding('utf8')

from scrapy import log
from scrapy.settings import CrawlerSettings 
from scrapy.selector import Selector

from ..base.singleton import Singleton
from ..base.utils import *
from ..base.logutil import Log
from ..base.url_filter import UrlFilter
from ..base.url_extend import load_lines_with_extend
from ..common.get_children_text import get_children_text

class ExtendMapHandler(Singleton):

  def init_onece(self, *args, **kwargs):
    self.loger = Log('extend_map_log', '../log/extend_map.log')
    self.loger.log.info('extend service is running... [%d]' % os.getpid())
    self.extend_map_ = {}
    self.setting_handler_ = ExtendMapBase(module_path = 'le_crawler.common.headline_video_settings',
        start_urls_path = '../start_urls/headline_urls.cfg',
        loger = self.loger)

  # must ensure call initialize avoid multi thread call
  def initialize(self, module_path = 'le_crawler.common.headline_video_settings', start_urls_path = '../start_urls/headline_urls_test.cfg'):
    self.setting_handler_ = ExtendMapBase(module_path = module_path,
        start_urls_path = start_urls_path, loger = self.loger)

  @property
  def settings(self):
    return self.setting_handler_

# url_extrdict: [(url, exted_dict)]
  def put_extend_map(self, url_extrdict):
    if not url_extrdict:
      return
    for (url, exs) in url_extrdict:
      self.loger.log.debug('put extend url [%s]' % url)
      tmpurl = UrlFilter.get_base_url(url)
      if not tmpurl or not self.setting_handler_.accept_url(tmpurl):
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
    tmpurl = UrlFilter.get_base_url(url)
    if not tmpurl:
      self.loger.log.error('Failed Got Url From[%s]' % (url))
      return None
    if self.extend_map_.has_key(url):
      if "json" == type:
        return self.setting_handler_._gen_json_result(self.extend_map_[tmpurl])
      elif "dict" == type:
        return self.extend_map_[tmpurl]
      else:
        self.loger.log.error('Unkown return type:%s' % type)
        return None
    else:
      self.loger.log.error('Failed lookup extend map for [%s]'% (url))
    return None

  def extract_extend_map(self, body = None, id = None, pageurl = None,
      ignore_empty_property = False):
    sta, urls, extmd = self.setting_handler_.extract_extend_map(body = body,
        id = id, pageurl = pageurl, ignore_empty_property = ignore_empty_property)
    self.put_extend_map(extmd)
    return sta, urls

class ExtendMapBase(object):
  #  #self.loger = Log('extend_map_log', '../log/extend_map.log')
  def __init__(self, module_path = '..common.extend_map_settings', start_urls_path =
      '../start_urls/start_urls.cfg', loger = None):
    #from scrapy.utils.misc import load_object
    __import__(module_path)
    self.__using_module = sys.modules[module_path]
    self.start_urls_file = start_urls_path
    if loger:
      self.loger = loger
    else:
      self.loger = Log('setting_extend_log', '../log/extend_setting.log')
    self.__init_setting()
  @property
  def settings(self):
    return CrawlerSettings(settings_module = self.__using_module)
  @property
  def id_map_regs(self):
    return self.url_id_mapping_regs_
  @property
  def property_path_dicts(self):
    return self.property_path_
  @property
  def table_name_dict(self):
    return self.tbl_n_
  @property
  def category_name_dict(self):
    return self.category_
  @property
  def ignore_dict(self):
    return self.ignore_extend_map_
  @property
  def dupe_data_dict(self):
    return self.delete_if_exist_
  @property
  def custom_property_dicts(self):
    return self.custom_property_path_

  def __convert_map_regs(self, regmap):
    if not regmap:
      return {}
    tmpres = {}
    for (id, reglist) in regmap.items():
      regstmp = []
      for r in reglist:
        #print 're....%s' % r
        regstmp.append(re.compile(r, re.IGNORECASE))
      if regstmp:
        tmpres[id] = regstmp
    return tmpres

  def __init_setting(self):
    assert self.settings
    mappings = self.settings.getdict('URL_MAPPING_ID', {})
    self.url_id_mapping_regs_ = self.__convert_map_regs(mappings)
    if not self.url_id_mapping_regs_:
      self.loger.log.error('Error Loading URL_MAPPING_ID')
    self.property_path_share_ = self.settings.getdict('PROPERTY_PATH_SHARE', {})
    self.property_path_ = self.settings.getdict('PROPERTY_PATH', {})
    if not self.property_path_:
      self.loger.log.error('Error Loading PROPERTY_PATH')
    accept_url_regs = self.settings.getdict('ACCEPT_URL_REG', {})
    self.accept_url_regs_ = self.__convert_map_regs(accept_url_regs)
    if not self.accept_url_regs_:
      self.loger.log.error('Error load ACCEPT_URL_REG')
    # store sider 
    self.tbl_n_ = self.settings.getdict('TABLE_NAME', {})
    if not self.tbl_n_:
      self.loger.log.error('Error loading table name')
    self.category_ = self.settings.getdict('CATEGORY_NAME', {})
    if not self.category_:
      self.loger.log.error('Error loading Category name')
    # load url id mapping from start urls
    self.__load_url_id_map(self.start_urls_file)
    # load ignore failed case
    self.ignore_extend_map_ = self.settings.getdict('IGNORE_EXTEND_MAP', {})
    # load if data exist doing
    self.delete_if_exist_ = self.settings.getdict('DELETE_IF_EXIST', {})
    # load custom
    self.custom_property_path_ = self.settings.getdict('CUSTOM_PATH', {})

  def __load_url_id_map(self, url_id_pathf = '../start_urls/start_urls.cfg'):
    lines = load_lines_with_extend(url_id_pathf)
    self.url_id_map_ = {}
    for line in lines:
      tmpkv = line.split()
      if not tmpkv or len(tmpkv) < 2:
        self.loger.log.error('Error start url %s' % line)
        continue
      self.url_id_map_[tmpkv[0]] = tmpkv[1]

    # base reg match
  def __accept_reg(self, id_reglist, item):
    if not item:
      return None
    for (id, tmpres) in id_reglist.items():
      for r in tmpres:
        if r.search(item):
          return id
    return None

  def get_id_from_referer(self, referer_url):
    if not referer_url:
      return None
    # first try to return id from start urls
    # if not will try return id from url mapping settting
    if self.url_id_map_.has_key(referer_url):
      return self.url_id_map_[referer_url]
    return self.need_extract_extend_map(referer_url)


  # if type == refer will get id from start url
  # else will get id from reg url config
  def get_id_from_url(self, url):
    return self.get_id_from_referer(url) or self.get_id_from_pattern(url)

  # FIXME:should inline
  def get_id_from_pattern(self, url):
    return self.__accept_reg(self.url_id_mapping_regs_, url)

  def need_extract_extend_map(self, url):
    return self.__accept_reg(self.id_map_regs, url)

  def ignore_id(self, id = None):
    if not id:
      return False
    return self.ignore_dict.has_key(id)

  def delete_dupe_data(self, id = None):
    if not id:
      return False
    return self.dupe_data_dict.has_key(id)

  # judgment the url is accept to store
  def accept_url(self, url):
    return self.__accept_reg(self.accept_url_regs_, url)

  # get extend map dict
  def get_property_dict(self, url = None, id = None):
    tmpid = id or self.get_id_from_url(url)
    if self.property_path_dicts.has_key(tmpid):
      return self.property_path_dicts[id]
    elif self.property_path_share_.has_key(tmpid) and\
        self.property_path_dicts.has_key(self.property_path_share_[tmpid]):
      return self.property_path_dicts[self.property_path_share_[tmpid]]
      
    return None
  # get custome map dict
  def get_custom_property_dict(self, url = None, id = None):
    tmpid = id or self.get_id_from_url(url)
    if self.custom_property_dicts.has_key(tmpid):
      return self.custom_property_dicts[id]
    return None

  def get_table_name(self, url = None, id = None):
    tmpid = id or self.get_id_from_url(url)
    if self.table_name_dict.has_key(tmpid):
      return self.table_name_dict[tmpid]
    return None

  def get_category_name(self, id = None, url = None):
    tmpid = id or self.get_id_from_url(url)
    if self.category_name_dict.has_key(tmpid):
      return self.category_name_dict[tmpid]
    return None
  # base on setting config, the reglist contains many
  # list as elecment, as the order the:
  # the first ele is xpath
  # the second ele is xpath's result index
  # the third ele is last result reg

  def __get_xpath_value(self, cur_sel, reglist, extract = True):
    if not cur_sel or not reglist:
      return None
    xvalues = None
    try:
      for xp in reglist[0]:
        if xp and xp != '':
          xvalues = cur_sel.xpath(xp)
        if xvalues:
          break
    except Exception, e:
      self.loger.log.error('xpath extract error[%s] using [%s]' %
        (e.message, reglist))
      return None

    if not xvalues or len(xvalues) == 0:
      return None
    index = 0
    #print 'xvalue:', xvalues
    if len(reglist) >= 2:
      index = int(reglist[1])
    if len(xvalues) <= index:
      index = -1
    if len(reglist) < 3:
      if extract:
        return xvalues[index].extract()
      else:
        return xvalues[index]
    regrst = None
    regindex = -1
    if len(reglist) > 3:
      regindex = int(reglist[3])
    for regtmp in reglist[2]:
      regrst = re.findall(regtmp, xvalues[index].extract())
      if regrst:
        if regindex >= 0 and regindex < len(regrst):
          return regrst[regindex]
        else:
          return ''.join(regrst)
    return None

  # extend value [(url, {property:value})]
  # return status, extend_urls, extend_map_dict
  def extract_extend_map(self, body = None, id = None, pageurl = None,
      ignore_empty_property = False):
    returls = []
    tmpid = id or self.get_id_from_url(pageurl)
    if not tmpid or not body:
      self.loger.log.info('Bad extract Url: %s %s' % (pageurl, id))
      return False, None, None
    self.loger.log.info('extract ---url: %s %s' % (pageurl, tmpid))
    sel = Selector(text = body, type = 'html')
    prop_dict = self.get_property_dict(id = tmpid)
    if not prop_dict:
      self.loger.log.error('Failed Found Property Dict For: %s' % id)
      return False, None, None
    if not sel:
      self.loger.log.error('can not get xpath config for [%r]'% tmpid)
      return False, None, None
    assert prop_dict.has_key('__root__') or not prop_dict['__root__'], 'property must contains __root__'
    rootstr = ''
    rootsels = []
    for rs in prop_dict['__root__']:
      rootsels.extend(sel.xpath(rs))
      # got all the path root select
      #rootstr = rs
      #if rootsels and len(rootsels) > 0:
      #  break
    #self.__get_xpath_value(sel, prop_dict['__root__'], extract = False)
    if not rootsels:
      self.loger.log.error('Failed get root selector data')
      return False ,None, None
    self.loger.log.debug('Got select url size: %d, for str: %s' % (len(rootsels),
      rootstr))
    retdicts = []
    assert prop_dict.has_key('__url__') or not prop_dict['__url__'], 'property must contains __url__'
    #rootsels.sort()
    status = False 
    try:
      for urls in rootsels:
        if not urls:
          continue
        tmpurl = self.__get_xpath_value(urls, prop_dict['__url__'])
        if not tmpurl:
          self.loger.log.error('Failed get root url: %s' % (prop_dict['__url__']))
          continue
        url = UrlFilter.get_accessable_url(pageurl, tmpurl)
        url = UrlFilter.get_base_url(url, scheme = 'http')
        if not url:
          self.loger.log.error('Failed get base url: %s' % (tmpurl[0]))
          continue
        if not self.accept_url(url):
          self.loger.log.info('not accept url[%s]' % (url))
          continue
        url = url.strip()
        #self.info('process: [%s]' % url)
        dicttmp = {}
        # every xpath will match from first to last until ok
        for (p, xps) in prop_dict.items():
          if not p.startswith("__"):
            #print 'property:', p, xps
            tmpvl = self.__get_xpath_value(urls, xps)
            if tmpvl:
              dicttmp[p] = tmpvl.strip().encode('utf8')
            # end of iner for
        if dicttmp:
         retdicts.append((url, dicttmp))
         returls.append(url)
        elif ignore_empty_property:
          returls.append(url)
        status = True
    except Exception, e:
      print e
      print traceback.format_exc()
      status = False
    self.loger.log.info('extend_map_size[%d], extract links[%s]' %
        (len(retdicts), len(returls)))
    #self.put_extend_map(retdicts)
    return status, returls, retdicts

  # extend value {property:value}
  # return status, extend_map_dict
  def extract_custom_map(self, body = None, id = None, pageurl = None):
    tmpid = id or self.accept_url(pageurl)
    if not tmpid or not body:
      self.loger.log.info('ignore extract custom url: %s %s' % (pageurl, tmpid))
      return False, None
    self.loger.log.debug('custom extract ---url: %s' % pageurl or tmpid)
    prop_dict = self.get_custom_property_dict(id = tmpid)
    if not prop_dict:
      self.loger.log.error('Failed Found Custom Property Dict For: %s' % id)
      return False, None
    sel = Selector(text = body, type = 'html')
    if not sel:
      self.loger.log.error('can not get xpath config for custom[%r]'% tmpid)
      return False, None
    retdicts = {}
    status = False 
    try:
        # every xpath will match from first to last until ok
        for (p, xps) in prop_dict.items():
          tmpvl = self.__get_xpath_value(sel, xps)
          if tmpvl:
            retdicts[p] = tmpvl.strip().encode('utf8')
          else:
            self.loger.log.debug('Empty [%s]' % (p))
            # end of iner for
        status = True
    except Exception, e:
      print e
      print traceback.format_exc()
      status = False
    self.loger.log.debug('Got Size[%d]' % len(retdicts))
    #self.put_extend_map(retdicts)
    return status, retdicts

  # return json object include {"cover": "http://kkkkkk", "title": "title""}
  def _gen_json_result(self, dicts):
    if not dicts:
      return None
    try:
      return json.dumps(dicts, ensure_ascii = False).encode('utf8')
    except Exception, e:
      self.loger.log.error('Convert to json ERROR [%s]' % (e.message))
      return None
if __name__ == '__main__':
  print 'tst:'
  tv = ExtendMapHandler()
