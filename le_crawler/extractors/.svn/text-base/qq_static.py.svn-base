#!/usr/bin/python
#coding=utf-8
import sys
from static_extractor import StaticExtractor

class QQStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        'http:\/\/v\.qq\.com\/\w+\/list.*',
        'http:\/\/v\.qq\.com\/mvlist.*', # MV
        'http:\/\/v\.qq\.com\/\w+\/latest.*',
        ]

    self._web_name = 'qq.com'

