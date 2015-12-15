#!/usr/bin/python
#coding=utf-8
# Copyright 2015 LeTV Inc. All Rights Reserved.

__author__ = 'zhaojincheng@letv.com'

import time
import logging

from pymongo import MongoClient, DESCENDING, ReadPreference
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings

# from scrapy.utils.request import request_fingerprint
# from scrapy.exceptions import IgnoreRequest
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from ..common.logutil import Log
from ..common.extend_map_handler import ExtendMapHandler
from ..common.start_url_loads import StartUrlsLoader
from ..common.domain_parser import query_domain_from_url
from ..common.url_filter import UrlFilter
from ..common.url_normalize import UrlNormalize, get_abs_url
from ..common.utils import atoi, build_video, gen_docid, massage_data, source_set # get_video_attr_state
from ..core.urlmd5_inserter import UrlMd5Inserter
from ..core.items import crawldoc_to_item, fill_doc
# from ..core.filter_client import UrlFilterClient
from ..extractors.video_adaptor import VideoAdaptor
from ..proto.crawl.ttypes import CrawlDocType, ScheduleDocType, PageType, Location, Anchor, CrawlDocState, CrawlStatus
from ..proto.crawl_doc.ttypes import CrawlDoc
from ..proto.video.ttypes import MediaVideo, OriginalUser

category_order_dict = {
    u'音乐': CrawlDocType.HUB_OLD,
    u'MV'  : CrawlDocType.HUB_OLD,
}


doctype_prefix_map = {
  CrawlDocType.HOME: '__home',
  CrawlDocType.HUB_USER_RANK: '__user'
}


class LejianCrawler(Spider):
    name = 'lejian'
    allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
    start_url_loader = StartUrlsLoader.get_instance('../start_urls/', random_sort = True)
    start_urls = start_url_loader.get_start_urls()

    def __init__(self, *a, **kw):
      super(LejianCrawler, self).__init__(*a, **kw)
      self._handle_debug()
      self.extend_map_h_ = ExtendMapHandler.get_instance(LejianCrawler.start_url_loader,
                                                         module_path='le_crawler.common.lejian_video_settings', loger=self.logger_)
      self.finished_count = 0
      self.start_size = len(LejianCrawler.start_urls)
      self.callback_map_ = {PageType.HOME:        self.parse_home,
                            PageType.CHANNEL:     self.parse_channel,
                            PageType.HUB:         self.parse_list,
                            PageType.PLAY:        self.parse_page,
                            PageType.ORDER_TYPE:  self.parse_order_list}
      self.url_normalize_ = UrlNormalize.get_instance()
      self.video_adaptor_ = VideoAdaptor('list_templates')

    def _handle_debug(self):
      debug_mode = get_project_settings().get('DEBUG_MODE', True)
      self.logger_ = Log('', log_path='../log/spider.log', log_level=logging.INFO if debug_mode else logging.INFO).log
      # filter_host = get_project_settings()['DEBUG_HOST' if debug_mode else 'URL_FILTER_HOST']
      self.mongo_client_ = MongoClient('10.180.91.41:9224,10.180.91.115:9224,10.180.91.125:9224')
      self.mongo_client_.admin.authenticate('admin', 'NjlmNTdkNGQ4OWY')
      self.read_client_ = self.mongo_client_.crawl.schedule_info.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
      self._recrawl_collection = self.mongo_client_.crawl.recrawl_failed_info
      self._ensure_indexs()
      if debug_mode:
        self._request_seen = self._request_seen_debug
        self._insert_md5 = self._insert_md5_debug
        self.update_status = self._update_status_debug
        self.update_recrawl_info = self.update_recrawl_info_debug
        self.remove_recrawl_info = self.remove_recrawl_info_debug
        # self.url_filter_client_ = UrlFilterClient(filter_host,
        #                                           get_project_settings()['URL_FILTER_PORT'],
        #                                           self.logger_)
        # self.url_filter_local_ = UrlFilterClient(get_project_settings()['URL_FILTER_LOCAL_HOST'],
        #                                          get_project_settings()['URL_FILTER_LOCAL_PORT'],
        #                                          self.logger_)
      else:
        self.inserter_ = UrlMd5Inserter(Log('urlmd5', log_path='../log/urlmd5.log', log_level=logging.DEBUG).log)

    def _ensure_indexs(self):
      self._recrawl_collection.create_index('url', unique=True)
      self._recrawl_collection.create_index([('next_schedule_time', DESCENDING)])

    def _update_status_debug(self, url, data):
      pass

    def _request_seen_debug(self, url, dont_filter=False):
      return False

    def _insert_md5_debug(self, crawl_doc):
      pass

    def update_recrawl_info_debug(self, url, data):
      pass

    def remove_recrawl_info_debug(self, url):
      pass

    def _gen_videos_from_list(self, base_url, data, crawl_doc):
      user = None
      if 'user' in data:
        user = OriginalUser()
        user_dict = data.pop('user')
        user.url = user_dict.get('user_url', [None])[0]
        user.user_name = user_dict.get('user_name', [None])[0]
        user.portrait_url = user_dict.get('user_portrait', [None])[0]
        user.video_num = atoi(user_dict.get('user_video_num', [None])[0])
        user.play_num = atoi(user_dict.get('user_play_num', [None])[0])
        user.fans_num = atoi(user_dict.get('user_fans_num', [None])[0])
        user.channel_desc = user_dict.get('user_channel_desc', [None])[0]
        user.update_time = int(time.time())
      blocks = []
      for item in data.keys():
        if 'items' in item:
          blocks.extend(data.pop(item))
      if not blocks:
        return []

      result_videos = []
      for block in blocks:
        for k, v in block.items():
          block[k] = v[0]
        url = get_abs_url(base_url,  block.get('url'))
        block['url'] = url
        if not url or not url.startswith('http://'):
          continue
        if not self.extend_map_h_.accept_url(url):
          continue
        block['doc_id'] = gen_docid(url)
        block['id'] = str(block['doc_id'])
        block['discover_time'] = block['crawl_time'] = block['create_time'] = int(time.time())
        for k, v in data.items():
          if v and not block.get(k):
            block[k] = v
        massage_data(block, printable=False)
        video = build_video(block, crawl_doc)
        if video:
          video.user = user
          result_videos.append(video)
      return result_videos


    def _gen_video(self, video_info):
      if not video_info.get('url'):
        return None
      video = MediaVideo()
      for k, v in video_info.iteritems():
        if hasattr(video, k):
          setattr(video, k, v)
      return video

    def update_recrawl_info(self, url, data):
      if not url:
        return
      try:
        data.update({'update_time': int(time.time())})
        self._recrawl_collection.update({'url': url}, {'$set': data}, upsert=True)
      except:
        self.logger_.exception('failed update recrawl info: [%s]', url)

    def remove_recrawl_info(self, url):
      if not url:
        return
      try:
        self._recrawl_collection.remove({'url': url})
      except:
        self.logger_.exception('Failed remove recrawl_info, url:[%s]' % url)


    def update_status(self, doc, status):
      data = {'url': doc.url,
              'status': status,
              'update_time': int(time.time()),
              'doc_type': CrawlDocType._VALUES_TO_NAMES.get(doc.doc_type)}
      self.logger_.debug('update status: %s, url: %s', status, doc.url)
      try:
        self.mongo_client_.crawl.schedule_info.update({'url': doc.url}, {'$set': data}, upsert=True)
      except:
        self.logger_.exception('failed update mongo, url: %s, data: %s', doc.url, data)


    def _insert_md5(self, crawl_doc):
      if crawl_doc:
        if not self.inserter_.insert_urlmd5(crawl_doc.url):
          crawl_doc.page_state |= CrawlDocState.NO_MD5


    def _request_seen(self, url, dont_filter=False):
      if dont_filter:
        return False
      return self.read_client_.find({'url': url}).count()
      # if self.url_filter_local_.url_seen(url):
      #   return True
      # return self.url_filter_client_.url_seen(url)


    def _has_new_data(self, url, video):
      if not video:
        return False
      # new_state = get_video_attr_state(video)
      # if not new_state:
      #   return False
      # result = list(self.read_client_.find({'url': url}, {'attr_state': 1}))
      # if result:
      #   old_state = result[0].get('attr_state', None)
      #   if old_state and new_state | old_state > old_state:
      #     return True
      # return False


    def _create_request(self, url, page_type=PageType.PLAY, doc_type=CrawlDocType.PAGE_PLAY,
                        schedule_doc_type=ScheduleDocType.NORMAL, meta=None, headers=None, dont_filter=False, in_doc=None, is_next=False):
      headers = headers or {}
      referer = headers.get('Referer')
      if not url:
        self.logger_.error('empty url, referer: %s', referer)
        return None
      if isinstance(url, unicode):
        try:
          url = url.encode('utf-8', errors='ignore')
        except:
          self.logger_.exception('failed encode url, %s', url)
          return None
      if self._request_seen(url, dont_filter):
        # if self._has_new_data(url, meta.get('video', None)):
        #   self.logger_.info('request duplicated but has new datas, %s', url)
        # else:
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
      crawl_doc.domain = query_domain_from_url(crawl_doc.url)
      crawl_doc.domain_id = source_set.get(crawl_doc.domain, 0)
      if in_doc and in_doc.in_links:
        in_links = in_doc.in_links
      else:
        in_links = []
      if is_next and in_links:
        in_links = in_links[:-1]
      if referer:
        inlink_anchor = Anchor()
        inlink_anchor.url = referer
        if in_doc:
          inlink_anchor.discover_time = in_doc.discover_time
        inlink_anchor.doc_type = meta.get('doc_type', CrawlDocType.HUB_OTHER)
        inlink_anchor.location = Location()
        inlink_anchor.location.position = meta.get('position', 0)
        inlink_anchor.location.page_index = meta.get('page_index', 0)
        in_links.append(inlink_anchor)
        crawl_doc.in_links = in_links
      meta['crawl_doc'] = crawl_doc
      crawl_status = CrawlStatus.DISCOVERED if schedule_doc_type == ScheduleDocType.NORMAL else CrawlStatus.RECRAWLED
      self.update_status(crawl_doc, CrawlStatus._VALUES_TO_NAMES.get(crawl_status))
      # self.logger_.error('==>url: %s, domain: %s, domain_id: %s', crawl_doc.url, crawl_doc.domain, crawl_doc.domain_id)
      return Request(crawl_doc.raw_url,
                     callback=self.callback_map_[page_type],
                     meta=meta,
                     dont_filter=dont_filter)


    def start_requests(self):
      for url in LejianCrawler.start_urls:
        page_type = self.start_url_loader.get_property(url, 'type', 'list')
        doc_type_str = self.start_url_loader.get_property(url, 'extend_map', {}).get('doc_type', 'hub_home')
        if page_type == 'home':
          doc_type = CrawlDocType.HUB_HOME
          if doc_type_str == 'web_home':
            doc_type = CrawlDocType.HOME
          elif doc_type_str == 'user_home':
            doc_type = CrawlDocType.HUB_USER_RANK
          yield self._create_request(url, PageType.HOME, doc_type, meta={'doc_type': doc_type}, dont_filter=True)
        elif page_type == 'channel':
          yield self._create_request(url, PageType.CHANNEL, CrawlDocType.HUB_CATEGORY, dont_filter=True)
        elif page_type == 'list':
          if doc_type_str == 'web_home':
            yield self._create_request(url, PageType.HUB, CrawlDocType.HUB_TIME_HOME, meta={'doc_type': CrawlDocType.HOME}, dont_filter=True)
          elif doc_type_str == 'user_home':
            doc_type = CrawlDocType.HUB_USER_RANK
            yield self._create_request(url, PageType.HUB, doc_type, meta={'doc_type': CrawlDocType.HUB_USER_RANK}, dont_filter=True)
          else:
            yield self._create_request(url, PageType.HUB, CrawlDocType.HUB_TIME_HOME, dont_filter=True)
        elif page_type == 'play':
          yield self._create_request(url, PageType.PLAY, CrawlDocType.PAGE_PLAY, dont_filter=True)


    def parse_home(self, response):
      if not response:
        return
      doc = response.meta.get('crawl_doc')
      try:
        self.logger_.info('parse home url: %s', doc.url)
        self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED))
        self.remove_recrawl_info(doc.url)
        page = response.body.decode(response.encoding, 'ignore')
        doc_type = response.meta.get('doc_type', CrawlDocType.HUB_HOME)
        prefix = doctype_prefix_map.get(doc_type, '')
        sta, channel_links_map = self.extend_map_h_.extract_channel_links_map(body = page, pageurl = doc.url, prefix = prefix)
        if not sta:
          self.logger_.error('parse_home failed sta: %s, url: %s' % (sta, doc.url))
          return
        self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED))
        for link, link_map in channel_links_map.items():
          if doc_type == CrawlDocType.HOME:
            yield self._create_request(link, PageType.HUB, CrawlDocType.HUB_TIME_HOME, meta={'doc_type': CrawlDocType.HOME}, dont_filter=True, in_doc=doc)
          elif doc_type == CrawlDocType.HUB_USER_RANK:
            yield self._create_request(link, PageType.HUB, CrawlDocType.HUB_USER_RANK, meta={'doc_type': CrawlDocType.HUB_USER_RANK}, dont_filter=True, in_doc=doc)
          else:
            category = link_map.get('category')
            doc_type = category_order_dict.get(category, CrawlDocType.HUB_CATEGORY)
            yield self._create_request(link, PageType.CHANNEL, doc_type, dont_filter=True, in_doc=doc)
      except:
        self.logger_.exception('failed parse home, url: %s', doc.url)


    def parse_channel(self, response):
      if not response:
        return
      doc = response.meta.get('crawl_doc')
      self.logger_.info('parse channel url: %s', doc.url)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED))
      self.remove_recrawl_info(doc.url)
      try:
        page = response.body.decode(response.encoding, 'ignore')
        sub_category_num = response.meta.get('sub_category_num', 0)
        sta, has_sub_category, links_list = self.extend_map_h_.extract_sub_links_list(body=page, pageurl=doc.url,sub_category_num=sub_category_num)
        if not sta:
          self.logger_.error('parse channel url failed, url: [%s]', doc.url)
          return
        self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED))
        if not links_list:
          yield self._create_request(doc.url, PageType.ORDER_TYPE, CrawlDocType.HUB_TIME_HOME, dont_filter=True, in_doc=doc)
          links_list = []
        sub_category_num += 1
        for link in links_list:
          if has_sub_category:
            yield self._create_request(link,
                                       PageType.CHANNEL,
                                       CrawlDocType.HUB_CATEGORY,
                                       meta={'sub_category_num': sub_category_num},
                                       dont_filter=True,
                                       in_doc=doc)
          else:
            yield self._create_request(link, PageType.ORDER_TYPE, CrawlDocType.HUB_TIME_HOME, dont_filter=True, in_doc=doc)
      except:
        self.logger_.exception('failed parse channel, url: %s', doc.url)


    def parse_order_list(self, response):
      if not response:
        return
      doc = response.meta.get('crawl_doc')
      self.logger_.info('parse order list url: %s', doc.url)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED))
      self.remove_recrawl_info(doc.url)
      try:
        page = response.body.decode(response.encoding, 'ignore')
        sta, order_select, url_map = self.extend_map_h_.extract_orderlist_map(body=page, pageurl=doc.url)
        if sta and order_select:
          self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED))
          if order_select == 'hot':
            response.meta['doc_type'] = CrawlDocType.HUB_HOT_HOME
          else:
            response.meta['doc_type'] = CrawlDocType.HUB_TIME_HOME
        for item in self.parse_list(response):
          yield item
        if url_map:
          for order_type, link in url_map.items():
            if order_type and order_type == 'hot':
              doc_type = CrawlDocType.HUB_HOT_HOME
            else:
              doc_type = CrawlDocType.HUB_TIME_HOME
            yield self._create_request(link,
                                       PageType.HUB,
                                       doc_type,
                                       schedule_doc_type=doc.schedule_doc_type,
                                       meta={'doc_type': doc_type},
                                       dont_filter=True,
                                       in_doc=doc)
      except:
        self.logger_.exception('failed parse_order_list, url: %s', doc.url)


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
        if doc_type == CrawlDocType.HUB_USER_RANK:
          sta, result = self.extend_map_h_.extract_users(doc.url, page)
          if not sta:
            self.logger_.error('extract users error: %s', doc.url)
          else:
            for user_url in result:
              if isinstance(user_url, dict):
                url = user_url['user_url'][0]
                yield self._create_request(url, PageType.HUB, CrawlDocType.HUB_USER_VIDEOS,\
                    meta={'doc_type': CrawlDocType.HUB_USER_VIDEOS, 'user': user_url}, in_doc=doc)
              else:
                yield self._create_request(user_url, PageType.HUB, CrawlDocType.HUB_USER_VIDEOS,
                                         meta={'doc_type': CrawlDocType.HUB_USER_VIDEOS}, in_doc=doc)
          return

        category_list = None
        fill_doc(doc, response)
        parsed_data = self.video_adaptor_.get_static(doc)
        if not parsed_data:
          self.logger_.error('parse list failed, list url: %s', doc.url)
        elif 'no_data' in parsed_data:
          category_list = parsed_data.get('category_list')
          self.logger_.error('no data in this list page, list url: %s', doc.url)
        else:
          category_list = parsed_data.get('category_list')
          if 'user' not in parsed_data and 'user' in response.meta:
            parsed_data['user'] = response.meta.get('user')
          videos = self._gen_videos_from_list(doc.url, parsed_data, doc)
          for position, video in enumerate(videos):
            if doc.doc_type == CrawlDocType.HUB_TIME_HOME:
              next_doc_type = CrawlDocType.PAGE_TIME
            elif doc.doc_type == CrawlDocType.HUB_HOT_HOME:
              next_doc_type = CrawlDocType.PAGE_HOT
            else:
              next_doc_type = CrawlDocType.PAGE_PLAY
            new_request = self._create_request(video.url,
                                       PageType.PLAY,
                                       next_doc_type,
                                       schedule_doc_type=doc.schedule_doc_type,
                                       meta={'doc_type': doc_type,
                                             'page_index': page_index,
                                             'position': position +1,
                                             'video': video},
                                       headers={'Referer': doc.url},
                                       in_doc=doc)
            if new_request:
              yield crawldoc_to_item(new_request.meta['crawl_doc'])
              yield new_request

        status, results = self.extend_map_h_.parse_api(body=page, pageurl=doc.url, list_page=True)
        if not status:
          self.logger_.error('api parse failed, list url: %s', doc.url)
        else:
          for video_info in results:
            video = self._gen_video(video_info)
            video.category_list = category_list
            yield self._create_request(video_info['url'],
                                       PageType.PLAY,
                                       CrawlDocType.PAGE_TIME,
                                       schedule_doc_type=doc.schedule_doc_type,
                                       meta={'doc_type':doc_type,
                                             'page_index': page_index,
                                             'video': video},
                                       headers={'Referer': doc.url},
                                       in_doc=doc)

        if doc_type != CrawlDocType.HOME:
          sta, next_link = self.extend_map_h_.extract_next_url(body=page, pageurl=doc.url)
          if sta and next_link and not (doc_type == CrawlDocType.HUB_HOT_HOME and page_index > 5):
            if (doc_type == CrawlDocType.HUB_TIME_HOME) and page_index > 10:
              doc_type = CrawlDocType.HUB_OTHER
            yield self._create_request(next_link,
                                       PageType.HUB,
                                       doc_type,
                                       meta={'doc_type': doc_type,
                                             'page_index': page_index + 1},
                                       in_doc=doc,
                                       is_next=True)
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
      self.logger_.info('parse page url: %s referer--> %s', url, doc.in_links[0].url if doc.in_links else None)
      response = self.extend_map_h_.assemble_html(url, response)
      page = response.body.decode(response.encoding, 'ignore')
      crawl_item = crawldoc_to_item(doc, response)
      # if not self.extend_map_h_.filter_by_page(body=page, pageurl=url): # for toutiao
      self._insert_md5(doc)
      yield crawl_item

      sta, result = self.extend_map_h_.extract_users(url, page)
      if result:
        for user_url in result:
          self.logger_.debug('extract user url from %s : %s', url, user_url)
          yield self._create_request(user_url,
                                     PageType.HUB,
                                     CrawlDocType.HUB_USER_VIDEOS,
                                     meta={'doc_type': CrawlDocType.HUB_USER_VIDEOS},
                                     in_doc=doc)

      status, extend_url = self.extend_map_h_.extract_urls(body=page, pageurl=url, extract_relative=True)
      if not status:
        self.logger_.error('parse relative videos failed,  video url: %s' %  url)
      else:
        for position, link in enumerate(extend_url):
          yield self._create_request(link,
                                     PageType.PLAY,
                                     CrawlDocType.PAGE_PLAY,
                                     meta={'doc_type':CrawlDocType.HUB_RELATIVES},
                                     headers={'Referer': url},
                                     in_doc=doc)

      status, results = self.extend_map_h_.parse_api(body = page, pageurl = url, list_page = False)
      if not status:
        self.logger_.error('parse api failed, play url: %s', url)
      else:
        for video_info in results:
          yield self._create_request(video_info['url'],
                                     PageType.PLAY,
                                     CrawlDocType.PAGE_PLAY,
                                     meta={'doc_type': CrawlDocType.HUB_RELATIVES,
                                           'video': self._gen_video(video_info)},
                                     headers={'Referer': url},
                                     in_doc=doc)

