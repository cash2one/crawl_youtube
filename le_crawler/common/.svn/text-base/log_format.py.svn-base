#!/usr/bin/python
#-*-coding:utf8-*-
#
# Copyright 2015 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
"""
this pipeline using for fetch content from html
"""
from scrapy.logformatter import LogFormatter
from scrapy import log

DROPPEDFMT = u"Dropped: %(exception)s"

class LetvLogFormatter(LogFormatter):
  def dropped(self, item, exception, response, spider):
    return {
        'level': log.WARNING,
        'format': DROPPEDFMT,
        'exception': exception,
        }
