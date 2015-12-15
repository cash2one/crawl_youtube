#!/usr/bin/python
# coding=utf-8

from static_extractor import StaticExtractor
import sys

class YoukuStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
      'http:\/\/www\.youku\.com\/v_showlist\/.*',
    ]

    self._invalid_category.extend(['全部','教育',])
    self._web_name = 'youku.com'

