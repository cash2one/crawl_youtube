#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
for douban all movie crawl
"""

import urllib2

import traceback

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
from scrapy.selector import Selector

from le_crawler.base.url_filter import UrlFilter
from le_crawler.core.items import CrawlerItem
from le_crawler.core.extra_extend_map_engine import ExtraExtendMapEngine
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.base.url_normalize import get_abs_url

class DoubanSpiderEn(Spider):
  name = 'douban_spider'
  allowed_domains = ['movie.douban.com']
  start_url_loader = StartUrlsLoader.get_instance('../start_urls/')
  start_urls = ['http://movie.douban.com/tag/']
  #start_url_loader.get_start_urls()

  def __init__(self, *kargs, **kwargs):
    super(DoubanSpiderEn, self).__init__(*kargs, **kwargs)
    import re
    self.finished_count = 0
    self.mid_reg = re.compile(r'.*\/subject\/(\d+)\/?.*', re.I | re.S)
    self.photo_reg = re.compile(r'\/subject\/(\d+)\/photos', re.I | re.S)
    self.photos_list_page = \
    'http://movie.douban.com/subject/(*mid*)/photos?type=R&start=0&sortby=vote&size=a&subtype=a'
    self.ptid_reg = re.compile(r'.*\/photos\/photo\/(\d+)\/?.*')
    self.extend_map_extract =\
        ExtraExtendMapEngine(DoubanSpiderEn.start_url_loader,
            'le_crawler.common.douban_settings')

  # return movie_ids, other_links
  def __simple_links_extract(self, url, body):
    sel = Selector(text = body, type = 'html')
    alinks = sel.xpath('//a/@href').extract()
    mids = set()
    otherlinks = set()
    for l in alinks:
      l = get_abs_url(url, l)
      mr = self.mid_reg.search(l)
      if mr:
        mids.add(mr.groups()[0])
        continue
      pr = self.photo_reg.search(l)
      if pr:
        continue
      otherlinks.add(l)
    return list(mids), list(otherlinks)

  def parse(self, response):
    url = response.url.strip()
    try:
      page = response.body.decode(response.encoding)
      mids, olinks = self.__simple_links_extract(url, page)
      self.finished_count += 1
      # yield movie subject page
      for i in mids:
        movie_home = self.__build_movie_home_url(i)
        # movie json
        yield Request(self.__build_movie_json_url(i),
            headers = {'Referer': movie_home},
            callback = self.parse_movie_json)
        # movie page
        yield Request(movie_home, callback = self.parse_movie_page)
        # movie photo
        photo_list_pg = self.photos_list_page.replace('(*mid*)', i)
        yield Request(photo_list_pg,
            headers={
              'Referer': '%s' % (url),
              'Mid' : '%s' % (i)
              },
              callback = self.parse_photo_list_page)
      for i in olinks:
        yield Request(i,
            headers = {'Referer' : '%s' % (url)},
            callback = self.parse)
      self.log('Parse [%s] State: movie id[%s]: %s, others links:%s'
          %(url, len(mids), mids, len(olinks)), log.INFO)
    except Exception, e:
      print 'spider error:', e, url
      print traceback.format_exc()
      self.log('%s, %s, %s' % (url, e.message, traceback.format_exc()), log.ERROR)

  def parse_movie_page(self, response):
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

  def parse_movie_json(self, response):
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
  def __build_movie_json_url(self, mid):
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
