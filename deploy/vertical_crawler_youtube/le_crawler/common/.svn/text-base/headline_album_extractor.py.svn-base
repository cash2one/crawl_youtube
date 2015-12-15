#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
"""
  this class using for video album crawl for headline video
"""

import sys
import re
import threading
import md5

from scrapy.settings import CrawlerSettings
from le_crawler.base.logutil import Log
from le_crawler.base.url_normalize import UrlNormalize
from le_crawler.common.extend_map_handler import ExtendMapHandler
from le_crawler.base.url_filter import UrlFilter
from le_crawler.base.url_domain_parser import query_domain_from_url


class PageType(object):
  ENTER_PAGES = 0x123
  ALBUM_INFO_PAGES = 0X124
  ALBUM_PAGES = 0X125

class HeadLineAlbumExtractor(object):
  _instance = None
  _instance_lock = threading.Lock()
  @staticmethod
  def get_instance(
      start_url_loader,
      setting_module_path = 'le_crawler.common.headline_album_settings',
      *kargs,
      **kwargs):
    HeadLineAlbumExtractor._instance_lock.acquire()
    if not HeadLineAlbumExtractor._instance:
      loger = Log('album_crawler', '../log/album_crawler.log')
      HeadLineAlbumExtractor._instance = \
      HeadLineAlbumExtractor(start_url_loader,
          loger,
          setting_module_path,
          *kargs,
          **kwargs)
    HeadLineAlbumExtractor._instance_lock.release()
    return HeadLineAlbumExtractor._instance

  def __init__(self,
      start_url_loader,
      loger,
      setting_module_path = 'le_crawler.common.headline_album_settings',
      *kargs,
      **kwargs):
    __import__(setting_module_path)
    self.__settings = CrawlerSettings(settings_module
        = sys.modules[setting_module_path])
    self.loger = loger
    # {album_id, {}}
    self.album_ids = {}
    self.__init_regs()
    self.__extend_map_handler = kwargs['extend_map_handler'] if \
    kwargs.has_key('extend_map_handler') else None
    if kwargs.has_key('extract_setting'):
      self.__extend_map_handler = \
      ExtendMapHandler.get_instance(start_url_loader,
          kwargs['extract_setting'])
    else:
      self.__extend_map_handler =\
          ExtendMapHandler.get_instance(start_url_loader)
    self.__url_normalize = UrlNormalize.get_instance()
    self.album_infos = {}
    self.url_filter = UrlFilter().get_instance()

  def get_category_id(self, refer_url):
    ca = self.__get_category_name(refer_url)
    if 'joke' == ca:
      return 109
    elif 'ent' == ca:
      return 104
    else:
      return -1

  def __get_category_name(self, refer_url):
    return self.__extend_map_handler.settings.get_category_name(refer_url)\
        if self.__extend_map_handler  else 'UNKONWN_CATEGORY'

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

  def __get_global_albumid(self, localid, site_album_id):
    url = self.global_albumid_reg[localid].replace('(*albumid*)', site_album_id)
    from le_crawler.core.docid_generator import gen_docid
    return gen_docid(url)

  def __get_localid(self, url):
    return query_domain_from_url(url) or self.url_filter.get_domain_from_url(url)
  # deprecated: using above
  #def __get_localid(self, url):
  #  for r in self.local_id_reg:
  #    sg = r.search(url)
  #    if not sg:
  #      continue
  #    g = sg.groups()
  #    if g:
  #      return g[0]
  #  return None

  def __parser_urls(self, sels):
    returls = []
    for urls in sels.xpath('//a'):
      for attr in self.href_tags:
        u = urls.xpath('./@%s' % attr)
        if u:
          returls.append(u.extract()[0].encode('utf8'))
    return returls

  # return [idlist]
  def __get_site_album_id(self, localid, urls):
    retlist = set()
    for u in urls:
      for r in self.album_id_match_regs[localid]:
        sg = r.search(u)
        if sg:
          g = sg.groups()
          if g:
            retlist.add(g[0])
            break
    return list(retlist)

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

  def get_global_albumid_by_refer(self, refer_url):
    if self.album_ids.has_key(refer_url):
      return self.album_ids[refer_url]
    else:
      print 'Error: can not found global id:', refer_url

  # return description
  # dict = {'enter_page': [], 'album_pages':[], 'album_infos_pages' : []}
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
    self.__extend_map_handler.settings.add_start_urls(albumurls)
    return albumurls

  # input enter page
  # return album info pages
  def parser_album_info_pages(self, body, url, refer_url):
    sta = False
    albumid = self.get_global_albumid_by_refer(url)
    if not self.album_infos.has_key(albumid):
      sta, items = self.__extend_map_handler.settings.extract_custom_map(
          body = body,
          pageurl = url)
      if not sta:
        return []
      cateid = self.get_category_id(refer_url)
      self.album_infos[albumid] = items
      self.album_infos[albumid]['album_cid'] = cateid
      self.album_infos[albumid]['album_id'] = albumid
      self.album_infos[albumid]['album_url'] = \
        self.__url_normalize.get_unique_url(url)
    # second extract urls
    status, extend_url = self.__extend_map_handler.extract_extend_map(body = body,
        pageurl = url, ignore_empty_property = True)
    if status:
      ldict = self.__extend_map_handler.get_inlink_location_dict()
      if not ldict.has_key(extend_url[0]):
        self.loger.log.error('Failed found inlink location for %s' %
            extend_url[0])
        assert False, 'Failed found inlink location, %s' %  extend_url[0]
      else:
        locationstr = ldict[extend_url[0]]
      self.album_infos[albumid].setdefault('album_vids', {})[locationstr] = \
            [self._get_store_key(i) for i in extend_url]
      video_url = extend_url[0] if extend_url else None
      album_pic = self.__extend_map_handler.lookup_extend_map(video_url, type
          = 'dict')['cover']\
          if video_url and \
          self.__extend_map_handler.lookup_extend_map(video_url, type = 'dict')\
              and self.__extend_map_handler.lookup_extend_map(video_url, type
                  = 'dict').has_key('cover') else None
      if album_pic:
        self.album_infos[albumid]['album_pic'] = album_pic

    return extend_url
  #Note: this docid should same as today_tv_writer
  def _get_store_key(self, url):
    return md5.new(url).hexdigest()

  def parser_enter_page(self, url, sels):
    glbid = self.get_global_albumid_by_refer(url)
    if not glbid:
      return

  def parser_ablum_pages(self, sels):
    pass

  def ignore_crawl_link(self, url):
    return self.__extend_map_handler.settings.ignore_link_to_crawler(url)

  def get_album_info(self, albumid):
    return self.album_infos[albumid] \
        if self.album_infos.has_key(albumid) else {}

  def get_album_infos(self):
    return self.album_infos

  def debug_album_infos(self):
    for k, v in self.album_infos.items():
      print '-------', 'albuminfo', '-------'
      for k1, v1 in v.items():
        print k1, v1
