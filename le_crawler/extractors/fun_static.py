#!/usr/bin/python
# coding=utf-8

from static_extractor import StaticExtractor
import sys

class FunStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        '.*www\.fun\.tv\/retrieve\/.*',
    ]

    self._invalid_category.append('微电影')
    self._web_name = 'fun.tv'

