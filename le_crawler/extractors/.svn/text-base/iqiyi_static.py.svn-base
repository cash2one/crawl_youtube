#!/usr/bin/python
# coding=utf-8
from static_extractor import StaticExtractor
import sys


class IqiyiStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        'http:\/\/list\.iqiyi\.com\/.*',
    ]


    self._invalid_category.extend(['教育','少儿','旅游','母婴','脱口秀'])

    self._web_name = 'iqiyi.com'

