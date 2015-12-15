#!/usr/bin/python
# coding=utf-8

from static_extractor import StaticExtractor
import sys

class PPTVStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
      'http://list.pptv.com.*',
    ]

    self._invalid_category.extend(['VIP尊享','亲子'])
    self._web_name = 'pptv.com'

