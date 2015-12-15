#!/usr/bin/python
# coding=utf-8
from static_extractor import StaticExtractor
import sys

class CztvStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        'http:\/\/me\.cztv\.com\/video-list.*',
    ]

    self._invalid_category.remove('综艺')

    self._web_name = 'cztv.com'

