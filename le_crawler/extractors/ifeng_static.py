#!/usr/bin/python
#coding=utf-8
from static_extractor import StaticExtractor
import sys

class IfengStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
        'http://v.ifeng.com/vlist'
        ]

    self._invalid_category.extend(['全部','原创','凤凰台','专题'])

    self._web_name = 'ifeng.com'

