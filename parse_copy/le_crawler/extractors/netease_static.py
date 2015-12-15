#!/usr/bin/python
# coding=utf-8

from static_extractor import StaticExtractor
import sys

class NeteaseStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        'http://v.163.com/hot.*',
    ]

    self._web_name = '163.com'

