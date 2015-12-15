# coding=utf-8

"""convert between python value and lxml.etree so that lxml's power can be applied to json data.
In particular, xpath queries can be run against json.
"""

import types
from lxml import etree

type_map = dict(
  int=int,
  unicode=unicode,
  NoneType=lambda x: None,
  list=list,
  bool=bool,
  str=str,
)


def element(k, v):
  # key, val --> etree.Element(key)
  node = etree.Element(k)
  if isinstance(v, dict):
    for ck, cv in v.items():
      node.append(element(ck, cv))
  elif isinstance(v, (int, float, bool, basestring, types.NoneType)):  # scalar
    node.set('type', type(v).__name__)
    node.text = unicode(v)
  elif isinstance(v, list):
    node.set('type', type(v).__name__)  # list xx this could be done across the board.
    for i, cv in enumerate(v):
      node.append(element("_list_element_%d" % i, cv))
  else:
    assert False, type(v)
  return node


def value(e):
  # etree.Element --> value
  if not hasattr(e, 'getchildren'):
    return unicode(e)
  children = e.getchildren()
  type_ = e.get('type')
  if children:
    if not type_:  # xx defaults dict
      return dict((c.tag.decode('utf8'), value(c)) for c in children)
    elif type_ == 'list':
      return [value(c) for c in children]
    else:
      raise TypeError('unexpected type', type_)

  # convert it back to the right python type
  ctor = type_map[type_]
  return ctor(e.text)


def xpath(val, xpath_str):
  for node in element('root', val).xpath(xpath_str):
    yield value(node)


if __name__ == '__main__':
  s = u"""
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
    "description": "" }] """
  import json
  s = json.loads(s)
  for i in xpath(s, '//docType/text()'):
    print i
  for i in xpath(s, '//source/text()'):
    print i

  s = u'''
{"subjects":[{"rate":"7.7","cover_x":328,"is_beetle_subject":false,"title":"稻田里的人们","url":"http:\/\/movie.douban.com\/subject\/1441906\/","playable":false,"cover":"http:\/\/img6.douban.com\/lpic\/s1635543.jpg","id":"1441906","cover_y":475,"is_new":false},{"rate":"8.4","cover_x":500,"is_beetle_subject":false,"title":"克鲁伯","url":"http:\/\/movie.douban.com\/subject\/1418091\/","playable":false,"cover":"http:\/\/img6.douban.com\/view\/movie_poster_cover\/lpst\/public\/p863236557.jpg","id":"1418091","cover_y":710,"is_new":false},{"rate":"7.7","cover_x":2025,"is_beetle_subject":false,"title":"影子大亨","url":"http:\/\/movie.douban.com\/subject\/1295227\/","playable":true,"cover":"http:\/\/img6.douban.com\/view\/movie_poster_cover\/lpst\/public\/p2203787782.jpg","id":"1295227","cover_y":3000,"is_new":false},{"rate":"8.8","cover_x":624,"is_beetle_subject":false,"title":"语词，语词，语词","url":"http:\/\/movie.douban.com\/subject\/1906051\/","playable":false,"cover":"http:\/\/img6.douban.com\/lpic\/s3927116.jpg","id":"1906051","cover_y":881,"is_new":false}]}
'''
  s = json.loads(s)
  for i in xpath(s, '//subjects//url/text()'):
    print i