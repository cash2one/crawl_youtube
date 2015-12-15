#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'
"""
this module should be improve after times
this module is templora way
"""

class PhoneWallPaperExtractor(object):
  def __init__(self, spider, *kargs, **kwargs):
    self.wallpaper_cache = {}
    self.spider = spider
    self.phone_w = 1440
    self.phone_h = 2560
  # return {'items':[], 'requests' : []}

  def __parser_lovebizhi_page(self, jbody):
    # prepare request
    items = []
    requests = set()
    category_name = ''
    if type(jbody) is list:
      for l in jbody:
        if 'url' in l:
          requests.add(l.get('url'))
    else:
      if 'browse' in jbody:
        for i in jbody['browse']:
          requests.add(i['api'])
      if 'url' in jbody and type(jbody['url']) is dict:
        for k, v in jbody['url'].items():
          requests.add(v)
      if 'link' in jbody and 'next' in jbody['link']:
        requests.add(jbody['link']['next'])
      if 'tags' in jbody and type(jbody['tags']) is list:
        for t in jbody['tags']:
          if 'url' in t:
            requests.add(t['url'])
      # prepare items
      category_name = jbody.get('name')
      if 'data' in jbody and type(jbody['data']) is list:
        for d in jbody['data']:
          if 'tags' in d and type(d['tags']) is list:
            for t in d['tags']:
              if 'url' in t:
                requests.add(t['url'])
          if 'detail' in d:
            requests.add(d.get('detail'))
          if 'image' in d:
            img_url = None
            if 'vip_original' in d['image']:
              img_url = d['image']['vip_original']
            elif 'original' in d['image']:
              img_url = d['image']['original']
            elif 'big' in d['image']:
              img_url = d['image']['big']
            if img_url:
              items.append({'url' : img_url})
    return {'items' : items, 'requests' : list(requests), 'category' : category_name}

  def __parser_sogou_page(self, jbody):
    items = []
    requests = set()
    category_name = ''
    def __cate_info_parse(cateinfo):
      retids = set()
      for i in cateinfo:
        if 'cate_id' in i:
          retids.add(i.get('cate_id'))
      return list(retids)

    if type(jbody) is dict:
      cate_ids = __cate_info_parse(jbody.get('cate_info1', []) +
          jbody.get('cate_info2', []))
      requests.update(self.__build_sogou_url('cate_info', cate_ids))
      if 'hotsearch' in jbody:
        category_name = 'hotsearch'
        for i in self.__build_sogou_url('image_url', [x.get('id', '') for x in
          jbody.get('hotsearch', {}).get('hotsearch', []) if x ]):
          items.append({'url' : i})
      if 'wallpaper' in jbody:
          for i in jbody['wallpaper']:
            if 'aa' in i:
              items.extend(
                  [{'url' : x } for x in
                    self.__build_sogou_url('image_url', [i.get('aa')])])
      if 'tab' in jbody:
        cateids = []
        for i in jbody['tab'].get('tabs', []):
          if 'first_name' in i and not category_name:
            category_name = i.get('first_name', None)
          if 'cate_id' in i:
            cateids.append(i.get('cate_id'))
        requests.update(self.__build_sogou_url('cate_info', cateids))
      if 'label_name' in jbody:
        category_name = jbody.get('label_name')
      if 'banner' in jbody and 'item' in jbody['banner']:
        requests.update(self.__build_sogou_url('search_url', [x.get('searchkey',
          '') for x in jbody['banner'].get('item', []) if x]))

    return {'items' : items,
        'requests' : list(requests),
        'category' : category_name}

  def __build_sogou_url(self, urltype, ids):
    if 'cate_info' == urltype:
      return [
        'http://download.android.bizhi.sogou.com/list_1.2.php?'
            'cate_id=%s&p=1&w=1440&h=2560&v=2.3.0.0024'
            '&dv=4.3&dn=vivo+Xplay3S&dr=1440x2560'
            '&r=0022-0022&j=380feabd6ab1673b79b749fb933126a4'
            '&i=f371d41256476857f8bef1cb77fb7f57&n=WIFI' % (x)
            for x in ids if x]
    elif 'image_url' == urltype:
      return [
        'http://download.android.bizhi.sogou.com/download_1.1.php?'
            'id=%s&w=1440&h=2560&v=2.3.0.0024&dv=4.3'
            '&dn=vivo+Xplay3S&dr=1440x2560&r=0022-0022'
            '&j=380feabd6ab1673b79b749fb933126a4'
            '&i=f371d41256476857f8bef1cb77fb7f57&n=WIFI' % (x)
            for x in ids if x]
    elif 'search_url' == urltype:
      import urllib2
      qws = [ urllib2.quote(x.encode('utf8')) for x in ids]
      return [
          'http://so.bizhi.sogou.com/androidquery'
              '?word=%s'
              '&w=1440&h=2560&v=2.3.0.0024&dv=4.3&dn=vivo+Xplay3S'
              '&dr=1440x2560&r=0022-0022&j=380feabd6ab1673b79b749fb933126a4'
              '&i=f371d41256476857f8bef1cb77fb7f57&n=WIFI' % (x)
              for x in qws if x]

  def parser_entery_info(self, url, body):
    try:
      import json
      j = json.loads(''.join(body.split()))
      if 'lovebizhi.com' in  url:
        return self.__parser_lovebizhi_page(j)
      elif 'sogou.com' in url:
        return self.__parser_sogou_page(j)
    except Exception, e:
      import traceback
      print traceback.format_exc()
      print e, url, body
      return {}
