#!/usr/bin/env python
#-*-coding:utf8-*-
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import json

class JsonPathList(object):
  def __init__(self, json_path, path_list):
    self.jpath_list = json_path
    self.path_list = path_list

  def Jpath(self, path_list):
    pass


class JsonPath(object):
  @staticmethod
  def get_json_path(jstr, encoding = None):
    return JsonPath(json.loads(jstr, encoding = encoding), [])

  def __init__(self, jobj, path, encoding = None):
    self.jobj = jobj
    self.path = path

  def __str__(self):
    return '<%s> %s' % ('.'.join(self.path), self.jobj)

  def __iter__(self):
    if isinstance(self.jobj, list):
      for i in self.jobj:
        yield JsonPath(i, self.path)
    elif isinstance(self.jobj, dict):
      yield self

  def Jpath(self, path_list):
    if isinstance(path_list, list):
      return self._jpath(path_list)
    elif isinstance(path_list, str):
      return self._jpath([x for x in path_list.split('/') if x])

  def _jpath(self, path_list):
    if not path_list:
      return self
    result = []
    if isinstance(self.jobj, list):
      for i in self.jobj:
        tmppath = JsonPath(i, self.path).Jpath(path_list)
        result.append(tmppath.jobj)
      return JsonPath(result, path_list)
    elif isinstance(self.jobj, dict) and path_list[0] in self.jobj:
      return JsonPath(self.jobj[path_list[0]], [path_list[0]]).Jpath(path_list[1:])
    else:
      return None


  def extract(self):
    return self.jobj

if __name__ == '__main__':
  testo = '''{"store": {"book": [{"category": "reference", "price": 8.95, "title":
  "Sayings of the Century", "author": "Nigel Rees"}, {"category": "fiction",
  "price": 12.99, "title": "Sword of Honour", "author": "Evelyn Waugh"},
  {"category": "fiction", "price": 8.99, "title": "Moby Dick", "isbn":
  "0-553-21311-3", "author": "Herman Melville"}, {"category": "fiction",
  "price": 22.99, "title": "The Lord of the Rings", "isbn": "0-395-19395-8",
  "author": "J. R. R. Tolkien"}], "bicycle": {"color": "red", "price": 19.95}}}
  '''
  jp = JsonPath.get_json_path(testo)
  print jp
  print '------------------>[store]'
  print 'store', jp.Jpath(['store'])
  print '------------------>'
  print 'store.category', jp.Jpath(['store', 'category'])
  print '------------------>'
  print 'store.book.category', jp.Jpath(['store', 'book', 'category'])
  print '------------------>'
  print 'store.book', jp.Jpath(['store', 'book',])
  print '------------------>'
  for i in jp.Jpath(['store', 'book', 'title']):
    print i
  for i in jp.Jpath(['store', 'book']):
    print '*' * 10
    print 'Title', i.Jpath(['title']).extract()
    print 'Category', i.Jpath(['category']).extract()
    print 'Price', i.Jpath(['price']).extract()
    print 'Author', i.Jpath(['author']).extract()

  jp = JsonPath.get_json_path("""
  [ {
     "docType": "doc",
     "title": "邹铭任民政部副部长|简历",
     "putDate": 1421658383,
     "source": "中国经济网",
     "aid": "94917189",
     "contentLink":
     "http://i.ifeng.com/news/news?ch=boya_news&aid=94917189&mid=673HXG&vt=5",
     "thumbnailPic":
     "http://y3.ifengimg.com/ifengimcp/pic/20150119/30dd2a160a8c44f73687_size15_w357_h255.jpg",
     "description": ""
     },
     { "docType": "doc",
    "title": "东莞一富豪被撤政协委员资格 曾办“小姐阅兵”",
    "putDate": 1421658178,
    "source": "南方都市报",
    "aid": "94917266",
    "contentLink": "http://i.ifeng.com/news/news?ch=boya_news&aid=94917266&mid=673HXG&vt=5",
    "thumbnailPic": "http://y3.ifengimg.com/ifengimcp/pic/20150119/b8c807ebca14875b57fa_size59_w449_h321.jpg",
    "description": "" }] """)
  for i in jp.Jpath("/"):
    print '-' * 10
    print i.Jpath('title').extract()
    print i.Jpath('source').extract()
    print i.Jpath('contentLink').extract()
