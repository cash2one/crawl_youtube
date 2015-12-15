#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for content desktop spider
"""
import traceback
import urlparse
import time
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy import log

from le_crawler.core.items import CrawlerItem
from le_crawler.core.extra_extend_map_engine import ExtraExtendMapEngine
from le_crawler.core.items import fill_base_item
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.common.cd_cateid_getter import get_cd_cateid_name

class CommonSpider(Spider):
    name = 'common_spider'
    #allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/')
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(CommonSpider, self).__init__(*a, **kw)
      self.extend_map_h_ = ExtraExtendMapEngine(
          CommonSpider.start_url_loader,
          module_path = 'le_crawler.common.cdesktop_settings')
      self.finished_count = 0
      self.start_size = len(CommonSpider.start_urls)
      self.collect_nums = 0
      import re
      self.json_reg = [
          re.compile(r'http\:\/\/ent\.cntv\.cn\/update\/(tv|movie)\/data\/\d+.json'),
          re.compile(r'o\.go2yd\.com\/api\/letv\/channel\?cid'),
          re.compile(r'\.myzaker\.com\/zaker\/apps_telecom\.php'),
          re.compile(r'\.myzaker\.com\/zaker\/article_telecom\.php'),
          ]
      # url --> attribute_obj
      self.share_cache = {}
    def parse(self, response):
      try:
        url = response.url.strip()
        page = response.body.decode(response.encoding).encode('utf8')
        self.finished_count += 1
        # first jugy json parser
        size = 0
        status = True
        if self.__accept_json_parser(url):
          extend_url = self.__json_parser(url, page)
        else:
          status, extend_url, tmpdict = self.extend_map_h_.extract_extend_map(
            body = page,
            pageurl = url,
            ignore_empty_property = True)
        if extend_url:
          size = len(extend_url)
          self.collect_nums += size
        if status:
          print 'Ok:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
        else:
          print 'Failed:(%5d/%d)Finished Extend: %s, %d' % (self.finished_count,
            self.start_size, url, size)
          return
        for i in extend_url:
          if isinstance(i, tuple):
            yield Request(i[2], headers={'Referer': '%s' % (url)}, callback =
              self.parse_page if i[0] == 'item' else self.parse, dont_filter =
              i[1])
          else:
            yield Request(i, headers={'Referer': '%s' % (url)}, callback =
              self.parse_page)
        #return self.parse_page(response)
      except Exception, e:
        print 'spider try catch error:', e
        print traceback.format_exc()
        return

    def parse_page(self, response):
      el = CrawlerItem()
      fill_base_item(response, el)
      refer_url = el.get('referer', '')
      if el.get('redirect_urls', []):
        rawurl = el.get('redirect_urls', [])[0]
      if 'yidianzixun.com' in rawurl:
        if rawurl:
          el['url'] = rawurl
        cache = self.share_cache.pop(el.get('url'), None)
        el['cate_id'] = self.__ydzixun_url_cid_getter(refer_url)
        if cache:
          el['title'] = cache.get('title', None)
          if 'images' in cache:
            el['content_imgs'] = [self.__ydzixun_img_url_process(
              cache.get('images')[0])] if cache.get('images', []) else []
          el['source_type'] = cache.get('source', None)
          if 'date' in cache:
            el['article_time_raw'] = cache['date']
        else:
          self.log('miss cache for url:%s' % (el.get('url')), log.WARNING)
      elif 'myzaker.com' in rawurl:
        if rawurl:
          el['url'] = rawurl
        #el['cate_id'] = self.__zaker_url_cid_getter(el.get('url'))
        cache = self.share_cache.pop(el.get('url'), None)
        if cache:
          el['title'] = cache.get('title', None)
          el['source_type'] = cache.get('author_name', None)
          el['article_time_raw'] = cache.get('date', None)
          el['content_imgs'] = [cache.get('thumbnail_pic', '')]
          el['cate_id'] = cache.get('category', '')
      else:
        sta, cdict = self.extend_map_h_.extract_custom_map(body = el['page'],
            pageurl = el['url'])
        if not sta or not cdict:
          print 'Failed extract custom value: %s' % (el['url'])
        else:
          # extract pure content text
          # all this spider process content
          #TODO(xiaohe): add type
          for (k, v) in cdict.items():
            el[k] = v
      el['item_type'] = self.extend_map_h_.\
          get_category_name(refer_url) or 'news'
      subcate_id = CommonSpider.start_url_loader.get_property(refer_url,
          'subcate_id', None)
      if subcate_id:
        el['cate_id'] = get_cd_cateid_name(subcate_id, el.get('cate_id', ''))
      assert el['item_type'], 'bad item_type'
      return el

    def closed(self, reason):
      self.log('Finished Collect Urls:%s' % self.collect_nums, log.INFO)

    def __accept_json_parser(self, url):
      #TODO(xiaohe): movie this logic to extend map
      # make extend_map support json extend
      for r in self.json_reg:
        if r.search(url):
          return True
      return False

    def __json_parser(self, url, body):
      import json
      # by now only deal with cntv
      try:
        j = json.loads(body)
        returl = []
        if 'cntv' in url:
          if j.has_key('rollData'):
            for u in j['rollData']:
              if u.has_key('url'):
                returl.append(('item', False, u['url']))
              else:
                self.log('Failed Found url key for : %s' % u, log.WARNING)
        elif 'go2yd.com' in url:
          if 'success' != j.get('status', ''):
            self.log('Failed Got news list page:%s' % (url), log.ERROR)
            return returl
          for i in j.get('data', []):
            url = i.get('url', None)
            if not url:
              self.log('Bad Data:%s' % (i), log.ERROR)
              continue
            nurl = self.__ydzixun_url_preprocess(url)
            returl.append(('item', False, nurl))
            self.share_cache[nurl] = dict(i)
        elif 'myzaker.com' in url:
          if '1' != j.get('stat', '0'):
            self.log('Failed Got news list page:%s' % (url), log.ERROR)
            return returl
          for d in j.get('data', {}).get('list', []):
            if 'api_url' in d:
              returl.append(('request', True, d.get('api_url') +
                '&since_date=%d&num=300' %
                  (int(time.time()))))
            elif 'url' in d:
              url = d.get('url')
              returl.append(('item', False, url))
              self.share_cache[url] = dict(d)
            else:
              self.log('Bad Data:%s' % (d), log.ERROR)
              continue
        return returl
      except Exception, e:
        self.log('Error loads json content:%s, %s' % (body, e.message), log.ERROR)
        return []

    def __zaker_url_cid_getter(self, url):
      pass

    def __ydzixun_url_cid_getter(self, url):
      pr = urlparse.urlparse(url)
      qd = urlparse.parse_qs(pr.query) or {}
      cid = qd.get('cid', [])[0]
      return get_cd_cateid_name(cid, '')

    def __ydzixun_url_preprocess(self, url):
      up = urlparse.urlparse(url)
      return urlparse.urlunsplit((up.scheme, up.netloc, up.path, 's=letv', 'app'))

    def __ydzixun_img_url_process(self, url):
      up = urlparse.urlparse(url)
      qd = urlparse.parse_qs(up.query)
      qd.pop('type', '')
      import urllib
      return urlparse.urlunsplit(
        (up.scheme,
         up.netloc,
         up.path,
         urllib.urlencode([(k, v[0]) for k, v in qd.items() if v]),
         ''))

