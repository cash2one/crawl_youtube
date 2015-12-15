#!/usr/bin/python
# coding=utf-8

from static_extractor import StaticExtractor
import sys

class VOneStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
      '.*?v1.cn/?$',
    ]

    self._invalid_category.extend(['首页','购物','秀场','游戏','V1圈','微电影','专题','公益'])
    self._web_name = 'v1.cn'

