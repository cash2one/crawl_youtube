#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for some site need discovery id then spell the final web page
the first we make this pipeline need three step
"""
import re

class LinksDiscovery(object):
  def __init__(self):
    pass

  def __parser_urls(self, sels):
    returls = []
    for urls in sels.xpath('//a'):
      for attr in self.href_tags:
        u = urls.xpath('./@%s' % attr)
        if u:
          returls.append(u.extract()[0].encode('utf8'))
    return returls

  def __init_regs(self):
    # load glob id url reg
    self.local_id_reg = []
    for r in self.__settings.getlist('LOCAL_ID_REG', []):
      self.local_id_reg.append(re.compile(r, re.I | re.S))
    # load album id url
    self.album_id_match_regs = {}
    for k, v in self.__settings.getdict('ALBUM_ID_URL', {}).items():
      for r in v:
        self.album_id_match_regs.setdefault(k, []).append(re.compile(r, re.I |
          re.S))
    # load extend url dict
    self.extend_album_pages = self.__settings.getdict('ALBUM_PAGE_URL', {})
    # load global album id reg
    self.global_albumid_reg = self.__settings.getdict('GLOBAL_ALBUMID_REG', {})

    # href tags
    self.href_tags = self.__settings.getlist('HREF_TAGs', [])
    self.loger.log.info('load href url tags: %s' % len(self.href_tags))


   # return album video urls
  def __get_album_pags(self, localid, idlist, refer_url):
    returls = []
    category = self.__get_category_name(refer_url)
    postfix = ' %s|channel' % category
    if self.extend_album_pages.has_key(localid):
      for pageurl in self.extend_album_pages[localid]:
        for id in idlist:
          glid = self.__get_global_albumid(localid, id)
          strtmp = pageurl.replace('(*albumid*)', id).replace('(*pagenum*)',
              '(*)') + postfix
          from le_crawler.base.url_extend import extend_url
          sta, extedurls = extend_url(strtmp, '1', '8', 0)
          if not sta:
            continue
          for eu in extedurls:
            # preprocess url
            self.album_ids[eu.split(' ')[0]] = glid
          returls.extend(extedurls)
    return returls


  def parser_enter(self, url, pages):
    localid = self.__get_localid(url)
    if not localid:
      return []
    from scrapy.selector import Selector
    sel = Selector(text = pages, type = 'html')
    if not sel:
      return []
    urls = self.__parser_urls(sel)
    albumids = self.__get_site_album_id(localid, urls)
    albumurls = self.__get_album_pags(localid, albumids, url)
    # hock start urls to extend_map_handler
    return albumurls
