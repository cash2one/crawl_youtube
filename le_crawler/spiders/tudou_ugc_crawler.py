#!/usr/bin/python
#coding=utf-8
# Copyright 2015 LeTV Inc. All Rights Reserved.


import time
import logging
import letvbase

from pymongo import MongoClient, DESCENDING
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings

# from scrapy.utils.request import request_fingerprint
# from scrapy.exceptions import IgnoreRequest
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from ..core.items import CrawlerItem, crawldoc_to_item
from ..common.start_url_loads import StartUrlsLoader
from ..common.url_filter import UrlFilter
from ..common.time_parser import *
from ..common.url_normalize import UrlNormalize, get_abs_url
from ..proto.crawl_doc.ttypes import CrawlDoc
from ..core.docid_generator import gen_docid
from ..proto.crawl.ttypes import CrawlDocType, ScheduleDocType, PageType, Location, Anchor, CrawlDocState, CrawlStatus

from lejian_crawler import LejianCrawler

category_dict = {u'搞笑': u'搞笑', u'恶搞': u'搞笑', u'爆笑': u'搞笑', u'吐槽': u'搞笑', u'幽默': u'搞笑', u'逗比': u'搞笑',\
    u'菜谱': u'生活', u'美食': u'生活', u'养生': u'生活', u'健康': u'生活', u'美妆': u'生活', u'时尚': u'生活', u'萌宠': u'生活',\
    u'宝宝': u'生活', u'亲子': u'生活', u'母婴': u'生活', u'舞蹈': u'生活', u'广场舞': u'生活', u'婚礼': u'生活',\
    u'明星': u'娱乐', u'粉丝': u'娱乐', u'电影': u'娱乐', u'片花': u'娱乐', u'预告片': u'娱乐', u'MV': u'娱乐', u'Tfboys': u'娱乐', \
    u'杨洋': u'娱乐', u'李易峰': u'娱乐', u'赵丽颖': u'娱乐', u'angelababy': u'娱乐', \
    u'美女主播': u'美女', u'美女写真': u'美女', u'模特': u'美女', u'丝袜美腿': u'美女', u'美女主播': u'美女', \
    u'英雄联盟': u'游戏', u'data': u'游戏', u'LOL': u'游戏', u'魔兽世界': u'游戏', u'游戏': u'游戏',\
    u'穿越火线': u'游戏', u'穿越火线': u'游戏', u'炉石传说': u'游戏', u'原创': u'原创', u'网络剧': u'原创',\
    u'网络剧': u'原创', u'微视频': u'原创', u'汽车': u'汽车', u'试驾': u'汽车', u'汽车改装': u'汽车',\
    u'车保养': u'汽车', u'车祸': u'汽车', u'车评': u'汽车', u'赛车': u'汽车', u'特斯拉': u'汽车',\
    u'足球': u'运动', u'世界杯': u'运动', u'英超': u'运动', u'篮球': u'运动', u'NBA': u'运动',\
    u'网球': u'运动', u'羽毛球': u'运动', u'男篮': u'运动', u'斯诺克': u'运动', u'库里': u'运动', \
    u'科比': u'运动', u'运动会': u'运动', u'旅游': u'旅游', u'游玩': u'旅游', u'旅行': u'旅游', \
    u'教育': u'教育', u'培训': u'教育', u'教学': u'教育', u'智能': u'科技', u'创新': u'科技', \
    u'科技': u'科技', u'手机': u'科技', u'笔记本电脑': u'科技', u'高科技': u'科技', u'军事': u'军事', \
    u'军情': u'军事', u'海军': u'军事', u'空军': u'军事', u'陆军': u'军事', u'动画': u'动漫', \
    u'动漫': u'动漫', u'cosplay': u'动漫', u'音乐': u'音乐', u'歌曲': u'音乐', u'翻唱': u'音乐', \
    u'演唱会': u'音乐', u'中国好声音': u'音乐'}


class TudouUgcCrawler(LejianCrawler):
    name = 'tudouugc'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/', random_sort = True)
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(TudouUgcCrawler, self).__init__(*a, **kw)
      self.calc_ts_obj = TimeParser()

    def _create_request(self, url, page_type=PageType.PLAY, doc_type=CrawlDocType.PAGE_PLAY,
                        schedule_doc_type=ScheduleDocType.NORMAL, meta=None, headers=None, dont_filter=False):
      headers = headers or {}
      referer = headers.get('Referer')
      if not url:
        self.logger_.error('empty url, referer: %s', referer)
        return None
      if self._request_seen(url, dont_filter):
        self.logger_.info('request duplicated, %s', url)
        return None

      meta = meta or {}
      crawl_doc = CrawlDoc()
      crawl_doc.raw_url = url
      crawl_doc.url = self.url_normalize_.get_unique_url(url) or url
      crawl_doc.id = gen_docid(crawl_doc.url)
      crawl_doc.doc_type = doc_type
      crawl_doc.page_type = page_type
      crawl_doc.discover_time = int(time.time())
      crawl_doc.schedule_doc_type = schedule_doc_type
      crawl_doc.video = meta.get('video', None)
      if referer:
        inlink_anchor = Anchor()
        inlink_anchor.url = referer
        inlink_anchor.discover_time = crawl_doc.discover_time
        inlink_anchor.doc_type = meta.get('doc_type', CrawlDocType.HUB_OTHER)
        inlink_anchor.location = Location()
        inlink_anchor.location.position = meta.get('position', 0)
        inlink_anchor.location.page_index = meta.get('page_index', 0)
        crawl_doc.in_links = [inlink_anchor]
      meta['crawl_doc'] = crawl_doc

      crawl_status = CrawlStatus.DISCOVERED if schedule_doc_type == ScheduleDocType.NORMAL else CrawlStatus.RECRAWLED
      self.update_status(crawl_doc, CrawlStatus._VALUES_TO_NAMES.get(crawl_status))
      return Request(crawl_doc.url,
                     callback=self.callback_map_[page_type],
                     meta=meta,
                     dont_filter=dont_filter)


    def start_requests(self):
      for url in TudouUgcCrawler.start_urls:
        page_type = self.start_url_loader.get_property(url, 'type', 'list')
        doc_type_str = self.start_url_loader.get_property(url, 'extend_map', {}).get('doc_type', 'hub_home')
        if page_type == 'list':
          if doc_type_str == 'web_home':
            yield self._create_request(url, PageType.HUB, CrawlDocType.HUB_TIME_HOME, meta={'doc_type': CrawlDocType.HOME}, dont_filter=False)
          else:
            yield self._create_request(url, PageType.HUB, CrawlDocType.HUB_TIME_HOME, dont_filter=False)


    def parse_list(self, response):
      if not response:
        return
      doc = response.meta.get('crawl_doc')
      self.logger_.info('parse_list url: %s', doc.url)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED))
      self.remove_recrawl_info(doc.url)
      response = self.extend_map_h_.assemble_html(doc.url, response)
      try:
        page = response.body.decode(response.encoding, 'ignore')
        doc_type = response.meta.get('doc_type', CrawlDocType.HUB_OTHER)
        page_index = response.meta.get('page_index', 1)

        category_list = None
        crawl_item = CrawlerItem()
        crawldoc_to_item(response, crawl_item)
        yield crawl_item
        parsed_data = self.video_adaptor_.get_static(crawl_item['crawl_doc'])
        if not parsed_data:
          self.logger_.error('parse list failed, list url: %s', doc.url)
        elif 'no_data' in parsed_data:
          category_list = parsed_data.get('category_list')
          self.logger_.error('no data in this list page, list url: %s', doc.url)
          return
        elif 'items' in parsed_data:
          category_list = parsed_data.get('category_list')
          if ',' in category_list:
            category_list = category_list.split(',')[0]
          if category_list and category_list in category_dict:
            category_list = category_dict[category_list]
          else:
            self.logger_.info('%(url)s has no relative category, category_list: %(category_list)s' %{'url' : video.url, 'category_list': category_list})
          videos = self._gen_videos_from_list(doc.url, parsed_data, crawl_item['crawl_doc'])
          for position, video in enumerate(videos):
            #判断上传时间是否为今天，如果是今天继续请求
            if video.showtime:
              showtime = video.showtime
              showtime_temp = self.calc_ts_obj.timestamp(showtime, refer_time=time.time())
              timearray = time.localtime(showtime_temp)
              other_showtime = time.strftime("%Y-%m-%d", timearray)
              current_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
              if other_showtime != current_time:
                self.logger_.info('%(url)s  off date, showtime: %(showtime)s' %{'url' : video.url, 'showtime': showtime})
                continue
            video.category_list = category_list
            if doc.doc_type == CrawlDocType.HUB_TIME_HOME:
              next_doc_type = CrawlDocType.PAGE_TIME
            elif doc.doc_type == CrawlDocType.HUB_HOT_HOME:
              next_doc_type = CrawlDocType.PAGE_HOT
            else:
              next_doc_type = CrawlDocType.PAGE_PLAY
            yield self._create_request(video.url,
                                       PageType.PLAY,
                                       next_doc_type,
                                       schedule_doc_type=doc.schedule_doc_type,
                                       meta={'doc_type': doc_type,
                                             'page_index': page_index,
                                             'position': position +1,
                                             'video': video},
                                       headers={'Referer': doc.url})
        if doc_type != CrawlDocType.HOME:
          sta, next_link = self.extend_map_h_.extract_next_url(body=page, pageurl=doc.url)
          if sta and next_link and not (doc_type == CrawlDocType.HUB_HOT_HOME and page_index > 5):
            if (doc_type == CrawlDocType.HUB_TIME_HOME) and page_index > 10:
              doc_type = CrawlDocType.HUB_OTHER
            yield self._create_request(next_link,
                                       PageType.HUB,
                                       doc_type,
                                       meta={'doc_type': doc_type,
                                             'page_index': page_index + 1})
        self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED))
      except:
        self.logger_.exception('failed parse list, url: %s', doc.url)


    def parse_page(self, response):
      if not response:
        return
      doc = response.meta.get('crawl_doc')
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED))
      # self.remove_recrawl_info(doc.url)
      url = doc.url
      self.logger_.info('parse_page url: %s referer--> %s' % (url, doc.in_links[0].url if doc.in_links else None))
      response = self.extend_map_h_.assemble_html(url, response)
      page = response.body.decode(response.encoding, 'ignore')
      crawl_item = CrawlerItem()
      crawldoc_to_item(response, crawl_item)
      if not self.extend_map_h_.filter_by_page(body = page, pageurl = url):
        self._insert_md5(doc, crawl_item)
        yield crawl_item
