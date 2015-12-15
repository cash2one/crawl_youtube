# -*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8

import re
import sys
import json

from scrapy.settings import Settings
from scrapy.selector import Selector

from ..common.logutil import Log
from ..common.utils import del_repeat, FetchHTML, atoi
from ..common.url_filter import UrlFilter
from ..common.url_normalize import get_abs_url
from ..common.url_normalize import UrlNormalize
from ..common.domain_parser import query_domain_from_url


"""
move from pre pycrawler.common.extend_map_handler module
base settings hold
"""

class ExtraExtendMapEngine(object):
  def __init__(self,
               start_url_loader,
               module_path='..common.extend_map_settings',
               logger=None):
    # from scrapy.utils.misc import load_object
    self.logger_ = logger if logger else Log('setting_extend_log', '../log/extend_setting.log')
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
      self.logger_.debug('Error Loading URL_MAPPING_ID')

    self.html_property_path_share_ = self.settings.getdict('PROPERTY_PATH_ALIASES', {})
    self.json_property_path_share_ = self.settings.getdict('JSON_PROPERTY_PATH_ALIASES', {})

    self.channel_path = self.settings.getdict('CHANNEL_PATH', {})
    self.sub_category_path = self.settings.getdict('SUB_CATEGORY_PATH', {})
    self.order_path = self.settings.getdict('ORDER_PATH', {})
    self.next_path = self.settings.getdict('NEXT_PATH', {})
    self.video_relatives_path = self.settings.getdict('VIDEO_RELATIVES_PATH', {})
    self.href_path = self.settings.getdict('HREF_PATH', {})
    self.page_verify = self.settings.getdict('PAGE_VERIFY', {})
    self.api_parse_func = self.settings.getdict('API_PARSE_FUNC', {})
    self.user_list_path = self.settings.getdict('USER_LIST_PATH', {})

    # change: using localid
    self.html_property_path_ = self.settings.getdict('PROPERTY_PATH', {})
    self.json_property_path_ = self.settings.getdict('JSON_PROPERTY_PATH', {})
    if not self.html_property_path_:
      self.logger_.error('Error Loading PROPERTY_PATH')
    if not self.json_property_path_:
      self.logger_.error('Error Loading JSON_PROPERTY_PATH')

    # load localid match reg
    # store sider
    self.tbl_n_ = self.settings.getdict('TABLE_NAME', {})
    if not self.tbl_n_:
      self.logger_.debug('Error loading table name')
    # load sub category id mapping
    self.subcategory_id_ = self.settings.getdict('SUBCATEGORY_ID', {})
    if not self.subcategory_id_:
      self.logger_.debug('Error loading Category ID Mapping')
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

  def get_href_path(self, url=None, localid=None):
    tmpid = localid or self.__get_localid(url)
    return self.href_path.get(tmpid, [])

  def get_video_relatives_path(self, url=None, localid=None):
    tmpid = localid or self.__get_localid(url)
    return self.video_relatives_path.get(tmpid, [])

  def get_order_path_dict(self, url=None, localid=None):
    tmpid = localid or self.__get_localid(url)
    if self.order_path.has_key(tmpid):
      return self.order_path[tmpid]
    else:
      return {}


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

  def _get_xpath_value(self, cur_sel, reglist, extract=True):
    if not cur_sel or not reglist:
      return None
    xvalues = None
    try:
      for xp in reglist[0]:
        if xp and xp != '':
          xvalues = cur_sel.xpath(xp)
        if xvalues:
          break
    except:
      self.logger_.exception('failed extract value: [%s]', reglist)
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
      self.logger_.error('Failed Found start url type')
      return False
    if sctype.lower() != 'list':
      return True
    return False

  def __get_localid(self, url):
    #domain = self.url_filter.get_domain_from_url(url)
    if not url:
      return None
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
                         ignore_empty_property=False, unique=True):
    if not body:
      return False, [], {}
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.logger_.critical('Failed get localid: %s' % (pageurl))
      return False, [], {}
    self.logger_.debug('Begin Extract URL: %s %s' % (pageurl, tmpid))
    if bd_type == 'html':
      return self.__extract_html_extend_map(body, id=tmpid, pageurl=pageurl,
                                            ignore_empty_property=ignore_empty_property, unique=unique)
    elif bd_type == 'json':
      return self.__extract_json_extend_map(body, id=tmpid, pageurl=pageurl,
                                            ignore_empty_property=ignore_empty_property)
    else:
      self.logger_.critical('Unsupport type:%s' % (bd_type))
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
      self.logger_.error('Failed Found Property Dict For: %s' % id)
      return False, None, None
    if not prop_dict.has_key('__root__') or not prop_dict['__root__']:
      self.logger_.critical('property must contains __root__, %s' % id)
      return False, None, None
    rootsels = []
    for rs in prop_dict['__root__']:
      jtmp = self.__get_json_path(j, rs)
      if jtmp:
        rootsels.extend(jtmp)
    if not rootsels:
      self.logger_.error('Failed get root selector data')
      return False, None, None
    returls = []
    retdict = []
    for blk in rootsels:
      tmpurl = self.__get_json_path_l(blk, prop_dict['__url__'][0])
      if not tmpurl:
        self.logger_.error('Failed Found __url__ Property for data')
        continue
      url = self.url_normalize_.get_unique_url(tmpurl, scheme='http')
      if not url:
        self.logger_.error('Failed get base url: %s' % (tmpurl))
        continue
      if not self.accept_url(url):
        self.logger_.debug('not accept url[%s]' % (url))
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
                                ignore_empty_property=False, unique=True):
    returls = []
    tmpid = id
    sel = Selector(text=body, type='html')
    prop_dict = self.get_property_dict(localid=tmpid)
    subcategory_id = self.get_category_id(self.get_category_name(pageurl))
    if not prop_dict:
      self.logger_.error('Failed Found Property Dict For: %s' % tmpid)
      return False, None, None
    if not sel:
      self.logger_.error('can not get xpath config for [%r]' % tmpid)
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
    #self._get_xpath_value(sel, prop_dict['__root__'], extract = False)
    if not rootsels:
      self.logger_.error('Failed get root selector data')
      return False, None, None
    self.logger_.debug('Got select url size: %d, for str: %s' % (len(rootsels),
                                                                  rootstr))
    retdicts = []
    assert prop_dict.has_key('__url__') or not prop_dict['__url__'], 'property must contains __url__'
    #rootsels.sort()
    status = False
    try:
      for urls in rootsels:
        if not urls:
          continue
        tmpurl = self._get_xpath_value(urls, prop_dict['__url__'])
        if not tmpurl:
          self.logger_.error('Failed get root url: %s' % (prop_dict['__url__']))
          continue
        url = get_abs_url(pageurl, tmpurl)
        if unique:
          url = self.url_normalize_.get_unique_url(url, scheme='http')
        if not url:
          self.logger_.error('Failed get base url: %s' % (tmpurl[0]))
          continue
        if not self.accept_url(url):
          self.logger_.debug('not accept url[%s]' % (url))
          continue
        url = url.strip()
        #self.info('process: [%s]' % url)
        dicttmp = {}
        # every xpath will match from first to last until ok
        for (p, xps) in prop_dict.items():
          if not p.startswith("__"):
            tmpvl = self._get_xpath_value(urls, xps)
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
    except:
      self.logger_.exception('Failed extend map for: %s', pageurl)
      status = False
    self.logger_.debug('extend_map_size[%d], extract links[%s]' %
                        (len(retdicts), len(returls)))
    #self.put_extend_map(retdicts)
    return status, returls, retdicts

  # extend value {property:value}
  # return status, extend_map_dict
  def extract_custom_map(self, body, localid=None, pageurl=None):
    tmpid = localid or self.__get_localid(pageurl)
    if not tmpid or not body:
      self.logger_.debug('ignore extract custom url: %s %s' % (pageurl, tmpid))
      return False, None
    self.logger_.debug('custom extract ---url: %s' % pageurl or tmpid)
    prop_dict = self.get_custom_property_dict(id=tmpid)
    if not prop_dict:
      self.logger_.error('Failed Found Custom Property Dict For: %s' % tmpid)
      return False, None
    sel = Selector(text=body, type='html')
    if not sel:
      self.logger_.error('can not get xpath config for custom[%r]' % tmpid)
      return False, None
    retdicts = {}
    status = False
    try:
      # every xpath will match from first to last until ok
      for p, xps in prop_dict.items():
        tmpvl = self._get_xpath_value(sel, xps)
        if tmpvl:
          retdicts[p] = tmpvl.strip()
        else:
          self.logger_.debug('Empty [%s]' % (p))
          # end of iner for
      status = True
    except:
      self.logger_.exception('failed extract custom map')
      status = False
    self.logger_.debug('got size[%d]' % len(retdicts))
    #self.put_extend_map(retdicts)
    return status, retdicts

  # return json object include {"cover": "http://kkkkkk", "title": "title""}
  def _gen_json_result(self, dicts):
    if not dicts:
      return None
    try:
      return json.dumps(dicts, ensure_ascii=False).encode('utf8')
    except:
      self.logger_.exception('Convert to json ERROR')
      return None

  def extract_channel_links_map(self, body=None, id=None, pageurl=None, prefix=''):
    if not body:
      return False, None
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.logger_.critical('Failed get localid: %s' % (pageurl))
      return False, {}
    sel = Selector(text=body, type='html')
    channel_dict = self.get_channel_dict(localid=tmpid)
    if not channel_dict:
      self.logger_.error('Failed Found Channel Property Dict For: %s' % tmpid)
      return False, None
    if not sel:
      self.logger_.error('can not get channel xpath config for [%r]' % tmpid)
      return False, None
    rootsels = []
    for rs in channel_dict[prefix + '__root__']:
      rootsels.extend(sel.xpath(rs))
    if not rootsels:
      self.logger_.error('Failed get root selector data')
      return False,None
    retdict = {}
    status = False
    try:
      for urls in rootsels:
        if not urls:
          continue
        tmpurl = self._get_xpath_value(urls, channel_dict[prefix + '__url__'])
        if not tmpurl:
          self.logger_.error('Failed get root url: %s' % (channel_dict[prefix + '__url__']))
          continue
        url = get_abs_url(pageurl, tmpurl)
        if not url:
          self.logger_.error('Failed get base url: %s' % (tmpurl[0]))
          continue
        url = url.strip()
        dicttmp = {}
        channel_xps = channel_dict.get(prefix + 'channel')
        channel = self._get_xpath_value(urls, channel_xps)
        if not channel:
          continue
        channel = channel.strip()
        if channel not in channel_dict.get(prefix + '__select__'):
          continue
        dicttmp['category'] = channel
        retdict[url] = dicttmp
        status = True
    except:
      self.logger_.exception('Failed extract link map for: %s', pageurl)
      status = False
    self.logger_.debug('extend_map_size[%d]' % len(retdict))
    return status, retdict


  def extract_sub_links_list(self, body=None, id=None, pageurl=None, sub_category_num=0):
    if not body:
      return False, False, None
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.logger_.critical('Failed get localid: %s' % (pageurl))
      return False, {}
    sel = Selector(text=body, type='html')
    sub_category_dict = self.get_sub_category_dict(localid=tmpid)
    if not sub_category_dict:
      self.logger_.error('Failed Found sub_category Dict For: %s' % tmpid)
      return False, False, None
    if not sel:
      self.logger_.error('can not get sub_category xpath config for [%r]' % tmpid)
      return False, False, None
    rootsels = []
    for rs in sub_category_dict['__root__']:
      rootsels.extend(sel.xpath(rs))
    if not rootsels:
      self.logger_.error('Failed get sub_category root selector data')
      return True, False, None
      #return False, False, None
    link_list = []
    status = False
    has_sub_category = False
    if sub_category_num >= len(rootsels):
      self.logger_.info('hava no much sub_category [%s]' % pageurl)
      return True, False, None
    elif sub_category_num == len(rootsels)-1:
      has_sub_category = False
    else:
      has_sub_category = True
    sub_sel = rootsels[sub_category_num]

    if sub_category_dict.get('tag', None):
      tag = self._get_xpath_value(sub_sel, sub_category_dict['tag'])
    else:
      tag = ''
    if (not tag or tag.strip()==u'') and (len(rootsels) == 1) :
      tag = 'tags'
    tag = tag.strip()
    tag = tag.strip('：')
    tag = tag.strip(':')
    tag = tag.replace(' ', '')

    except_list = sub_category_dict.get('__except__', None)
    if except_list and tag in except_list:
      link_list.append(pageurl)
      return True, has_sub_category, link_list

    sub_rootsels = []
    for xs in sub_category_dict['__sub_root__']:
      sub_rootsels.extend(sub_sel.xpath(xs))
    status = False
    try:
      for urls in sub_rootsels:
        if not urls:
          continue
        tmpurl = self._get_xpath_value(urls, sub_category_dict['__url__'])
        if not tmpurl:
          self.logger_.error('Failed get root url: %s' % (sub_category_dict['__url__']))
          continue
        url = get_abs_url(pageurl, tmpurl)
        if not url:
          self.logger_.error('Failed get base url: %s' % (tmpurl[0]))
          continue
        url = url.strip()
        link_list.append(url)
        status = True
    except:
      self.logger_.exception('Failed extract link map for: %s', pageurl)
      status = False
    self.logger_.debug('extend_sub_links_list[%d]' % len(link_list))
    return status, has_sub_category, link_list

  def extract_next_url(self, body=None, id=None, pageurl=None):
    if not body:
      return False, None
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.logger_.critical('Failed get localid: %s' % (pageurl))
      return False, {}
    sel = Selector(text=body, type='html')
    next_path = self.get_next_path(localid=tmpid)
    if not next_path:
      self.logger_.debug('failed found next path dict: %s', pageurl)
      return False, None
    if not sel:
      self.logger_.debug('can not get next xpath config: %s', pageurl)
      return False, None
    status = False
    try:
      tmp_url = self._get_xpath_value(sel, next_path)
      if not tmp_url:
        self.logger_.info('has no next page for: [%s]', pageurl)
        return False, None
      next_url = get_abs_url(pageurl, tmp_url)
      #next_url = self.url_normalize_.get_unique_url(next_url, scheme='http')
      next_url = next_url.strip()
      if not next_url:
        self.logger_.error('failed get next url: %s', tmp_url[0])
        return False, None
      status = True
    except:
      self.logger_.exception('failed extract next url for : [%s]', pageurl)
      status = False
    return status, next_url


  def extract_orderlist_map(self, body=None, id=None, pageurl=None):
    if not body:
      return False, None, None
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.logger_.critical('Failed get localid: %s' % (pageurl))
      return False, None, {}
    order_dict = self.get_order_path_dict(localid=tmpid)
    if not order_dict:
      self.logger_.error('Failed Found ordertype path for: %s' % tmpid)
      return False, None, None
    sel = Selector(text=body, type='html')
    retdict = {}
    status = False
    try:
      order_select = self._get_xpath_value(sel, order_dict['order_select'])
      order_select = order_dict.get('order_map', {}).get(order_select, None)
      if not order_select:
        return False, None, None
      order_list = ['time', 'hot']
      for order in order_list:
        if order == order_select:
          continue
        tmp_url = self._get_xpath_value(sel, order_dict.get(order, None))
        if tmp_url:
          tmp_url = get_abs_url(pageurl, tmp_url)
        if tmp_url:
          retdict[order] = tmp_url
      status = True
    except:
      self.logger_.exception('failed extract order list url for: [%s]' % pageurl)
      status = False
    return status, order_select, retdict

  def extract_urls(self, body=None, id=None, pageurl=None, extract_relative=True):
    if not body:
      return False, None
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid:
      self.logger_.critical('Failed get localid: %s' % (pageurl))
      return False, None
    sel = Selector(text=body, type='html')
    ret_urls = []
    if extract_relative:
      href_list = self.get_video_relatives_path(localid=tmpid)
    else:
      href_list = self.get_href_path(localid=tmpid)
    for href in href_list:
      for link in sel.xpath(href):
        if not link:
          continue
        link = link.extract()
        self.logger_.debug('xpath url: %s', link)
        link = get_abs_url(pageurl, link)
        self.logger_.debug('find url: %s', link)
        link = self.url_normalize_.get_unique_url(link, scheme='http')
        if link == pageurl:
          self.logger_.debug('get the same url[%s]', link)
        elif self.accept_url(link):
          ret_urls.append(link)
        else:
          self.logger_.debug('not accept url[%s]', link)
    ret_urls = del_repeat(ret_urls)
    return True, ret_urls


  def assemble_html(self, pageurl, response):
    def assemble_youku_rank_html(pageurl, result_page):
      match = re.search(r'channel/(\d+)/rank/(\d+)', pageurl)
      if not match:
        return result_page
      channel = match.group(1)
      rank = match.group(2)
      api_model = 'http://www.youku.com/u/channelRanking?channel=%s&rank=%s&pn=%s&ajaxget=1'
      for pn in range(2, 200):
        api = api_model % (channel, rank, pn)
        try:
          result = json.loads(FetchHTML(api))
        except:
          self.logger_.exception('Failed load json in api parse func')
          continue
        html = result.get('html', '')
        if not html.strip():
          break
        result_page += ' ' + html
      return result_page

    def assemble_youku_user_video_html(pageurl, result_page):
      api_model = '/fun_ajaxload/?__rt=1&v_page=1&page_num=%s&page_order=1'
      for i in range(2, 200):
        api = api_model % i
        result = FetchHTML(pageurl + api)
        if not result:
          continue
        if result.strip() == '0':
          break
        result_page += ' ' + result
      return result_page

    def assemble_youku_video_album_html(pageurl, result_body):
      sel = Selector(text=result_body, type='html')
      scripts_str = sel.xpath('/html/head/script/text()').extract()
      f = None
      vid = None
      for s in scripts_str:
        match = re.search(r'var videoId.*?(\d+)[\s\S]*?var f.*?(\d+)', s)
        if match:
          vid = match.group(1)
          f = match.group(2)
          break
      if not f or not vid:
        self.logger_.debug('not found f or vid: %s ' % pageurl)
        return result_body
      api_model = 'http://v.youku.com/v_vpvideoplaylistv5?f=%s&vid=%s&pl=50&pn=%s'
      item_ids = sel.xpath('//li[@class="item"]/@id').extract()
      if not item_ids:
        self.logger_.debug('no item_ids: %s ' % pageurl)
        return result_body
      last_id = item_ids[0]
      # as to video album in play page, we try to get 50 * 10 videos maximum
      for pn in range(2, 10):
        next_page = FetchHTML(api_model % (f, vid, pn))
        sel = Selector(text=next_page, type='html')
        item_ids = sel.xpath('//li[@class="item"]/@id').extract()
        if not item_ids:
          continue
        if item_ids[0] == last_id:
          break
        last_id = item_ids[0]
        result_body += ' ' + next_page
      return result_body

    if pageurl.startswith('http://www.youku.com/u/channelRanking'):
      result_body = assemble_youku_rank_html(pageurl, response.body)
    elif pageurl.startswith('http://i.youku.com/u/') and pageurl.endswith('/videos'):
      result_body = assemble_youku_user_video_html(pageurl, response.body)
    elif pageurl.startswith('http://v.youku.com/v_show/'):
      result_body = assemble_youku_video_album_html(pageurl, response.body)
    else:
      return response
    if not result_body:
      return response
    return response.replace(body=result_body)


  def filter_by_page(self, body=None, id=None, pageurl=None):
    tmpid = id or self.__get_localid(pageurl)
    if not tmpid or tmpid != 'toutiao.com':
      return False
    sel = Selector(text=body, type='html')
    xps = self.page_verify[tmpid]
    for xp in xps:
      if sel.xpath(xp):
        return False
    return True


  def api_parse_youku_reletives(self, body, pageurl):
    def fill_video(video):
      video_info = {}
      video_info['url'] = video.get('playLink')
      video_info['poster'] = video.get('picUrl')
      video_info['title'] = video.get('title')
      video_info['play_total'] = atoi(video.get('playAmount'))
      video_info['duration'] = video.get('totalTime')
      return video_info

    api_model = 'http://ykrec.youku.com/show/packed/list.json?vid=%s&sid=%s&apptype=1&pg=%s&module=%s&pl=20'
    sel = Selector(text=body, type='html')
    script_str = sel.xpath('/html/head/script[@type="text/javascript"]/text()').extract()
    if not script_str:
      return True, []

    m = None
    for s in script_str:
      m = re.search('videoId.*?(\d+)[\s\S]*?showid.*?(\d+)', s)
      if m:
        break
    if not m:
      self.logger_.debug('no match for vid and sid', pageurl)
      return True, []
    vid = m.group(1)
    sid = m.group(2)
    if sid == '0':
      pg = 1
      modules = [1]
    else:
      pg = 3
      modules = [1, 9]

    results = []
    for module in modules:
      api = api_model % (vid, sid, pg, module)
      try:
        result = json.loads(FetchHTML(api))
      except:
        self.logger_.exception('Failed load json in api parse func')
        return False, None
      relative_items = result.get('data', [])
      for item in relative_items:
        results.append(fill_video(item))
    if not results:
      self.logger_.debug('no data found', pageurl)
    return True, results


  def api_parse_tudou_reletives(self, body, pageurl):
    def fill_video(video):
      video_info = {}
      video_info['url'] = video.get('playLink')
      video_info['poster'] = video.get('picUrl')
      video_info['title'] = video.get('title')
      play_total = video.get('playAmount')
      if not play_total:
        play_total = video.get('playNum')
      video_info['play_total'] = atoi(play_total)
      video_info['duration'] = video.get('totalTime')
      return video_info

    def fill_list_video(video, lcode):
      video_info = {}
      video_info['url'] = 'http://www.tudou.com/listplay/%s/%s.html' % (lcode, video.get('icode'))
      video_info['poster'] = video.get('pic')
      video_info['title'] = video.get('kw')
      video_info['play_total'] = atoi(video.get('playTimes'))
      video_info['duration'] = video.get('time')
      return video_info

    if not body or not pageurl:
      return True, []

    api_model = None
    re_str = None
    if pageurl.startswith('http://www.tudou.com/listplay/'):
      api_model = 'http://tdrec.youku.com/tjpt/tdrec?encode=utf-8&count=20&pcode=20000200&itemid=%s'
      re_str = r'iid.*?(\d+)'
    elif pageurl.startswith('http://www.tudou.com/albumplay/'):
      api_model = 'http://tdrec.youku.com/tjpt/tdrecshow?encode=utf-8&count=10&scode=%s&pcode=20000502&req_type=3'
      re_str = r"lcode.*?'(.*?)'"
    elif pageurl.startswith('http://www.tudou.com/programs/'):
      api_model = 'http://tdrec.youku.com/tjpt/tdrec?encode=utf-8&count=20&pcode=20000300&itemid=%s'
      re_str = r'iid.*?(\d+)'
    if not api_model:
      return True, []

    sel = Selector(text=body, type='html')
    script_str = sel.xpath('/html/body/script/text()').extract()
    if not script_str:
      return True, []
    m = None
    for s in script_str:
      m = re.search(re_str, s)
      if m:
        break
    if not m:
      return True, []
    api = api_model % m.group(1)

    results = []
    try:
      result = json.loads(FetchHTML(api))
    except:
      self.logger_.exception('Failed load json in api parse func')
      return False, None
    relative_items = result.get('recommendItems', [])
    for item in relative_items:
      results.append(fill_video(item))

    if pageurl.startswith('http://www.tudou.com/listplay/'):
      lcode = re.search(r'listplay/(.*?)(/|\.)', pageurl)
      if lcode:
        lcode = lcode.group(1)
      try:
        result = json.loads(FetchHTML('http://www.tudou.com/crp/plist.action?lcode=%s' % lcode))
      except:
        self.logger_.exception('Failed load json in api parse func')
      list_items = result.get('items', [])
      for item in list_items:
        results.append(fill_list_video(item, lcode))

    return True, results


  def api_parse_sohu_relative(self, body=None, url=None):
    def fill_video(video):
      video_info = {}
      video_info['url'] = video.get('pageUrl')
      video_info['poster'] = video.get('largePicUrl')
      video_info['title'] = video.get('name')
      video_info['duration'] = str(video.get('playLength'))
      video_info['showtime'] = video.get('publishTime')
      return video_info
    if not body or not url:
      self.logger_.error('no body or no url, body : %(body)s, url : %(url)s' % {'body': body, 'url': url})
      return True, []
    if url.startswith('http://tv.sohu.com/'):
      api_relative = "http://pl.hd.sohu.com/videolist?playlistid=%s&o_playlistId=&vid=%s&pagesize=1000"
    elif url.startswith('http://my.tv.sohu.com/play/'):
      api_relative = "http://my.tv.sohu.com/play/getvideolist.do?callback4&playlistid=%s&pagesize=1000&vid=%s"
    else:
      self.logger_.info("url : %(url)s does not startwith (http://tv.sohu.com/) or (http://my.tv.sohu.com/play/)" % {'url': url})
      return False, []

    #get playlistid and vid
    #url example: http://tv.sohu.com/20151023/n423988637.shtml
    #url example: http://my.tv.sohu.com/pl/9034514/81702404.shtml
    playlistid = re.findall('.*?playlistId[=\'\" ]*(\d+)', body)
    vid = re.findall('var vid="(\d+)', body)
    if playlistid and vid:
      playlistid = playlistid[0]
      vid = vid[0]
    else:
      self.logger_.exception('playlistid : %(playlistid)s, vid : %(vid)s' % {'playlistid': playlistid, 'vid': vid})
      return False, []

    results = []
    api = api_relative %(playlistid, vid)
    result_videos = FetchHTML(api)
    try:
      result_videos = json.loads(result_videos)
    except:
      self.logger_.exception('get videos fail of sohu, failed url is %(url)s' % {'url': api})
      return False, results
    for video in result_videos.get("videos", []):
      if video:
        results.append(fill_video(video))
    return True, results


  def api_parse_qq_sports_nba_teamvideo(self, body=None, pageurl=None):
    def fill_video(video):
      video_info = {}
      video_info['url'] = video.get('playUrl')
      video_info['poster'] = video.get('pic')
      video_info['title'] = video.get('title')
      video_info['duration'] = video.get('duration')
      video_info['play_total'] = atoi(video.get('view'))
      video_info['showtime'] = video.get('checkUpTime')
      return video_info

    if not body or not pageurl:
      return True, []
    api_team = "http://sportswebapi.qq.com/sportsVideo/team?callback=json&teamId=allTeams&competitionId=100000"
    api_match = "http://sportswebapi.qq.com/sportWeb/nbaTeamInfo?callback=json&teamId=%s&needVideo=1"

    results = []
    result_teams = FetchHTML(api_team).lstrip("json(").rstrip(");")
    try:
      result_teams = json.loads(result_teams)
    except:
      self.logger_.exception('Failed load team json in qq_nba_team api parse func')
      return True, results

    if len(result_teams) > 1:
      for item in result_teams[1]:
        team_id = item.get("teamId", "")
        if not team_id:
          continue
        api = api_match % (team_id)
        result_matches = FetchHTML(api).lstrip("json(").rstrip(")")
        try:
          result_matches = json.loads(result_matches)
        except:
          self.logger_.exception('Failed load match json in nab_team_video api parse func')
          continue
        if 'data' in result_matches and result_matches['data']:
          for video in result_matches['data'].get('videos', []):
            results.append(fill_video(video))
        else:
           self.logger_.exception('no data in match api in api parse func')
           continue
    else:
      self.logger_.exception('no data in team api in api parse func')
    return True,results

  def get_qq_sports_idlist(self, url):
    result = FetchHTML(url).lstrip("QZOutputJson=").rstrip(";")
    result_idlist = list()
    try:
      result = json.loads(result)
    except:
      self.logger_.exception("Fail get qq sports idlist in func")
      return result_idlist
    for item in result.get('data',[]):
      video_id = item.get('video_id')
      if video_id:
        result_idlist.append(video_id)
    return result_idlist

  def api_parse_qq_sports_ogyc(self, body=None, pageurl=None):
    def fill_video(video):
      video_info = {}
      video_info['url'] = video.get('c_play_url')
      video_info['poster'] = video.get('c_pic_496_280')
      video_info['title'] = video.get('c_title')
      return video_info

    if not body or not pageurl:
      return True, []
    results = []
    result_idlist = []
    sel = Selector(text=body, type='html')
    video_tabs = sel.xpath('//div[contains(@class, "mod_classicvideo")]//li/@data-name').extract()
    video_tab_api = 'http://v.qq.com/commurl/json/%s/%s.json'
    #get idlist
    for video_tab in video_tabs:
      if pageurl == 'http://sports.qq.com/video/og/':
        api_idlist = video_tab_api %('og', video_tab)
      else:
        api_idlist = video_tab_api %('yc', video_tab)
      result_idlist.extend(self.get_qq_sports_idlist(api_idlist))

    api_match = "http://data.video.qq.com/fcgi-bin/data?tid=146&idlist=%s&appid=10001009&appkey=c5a3e1529a7ba805&otype=json&callback=json"
    if not result_idlist:
      self.logger_.exception("get idlist fail in func:api_parse_qq_sports_ogyc")
      return False, None
    for item in result_idlist:
      match = api_match % (item)
      try:
        result_matches = FetchHTML(match).lstrip("json(").rstrip(")")
      except:
        self.logger_.exception('fetch html faile, url is %(url)s' %{'url' : match})
        continue
      try:
        if isinstance(result_matches, unicode):
          result_matches = result_matches.encode('utf8', 'ignore')
        result_matches = json.loads(result_matches)
      except:
        self.logger_.exception('Fail load match json in video api parse func')
        continue
      for item in result_matches.get("results", []):
        video = item.get("fields")
        if video:
          results.append(fill_video(video))
    return True, results


  def api_parse_qq_sports_home(self, body=None, pageurl=None):
    def fill_video(video, start_time=None):
      video_info = {}
      video_info['url'] = video.get('url')
      video_info['poster'] = video.get('pic')
      video_info['title'] = video.get('title')
      video_info['showtime'] = start_time
      return video_info

    if not body or not pageurl:
      return True, []

    api_team = 'http://sportswebapi.qq.com/sportsVideo/team?teamId=allTeams&competitionId=%s'
    api_match = 'http://sportswebapi.qq.com/sportsVideo/team?teamId=%s&competitionId=%s'
    sel = Selector(text=body, type='html')
    comptIds = sel.xpath('//div[@class="mod_schedule"]/div[@class="mod_types"]/ul/li/@data-competitionid').extract()

    results = []
    for cid in comptIds:
      api = api_team % cid
      result_teams = FetchHTML(api)
      try:
        result_teams = json.loads(result_teams)
      except:
        self.logger_.exception('Failed load json in api parse func')
        continue
      for item in result_teams[1]:
        teamId = item.get('teamId', '')
        if not teamId:
          continue
        api = api_match % (teamId, cid)
        result_matches = FetchHTML(api)
        try:
          result_matches = json.loads(result_matches)
        except:
          self.logger_.exception('Failed load json in api parse func')
          continue
        for group in result_matches[1]:
          for video in group.get('video', []):
            results.append(fill_video(video, group.get('startTime')))
          for cover in group.get('cover', []):
            results.append(fill_video(cover, group.get('startTime')))
    return True, results


  def api_parse_toutiao_user(self, body, pageurl):
    def fill_user(user):
      user_info = {}
      user_info['user_name'] = [user.get('name', None)]
      user_info['user_channel_desc'] = [user.get('description', None)]
      user_info['user_portrait'] = [user.get('icon', None)]
      user_info['user_fans_num'] = [user.get('subscribe_count', None)]
      user_info['user_url'] = [user.get('share_url', None)]
      return user_info
#find video dict and fill user
    try:
      result = json.loads(body)
    except:
      self.logger_.exception('url: %s json load fail', pageurl)
      return False, []
    results = []
    for data in result.get('data', {}):
      if data and data.get('name') == '视频':
        results.extend(fill_user(item) for item in data.get('list', []))
        break
    return True, results


  def parse_api(self, body, pageurl, list_page=False):
    id = pageurl if list_page else self.__get_localid(pageurl)
    if not id:
      self.logger_.critical('Failed get localid: %s' % (pageurl))
      return False, None
    func_name = self.api_parse_func.get(id, None)
    if not func_name:
      return True, []
    try:
      func = eval('ExtraExtendMapEngine.' + func_name)
      return func(self, body, pageurl)
    except:
      self.logger_.exception('api parse exception!')
      return False, None


  def extract_users(self, pageurl, body):
      if not body:
        return False, None
# parse api (eg toutiao)
      if 'snssdk.com' in pageurl:
        tmpid = pageurl
        if self.api_parse_func.get(tmpid):
          return self.parse_api(body, pageurl, True)

      tmpid = self.__get_localid(pageurl)
      user_path_dict = self.user_list_path.get(tmpid, {})
      if not user_path_dict:
        return True, []
      sel = Selector(text=body, type='html')
      user_urls = []
      postfix = user_path_dict.get('__postfix__', [])
      for href in user_path_dict.get('__url__', []):
        for link in sel.xpath(href):
          link = get_abs_url(pageurl, link.extract())
          link = self.url_normalize_.get_unique_url(link, scheme='http')
          for pf in postfix:
            user_urls.append(link + pf)
      return True, user_urls


if __name__ == '__main__':
  print 'tst:'
