#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# this class inherited from singleton
import sys
import re
import urlparse

from scrapy.settings import CrawlerSettings 

"""
for video searching, we need distinct one video page by it's url
but, some unnecessary include some param, but some need:
eg: http://a.b.c/test.html?vid=12444&other=vaddfs#frag
eg: http://a.b.c/test.html?sourceid=234&vid=12444&other=vaddfs#frag
"""

class UrlNormalize():
  #def init_onece(self, *args, **kwargs):
  def __init__(self, module_path = 'le_crawler.base.url_normalize_settings'):
    module_path = module_path
    __import__(module_path)
    self.__settings = CrawlerSettings(settings_module = sys.modules[module_path])
    self.__load_settings()

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

  def __accept_reg(self, id_reglist, item):
    if not item:
      return None
    for (id, tmpres) in id_reglist.items():
      for r in tmpres:
        if r.search(item):
          return id
    return None

  def __get_keep_para_list(self, mapdict, id):
    if mapdict.has_key(id):
      return mapdict[id]
    return []

  def __get_keep_query_lst(self, id):
    return self.__get_keep_para_list(self.__keep_query, id)

  def __keep_fragment(self, id):
    if not self.__keep_fragments or not self.__keep_fragments.has_key(id):
      return False
    return self.__keep_fragments[id]
  def __update_paras_with_extra(self, input_dict, id):
    if not self.__extra_para.has_key(id):
      return input_dict
    input_dict.update(self.__extra_para[id])

  def get_mapping_id(self, url = None, domain = None):
    # first mapping domain
    if self.__id_mapping_domain.has_key(domain):
      return self.__id_mapping_domain(domain)
    # second try match reg
    return self.__accept_reg(self.__id_mapping_reg, url)

  def __set_query_dict(self, org_dict, id):
    if org_dict is None or id is None:
      return {}
    domain_k_p = self.__get_keep_query_lst(id)
    retdict = {} for (k,ef) in domain_k_p:
      if org_dict.has_key(k) and org_dict[k] != '':
        retdict[k] = org_dict[k]
      elif ef:
        retdict[k] = ''
    return retdict

  def __join_query(self, inputd):
    if not inputd:
      return ''
    query_str = None
    reslist = sorted(inputd.items(), key = lambda d: d[0], reverse = True)
    for (k, v) in reslist:
      if query_str:
        query_str += '&%s=%s' % (k, v[0])
      query_str = '%s=%s' % (k, v[0])
    return query_str

  def __load_settings(self):
    self.__id_mapping_reg = self.__convert_map_regs(self.__settings.getdict('ID_MAPPING_REG', {}))
    self.__id_mapping_domain = self.__convert_map_regs(self.__settings.getdict('ID_MAPPING_DOMAIN', {}))
    self.__keep_query = self.__settings.getdict('KEEP_QUERY', {})
    self.__keep_fragments = self.__settings.getdict('KEEP_FRAGEMENT', {})
    self.__extra_para = self.__settings.getdict('ADD_EXTRA_PARA', {})

  def get_unique_url(self,
      url,
      scheme = None,
      netloc = None,
      domain = None,
      no_conf_no_oper = False):
    id = self.get_mapping_id(url = url, domain = domain)
    if id is None:
      if not no_conf_no_oper:
        id = 'DEFAULT'
      else:
        return url
    if id is None or url is None:
      raise Exception('Failed get mapping id for: %s, %s' % (domain, url))
    urlp = urlparse.urlsplit(url.strip(), allow_fragments =
        self.__keep_fragment(id))
    if not urlp:
      raise Exception('Failed convert urlparse %s' % url)
    nscheme = urlp.scheme or scheme
    nnetloc = urlp.netloc or netloc
    qdict = urlparse.parse_qs(urlp.query)
    fqdict = self.__set_query_dict(qdict, id)
    self.__update_paras_with_extra(fqdict, id)
    nquery = self.__join_query(fqdict)
    return urlparse.urlunsplit((nscheme, nnetloc, urlp.path, nquery,
      urlp.fragment)).strip()

if __name__ == '__main__':
  un = UrlNormalize()
  print un.get_unique_url('http://google.com/test.html;12445#fadk?k1=v1&k2=v2')
  print un.get_unique_url('http://google.com/test.html;12445#fadk?k1=v1&k2=v2',
      no_conf_no_oper = True)
  print un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg')
  print un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg&nonokey=nonvalue')
  print un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?id=w0015xnrgrg&nonokey=nonvalue')
  print un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?nonokey=nonvalue&vid=w0015xnrgrg')
