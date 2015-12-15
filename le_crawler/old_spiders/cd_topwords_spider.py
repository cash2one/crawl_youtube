#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for content desktop spider
"""
import traceback
import re
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy import log


from le_crawler.core.items import CrawlerItem
from le_crawler.core.items import fill_base_item
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.common.cd_cateid_getter import get_cd_cateid_name
from le_crawler.core.links_extractor import LinksExtractor
from le_crawler.core.base_extract import ExtractLinks

class CDesktopSpider(Spider):
    name = 'cd_crawler'
    #allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/')
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(CDesktopSpider, self).__init__(*a, **kw)
      self.finished_count = 0
      self.start_size = len(CDesktopSpider.start_urls)
      self.collect_nums = 0
      self.new_links_extract = \
      LinksExtractor('le_crawler.common.cdesktop_settings',
          start_url_loader = CDesktopSpider.start_url_loader)
      self.share_cache = {}
      self._dont_need_custom_ext = [
          re.compile('\.myzaker\.com'),
          re.compile('\.hupu\.com'),
          ]

    def parse(self, response):
      try:
        url = response.url.strip()
        page = response.body.decode(response.encoding)
        self.finished_count += 1
        # first jugy json parser
        size = 0
        status = True
        refer_url = response.request.headers.get('Referer', None)
        bd_type = self.get_parse_type(refer_url or url)
        status, links_map = self.new_links_extract.extract_block_links(url,
              body = page, bd_type = bd_type)
        if status:
          size = len(links_map)
          print 'Ok:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
        else:
          print 'Failed:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
          return
        for i in links_map:
          if i.extend_map:
            i.extend_map.pop('sid', None)
          if i.item_type == ExtractLinks.LIST_REQUEST:
            self.share_cache[i.url] = i.extend_map
            yield Request(i.url, headers={'Referer': '%s' % (refer_url or url)},
                callback = self.parse, dont_filter = True)
          elif i.item_type == ExtractLinks.ITEM_REQUEST:
            self.share_cache[i.url] = i.extend_map
            yield Request(i.url, headers={'Referer': '%s' % (url)}, callback =
              self.parse_page, dont_filter = i.dont_filter)
          elif i.item_type == ExtractLinks.ITEM_ITEM:
            item = CrawlerItem()
            item['url'] = i.url
            self.item_covert(item, i.extend_map)
            cate_id = CDesktopSpider.start_url_loader.get_property(url,
                'cate_id', None)
            if cate_id:
              item['cate_id'] = get_cd_cateid_name(cate_id)
            item['item_type'] = CDesktopSpider.start_url_loader.get_property(refer_url,
                'category', None) or 'news'
            self._post_item_process(item, refer_url)
            yield item
          else:
            self.log('Bad response parse type:%s' % (i.item_type), log.ERROR)
        #return self.parse_page(response)
      except Exception, e:
        msg = 'spider try catch error:', e
        msg += traceback.format_exc()
        self.log(msg, log.ERROR)
        return

    def parse_page(self, response):
      el = CrawlerItem()
      fill_base_item(response, el)
      refer_url = el.get('referer', '')
      rawurl = response.request.url
      redirect_url = ''
      bd_type = self.get_parse_type(refer_url)
      assert bd_type, 'Failed got bd_type from %s' % (refer_url)
      if el.get('redirect_urls', []):
        redirect_url = el.get('redirect_urls', [])[0]
      cache_ref_url = None
      if rawurl in self.share_cache:
        cache_ref_url = rawurl
      elif el['url'] in self.share_cache:
        cache_ref_url = el['url']
      elif redirect_url in self.share_cache:
        cache_ref_url = redirect_url
      if cache_ref_url:
        cache_tmp = self.share_cache.pop(cache_ref_url)
        self.item_covert(el, cache_tmp)
      if self.need_cusom_extract(el['url']):
        sta, links = self.new_links_extract.extract_custom_links(el['url'],
        el['page'], LinksExtractor.HTML_EXTRA)
        if sta:
          self.item_covert(el, links.extend_map)
      el['item_type'] = CDesktopSpider.start_url_loader.get_property(refer_url,
          'category', None) or 'news'
      subcate_id = CDesktopSpider.start_url_loader.get_property(refer_url,
          'subcate_id', None)
      if subcate_id:
        el['cate_id'] = get_cd_cateid_name(subcate_id, el.get('cate_id', ''))
      assert el['item_type'], 'bad item_type'
      self._post_item_process(el, refer_url)
      yield el

    def closed(self, reason):
      self.log('Finished Collect Urls:%s' % self.collect_nums, log.INFO)

    def get_parse_type(self, refer_url):
      parser_type = CDesktopSpider.start_url_loader.get_property(refer_url,
          'parser_type',
          'html')
      if parser_type == 'html':
        return LinksExtractor.HTML_EXTRA
      elif parser_type == 'xml':
        return LinksExtractor.XML_EXTRA
      elif parser_type == 'json':
        return LinksExtractor.JSON_EXTRA
      raise Exception('Unsupport parser type:%s' % parser_type)

    def need_cusom_extract(self, url):
      for i in self._dont_need_custom_ext:
        if i.search(url):
          return False
      return True

    def item_covert(self, item, inputd):
      # trick
      if not item or not inputd:
        return None
      img = inputd.pop('cover', None)
      item.update(inputd)
      if 'content_imgs' in item:
        item['content_imgs'].append(img)
      else:
        item['content_imgs'] = [img]
      return item

    # like change category
    def _post_item_process(self, item, refer_url):
      if not refer_url: return
      if 'zaker' in refer_url and refer_url in self.share_cache:
        extend_m = self.share_cache.get(refer_url)
        cate_id = extend_m.get('title', None)
        if cate_id:
          item['cate_id'] = cate_id
