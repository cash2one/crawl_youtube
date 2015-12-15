#!/usr/bin/python
# -*- encoding: utf8 -*-
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""One-line documentation for test module.
A detailed description of test.
"""
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
import traceback
import json

from le_crawler.common.cd_cateid_getter import get_cd_cateid_name
from le_crawler.core.items import CrawlerItem
from le_crawler.common.extend_map_handler import ExtendMapHandler
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.common.extend_map_json_parser import ExtendMapJsonParser
from le_crawler.core.items import fill_base_item


#global var
class CDesktopSportsSpider(Spider):
    name = 'cd_sports_crawler'
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/',
        random_sort = True)
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(CDesktopSportsSpider, self).__init__(*a, **kw)
      self.extend_map_h_ =\
          ExtendMapHandler.get_instance(
              CDesktopSportsSpider.start_url_loader,
              'le_crawler.common.cdesktop_settings')
      self.finished_count = 0
      self.start_size = len(CDesktopSportsSpider.start_urls)
      self.use_sys_extract_link = False
      self.api_parser_ = ExtendMapJsonParser()
      self.share_obj = {}

    def parse(self, response):
      try:
        url = response.url.strip()
        page = response.body.decode(response.encoding)
        self.finished_count += 1
        extend_url = []
        status = True
        size = 0
        if self.accepted_api_parse(url):
          red = self.wap_api_parse(url, page)
          if red:
            size = len(red.get('request', []))
            status = bool(size)
            for u in red.get('request', []):
              yield Request(u, headers = {'Referer' : '%s' % (url)}, callback =
                  self.parse_page)
        else:
          status, extend_url =\
            self.extend_map_h_.extract_extend_map(body = page, pageurl = url)
        if extend_url:
          size = len(extend_url)
        if status:
          print 'Ok:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
        else:
          print 'Failed:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
          return
        ignore_crawl = self.extend_map_h_.setting_handler_.ignore_link_to_crawler(url)
        if not ignore_crawl and not self.use_sys_extract_link:
          for i in extend_url:
            yield Request(i, headers={'Referer': '%s' % (url)}, callback =
                self.parse_page)
        else:
          self.log('ignore crawl: %s' % (url), log.INFO)
      except Exception, e:
        msg = e.message
        msg += traceback.format_exc()
        print msg
        self.log('Failed parse response: %s' % (msg), log.ERROR)
        return
    def parse_page(self, response):
      el = CrawlerItem()
      fill_base_item(response, el)
      el['source_type'] =  self.default_source_type(el.get('url', ''))
      el['item_type'] = 'sports'
      share_obj = self.share_obj.pop(el.get('url', ''), None)
      if share_obj:
        el['title'] = share_obj.get('title', '')
        el['extend_map'] = {'cover' : el.get('imgsrc', ''),
            'desc' : el.get('digest', '')}
        el['comment_num'] = el.get('commentcount', '0')
        el['article_time_raw'] = el.get('ptime', '')
      else:
        referer_url = response.request.headers.get('Referer', '')
        extend_map = self.extend_map_h_.lookup_extend_map(el.get('url'),
            'dict', True)
        if extend_map:
          el['title'] = extend_map.get('title', None)
          el['extend_map'] = {'cover' : extend_map.get('cover', '')}
          el['article_time_raw'] = extend_map.get('article_time_raw', None)
        else:
          self.log('Failed found extend map for:%s' % (el['url']), log.ERROR)
        sta, custom_dict = self.extend_map_h_.setting_handler_.extract_custom_map(body = el['page'],
            pageurl = el['url'])
        if not sta or not custom_dict:
          print 'Failed extract custom value: %s' % (el['url'])
        else:
          for k, v in custom_dict.items():
            el[k] = v
        subid = CDesktopSportsSpider.\
                start_url_loads.get_property(referer_url,
                    'subcategory', '10')
        el['cate_id'] = get_cd_cateid_name(subid, '体育')
      return el

    def default_source_type(self, refer_url):
      if 'sina.cn' in refer_url:
        return '新浪体育'
      elif '163.com' in refer_url:
        return '网易体育'
      elif 'hupu.com' in refer_url:
        return '虎扑体育'
      elif 'qq.com' in refer_url:
        return '腾讯体育'
      else:
        self.log('Failed set default item type:%s' % (refer_url), log.ERROR)

    # return dict {request, item}
    def accepted_api_parse(self, url):
      if '163.com' in url:
        return True
      return False

    def wap_api_parse(self, url, page):
      if '163.com' in url:
        return self.__163_parse(url, page)
      else: return None
    def __163_parse(self, url, page):
      retlist = []
      if page.startswith('artiList(') and page.endswith(')'):
        bi = page.find('artiList') + 9
        ei = page.rfind(')')
        nb = page[bi : ei]
        try:
          jb = json.loads(nb)
          for k,v in jb.items():
            for item in v:
              url = item.get('url', None)
              if url:
                retlist.append(url)
                self.share_obj[url] = dict(item)
        except Exception, e:
          self.log(e, log.ERROR)
      return {'request' : retlist}

    def closed(self, reason):
      pass
