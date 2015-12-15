#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for spider picture from some mobile site
for cdesktop project templore
"""
import threading
import os
import json

from le_crawler.base.url_extend import extend_url_en
"""
upgrade start url loader, by this module
starurl define line like:
  { "content" : [
    {"url" : [
       "http://example.com"
       ],
     "type" : "list",
     "category" : "",
     "subcategory" : "",
     "enable" : true
    }
   ]
  }
"""

class StartUrlsLoader(object):
  _instance = {}
  _instance_lock = threading.Lock()

  @staticmethod
  def get_instance(start_url_path, random_sort = False, *kargs, **kwargs):
    StartUrlsLoader._instance_lock.acquire()
    singleton_id = start_url_path
    if singleton_id not in StartUrlsLoader._instance:
      StartUrlsLoader._instance[singleton_id] =\
          StartUrlsLoader(start_url_path, random_sort, *kargs, **kwargs)
    StartUrlsLoader._instance_lock.release()
    return StartUrlsLoader._instance[singleton_id]

  def __init__(self, filepath, random_sort, *kargs, **kwargs):
    #url -> (id, inlink_location)
    self._id_map = {}
    #id -> property
    self.url_property = {}
    self.__load_urlf(filepath, random_sort)

  def __load_urls(self, starturldict, oper_type, random_sort = False):
    body_j = starturldict
    for line in body_j.get('content', []):
      j = line
      if not j.get('enable', True):
        continue
      if 'url' not in j or 'id' not in j:
        raise Exception('url/id needed!%s' % line)
      id = j.get('id')
      if id not in self.url_property or oper_type == 'overwrite':
        self.url_property[id] = j.copy()
        self.url_property[id].pop('url')
      elif oper_type == 'merg':
        self.url_property[id].update(j.copy())
        self.url_property[id].pop('url')
      else:
        raise Exception('%s already used with type:%s' % (id, oper_type))

      for u in j.get('url', []):
        exus = extend_url_en(u + ' ', add_num_tail = True)
        if not exus:
            raise Exception('Failed extend urls: %s' % u)
        for l in exus:
          tmpurls = l.split()
          if not tmpurls:
            continue
          url = tmpurls[0]
          page_num = 0
          if len(tmpurls) >= 2:
            page_num = tmpurls[1].split('|')[-1]
          self._id_map[url] = (id, page_num)

  def __load_urlf(self, fpath, random_sort = False):
    if not fpath or not os.path.exists(fpath):
      return []
    flist = []
    if os.path.isfile(fpath):
      flist.append(fpath)
    else:
      flist = [os.path.join(fpath, f) for f in os.listdir(fpath) ]
    from url_filter import UrlFilter
    for f in flist:
      tmplines = ''.join(UrlFilter.load_lines(f))
      body_j = json.loads(tmplines)
      self.__load_urls(body_j, 'merg')

  def load_start_urlf(self, fpath, random_sort = False):
    self.__load_urlf(fpath)

  def add_start_urls(self, sdict, random_sort = False, oper_type = 'merg'):
    self.__load_urls(sdict, oper_type, random_sort)

  def get_start_urls(self):
     return self._id_map.keys()

  def ignore_crawl_extract_links(self, referer_url):
    id = self._id_map.get(referer_url, None)
    return True if id and\
        self.url_property.get(id).get('type', '') != 'list' else False

  def get_url_page_num(self, url):
    return self._id_map.get(url, (-1, -1))[1]

  def get_property(self, url, word, default_value = None):
    id = self._id_map.get(url, (-1, -1))[0]
    return  self.url_property.get(id, {}).get(word, default_value)
