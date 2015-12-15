#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
"""
get base crawler items to fill
decoing item with utf8
in crawler we recommend using coding unicode
when output data should using utf8
"""

__author__ = 'guoxiaohe@letv.com (Guo XiaoHe)'

import json
import traceback
from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst, Join
import time

from le_crawler.genpy.crawl.ttypes import CrawlDoc, CrawlDocType, CrawlDocAttachment, Request, Response, RedirectInfo
from le_crawler.core.docid_generator import gen_docid

# all item should first alig to unicode,
# output should encod utf8
def fill_base_item(response, item):
  item['page_encoding'] = response.encoding
  item['url'] =  response.url
  try:
    item['page'] = response.body
  except Exception, e:
    print 'decoding error:%s, %s, %s' % (response.encoding, response.url, e.message)
    print traceback.format_exc()
    item['page'] = response.body
  item['http_header'] = response.headers.to_string()
  item['status'] = '%s' % response.status
  item['referer'] = response.request.headers.get('Referer')
  item['down_time'] = int(time.time())
  if response.request.meta and response.request.meta.has_key('Rawurl'):
    item['rawurl'] = response.request.meta['Rawurl']
  # redirect_urls can be found in meta
  if response.meta:
    item['meta'] = '%s' % response.meta
    if response.meta.has_key('redirect_urls'):
      item['redirect_urls'] = response.meta['redirect_urls']
  return process_item(item, item['page_encoding'])

# post item process
def process_item(item, encoding):
  if not item:
    return item
  keys = item.keys()
  for k in keys:
    if type(item[k]) is str or k == 'page':
      item[k] = item[k].decode(encoding, 'ignore').encode('utf8')

class CrawlerItem(Item):
  comment_num = Field()
  content_body = Field()
  down_time = Field()
  http_header = Field()
  meta = Field()
  page_date = Field()
  page_encoding = Field()
  page = Field()
  read_num = Field()
  referer = Field()
  status = Field()
  title = Field()
  url = Field()
  version = Field()
  redirect_urls = Field()
  rawurl = Field()

  def to_jsonStr(self, include_empty = False, encodeing = 'utf8'):
    try:
      tmpdict = {}
      iterkeys = self.keys()
      for k in iterkeys:
       # print type(self[k])
        tmpdict[k] = self[k]
      return json.dumps(tmpdict, ensure_ascii = False).encode(encodeing)
    except Exception, e:
      print traceback.format_exc()
      print 'Failed encoding json: %s, %s'% (self, e.message)
      return None

  def get_key(self, key, type_need = str):
    try:
      if self.has_key(key):
        if isinstance(self[key], type_need):
          return True, self[key]
        else:
          return True, type_need(self[key])
    except Exception, e:
      pass
    return False, None

  def to_crawldoc(self):
    if self is None:
      return None
    try:
      # base
      crawldoc = CrawlDoc()
      crawldoc.request = Request()
      crawldoc.response = Response()
      crawldoc.attachment = CrawlDocAttachment()
      crawldoc.response.redirect_info = RedirectInfo()
      # docid generate from response url
      if self.has_key('url'):
        crawldoc.docid = gen_docid(self['url'])
        crawldoc.response.url = self['url']
      else:
        raise Exception('Can not get url from item, drop')
        return None
      crawldoc.doctype = CrawlDocType.RESPONSEDOC
      isset, crawldoc.crawl_time = self.get_key('down_time', int)
      isset, crawldoc.original_code = self.get_key('page_encoding')
      isset, crawldoc.content = self.get_key('page')
      isset, crawldoc.refer_url = self.get_key('referer')
      # attachment
      isset = False
      resta, crawldoc.attachment.article_time_str = self.get_key('page_date')
      isset = isset or resta
      resta, crawldoc.attachment.title = self.get_key('title')
      isset = isset or resta
      resta, crawldoc.attachment.comment_num = self.get_key('comment_num', int)
      isset = isset or resta
      resta, crawldoc.attachment.read_num = self.get_key('read_num', int)
      isset = isset or resta
      resta, crawldoc.attachment.content_body = self.get_key('content_body')
      isset = isset or resta
      if not isset:
        crawldoc.attachment = None
      # redirect
      isset = False
      resta, crawldoc.response.redirect_info.redirect_urls = self.get_key('redirect_urls')
      isset = isset or resta
      if not isset:
        crawldoc.response.redirect_info = None
      # response
      resta, crawldoc.response.header = self.get_key('http_header')
      isset = isset or resta
      resta, crawldoc.response.meta = self.get_key('meta')
      isset = isset or resta
      resta, crawldoc.response.return_code = self.get_key('status', int)
      isset = isset or resta
      if not isset:
        crawldoc.response = None
      # request
      isset = False
      resta, crawldoc.request.raw_url= self.get_key('rawurl')
      isset = isset or resta
      if not isset:
        crawldoc.request = None
      # base
      return crawldoc
    except Exception, e:
      print traceback.format_exc()
      print "Failed Convert Item to Crawldoc"
      return None

class CrawlerLoader(ItemLoader):
    default_item_class = CrawlerItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
