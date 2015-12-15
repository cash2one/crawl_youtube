#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# this class inherited from singleton
import os
import re
import sys
import urllib
import urlparse

"""
for video searching, we need distinct one video page by it's url
but, some unnecessary include some param, but some need:
eg: http://a.b.c/test.html?vid=12444&other=vaddfs#frag
eg: http://a.b.c/test.html?sourceid=234&vid=12444&other=vaddfs#frag
"""


def is_valid_url(url):
  return bool(re.match(r'^https?:/{2}\w.+$', url))


def get_abs_url(base_url, test_url, canonicalize=False):
  """
    reture full accessable url, base root url
    # eg:
    # base_url : 'http://ent.qq.com/a/b/c'
    # test_url : 'http://ent.qq.com/a/b/c1.html'
    # test_url : '/a/b/c1.html'
    # test_url : '../c1.html''
    # all will return "http://ent.qq.com/a/b/c1.html"

    # url parse
    @staticmethod
    # input http://a.b/dc/htm.html;par?ksj&ddk
    # return http://a.b/dc/htm.html
  """
  if not test_url:
    return None
  test_url = test_url.strip()
  if is_valid_url(test_url):
    return test_url
  purl = urlparse.urlparse(base_url.strip())
  if not purl:
    return None
  nsc = purl.scheme
  nnetl = purl.netloc
  npth = purl.path
  if not npth:
    npth = '/'
  npth = os.path.dirname(npth)
  if test_url.startswith("./") or test_url.startswith("../"):
    npth = os.path.join(npth, test_url)
    npth = os.path.abspath(npth)
  else:
    npth = os.path.join(npth, test_url)
  nurl = urlparse.urlunparse((nsc, nnetl,
                              npth,
                              '',
                              '',
                              ''))
  if canonicalize:
    from scrapy.utils.url import canonicalize_url

    return canonicalize_url(nurl)
  return nurl


# static class define
class UrlNormalize():
  # def init_onece(self, *args, **kwargs):
  import threading

  _instance = {}
  _instance_lock = threading.Lock()

  @staticmethod
  def get_instance(module_path='le_crawler.common.url_normalize_settings',
                   *kargs, **kwargs):
    UrlNormalize._instance_lock.acquire()
    if not UrlNormalize._instance.has_key(module_path):
      UrlNormalize._instance[module_path] = UrlNormalize(module_path)
    UrlNormalize._instance_lock.release()
    return UrlNormalize._instance[module_path]

  def __init__(self, module_path, *kargs, **kwargs):
    self._load_settings(module_path)

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

  def get_mapping_id(self, url=None, domain=None):
    # first mapping domain
    if self.__id_mapping_domain.has_key(domain):
      return self.__id_mapping_domain(domain)
    # second try match reg
    return self.__accept_reg(self.__id_mapping_reg, url)

  def __set_query_dict(self, org_dict, id):
    if org_dict is None or id is None:
      return {}
    domain_k_p = self.__get_keep_query_lst(id)
    retdict = {}
    for (k, ef) in domain_k_p:
      if org_dict.has_key(k) and org_dict[k] != '':
        retdict[k] = org_dict[k]
      elif ef:
        retdict[k] = ''
    return retdict

  def __join_query(self, inputd):
    return urllib.urlencode([(k, v[0]) for k, v in inputd.items() if v])

  def _load_settings(self, module_path):
    __import__(module_path)
    self.__id_mapping_reg = self.__convert_map_regs(getattr(sys.modules[module_path], 'ID_MAPPING_REG'))
    self.__id_mapping_domain = self.__convert_map_regs(getattr(sys.modules[module_path], 'ID_MAPPING_DOMAIN'))
    self.__keep_query = getattr(sys.modules[module_path], 'KEEP_QUERY')
    self.__keep_fragments = getattr(sys.modules[module_path], 'KEEP_FRAGEMENT')
    self.__extra_para = getattr(sys.modules[module_path], 'ADD_EXTRA_PARA')

  def get_unique_url(self,
                     url,
                     scheme=None,
                     netloc=None,
                     domain=None,
                     no_conf_no_oper=False):
    id = self.get_mapping_id(url=url, domain=domain)
    if id is None:
      if not no_conf_no_oper:
        id = 'DEFAULT'
      else:
        return url
    if id is None or url is None:
      raise Exception('Failed get mapping id for: %s, %s' % (domain, url))
    urlp = urlparse.urlsplit(url.strip())
    if not urlp:
      raise Exception('Failed convert urlparse %s' % url)
    frgment = urlp.fragment if self.__keep_fragment(id) else ''
    nscheme = urlp.scheme or scheme
    nnetloc = urlp.netloc or netloc
    qdict = urlparse.parse_qs(urlp.query)
    fqdict = self.__set_query_dict(qdict, id)
    self.__update_paras_with_extra(fqdict, id)
    nquery = self.__join_query(fqdict)
    return urlparse.urlunsplit((nscheme, nnetloc, urlp.path, nquery,
                                frgment)).strip()


if __name__ == '__main__':
  print 'test...'
  test_url = get_abs_url('http://www.fun.tv/retrieve/c-e7baaae5bd95e78987/',
                         '/vplay/v-3194641/')
  assert test_url == 'http://www.fun.tv/vplay/v-3194641/', test_url
  test_url = get_abs_url('http://v.qq.com/ent/latest/all_1.html',
                         '/cover/j/jk9eis9j54nmuaa.html')
  assert test_url == 'http://v.qq.com/cover/j/jk9eis9j54nmuaa.html', test_url
  test_url = get_abs_url('http://top.baidu.com/buzz?b=342&fr=topdetail_b1_c513',
                         './detail?b=342&c=513&w=%C6%BB%B9%FB%B7%A2%B2%BC%BB%E1')
  assert test_url == 'http://top.baidu.com/detail?b=342&c=513&w=%C6%BB%B9%FB%B7%A2%B2%BC%BB%E1'
  un = UrlNormalize.get_instance('url_normalize_settings')
  output = un.get_unique_url('http://www.iqiyi.com/v_19rrn8rzbs.html#vfrm=2-4-0-1')
  assert output == 'http://www.iqiyi.com/v_19rrn8rzbs.html', output
  output = un.get_unique_url('http://google.com/test.html;12445#fadk?k1=v1&k2=v2')
  assert output == 'http://google.com/test.html;12445', output
  output = un.get_unique_url('http://google.com/test.html;12445#fadk?k1=v1&k2=v2',
                             no_conf_no_oper=True)
  assert output == 'http://google.com/test.html;12445#fadk?k1=v1&k2=v2', output
  output = un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg')
  assert output == 'http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg', output
  output = un.get_unique_url("http://iphone.myzaker.com/zaker/article_telecom.php?app_id=1&for=lephone")
  assert output == 'http://iphone.myzaker.com/zaker/article_telecom.php?app_id=1&for=lephone', output
  print 'Ok'
