#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for content desktop spider
"""
import traceback
import re
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy import log

from le_crawler.core.items import CrawlerItem
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.core.links_extractor import LinksExtractor
from le_crawler.base.html_utils import remove_tags, clear_tags
from le_crawler.base.url_normalize import UrlNormalize

class YoukuStarSpider(Spider):
    name = 'youku_star_spider'
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/')
    start_urls = start_url_loader.get_start_urls()
    url_normalize = UrlNormalize.get_instance()
    def __init__(self, *a, **kw):
      super(YoukuStarSpider, self).__init__(*a, **kw)
      self.finished_count = 0
      self.start_size = len(YoukuStarSpider.start_urls)
      self.collect_nums = 0
      self.new_links_extract = \
      LinksExtractor('le_crawler.common.page_info_settings',
          start_url_loader = YoukuStarSpider.start_url_loader)
      self.share_cache = {}
    def parse(self, response):
      try:
        url = response.url.strip()
        page = response.body.decode(response.encoding)
        self.finished_count += 1
        # first jugy json parser
        size = 0
        status = True
        refer_url = response.request.headers.get('Referer', None)
        status, links_map = self.new_links_extract.extract_block_links(url,
              body = page, bd_type = LinksExtractor.HTML_EXTRA)
        if status:
          size = len(links_map)
          print 'Ok:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
        else:
          print 'Failed:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
          return
        sta, links = self.new_links_extract.extract_custom_links(url, page,
        LinksExtractor.HTML_EXTRA)
        if sta:
          item = self._youku_star_blk_parse(links.extend_map)
          if item:
            item['url'] = YoukuStarSpider.url_normalize.get_unique_url(url)
            yield item
        else:
          self.log('Failed extract custom value', log.ERROR)
        for i in links_map:
          yield Request(i.url, headers={'Referer': '%s' % (refer_url or url)},
              callback = self.parse)
      except Exception, e:
        print 'spider try catch error:', e
        print traceback.format_exc()
        return

    def _extract_value(self, selec, path):
      exs = selec.xpath(path)
      if exs:
        exts = exs.extract()
        if exts:
          return exts[0].replace('\t', '').replace('\n', '')
      return None

    def _process_figurebase(self, html):
      ret = {}
      from scrapy.selector import Selector
      if not html:
        return ret
      sel_html = Selector(text = html, type = 'html')
      for i in sel_html.xpath('//li'):
        keyl = i.xpath('./label/text()').extract()
        valuel = i.xpath('.//span/@title').extract() or i.xpath('.//span/text()').extract()
        if keyl and valuel:
          ret[keyl[0].replace(':', '')] = valuel[0]
      return ret

    def _youku_star_blk_parse(self, src_obj):
      item = CrawlerItem()
      if not src_obj:
        return None
      if 'figurebase' in src_obj:
        base_info = self._process_figurebase(src_obj['figurebase'])
        if base_info: item.setdefault('extend_map', {})['base_info'] = base_info
      if 'name' in src_obj:
        item['title'] = src_obj['name']
      if 'excellent' in src_obj:
        exe_sel = Selector(text = src_obj['excellent'], type = 'html')
        exe_list = []
        for i in exe_sel.xpath('//li[@class="p_title"]/a/text()').extract():
          exe_list.append(i)
        if exe_list: item.setdefault('extend_map', {})['excellent'] = exe_list 
      if 'honor' in src_obj:
        hor_sel = Selector(text = src_obj['honor'], type = 'html')
        hor_list = []
        for i in hor_sel.xpath('//li'):
          hl = {}
          tmps = self._extract_value(i, './span[@class="data"]/text()')
          if tmps: hl['year'] = tmps
          tmps = self._extract_value(i, './a[1]/text()')
          if tmps: hl['name'] = tmps
          tmps = self._extract_value(i, './span[2]/text()')
          if tmps: hl['title'] = tmps
          tmps = self._extract_value(i, './a[2]/text()')
          if tmps: hl['product'] = tmps
          if hl: hor_list.append(hl)
        if hor_list: item.setdefault('extend_map', {})['honor'] = hor_list
      if 'introduction' in src_obj:
        item.setdefault('extend_map', {})['introduction'] = clear_tags([''],
            src_obj['introduction']).replace('\t', '').replace('\n', '').replace('...', '')
      if 'productions' in src_obj:
        pr_sel = Selector(text = src_obj['productions'], type = 'html')
        prl = []
        for i in pr_sel.xpath('//tbody/tr[@lastyear]'):
          prd_inf = {}
          tmps = self._extract_value(i, './td[@class="action"]//a/@href')
          if tmps: prd_inf['play_url'] = YoukuStarSpider.url_normalize.get_unique_url(tmps)
          tmps = self._extract_value(i, './@lastyear')
          if tmps: prd_inf['year'] = tmps
          tmps = self._extract_value(i, './td[@class="type"]/text()')
          if tmps: prd_inf['type'] = tmps
          tmps = clear_tags(['span', 'a', 'td'],
              self._extract_value(i, './td[@class="title"]'))
          if tmps: prd_inf['title'] = tmps
          tmps = self._extract_value(i, './td[@class="role"]/text()')
          if tmps: prd_inf['role'] = tmps
          if prd_inf: prl.append(prd_inf)
        if prl: item.setdefault('extend_map', {})['productions'] = prl
      if 'cover' in src_obj:
        item.setdefault('extend_map', {})['cover'] = src_obj['cover']
      if item: return item
      return None



