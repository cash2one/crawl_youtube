#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'


# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
def _crawler_path_HTTPClientParser_statusReceived():
  """
  for monkey patching for scrapy.xlib.tx._newclient.HTTPClientParser.statusReceived
  fix status is not enogh 3 parts, some times not reason, but 
  So the reason phrase should be there but at the same time the RFC says "The
  client is not required to examine or display the Reason-Phrase."
  """
  print '============using HTTPClientParser pathing======================'
  from scrapy.xlib.tx._newclient import HTTPClientParser, ParseError
  old_sr = HTTPClientParser.statusReceived
  def statusReceived(self, status):
    try:
      return old_sr(self, status)
    except ParseError, e:
      if e.args[0] == 'wrong number of parts':
        return old_sr(self, status + ' OK')
      raise
  statusReceived.__doc__ = old_sr.__doc__
  HTTPClientParser.statusReceived = statusReceived
_crawler_path_HTTPClientParser_statusReceived()





