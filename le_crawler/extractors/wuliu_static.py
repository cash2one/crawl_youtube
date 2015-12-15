#!/usr/bin/python
# coding=utf-8
from static_extractor import StaticExtractor
import sys


class WuliuStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        'http:\/\/video\.56\.com\/wolelist.*',
    ]


    self._invalid_category.extend(['全部'])

    self._web_name = '56.com'

