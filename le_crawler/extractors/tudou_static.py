#!/usr/bin/python
# coding=utf-8

from static_extractor import StaticExtractor
import sys

# 土豆大部分的信息都是api请求的，albumplay的页面有类似youku的类别网址，但programs、listplay都没有
# 因此没有爬去albumplay的source元素，而是通过head中有个irCategory来过滤长视频
class TudouStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
      'http:\/\/www\.tudou\.com\/list\/.*'
    ]

    self._invalid_category.extend(['全部','纪实','教育'])
    self._web_name = 'tudou.com'

