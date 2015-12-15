#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

from le_crawler.core.base_extract import BaseExtractor
from le_crawler.core.json_path import JsonPath
from le_crawler.core.base_extract import ExtractLinks

class JsonExtractor(BaseExtractor):
  def __init__(self, settings, loger, *kargs, **kwargs):
    super(JsonExtractor, self).__init__(settings, loger, *kargs, **kwargs)

  def _get_jpath_value(self, jsel, prolist):
    for p in prolist:
      v = jsel.Jpath(p)
      if v:
        return v.extract()
    return None

  def extract_block_links(self, url, body, bd_type, filter): 
    localid = self.get_localid(url)
    if not localid:
      self.loger.log.error('Failed get localid for %s' % (url))
      return False, None
    prop_dict = self.json_property_path.get(localid, None)
    if not prop_dict:
      self.loger.log.error('Failed get property dict for %s %s' % (url, localid))
      return False, None
    rootsels = []
    sel = JsonPath.get_json_path(body)
    for rs in prop_dict['__root__']:
      jtmp = sel.Jpath(rs)
      if jtmp:
        rootsels.extend(jtmp)
    if not rootsels:
      self.loger.log.error('Failed get root selector data')
      return False ,None
    returls = []
    item_type = self.get_request_type_from_start_url(url)
    for blk in rootsels:
      tmpurl = self._get_jpath_value(blk, prop_dict['__url__'])
      if not tmpurl:
        self.loger.log.error('Failed Found __url__ Property for data')
        continue
      url = self.url_normalize.get_unique_url(tmpurl, scheme = 'http')
      if not url:
        self.loger.log.error('Failed get base url: %s' % (tmpurl))
        continue
      if filter and not self.accept_url(url):
        self.loger.log.info('not accept url[%s]' % (url))
        continue
        url = url.strip()
      link = ExtractLinks()
      link.url = url
      link.item_type = item_type
      tmpdict = {}
      for k, v in prop_dict.items():
        if k.startswith('__'):
          continue
        if not v:
          continue
        tmpv = self._get_jpath_value(blk, v)
        if tmpv:
          tmpdict[k] = tmpv
      if tmpdict:
        link.extend_map = tmpdict
      returls.append(link)
    return True, returls

  def extract_custom_links(self, url, body, bd_type): 
    pass
