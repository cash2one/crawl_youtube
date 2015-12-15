#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import sys
sys.path.append('/letv/workspace/search2/crawler_ver2/pycrawler')
from base.thrift_util import thrift_to_str
from base.thrift_util import str_to_thrift
from base.thrift_util import thrift_to_debug_str
from genpy.crawl.ttypes import CrawlDoc, Request, CrawlDocType, Response

def creat_crawldoc():
  crawldoc = CrawlDoc()
  crawldoc.request = Request()
  crawldoc.request.url = 'http://baidu.com'
  crawldoc.request.header = 'header....'
  crawldoc.response = Response()
  crawldoc.response.url = 'http://helloworld.com'
  crawldoc.response.return_code = 200
  crawldoc.docid = 19999;
  crawldoc.doctype = CrawlDocType.REQUESTDOC
  return crawldoc


def test_thrift():
  crawldoc1 = creat_crawldoc()
  crawldoc2 = creat_crawldoc()
  assert crawldoc1 == crawldoc2
  str1 = thrift_to_str(crawldoc1)
  str2 = thrift_to_str(crawldoc2)
  assert str1 is not str2
  assert str1 == str2
  crawldoc3 = CrawlDoc()
  crawldoc4 = CrawlDoc()
  assert crawldoc3 == crawldoc4
  assert str_to_thrift(str1, crawldoc3)
  assert str_to_thrift(str2, crawldoc4)
  assert crawldoc3 == crawldoc4
  assert crawldoc3 is not crawldoc4
test_thrift()



