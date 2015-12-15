#!/usr/bin/python
# coding=utf-8

from static_extractor import StaticExtractor
import sys

class PeopleStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        'http://tv.people.com.cn/GB/.*',
    ]

    self._invalid_category.extend(['首页','时政','访谈','微视频'])
    self._web_name = 'people.com.cn'

