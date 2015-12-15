#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
import sys, os
import re
import json
import traceback
from scrapy.settings import CrawlerSettings 
from scrapy.selector import Selector

from le_crawler.base.logutil import Log
from le_crawler.base.url_extend import load_lines_with_extend
from le_crawler.base.url_normalize import UrlNormalize
from le_crawler.base.url_normalize import get_abs_url
from le_crawler.base.url_filter import UrlFilter

"""
move from pre pycrawler.common.extend_map_handler module
base settings hold
"""
class ExtraExtendMapEngine(object):
  #  #self.loger = Log('extend_map_log', '../log/extend_map.log')
  def __init__(self,
      module_path = '..common.extend_map_settings',
      start_urls_path = '../start_urls/start_urls.cfg',
      loger = None):
    #from scrapy.utils.misc import load_object
    self.loger = loger if loger else Log('setting_extend_log', '../log/extend_setting.log')
    __import__(module_path)
    self.__using_module = sys.modules[module_path]
    self.url_id_map_ = {}
    self.location_dict = {} # {0:0} {home|list|channel:page_num}
    self.ignore_crawl_set = set()
    self.add_start_urls(start_urls_path)
    self.url_normalize_ = UrlNormalize()
    self.url_filter = UrlFilter.get_instance()
    self.__init_setting()

  @property
  def url_normalizer(self):
    return self.url_normalize_

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
  def custom_property_dicts(self):
    return self.custom_property_path_

  def __convert_map_regs(self, regmap):
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

  def __init_setting(self):
    assert self.settings
    mappings = self.settings.getdict('URL_MAPPING_ID', {})
    self.url_id_mapping_regs_ = self.__convert_map_regs(mappings)
    if not self.url_id_mapping_regs_:
      self.loger.log.error('Error Loading URL_MAPPING_ID')

    self.property_path_share_ = self.settings.getdict('PROPERTY_PATH_ALIASES', {})

    # change: using localid
    self.property_path_ = self.settings.getdict('PROPERTY_PATH', {})
    if not self.property_path_:
      self.loger.log.error('Error Loading PROPERTY_PATH')
    # load localid match reg
    # store sider 
    self.tbl_n_ = self.settings.getdict('TABLE_NAME', {})
    if not self.tbl_n_:
      self.loger.log.error('Error loading table name')
    # load sub category id mapping
    self.subcategory_id_ = self.settings.getdict('SUBCATEGORY_ID', {})
    if not self.subcategory_id_:
      self.loger.log.error('Error loading Category ID Mapping')
    # load url id mapping from start urls
    # load ignore failed case
    self.ignore_extend_map_ = self.settings.getdict('IGNORE_EXTEND_MAP', {})
    # load if data exist doing
    self.delete_if_exist_ = self.settings.getdict('DELETE_IF_EXIST', {})
    # load custom
    self.custom_property_path_ = self.settings.getdict('CUSTOM_PATH', {})
    self.custom_property_alises_ = self.settings.getdict('CUSTOM_PATH_ALIASES', {})
    # localid
    self.localid_regs = [ re.compile(i, re.I | re.S) for i in
        self.settings.getlist('LOCALID_URL_MATCH', [])]
    # accept url
    self.accept_url_regs = self.__convert_map_regs(self.settings.getdict('ACCEPT_URL_REG', {}))

  # input id|type|page_num or id|type
  # return (id, location_str)
  def __analyse_idstr(self, idstr):
    if idstr is None:
      return (None, None)
    wds = str.split(idstr, '|')
    if not wds:
      return (None, None)
    if len(wds) < 2:
      raise Exception('Bad idstr for start url: %s' % (idstr))
    if len(wds) == 2:
      wds.append(0)
    retres = (None, None)
    if wds[1] == 'home':
      retres = (wds[0], '1:%s' % wds[2], 'home')
    elif wds[1] == 'channel':
      retres = (wds[0], '2:%s' % wds[2], 'channel')
    else:
      retres = (wds[0], '3:%s' % wds[2], 'list')
    return retres

  def add_start_urls(self, start_urls):
    if not start_urls:
      return
    urls = []
    if type(start_urls) is str:
      urls = load_lines_with_extend(start_urls)
    elif type(start_urls) is list:
      urls = start_urls
    if not urls:
      return
    self.__init_start_urls(urls)

  def __init_start_urls(self, lines):
    # using for store url -> category_type
    for line in lines:
      tmpkv = line.split()
      if not tmpkv or len(tmpkv) < 2:
        self.loger.log.error('Error start url %s' % line)
        continue
      rettmp = self.__analyse_idstr(tmpkv[1])
      if not rettmp or not rettmp[0] or not rettmp[1]:
        self.loger.log.error('Error analyse idstr %s' % line)
        continue
      self.url_id_map_[tmpkv[0]] = rettmp[0]
      self.location_dict[tmpkv[0]] = rettmp[1]
      if 'list' != rettmp[2]:
        self.ignore_crawl_set.add(tmpkv[0])

  def get_id_from_referer(self, referer_url):
    return self.__get_localid(referer_url)
  
  def get_location_from_referer(self, referer_url = None, mapid = None):
    if not referer_url:
      return None
    if self.location_dict.has_key(referer_url):
      return self.location_dict[referer_url]
    return None

  def accept_url(self, url):
    localid = self.__get_localid(url)
    if self.accept_url_regs.has_key(localid):
      for r in self.accept_url_regs[localid]:
        if r.search(url):
          return True
    return False

  # get extend map dict
  def get_property_dict(self, url = None, localid = None):
    tmpid = localid or self.__get_localid(url)
    if self.property_path_dicts.has_key(tmpid):
      return self.property_path_dicts[tmpid]
    else:
      return self.property_path_dicts[self.property_path_share_[tmpid]] if\
          self.property_path_share_.has_key(tmpid) and \
          self.property_path_dicts.has_key(self.property_path_share_[tmpid]) \
          else {}
  # get custome map dict
  def get_custom_property_dict(self, url = None, id = None):
    tmpid = id or self.__get_localid(url)
    if self.custom_property_dicts.has_key(tmpid):
      return self.custom_property_dicts[id]
    else:
      return self.custom_property_dicts[self.custom_property_alises_[tmpid]] if\
          self.custom_property_alises_.has_key(tmpid) and\
        self.custom_property_dicts.has_key(self.custom_property_alises_[tmpid]) else {}

  def get_table_name(self, url = None, id = None):
    tmpid = id or self.__get_localid(url)
    if self.table_name_dict.has_key(tmpid):
      return self.table_name_dict[tmpid]
    return None

  def get_category_id(self, category_name):
    if category_name is None:
      return None
    if self.subcategory_id_.has_key(category_name):
      return self.subcategory_id_[category_name]

  def get_category_name(self, url):
    if self.url_id_map_.has_key(url):
      return self.url_id_map_[url]
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
    if len(reglist) < 3 or not reglist[2]:
      return xvalues[index].extract() if extract else xvalues[index]
    regrst = None
    regindex = -1
    if len(reglist) > 3:
      regindex = int(reglist[3])
    for regtmp in reglist[2]:
      regrst = re.findall(regtmp, xvalues[index].extract())
      if regrst:
        return regrst[regindex] if regindex >= 0 and regindex < len(regrst) else ''.join(regrst)
    return None

  def ignore_link_to_crawler(self, referer_url):
    return referer_url in self.ignore_crawl_set

  def __get_localid(self, url):
    return self.url_filter.get_domain_from_url(url)
    #for i in self.localid_regs:
    #  sr = i.search(url)
    #  if sr:
    #    mg = sr.groups()
    #    if mg:
    #      return mg[0]
  # extend value [(url, {property:value})]
  # return status, extend_urls, extend_map_dict

  def extract_extend_map(self, body, id = None, pageurl = None,
      ignore_empty_property = False):
    returls = []
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid or not body:
      self.loger.log.info('Bad extract Url: %s %s' % (pageurl, id))
      return False, None, None
    self.loger.log.info('extract ---url: %s %s' % (pageurl, tmpid))
    sel = Selector(text = body, type = 'html')
    prop_dict = self.get_property_dict(localid = tmpid)
    subcategory_id = self.get_category_id(self.get_category_name(pageurl))
    if not prop_dict:
      self.loger.log.error('Failed Found Property Dict For: %s' % tmpid)
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
        url = get_abs_url(pageurl, tmpurl)
        url = self.url_normalize_.get_unique_url(url, scheme = 'http')
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
              if p == 'cover': # img url, eed do full path process
                dicttmp[p] = get_abs_url(pageurl, dicttmp[p])

            # end of iner for
        if dicttmp:
         dicttmp['sid'] = '%s' % subcategory_id
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
  def extract_custom_map(self, body, localid = None, pageurl = None):
    tmpid = localid or self.__get_localid(pageurl)
    if not tmpid or not body:
      self.loger.log.info('ignore extract custom url: %s %s' % (pageurl, tmpid))
      return False, None
    self.loger.log.debug('custom extract ---url: %s' % pageurl or tmpid)
    prop_dict = self.get_custom_property_dict(id = tmpid)
    if not prop_dict:
      self.loger.log.error('Failed Found Custom Property Dict For: %s' % tmpid)
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
