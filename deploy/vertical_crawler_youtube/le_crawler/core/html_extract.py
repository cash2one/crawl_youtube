#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
import re
import json
import traceback

from scrapy.selector import Selector

from le_crawler.core.base_extract import BaseExtractor
from le_crawler.base.url_normalize import get_abs_url
from le_crawler.core.base_extract import ExtractLinks

class HtmlExtractor(BaseExtractor):
  def __init__(self, settings, loger, *kargs, **kwargs):
    super(HtmlExtractor, self).__init__(settings, loger, *kargs, **kwargs)
    self.__init_setting()
   
  def __init_setting(self):
    assert self.settings
    self.subcategory_id_ = self.settings.getdict('SUBCATEGORY_ID', {})
    if not self.subcategory_id_:
      self.loger.log.error('Error loading Category ID Mapping')

    self.ignore_extend_map_lost_reg = [ re.compile(x) for x in
        self.settings.getlist('IGNORE_EXTEND_REG', []) if x]
    self.tbl_n_ = self.settings.getdict('TABLE_NAME', {})
    if not self.tbl_n_:
      self.loger.log.error('Error loading table name')

  def get_id_from_referer(self, referer_url):
    return self.get_localid(referer_url)
  
  def get_location_from_referer(self, referer_url):
    return self.start_url_loader.get_url_page_num(referer_url)

  
  def ignore_extend_map_miss(self, url):
    for r in self.ignore_extend_map_lost_reg:
      if r.search(url):
        return True
    return False
  
  def get_property_dict(self, url = None, localid = None, bd_type = 'html'):
    tmpid = localid or self.get_localid(url)
    if tmpid in self.property_path:
      return self.property_path[tmpid]

  # get custome map dict
  def get_custom_property_dict(self, url = None, id = None):
    tmpid = id or self.get_localid(url)
    return self.custom_property_path.get(tmpid, None)

  def get_table_name(self, url = None, id = None):
    tmpid = id or self.get_localid(url)
    if self.table_name_dict.has_key(tmpid):
      return self.table_name_dict[tmpid]
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
    sctype = self.start_url_loader.get_property(referer_url, 'type', None)
    if not sctype:
      self.loger.log.error('Failed Found start url type')
      return False
    if sctype.lower() != 'list':
      return True
    return False

  def extract_block_links(self, url, body, bd_type, filter):
    if not body:
      return False, []
    tmpid = self.get_localid(url)
    if not tmpid:
      self.loger.log.critical('Failed get localid: %s' % (url))
      return False, []
    self.loger.log.info('Begin Extract URL: %s %s' % (url, tmpid))
    return self._extract_extend_map(body, id = tmpid, pageurl = url,
        bd_type = bd_type, filter = filter) 

  def extract_custom_links(self, url, body, bd_type):
    return self._extract_custom_map(body = body,
        pageurl = url, bd_type = bd_type)

  def _extract_extend_map(self, body, id = None, pageurl = None, bd_type =
      'html', filter = True):
    returls = []
    tmpid = id
    sel = Selector(text = body, type = bd_type)
    prop_dict = self.get_property_dict(localid = tmpid)
    subcategory_id = self.get_category_id(self.get_category_name(pageurl))
    if not prop_dict:
      self.loger.log.error('Failed Found Property Dict For: %s' % tmpid)
      return False, None
    if not sel:
      self.loger.log.error('can not get xpath config for [%r]'% tmpid)
      return False, None
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
      return False ,None
    self.loger.log.info('Got select url size: %d, for str: %s' % (len(rootsels),
      rootstr))
    retdicts = []
    assert prop_dict.has_key('__url__') or not prop_dict['__url__'], 'property must contains __url__'
    #rootsels.sort()
    status = False 
    item_type = self.get_request_type_from_start_url(pageurl)
    try:
      for urls in rootsels:
        if not urls:
          continue
        tmpurl = self.__get_xpath_value(urls, prop_dict['__url__'])
        if not tmpurl:
          self.loger.log.error('Failed get root url: %s' % (prop_dict['__url__']))
          continue
        url = get_abs_url(pageurl, tmpurl)
        url = self.url_normalize.get_unique_url(url, scheme = 'http')
        if not url:
          self.loger.log.error('Failed get base url: %s' % (tmpurl[0]))
          continue
        if filter and not self.accept_url(url):
          self.loger.log.info('not accept url[%s]' % (url))
          continue
        url = url.strip()
        #self.info('process: [%s]' % url)
        dicttmp = {}
        # every xpath will match from first to last until ok
        #item_type = prop_dict.get('__itemtype__', None)
        for (p, xps) in prop_dict.items():
          if not p.startswith("__"):
            #print 'property:', p, xps
            tmpvl = self.__get_xpath_value(urls, xps)
            if tmpvl:
              dicttmp[p] = tmpvl.strip()
              if p == 'cover': # img url, eed do full path process
                dicttmp[p] = get_abs_url(pageurl, dicttmp[p])
            # end of iner for
        link = ExtractLinks()
        link.url = url
        link.item_type = item_type
        if dicttmp:
          if subcategory_id:
            dicttmp['sid'] = '%s' % subcategory_id
          link.extend_map = dicttmp
        returls.append(link)
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
    return status, returls 

  # extend value {property:value}
  # return status, extend_map_dict
  def _extract_custom_map(self, body, localid = None, pageurl = None,
      bd_type = 'html'):
    tmpid = localid or self.get_localid(pageurl)
    if not tmpid or not body:
      self.loger.log.info('ignore extract custom url: %s %s' % (pageurl, tmpid))
      return False, [] 
    self.loger.log.debug('custom extract ---url: %s' % pageurl or tmpid)
    prop_dict = self.get_custom_property_dict(id = tmpid)
    if not prop_dict:
      self.loger.log.error('Failed Found Custom Property Dict For: %s' % tmpid)
      return False, []
    sel = Selector(text = body, type = 'html')
    if not sel:
      self.loger.log.error('can not get xpath config for custom[%r]'% tmpid)
      return False, None
    link = ExtractLinks()
    link.extend_map = {}
    link.item_type = ExtractLinks.ITEM_ITEM
    link.url = pageurl
    status = False 
    try:
        # every xpath will match from first to last until ok
        for (p, xps) in prop_dict.items():
          tmpvl = self.__get_xpath_value(sel, xps)
          if tmpvl:
            link.extend_map[p] = tmpvl.strip()
          else:
            self.loger.log.debug('Empty [%s]' % (p))
            # end of iner for
        status = True
    except Exception, e:
      print e
      print traceback.format_exc()
      self.loger.log.error('exception for:%s, %s' %(e.message,
        traceback.format_exc()))
      status = False
    self.loger.log.debug('Got Size[%d]' % len(link.extend_map))
    #self.put_extend_map(retdicts)
    return status, link 

  # return json object include {"cover": "http://kkkkkk", "title": "title""}
  def _gen_json_result(self, dicts):
    if not dicts:
      return None
    try:
      return json.dumps(dicts, ensure_ascii = False).encode('utf8')
    except Exception, e:
      self.loger.log.error('Convert to json ERROR [%s]' % (e.message))
      return None
  def get_category_id(self, category_name):
    if category_name is None:
      return None
    if self.subcategory_id_.has_key(category_name):
      return self.subcategory_id_[category_name]

  def get_category_name(self, url):
    return self.start_url_loader.get_property(url, 'category', None)

if __name__ == '__main__':
  print 'tst:'
