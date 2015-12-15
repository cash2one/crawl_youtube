#!/usr/bin/python
# coding=utf-8

from static_extractor import StaticExtractor
import sys

class SokuStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)

    self._lists = [
      'http:\/\/www\.soku\.com\.*'
    ]

    self._web_name = 'soku.com'

