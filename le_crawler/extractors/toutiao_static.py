#!/usr/bin/python

from static_extractor import StaticExtractor

class ToutiaoStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
      r'http://toutiao\.com/articles.+',
      r'http://toutiao\.com/m\d+'
    ]

    self._web_name = 'toutiao.com'
