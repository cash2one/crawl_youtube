#!/usr/bin/python
# coding=utf-8
from static_extractor import StaticExtractor
import sys


class WasuStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        '.*all\.wasu\.cn\/index.*',
    ]


    self._invalid_category.extend(['收费','教育','求索','直播','全部','微电影'])

    self._web_name = 'wasu.cn'

