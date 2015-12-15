#!/usr/bin/python
# coding=utf-8

from static_extractor import StaticExtractor
import sys

class SinaStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        'http://news.sina.com.cn/zxt/.*',
        'http://news.video.sina.com.cn/*',
        'http://sports.video.sina.com.cn/*',
        'http://video.sina.com.cn/topic/'
    ]

    self._web_name = 'sina.com.cn'

