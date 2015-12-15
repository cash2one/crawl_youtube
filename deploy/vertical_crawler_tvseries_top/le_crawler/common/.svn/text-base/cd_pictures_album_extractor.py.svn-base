#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'
"""
this module should be improve after times
this module is templora way
"""
from scrapy import log
from le_crawler.base.timestr_parser import TimestrParser
from le_crawler.core.extra_extend_map_engine import ExtraExtendMapEngine

class CdPicturesAlbumExtractor(object):
  def __init__(self, spider, *kargs, **kwargs):
    # this album_infos contains url to dict
    self.album_infos = {}
    self.spider = spider
    self.timep = TimestrParser()
    self.qq_js_post = ['hdBigPic.js', 'hdPic.js', 'hdBigPic.js']
    import re
    self.qq_aritcle_time_reg = \
    re.compile(r'\.qq\.com\/.*\/(\d+)\/\d+.htm')
    self.links_extractor =\
        ExtraExtendMapEngine('le_crawler.common.cdesktop_settings', None, None)

  # return album_request_urls
  def _parser_sina_album_list(self, jsobj):
    albumurls = []
    for alb in jsobj:
      ch = alb.get('ch')
      aid = alb.get('aid')
      sid = alb.get('sid')
      cover = alb.get('img')
      album_desc = alb.get('summary')
      album_url = alb.get('url')
      album_name = alb.get('name')
      if not ch or not aid or not sid or not album_url:
        self.spider.log('Bad Album Info, %s' % (alb), log.ERROR)
        continue
      request_url =\
      'http://photo.sina.cn/aj/album?action=image&ch=%s&sid=%s&aid=%s&w=360&h=487&wm=&dpr=4'\
      %(ch, sid, aid)
      albumurls.append(request_url)
      self.album_infos[request_url] = {'title' : album_name,
          'rawurl': cover,
          'content_body' : [album_desc],
          'url' : album_url
          }
    self.spider.log('extract %s album infos' % (len(albumurls)), log.INFO)
    return {'requests' : albumurls}

  def __is_album_exist(self, album_url):
    return False

  # return the item dict
  def _parser_sina_album_info(self, jsobj, request_url):
    imgs = []
    # this can get img title but, this time we ignored
    source_type = '新浪娱乐讯'
    for alb in jsobj:
      imgurl = alb.get('picurl')
      #imgurl = alb.get('original')
      if not imgurl:
        continue
      imgs.append(imgurl)
    if not imgs:
      return ()
    albuminfo = self.album_infos.get(request_url)
    if not albuminfo:
      return ()
    retalbuminfo = {}
    retalbuminfo['content_imgs'] = imgs
    retalbuminfo.update(albuminfo)
    #retalbuminfo['item_type'] = 'picture'
    retalbuminfo['source_type'] = source_type
    self.album_infos.pop(request_url)
    return {'items': [retalbuminfo]}
 
  def _parser_sohu_album_info(self, jsobj):
    albums = jsobj.get('group_list')
    if not albums:
      return {}
    retalbuminfos = []
    for alb in albums:
      comment_num = alb.get('cmt_count') if 'cmt_count' in alb else '0'
      article_time_raw = alb.get('create_time')
      imglistobj = alb.get('img')
      title = ''
      content_body = ''
      imgs = []
      urlid = alb.get('id')
      for i in imglistobj:
        if not title:
          title = i.get('title')
        if not content_body:
          content_body = i.get('desc')
        tmpimg = i.get('source')
        if tmpimg:
          imgs.append(tmpimg)
      if not urlid or not imgs:
        self.spider.log('Bad Album Info:%s' % (alb), log.ERROR)
        continue
      url = 'http://m.sohu.com/p/%s/' % (urlid)
      if self.__is_album_exist(url):
        continue
      retalbuminfos.append({
        'url' : url,
        'title' : title,
        'content_body' : [content_body],
        'content_imgs' : imgs,
        'article_time_raw' : article_time_raw,
        'source_type'  :  '搜狐娱乐讯',
        'comment_num' : comment_num,
        #'item_type' : 'picture'
        })
    return {'items' : retalbuminfos}

  def _parser_qq_album_list_page(self, body, url):
    status, urlexts, propertyl =\
        self.links_extractor.extract_extend_map(body, pageurl = url)
    
    property = {}
    if not status:
      self.spider.log('Failed extract body links', log.ERROR)
      return {}
    else:
      for p in propertyl:
        property[p[0]] = p[1]
    request_urls = []
    for url in urlexts:
      # this may hdBigPic.js
      import random
      requ = url.replace('htm', random.choice(self.qq_js_post))
      request_urls.append(requ)
      times = self.qq_aritcle_time_reg.search(url).groups('')[0]
      article_time_raw = None
      if len(times) == 8:
        article_time_raw = times[0:4] + '-' + times[4:6] + '-' + times[6:8]
      if times > '20140101':
        article_time_raw = property.get('article_time_raw', article_time_raw)
      if article_time_raw:
        article_time_raw = article_time_raw.replace(' ', ' ')
        self.album_infos.setdefault(url, {})['article_time_raw']\
            =  article_time_raw
      #self.album_infos.setdefault(url, {})['url'] = url

    return {'requests' : request_urls}

  def _extract_qq_value(self, itemjson, keys, retdict):
    for k in keys:
      tmplist = retdict.setdefault(k, [])
      if itemjson.has_key('Name') and itemjson['Name'] == k:
        if itemjson.has_key('Children'):
          for c in itemjson['Children']:
            if c.has_key('Content') and c['Content']:
              if c['Content'] not in tmplist:
                tmplist.append(c['Content'])
  
  def _extract_qq_json(self, json_object, get_keys, retdict):
    self._extract_qq_value(json_object, get_keys, retdict)
    if json_object.has_key('Children'):
      for c in json_object['Children']:
        self._extract_qq_json(c, get_keys, retdict)

  def refactory_qq_request_url(self, rawlurl):
    if 'qq.com' not in rawlurl:
      return None
    nurl = None
    if 'hdPic.js' in rawlurl:
      nurl = rawlurl.replace('hdPic', 'hdBigPic')
    elif 'hdBigPic' in rawlurl:
      nurl = rawlurl.replace('hdBigPic', 'hdPic')
    else:
      return None
    self.spider.log('refactory qq url:%s, %s' %(rawlurl, nurl), log.INFO)
    return nurl

  def _parser_qq_album_info(self, body, url, content_type):
    if 'application/x-javascript' not in content_type:
      self.spider.log('Bad qq js page content:%s, %s' % (body, content_type),
          log.ERROR)
      return {}
    tmpdict = {}
    bidx = body.find('{')
    eidx = body.rfind('}')
    jstr = body[bidx : eidx + 1]
    import json
    try:
      self._extract_qq_json(json.loads(jstr.replace('\'', '\"')),
        ['bigimgurl', 'cnt_article', 'bottom_content',], tmpdict)
      content_imgs = tmpdict.get('bigimgurl')
      content_body = tmpdict.get('bottom_content')
      if not content_body:
        content_body = tmpdict.get('cnt_article')
      album_key = url.replace('hdBigPic.js', 'htm').replace('hdPic.js', 'htm')
      # refactory result items
      cached_res = self.album_infos.get(album_key)
      if not cached_res:
        self.spider.log('Failed found album dict for:%s' % (album_key), log.ERROR)
        return {}
      res = {}
      res.update(cached_res)
      res['content_imgs'] = content_imgs
      #res['content_body'] = content_body  #this content type is list
      res['page'] = ''.join(content_body)  
      # dispath this content to content extract pipeline to process, remove tag
      res['source_type'] = '腾讯娱乐讯'
      res['url'] = album_key
      #res['item_type'] = 'picture'
      return  {'items' : [res]}
    except Exception, e:
      import traceback
      print traceback.format_exc()
      self.spider.log('Bad content body:%s' % (url), log.ERROR)
      return {}
  # return elec_dict, urls
  def parser_album_list_page(self, url, body):
    import json
    if 'sina.cn' in url:
      return self._parser_sina_album_list(json.loads(body))
    elif 'm.sohu.com' in url:
      return self._parser_sohu_album_info(json.loads(body))
    elif 'qq.com' in url:
      return self._parser_qq_album_list_page(body, url)
    else:
      self.spider.log('Unsupport Type: %s' % url, log.ERROR)
      return {}

  # return item need words
  def parser_album_info_pages(self, url, body, content_type = 'html'):
    if 'sina.cn' in url:
      import json
      j = json.loads(body)
      return self._parser_sina_album_info(j, url)
    elif 'ent.qq.com' in url:
      return self._parser_qq_album_info(body, url, content_type)
    else:
      self.spider.log('Unsupport Album Info Type:%s' % url, log.ERROR)
      return {}
