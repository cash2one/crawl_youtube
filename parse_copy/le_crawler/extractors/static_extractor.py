#!/usr/bin/python
# coding=utf-8

import os
import re
import json

from ..common.utils import multi_key_fields, source_set
from ..proto.video.ttypes import State


class StaticExtractor:
  def __init__(self, xpather, deadlinks):
    self._invalid_category = ['电视剧', '电影', '动漫', '综艺', '纪录片']
    self._xpather = xpather
    self._deadlink_urls = deadlinks
    self._valid_video = []
    self._lists = []
    self._web_name = ''

  def _is_invalid_page(self, url):
    for vlist in self._lists:
      if re.search(vlist, url):
        return True, 'list'
    return True, 'video'


  def _filter_long_video(self, html_data, url_type):
    if url_type == 'list':
      return html_data
    elif url_type == 'video':
      category = html_data.get('category', '').encode('utf-8', 'ignore')
      if category in self._invalid_category:
        return {}
      return html_data


  def _decide_from_http_code(self, response):
    if response.return_code in [404, 302] :
      return True
    return response.url.rstrip('/') in self._deadlink_urls.get(self._web_name, [])


  def _is_deadlink(self, crawl_doc, html_data):
    if self._decide_from_http_code(crawl_doc.response):
      return True
    return html_data and 'deadlink' in html_data


  def GetStatic(self, crawl_doc):
    url = crawl_doc.url
    valid, url_type = self._is_invalid_page(url)
    if not valid:
      return None

    html_data = {}
    is_dead_link = False
    if crawl_doc.response:
      html_data = self._xpather.parse(url, crawl_doc.response.body) or {}
      is_dead_link = self._is_deadlink(crawl_doc, html_data)
      if not is_dead_link and not html_data:
        return None

    for k, v in html_data.items():
      if k not in multi_key_fields and not k.startswith('items'):
        html_data[k] = v[0]
      elif k in multi_key_fields:
        html_data[k] = ';'.join(v).strip(';')

    html_data['doc_id'] = crawl_doc.id
    html_data['id'] = str(crawl_doc.id)
    html_data['crawl_time'] = html_data['create_time'] = crawl_doc.crawl_time
    html_data['discover_time'] = crawl_doc.discover_time
    html_data['url'] = crawl_doc.url
    html_data['domain'] = self._web_name
    html_data['domain_id'] = source_set[self._web_name]
    html_data['in_links'] = crawl_doc.in_links
    html_data['inlink_history'] = [crawl_doc.in_links]
    html_data['page_state'] = crawl_doc.page_state
    if is_dead_link:
      html_data['page_state'] = crawl_doc.page_state | State.DEAD_LINK
      html_data['dead_link'] = is_dead_link

    return self._filter_long_video(html_data, url_type)


if __name__ == '__main__':
  class Response:
    def __init__(self):
      #self.url = 'http://www.tudou.com/error.php?msg=%E6%97%A0%E6%95%88%E7%9A%84%E8%8A%82%E7%9B%AEID'
      self.url = 'http://www.tudou.com/albumcover/blKTQQK5d7c.html?qq-pf-to=pcqq.c2c'
      self.return_code = 200
      # body = 'abc'

  class CrawlDoc:
	def __init__(self, rs):
	  self.response = rs

  response = Response()
  crawldoc = CrawlDoc(response)
  with open(os.path.join('../templates', 'deadlink_urls.txt')) as f:
    dl = json.load(f)
  # print StaticExtractor(None, dl)._decide_from_http_code(response)
  # from extractors.youku_static import YoukuStatic
  # print YoukuStatic(None, dl)._is_deadlink(crawldoc)
