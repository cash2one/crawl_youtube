#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
"""
get base crawler items to fill
decoing item with utf8
"""

__author__ = 'guoxiaohe@letv.com (Guo XiaoHe)'


def fill_base_item(response, item):
  item['url'] = response.url
  item['page'] = response.body
  item['http_header'] = response.headers.to_string()
  item['page_encoding'] = response.encoding
  item['meta'] = '%s' % response.meta
  item['status'] = '%s' % response.meta
  item['referer'] = response.request.headers.get('Referer')
  # redirect_urls can be found in meta
  if response.meta.has_key('redirect_urls'):
    item['redirect_urls'] = response.meta['redirect_urls']
  return process_item(item, item['page_encoding'])


# post item process
def process_item(item, encoding):
  return item

