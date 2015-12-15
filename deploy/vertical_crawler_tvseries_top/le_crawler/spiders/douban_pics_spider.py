#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
for douban all movie pics crawl
"""

import json
import urllib2

from urllib import urlencode
import traceback

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
from scrapy.selector import Selector

from le_crawler.base.url_filter import UrlFilter
from le_crawler.core.items import CrawlerItem
from le_crawler.core.extra_extend_map_engine import ExtraExtendMapEngine
from le_crawler.base.start_url_loads import StartUrlsLoader

class DoubanPicSpider(Spider):
  name = 'douban_pic_spider'
  allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
  start_url_loader = StartUrlsLoader.get_instance('../start_urls/')
  start_urls = start_url_loader.get_start_urls()

  def __init__(self, *kargs, **kwargs):
    super(DoubanPicSpider, self).__init__(*kargs, **kwargs)
    self.movie_list_page =\
        'http://movie.douban.com/j/search_subjects?type=movie&tag=(*tag*)&sort=recommend&page_limit=40&page_start=0'
    import re
    self.mid_reg = re.compile(r'.*\/subject\/(\d+)\/?.*')
    self.photos_list_page = \
    'http://movie.douban.com/subject/(*mid*)/photos?type=R&start=0&sortby=vote&size=a&subtype=a'
    self.ptid_reg = re.compile(r'.*\/photos\/photo\/(\d+)\/?.*')
    self.finished_count = 0
    self.extend_map_extract =\
        ExtraExtendMapEngine(DoubanPicSpider.start_url_loader,
            'le_crawler.common.douban_settings')

  def parse(self, response):
    try:
      url = response.url.strip()
      if response.encoding != 'utf8' and response.encoding != 'utf-8':
        page = response.body.decode(response.encoding).encode('utf8')
      else:
        page = response.body
      self.finished_count += 1
      j = json.loads(page)
      tags = j['tags']
      print 'Ok:(%5d)ParserEnterUrl: %s' % (len(tags), url)
      for i in tags:
        yield Request(self.movie_list_page.replace('(*tag*)', i),
            headers={'Referer': '%s' % (url)},
            callback = self.parse_movie_list_page,
            dont_filter = True)
      self.log('Finished send %s tag search request' % len(tags), log.INFO)
    except Exception, e:
      print 'spider try catch error:', e
      print traceback.format_exc()


  def parse_movie_list_page(self, response):
    url = response.url.strip()
    if response.encoding != 'utf8' and response.encoding != 'utf-8':
        page = response.body.decode(response.encoding).encode('utf8')
    else:
      page = response.body
    # cause yile code block not allowed has return
    local_status = True
    j = json.loads(page)
    if not j.has_key('subjects') or not j['subjects']:
      self.log('Empty movie list return, stoped: %s' % url, log.INFO)
      local_status = False
        # parser movie's id
    mids = []
    if local_status:
      for mblk in j['subjects']:
        mid = self.__get_id(mblk['url'], self.mid_reg) if mblk.has_key('url') else None
        #title = mblk['title'] if mblk.has_key('title') else None
        if mid:
          mids.append(mid)
    if not mids:
      self.log('Extract movie id list empty, stoped: %s' % url, log.INFO)
      local_status = False
    # yield movies info json for other purepose
    #TODO(xiaohe)
    if local_status:
      #build next page url
      next_mv_lst_pg_url = self.__gen_next_list_page(url, 'page_start', 1)
      self.log('crawl next movie list page:%s' % next_mv_lst_pg_url, log.INFO)
      yield Request(next_mv_lst_pg_url,
              headers={'Referer': '%s' % (url)},
              callback = self.parse_movie_list_page,
              dont_filter = True)
      # build photo link list page
      for i in mids:
        photo_list_pg = self.photos_list_page.replace('(*mid*)', i)
        # send request of movie details
        movie_home = self.__build_movie_home_url(i)
        yield Request(self.__build_movie_details_url(i),
            headers = {'Referer': movie_home},
            callback = self.parse_movie_details)
        yield Request(movie_home, callback = self.parse_movie_tags)

        #print 'send photo list page:', photo_list_pg
        yield Request(photo_list_pg,
            headers={
              'Referer': '%s' % (url),
              #'Title' : '%s' % (i[1]),
              'Mid' : '%s' % (i)
              },
              callback = self.parse_photo_list_page)
        self.log('Send %s movie(s) photo request : %s' % (len(mids), mids), log.INFO)

  def parse_movie_tags(self, response):
    url = response.url.strip()
    page = response.body.decode(response.encoding)
    status, extendus, maplist = \
    self.extend_map_extract.extract_extend_map(page, pageurl = url)
    #tags
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
    status, mapdict = \
        self.extend_map_extract.extract_custom_map(
            page,
            pageurl = url)
    if status:
      moviedict.update(mapdict)
      if 'movie_info' in mapdict:
        tmpdict, rawinfo =\
        self.__parse_movie_details_from_blk(mapdict.get('movie_info'))
        moviedict['additional'] = tmpdict
        #moviedict['rawinfo'] = rawinfo
        moviedict.pop('movie_info')

    if moviedict:
      it = CrawlerItem()
      it['url'] = url
      it['item_type'] = 'MOVIES_MISC'
      #it['dont_filter'] = True
      it['page'] = moviedict
      yield it
    else:
      self.log('Failed Parser Movie Tags:%s' % (url), log.ERROR)

  def parse_movie_details(self, response):
    url = response.url.strip()
    page = response.body.decode(response.encoding)
    it = CrawlerItem()
    it['item_type'] = 'MOVIES_JSON'
    it['url'] = response.request.headers.get('Referer', url)
    it['page'] = page
    yield it

  def parse_photo_list_page(self, response):
    encoding = response.encoding
    url = response.url.strip()
    page = response.body.decode(encoding)
    #title = response.request.headers.get('Title').decode(encoding)
    mid = response.request.headers.get('Mid')
    # yield movies info json for other purepose
    # parser movie's id
    # parser next photo link pages
    pids = self.__parse_pics_ids(page)
    local_status = True
    if not pids:
      self.log('Extract picture list empty, stoped: %s' % url, log.INFO)
      local_status = False

    if local_status:
      it = CrawlerItem()
      it['url'] = self.__build_movie_home_url(mid)
      it['item_type'] = 'PIC'
      it['content_imgs'] = self.__build_pic_urls(pids)
      it['dont_filter'] = True
      yield it
      self.log('got %s pictures for %s' % (len(pids), url), log.INFO)
      # gen next photo list page
      next_photos_page = self.__gen_next_list_page(url, 'start', 40)
      yield Request(next_photos_page,
            headers={'Referer': '%s' % (url),
              #'Title' : '%s' % (title),
              'Mid' : '%s' % (mid)},
              callback = self.parse_photo_list_page)

  def __gen_next_list_page(self, url, next_str, page_step_num):
    pres = urllib2.urlparse.urlsplit(url)
    qdict = urllib2.urlparse.parse_qs(pres.query)
    start_page = qdict[next_str][0] if qdict.has_key(next_str) else -1
    next_start = int(start_page) + page_step_num
    qdict[next_str] = [next_start]
    return urllib2.urlparse.urlunsplit((pres.scheme,
        pres.netloc,
        pres.path,
        self.__join_query(qdict),
        pres.fragment))

  def __join_query(self, nqd):
    qlst = []
    for k, v in nqd.items():
      qlst.append('%s=%s' % (k, v[0]))
    return '&'.join(qlst)

  def __get_id(self, url, regs):
    tmp = regs.search(url)
    if tmp:
      return tmp.groups()[0]
    return None

  def __build_movie_home_url(self, mid):
    return 'http://movie.douban.com/subject/%s/' %(mid)
  def __build_movie_details_url(self, mid):
    return 'http://movie.douban.com/j/subject_abstract?subject_id=%s'%(mid)
  def __build_pic_urls(self, pids):
    import random
    return ['http://img%s.douban.com/view/photo/raw/public/p%s.jpg' %\
  (random.choice([3, 5]), x) for x in pids ]

  #return pic_urls
  def __parse_pics_ids(self, body):
    sel = Selector(text = body, type = 'html')
    tmpurls  = sel.xpath('//div[@class="cover"]/a/@href')
    ptids = []
    for u in tmpurls:
      tmpurl = u.extract()
      if tmpurl:
        tmptid = self.__get_id(tmpurl, self.ptid_reg)
        if tmptid:
          ptids.append(tmptid)
    return ptids

  def __parse_movie_details_from_blk(self, htmlblk):
    from le_crawler.base.html_utils import remove_tags
    movies = remove_tags(['div', 'span', 'a'], htmlblk)
    redict = {}
    for l in movies:
      kv = l.split(':')
      if len(kv) >= 2:
        redict[kv[0].strip()] = ''.join(kv[1:])
    return redict, movies
