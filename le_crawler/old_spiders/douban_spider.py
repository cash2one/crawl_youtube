#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""
Crawler for douban
"""

__author__ = 'gaoqiang@letv.com (Gao Qiang)'

import re
import json
import random
from urlparse import urlparse

from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider

from ..base.html_utils import remove_tags
from ..core import json_pather
from ..core.items import CrawlerItem
from ..core.extra_extend_map_engine import ExtraExtendMapEngine


def _gen_next_url(url, key, delta=1):
  query = urlparse(url).query
  query_data = {item.split('=')[0]: item.split('=')[1] for item in query.split('&') if item}
  query_data[key] = int(query_data[key]) + delta
  query_new = '&'.join(['%s=%s' % (k, v) for k, v in query_data.items()])
  next_url = url.replace(query, query_new)
  print 'prev url:', url, 'query:', query, 'query_new:', query_new
  print 'next url:', next_url
  return next_url


def _parse_id(s, reg):
  match = reg.search(s)
  if match:
    return match.groups()[0]


def parse_movie_details(response):
  url = response.url.strip()
  item = CrawlerItem()
  item['item_type'] = 'MOVIES_JSON'
  item['url'] = response.request.headers.get('Referer', url)
  item['page'] = response.body
  yield item


class DoubanSpider(CrawlSpider):
  name = 'douban_spider'
  allowed_domains = ['douban.com']
  start_urls = ['http://movie.douban.com/tag/',
                'http://movie.douban.com/tag/?view=cloud',
                'http://movie.douban.com/j/search_tags?type=movie']

  def __init__(self, *a, **kw):
    super(DoubanSpider, self).__init__(*a, **kw)
    self._movies_api = ('http://movie.douban.com/j/search_subjects?type=movie&'
                        'tag=%s&sort=recommend&page_limit=40&page_start=0')
    self._posters_api = ('http://movie.douban.com/subject/%s/photos?type=R'
                         '&start=0&sortby=vote&size=a&subtype=a')
    self._movie_id_re = re.compile('.*/subject/(\d+)/?.*')
    self._photo_id_re = re.compile('.*/photos/photo/(\d+)/?.*')
    self.extend_map_extract = ExtraExtendMapEngine(None, 'le_crawler.common.page_info_settings')
    self._tag_set = set()

  def parse_start_url(self, response):
    url = response.url.strip()
    if url.startswith('http://movie.douban.com/j/'):
      tags = json.loads(response.body).get('tags', [])
    else:
      selector = Selector(text=response.body, type='html')
      tags = selector.xpath('//table[@class="tagCol"]//a/text()').extract()
      if not tags:
        tags = selector.xpath('//*[@class="indent tag_cloud"]//a/text()').extract()
    if not tags:
      raise Exception('Failed to parse start urls')
    for tag in tags:
      if tag in self._tag_set:
        continue
      self.log('begin crawl movie tag: %s' % tag, log.INFO)
      self._tag_set.add(tag)
      yield Request(self._movies_api % tag,
                    callback=self._parse_tag_api,
                    headers={'Referer': url}, dont_filter=True)

  def _parse_tag_api(self, response):
    url = response.url.strip()
    self.log('begin parse tag api, %s' % url)
    data = json.loads(response.body).get('subjects', None)
    if not data:
      self.log('finished parsing tag api, or error occurred, %s' % url, log.DEBUG)
      return
    yield Request(_gen_next_url(url, 'page_start'), callback=self._parse_tag_api,
                  headers={'Referer': url}, dont_filter=True)
    for url in json_pather.xpath(data, '//url/text()'):
      movie_id = _parse_id(url, self._movie_id_re)
      if not movie_id:
        self.log('failed match movie id from url, %s' % url, log.ERROR)
        continue
      photo_list_pg = self._posters_api % movie_id
      # send request of movie details
      movie_home = 'http://movie.douban.com/subject/%s/' % movie_id
      yield Request('http://movie.douban.com/j/subject_abstract?subject_id=%s' % movie_id,
                    headers={'Referer': movie_home},
                    callback=parse_movie_details, dont_filter=True)
      yield Request(movie_home, callback=self.parse_movie_tags)
      yield Request(photo_list_pg, headers={'Referer': url, 'Mid': movie_id},
                    callback=self.parse_photo_list_page, dont_filter=True)

  def parse_photo_list_page(self, response):
    url = response.url.strip()
    self.log('begin parse poster list page, %s' % url)
    mid = response.request.headers.get('Mid')
    pids = self._parse_pics_ids(response.body)
    if not pids:
      self.log('failed to parse poster page, %s' % url, log.INFO)
      return
    item = CrawlerItem()
    item['url'] = 'http://movie.douban.com/subject/%s/' % mid
    item['item_type'] = 'PIC'
    item['content_imgs'] = ['http://img%s.douban.com/view/photo/raw/public/p%s.jpg' %
                            (random.randint(3, 6), x) for x in pids]
    item['dont_filter'] = True
    yield item
    self.log('fetch %s pictures [%s]' % (len(pids), url), log.INFO)
    yield Request(_gen_next_url(url, 'start', 40),
                  headers={'Referer': url, 'Mid': mid},
                  callback=self.parse_photo_list_page)

  def _parse_pics_ids(self, body):
    sel = Selector(text=body, type='html')
    tmpurls = sel.xpath('//div[@class="cover"]/a/@href')
    pic_ids = []
    for u in tmpurls:
      tmpurl = u.extract()
      if tmpurl:
        tmptid = _parse_id(tmpurl, self._photo_id_re)
        if tmptid:
          pic_ids.append(tmptid)
    return pic_ids

  def parse_movie_tags(self, response):
    url = response.url.strip()
    print 'begin extract movie page, %s' % url
    self.log('begin extract movie page, %s' % url, log.INFO)
    status, extendus, maplist = self.extend_map_extract.extract_extend_map(response.body, pageurl=url)
    # tags
    moviedict = {}
    if status and maplist:
      for i in maplist:
        if 'cover' in i[1]:
          tmpdict = {'url': i[0]}
          tmpdict.update(i[1])
          moviedict.setdefault('trailer', []).append(tmpdict)
        elif 'tags' in i[1]:
          moviedict.setdefault('tags', []).append(i[1])
    # movie info
    status, mapdict = self.extend_map_extract.extract_custom_map(response.body, pageurl=url)
    print '---------------custom map:', mapdict
    print url
    if status:
      moviedict.update(mapdict)
      if 'movie_info' in mapdict:
        tmpdict, rawinfo = self._parse_movie_details_from_blk(mapdict.get('movie_info'))
        moviedict['additional'] = tmpdict
        moviedict.pop('movie_info')

    if moviedict:
      item = CrawlerItem()
      item['url'] = url
      item['item_type'] = 'MOVIES_MISC'
      item['page'] = moviedict
      yield item
    else:
      self.log('failed to parse movie page, %s' % url, log.ERROR)

  def _parse_movie_details_from_blk(self, htmlblk):
    movies = remove_tags(['div', 'span', 'a'], htmlblk)
    redict = {}
    for l in movies:
      kv = l.split(':')
      if len(kv) >= 2:
        redict[kv[0].strip()] = ''.join(kv[1:])
    return redict, movies
