#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe
__author__ = 'guoxiaohe@letv.com'

from scrapy.selector import Selector
from scrapy.selector import SelectorList
from le_crawler.base.extract_content import ContentExtractor

def get_pure_texts(html, encode_type):
  if not html or not encode_type:
    return None, None
  ex = ContentExtractor()
  return ex.analyse(html, encode_type = encode_type)

def get_pure_paragraphs(html, encode_type):
  if not html or not encode_type:
    return None, None
  ex = ContentExtractor()
  return ex.extract_with_paragraph(html, encode_type = encode_type)

# @deprecated
def get_children_text_from_selector(sel):
  if not sel:
    return None
  if not isinstance(sel, Selector) and not isinstance(sel, SelectorList):
    raise Exception('get_children_text() need scrapy.selector(list) class')
  return_text = ''
  child_sel = sel.xpath('./*')
  child_text = sel.xpath('./text()').extract()
  idx = 0
  if not child_text:
    for s in child_sel:
      tmpt = None
      tmpt = get_children_text_from_selector(s)
      if tmpt:
        return_text += tmpt + '\n'
  elif not child_sel:
    for t in child_text:
      if t:
        return_text += t.encode('utf8')
    return return_text
  elif len(child_text) >= len(child_sel):
    for rtxt in child_text:
      if rtxt and rtxt != '\n' and rtxt != '\r\n':
        return_text += rtxt.encode('utf8')
      #return_text += rtxt
      if idx < len(child_sel):
        tmpt = get_children_text_from_selector(child_sel[idx])
        if tmpt:
          return_text += tmpt
        idx += 1
  else:
    for rts in child_sel:
      tmpt = get_children_text_from_selector(rts)
      if tmpt:
        return_text += tmpt
      if idx < len(child_text):
        tmpt = child_text[idx].encode('utf8')
        if tmpt:
          return_text += tmpt
        idx += 1
  if not return_text or return_text == '':
    return None
  return return_text
