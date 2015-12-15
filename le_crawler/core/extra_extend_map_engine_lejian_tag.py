# -*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
import sys
import re
import json
import traceback

from scrapy.settings import Settings
from scrapy.selector import Selector

from ..common.logutil import Log
from ..common.url_normalize import UrlNormalize
from ..common.url_normalize import get_abs_url
from ..common.url_filter import UrlFilter
from ..common.domain_parser import query_domain_from_url


"""
move from pre pycrawler.common.extend_map_handler module
base settings hold
"""
tag_dict = {
    u'频道':'channel',
    u'类别':'tags',
    u'类型':'tags',
    u'按类型':'tags',
    'subcategory':'tags',
    u'一级分类':'tags',
    u'特色分类':'tags',
    u'车型':'tags',
    u'分类':'tags',
    u'地区':'area',
    u'按地区':'area',
    u'按产地':'area',
    u'地域':'area',
    u'语言':'language',
    u'语种':'language',
    u'风格':'tags',
    u'流派':'tags',
    u'按流派':'tags',
    u'按风格':'tags',
    u'大项':'tags',
    u'内容':'tags',
    u'年份':'showyear',
    u'按年份':'showyear',
    u'范围':'showyear',
    u'发行':'showyear',
    u'画质':'quality',
    u'演唱':'actor',
    u'热门歌手':'singer',
    u'时长':'duration',
    u'片种':'genre',
    u'资费':'is_pay',
    u'行业':'tags',
    u'季节':'tags',
    u'版块':'tags',
    u'年龄段':'tags',
    u'大项':'tags',
    u'次项':'tags',
    u'已选条件':'conditions',
    u'筛选':'conditions',
    }

class ExtraExtendMapEngine(object):
  # self.loger = Log('extend_map_log', '../log/extend_map.log')
  def __init__(self,
               start_url_loader,
               module_path='..common.extend_map_settings',
               loger=None):
    # from scrapy.utils.misc import load_object
    self.loger = loger if loger else Log('setting_extend_log', '../log/extend_setting.log')
    __import__(module_path)
    self.__using_module = sys.modules[module_path]
    self.surl_loader = start_url_loader
    self.url_normalize_ = UrlNormalize.get_instance()
    self.url_filter = UrlFilter.get_instance()
    self.__init_setting()

  @property
  def url_normalizer(self):
    return self.url_normalize_

  @property
  def settings(self):
    return Settings({name: getattr(self.__using_module, name)
                     for name in dir(self.__using_module)})

  @property
  def id_map_regs(self):
    return self.url_id_mapping_regs_

  @property
  def html_property_path_dicts(self):
    return self.html_property_path_

  @property
  def table_name_dict(self):
    return self.tbl_n_

  @property
  def ignore_dict(self):
    return self.ignore_extend_map_

  @property
  def custom_property_dicts(self):
    return self.custom_html_property_path_

  @property
  def start_url_loader(self):
    return self.surl_loader

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
    self.ignore_extend_map_lost_reg = [re.compile(x) for x in
                                       self.settings.getlist('IGNORE_EXTEND_REG', []) if x]

    mappings = self.settings.getdict('URL_MAPPING_ID', {})
    self.url_id_mapping_regs_ = self.__convert_map_regs(mappings)
    if not self.url_id_mapping_regs_:
      self.loger.log.error('Error Loading URL_MAPPING_ID')

    self.html_property_path_share_ = self.settings.getdict('PROPERTY_PATH_ALIASES', {})
    self.json_property_path_share_ = self.settings.getdict('JSON_PROPERTY_PATH_ALIASES', {})

    self.channel_path = self.settings.getdict('CHANNEL_PATH', {})
    self.sub_category_path = self.settings.getdict('SUB_CATEGORY_PATH', {})
    self.next_path = self.settings.getdict('NEXT_PATH', {})

    # change: using localid
    self.html_property_path_ = self.settings.getdict('PROPERTY_PATH', {})
    self.json_property_path_ = self.settings.getdict('JSON_PROPERTY_PATH', {})
    if not self.html_property_path_:
      self.loger.log.error('Error Loading PROPERTY_PATH')
    if not self.json_property_path_:
      self.loger.log.error('Error Loading JSON_PROPERTY_PATH')

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
    self.custom_html_property_path_ = self.settings.getdict('CUSTOM_PATH', {})
    self.custom_html_property_alises_ = self.settings.getdict('CUSTOM_PATH_ALIASES', {})
    # localid
    self.localid_regs = [re.compile(i, re.I | re.S) for i in
                         self.settings.getlist('LOCALID_URL_MATCH', [])]
    # accept url
    self.accept_url_regs = self.__convert_map_regs(self.settings.getdict('ACCEPT_URL_REG', {}))
    self.localid_share_dict = self.settings.getdict('LOCAL_ID_SHARE', {})

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

  # deprecated, pls using start_url_loader directly
  def add_start_urls(self, surl_json, random_sort=False):
    self.start_url_loader.add_start_urls(surl_json, random_sort=random_sort)

  def get_id_from_referer(self, referer_url):
    return self.__get_localid(referer_url)

  def get_location_from_referer(self, referer_url):
    return self.start_url_loader.get_url_page_num(referer_url)

  def accept_url(self, url):
    localid = self.__get_localid(url)
    if self.accept_url_regs.has_key(localid):
      for r in self.accept_url_regs[localid]:
        if r.search(url):
          return True
    return False

  def ignore_extend_map_miss(self, url):
    for r in self.ignore_extend_map_lost_reg:
      if r.search(url):
        return True
    return False

  # get extend map dict
  def get_property_dict(self, url=None, localid=None, bd_type='html'):
    tmpid = localid or self.__get_localid(url)
    if bd_type == 'html':
      iterpd = self.html_property_path_
      iterpds = self.html_property_path_share_
    elif bd_type == 'json':
      iterpd = self.json_property_path_
      iterpds = self.json_property_path_share_
    else:
      return {}
    if iterpd.has_key(tmpid):
      return iterpd[tmpid]
    else:
      return iterpd[iterpds[tmpid]] if \
        iterpds.has_key(tmpid) and \
        iterpd.has_key(iterpds[tmpid]) \
        else {}
  def get_channel_dict(self, url=None, localid=None):
    tmpid = localid or self.__get_localid(url)
    channel_path_dict = self.channel_path
    if channel_path_dict.has_key(tmpid):
      return channel_path_dict[tmpid]
    else:
      return {}

  def get_sub_category_dict(self, url=None, localid=None):
    tmpid = localid or self.__get_localid(url)
    if self.sub_category_path.has_key(tmpid):
      return self.sub_category_path[tmpid]
    else:
      return {}

  def get_next_path(self, url=None, localid=None):
    tmpid = localid or self.__get_localid(url)
    return self.next_path.get(tmpid, [])

  # get custome map dict
  def get_custom_property_dict(self, url=None, id=None):
    tmpid = id or self.__get_localid(url)
    if self.custom_property_dicts.has_key(tmpid):
      return self.custom_property_dicts[id]
    else:
      return self.custom_property_dicts[self.custom_html_property_alises_[tmpid]] if \
        self.custom_html_property_alises_.has_key(tmpid) and \
        self.custom_property_dicts.has_key(self.custom_html_property_alises_[tmpid]) else {}

  def get_table_name(self, url=None, id=None):
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
    return self.start_url_loader.get_property(url, 'category', None)

  # base on setting config, the reglist contains many
  # list as elecment, as the order the:
  # the first ele is xpath
  # the second ele is xpath's result index
  # the third ele is last result reg

  def __get_xpath_value(self, cur_sel, reglist, extract=True):
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
    # return self.start_url_loader.ignore_crawl_extract_links(referer_url)
    sctype = self.start_url_loader.get_property(referer_url, 'type', None)
    if not sctype:
      self.loger.log.error('Failed Found start url type')
      return False
    if sctype.lower() != 'list':
      return True
    return False

  def __get_localid(self, url):
    #domain = self.url_filter.get_domain_from_url(url)
    domain = query_domain_from_url(url) or \
             self.url_filter.get_domain_from_url(url)
    return self.localid_share_dict[domain] if \
      self.localid_share_dict.has_key(domain) else domain
    #for i in self.localid_regs:
    #  sr = i.search(url)
    #  if sr:
    #    mg = sr.groups()
    #    if mg:
    #      return mg[0]

  # extend value [(url, {property:value})]
  # return status, extend_urls, extend_map_dict
  def extract_extend_map(self, body, id=None, bd_type='html', pageurl=None,
                         ignore_empty_property=False):
    if not body:
      return False, [], {}
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.loger.log.critical('Failed get localid: %s' % (pageurl))
      return False, [], {}
    self.loger.log.info('Begin Extract URL: %s %s' % (pageurl, tmpid))
    if bd_type == 'html':
      return self.__extract_html_extend_map(body, id=tmpid, pageurl=pageurl,
                                            ignore_empty_property=ignore_empty_property)
    elif bd_type == 'json':
      return self.__extract_json_extend_map(body, id=tmpid, pageurl=pageurl,
                                            ignore_empty_property=ignore_empty_property)
    else:
      self.loger.log.critical('Unsupport type:%s' % (bd_type))
      return False, [], {}

  def __get_json_path(self, json_val, jpath):
    jpl = [u for u in jpath.split('/') if u.strip() != '']
    iter_j = json_val
    for jp in jpl:
      if iter_j.has_key(jp):
        iter_j = iter_j[jp]
      else:
        return None
    return iter_j

  def __get_json_path_l(self, jsonv, jplist):
    retv = None
    for jp in jplist:
      retv = self.__get_json_path(jsonv, jp)
      if retv:
        return retv
    return None

  def __preprocess_json_body(self, body):
    body = body.strip()
    rebody = body.strip()
    if rebody.startswith("QZOutputJson="):
      rebody = rebody.replace('QZOutputJson=', '')
    if rebody.endswith('};'):
      rebody = rebody[0:-1]
    return rebody

  def __extract_json_extend_map(self, body, id=None, pageurl=None,
                                ignore_empty_property=False):
    j = json.loads(self.__preprocess_json_body(body))
    prop_dict = self.get_property_dict(localid=id, bd_type='json')
    if not prop_dict:
      self.loger.log.error('Failed Found Property Dict For: %s' % id)
      return False, None, None
    if not prop_dict.has_key('__root__') or not prop_dict['__root__']:
      self.loger.log.critical('property must contains __root__, %s' % id)
      return False, None, None
    rootsels = []
    for rs in prop_dict['__root__']:
      jtmp = self.__get_json_path(j, rs)
      if jtmp:
        rootsels.extend(jtmp)
    if not rootsels:
      self.loger.log.error('Failed get root selector data')
      return False, None, None
    returls = []
    retdict = []
    for blk in rootsels:
      tmpurl = self.__get_json_path_l(blk, prop_dict['__url__'][0])
      if not tmpurl:
        self.loger.log.error('Failed Found __url__ Property for data')
        continue
      url = self.url_normalize_.get_unique_url(tmpurl, scheme='http')
      if not url:
        self.loger.log.error('Failed get base url: %s' % (tmpurl))
        continue
      if not self.accept_url(url):
        self.loger.log.info('not accept url[%s]' % (url))
        continue
        url = url.strip()
      returls.append(url)
      tmpdict = {}
      for k, v in prop_dict.items():
        if k.startswith('__'):
          continue
        if not v:
          continue
        tmpv = self.__get_json_path_l(blk, v[0])
        if tmpv:
          tmpdict[k] = tmpv
      if tmpdict:
        retdict.append((url, tmpdict))
    return True, returls, retdict

  def __extract_html_extend_map(self, body, id=None, pageurl=None,
                                ignore_empty_property=False):
    returls = []
    tmpid = id
    sel = Selector(text=body, type='html')
    prop_dict = self.get_property_dict(localid=tmpid)
    subcategory_id = self.get_category_id(self.get_category_name(pageurl))
    if not prop_dict:
      self.loger.log.error('Failed Found Property Dict For: %s' % tmpid)
      return False, None, None
    if not sel:
      self.loger.log.error('can not get xpath config for [%r]' % tmpid)
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
      return False, None, None
    self.loger.log.info('Got select url size: %d, for str: %s' % (len(rootsels),
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
        url = self.url_normalize_.get_unique_url(url, scheme='http')
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
            tmpvl = self.__get_xpath_value(urls, xps)
            if tmpvl:
              dicttmp[p] = tmpvl.strip()
              if p == 'cover':  # img url, eed do full path process
                dicttmp[p] = get_abs_url(pageurl, dicttmp[p])
                # end of iner for
        if dicttmp:
          if subcategory_id:
            dicttmp['sid'] = '%s' % subcategory_id
          retdicts.append((url, dicttmp))
          returls.append(url)
        elif ignore_empty_property:
          returls.append(url)
        status = True
    except Exception, e:
      print e
      print traceback.format_exc()
      self.loger.log.error('Failed extend map for:%s, %s'
                           % (pageurl, traceback.format_exc()))
      status = False
    self.loger.log.info('extend_map_size[%d], extract links[%s]' %
                        (len(retdicts), len(returls)))
    #self.put_extend_map(retdicts)
    return status, returls, retdicts

  # extend value {property:value}
  # return status, extend_map_dict
  def extract_custom_map(self, body, localid=None, pageurl=None):
    tmpid = localid or self.__get_localid(pageurl)
    if not tmpid or not body:
      self.loger.log.info('ignore extract custom url: %s %s' % (pageurl, tmpid))
      return False, None
    self.loger.log.debug('custom extract ---url: %s' % pageurl or tmpid)
    prop_dict = self.get_custom_property_dict(id=tmpid)
    if not prop_dict:
      self.loger.log.error('Failed Found Custom Property Dict For: %s' % tmpid)
      return False, None
    sel = Selector(text=body, type='html')
    if not sel:
      self.loger.log.error('can not get xpath config for custom[%r]' % tmpid)
      return False, None
    retdicts = {}
    status = False
    try:
      # every xpath will match from first to last until ok
      for (p, xps) in prop_dict.items():
        tmpvl = self.__get_xpath_value(sel, xps)
        if tmpvl:
          retdicts[p] = tmpvl.strip()
        else:
          self.loger.log.debug('Empty [%s]' % (p))
          # end of iner for
      status = True
    except Exception, e:
      print e
      print traceback.format_exc()
      self.loger.log.error('exception for:%s, %s' % (e.message,
                                                     traceback.format_exc()))
      status = False
    self.loger.log.debug('Got Size[%d]' % len(retdicts))
    #self.put_extend_map(retdicts)
    return status, retdicts

  # return json object include {"cover": "http://kkkkkk", "title": "title""}
  def _gen_json_result(self, dicts):
    if not dicts:
      return None
    try:
      return json.dumps(dicts, ensure_ascii=False).encode('utf8')
    except Exception, e:
      self.loger.log.error('Convert to json ERROR [%s]' % (e.message))
      return None

  def extract_channel_links_map(self, body=None, id=None, pageurl=None):
    if not body:
      return False, None
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.loger.log.critical('Failed get localid: %s' % (pageurl))
      return False, {}
    sel = Selector(text=body, type='html')
    channel_dict = self.get_channel_dict(localid=tmpid)
    if not channel_dict:
      self.loger.log.error('Failed Found Channel Property Dict For: %s' % tmpid)
      return False, None
    if not sel:
      self.loger.log.error('can not get channel xpath config for [%r]' % tmpid)
      return False, None
    rootsels = []
    for rs in channel_dict['__root__']:
      rootsels.extend(sel.xpath(rs))
    if not rootsels:
      self.loger.log.error('Failed get root selector data')
      return False,None
    retdict = {}
    status = False
    try:
      for urls in rootsels:
        if not urls:
          continue
        tmpurl = self.__get_xpath_value(urls, channel_dict['__url__'])
        if not tmpurl:
          self.loger.log.error('Failed get root url: %s' % (channel_dict['__url__']))
          continue
        url = get_abs_url(pageurl, tmpurl)
        if tmpid != 'pptv.com':
          url = self.url_normalize_.get_unique_url(url, scheme='http')
        if not url:
          self.loger.log.error('Failed get base url: %s' % (tmpurl[0]))
          continue
        url = url.strip()
        dicttmp = {}
        channel_xps = channel_dict.get('channel')
        channel = self.__get_xpath_value(urls, channel_xps)
        if not channel:
          continue
        if channel not in channel_dict.get('__select__'):
          continue
        dicttmp['category'] = channel
        retdict[url] = dicttmp
        status = True
    except Exception, e:
      print e
      print traceback.format_exc()
      self.loger.log.error('Failed extract link map for:%s, %s' % (pageurl, traceback.format_exc()))
      status = False
    self.loger.log.info('extend_map_size[%d]' % len(retdict))
    return status, retdict


  def extract_sub_links_map(self, body=None, id=None, pageurl=None, sub_category_num=0):
    if not body:
      return False, False, None
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.loger.log.critical('Failed get localid: %s' % (pageurl))
      return False, {}
    sel = Selector(text=body, type='html')
    sub_category_dict = self.get_sub_category_dict(localid=tmpid)
    if not sub_category_dict:
      self.loger.log.error('Failed Found sub_category Dict For: %s' % tmpid)
      return False, False, None
    if not sel:
      self.loger.log.error('can not get sub_category xpath config for [%r]' % tmpid)
      return False, False, None
    rootsels = []
    for rs in sub_category_dict['__root__']:
      rootsels.extend(sel.xpath(rs))
    if not rootsels:
      self.loger.log.error('Failed get sub_category root selector data')
      retdict = {}
      dicttmp = {}
      retdict[pageurl] = dicttmp
      return True, False, retdict
      #return False, False, None
    retdict = {}
    status = False
    has_sub_category = False
    if sub_category_num >= len(rootsels):
      self.loger.log.error('hava no much sub_category [%s]' % pageurl)
    elif sub_category_num == len(rootsels)-1:
      has_sub_category = False
    else:
      has_sub_category = True
    sub_sel = rootsels[sub_category_num]
    tag = self.__get_xpath_value(sub_sel, sub_category_dict['tag'])
    if (not tag or tag.strip()==u'') and (len(rootsels) == 1) :
      tag = 'subcategory'
    tag = tag.strip(':\r\n\t ')
    #tag = tag.strip()
    tag = tag.strip('：')
    tag = tag.strip()
    tag = tag.replace(u'\xa0',u'')
    tag = tag_dict[tag]
    except_list = sub_category_dict.get('__except__', None)
    if except_list and tag in except_list:
      dicttmp = {}
      retdict[pageurl] = dicttmp
      return True, has_sub_category, retdict
    sub_rootsels = []
    for xs in sub_category_dict['__sub_root__']:
      sub_rootsels.extend(sub_sel.xpath(xs))
    retdict = {}
    status = False
    try:
      for urls in sub_rootsels:
        if not urls:
          continue
        tmpurl = self.__get_xpath_value(urls, sub_category_dict['__url__'])
        if not tmpurl:
          self.loger.log.error('Failed get root url: %s' % (sub_category_dict['__url__']))
          continue
        url = get_abs_url(pageurl, tmpurl)
        if tmpid != 'pptv.com':
          url = self.url_normalize_.get_unique_url(url, scheme='http')
        if not url:
          self.loger.log.error('Failed get base url: %s' % (tmpurl[0]))
          continue
        url = url.strip()
        dicttmp = {}
        sub_category_xps = sub_category_dict.get('sub_category')
        sub_category = self.__get_xpath_value(urls, sub_category_xps)
        if not sub_category or sub_category.strip() == u'全部':
          continue
        sub_category = sub_category.strip()
        dicttmp[tag] = sub_category
        retdict[url] = dicttmp
        status = True
    except Exception, e:
      print e
      print traceback.format_exc()
      self.loger.log.error('Failed extract link map for:%s, %s' % (pageurl, traceback.format_exc()))
      status = False
    self.loger.log.info('extend_map_size[%d]' % len(retdict))
    return status, has_sub_category, retdict

  def extract_next_url(self, body=None, id=None, pageurl=None):
    if not body:
      return False, None
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.loger.log.critical('Failed get localid: %s' % (pageurl))
      return False, {}
    sel = Selector(text=body, type='html')
    next_path = self.get_next_path(localid=tmpid)
    if not next_path:
      self.loger.log.error('Failed Found next_path Dict For: %s' % tmpid)
      return False, None
    if not sel:
      self.loger.log.error('can not get next xpath config for [%r]' % tmpid)
      return False, None
    status = False
    try:
      tmp_url = self.__get_xpath_value(sel, next_path)
      if not tmp_url:
        self.loger.log.error('has no next page for: [%s]', pageurl)
        return False, None
      next_url = get_abs_url(pageurl, tmp_url)
      next_url = self.url_normalize_.get_unique_url(next_url, scheme='http')
      next_url = next_url.strip()
      if not next_url:
        self.loger.log.error('Failed get next url: %s' % (tmp_url[0]))
        return False, None
      status = True
    except Exception, e:
      print e
      print traceback.format_exc()
      self.loger.log.error('Failed extract next url for : [%s]' % pageurl)
      status = False
    return status, next_url

if __name__ == '__main__':
  print 'tst:'
