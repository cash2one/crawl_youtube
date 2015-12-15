#!/usr/bin/python
# coding=utf-8

import sys
from static_extractor import StaticExtractor

class SohuStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
      'http:\/\/so\.tv\.sohu\.com\/list_.*',
    ]

    self._invalid_category.extend(['精选', '纪录片','明星','出品人'])

    self._web_name = 'sohu.com'

