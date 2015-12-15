__author__ = 'zhaojincheng'

import traceback
import urlparse
import logging
import time
import re
import json
import copy

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from pybloom import ScalableBloomFilter

from ..common.logutil import Log
from ..core.items import crawldoc_to_youtube_item
from ..common.url_filter import UrlFilter
from ..proto.crawl.ttypes import CrawlDocType, ScheduleDocType, PageType, Location, Anchor, CrawlDocState, CrawlStatus, SourceType
from ..proto.crawl_doc.ttypes import CrawlDoc
#from ..common.utils import safe_eval
from ..core.url_filter_client import UrlFilterClient
from ..common.parse_youtube import parse_channel_detail



class YouTubeCrawler(Spider):
  name = 'youtube'
  allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')

  def __init__(self, *a, **kw):
    super(YouTubeCrawler, self).__init__(*a, **kw)
    self.logger_ = Log('', log_path='../log/spider.log', log_level=logging.INFO).log
    self.finished_count = 0
    self.callback_map_ = {PageType.HUB:                   self.parse_list,
                          PageType.HOME:                  self.parse_channel,
                          PageType.CHANNEL:               self.parse_playlist,
                          PageType.PLAY:                  self.parse_page,
                          PageType.RELATED_CHANNEL:       self.parse_relatedchannel}
    self._init_client()
    self.start_size = self._starturl_collection.count()
    self._sub_key_pattern = re.compile(r"&key=.*")
    self.deduper_ = ScalableBloomFilter(100000, 0.0001, 4)
    self.url_filter_client_ = UrlFilterClient(get_project_settings()['CRAWLDOC_SCHEDULER_HOST'],
                                              get_project_settings()['URL_FILTER_PORT'],
                                              self.logger_)

  def _init_client(self):
    try:
      client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')
      self._db = client.admin
      self._db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
      if get_project_settings()['DEBUG_MODE']:
        #print 'open debug_model ...'
        self._collection = self._db.debug_schedule_info
        self._starturl_collection = self._db.debug_starturl_info
        self._recrawl_collection = self._db.debug_recrawl_failed_info
        self._channel_collection = self._db.debug_channel_info
      else:
        self._collection = self._db.schedule_info
        self._starturl_collection = self._db.starturl_info
        self._recrawl_collection = self._db.recrawl_failed_info
        self._channel_collection = self._db.channel_info
      self._ensure_indexs()
    except Exception, e:
      self._collection = None
      self.logger_.exception('failed to connect to mongodb...')

  def _ensure_indexs(self):
    #index_info = self._collection.index_information()
    #if not index_info or 'url_1' not in index_info or 'update_time_-1' not in index_info:
    from pymongo import IndexModel, ASCENDING, DESCENDING
    self._collection.create_index('url', unique=True)
    self._collection.create_index([('update_time', DESCENDING)])
    self._recrawl_collection.create_index('url', unique=True)
    self._recrawl_collection.create_index([('next_schedule_time', DESCENDING)])
    self._channel_collection.create_index('channel_id', unique=True)

  def _strip_key(self, url):
    if not url:
      self.logger_.error('empty url ......')
      return None
    return self._sub_key_pattern.sub('', url)

  def update_status(self, doc, status):
    url = self._strip_key(doc.url)
    if not url:
      return
    data = {'url': doc.url,
            'status': status,
            'update_time': int(time.time()),
            'doc_type': CrawlDocType._VALUES_TO_NAMES.get(doc.doc_type)}
    try:
      self._collection.update({'url': url}, {'$set': data}, upsert=True)
    except Exception, e:
      self.logger_.exception('Failed update status:[%s], data: %s' % (url, data))

  def update_recrawl_info(self, url, data):
    url = self._strip_key(url)
    if not url:
      return
    data.update({'update_time': int(time.time())})
    #print 'update recrawl info, url: %s' % url
    try:
      self._recrawl_collection.update({'url': url}, {'$set': data}, upsert=True)
    except:
      self.logger_.exception('Failed update recrawl info:[%s]' % url)

  def remove_recrawl_info(self, url):
    url = self._strip_key(url)
    if not url:
      return
    #print 'remove recrawl info, url: %s' % url
    try:
      self._recrawl_collection.remove({'url': url})
    except:
      self.logger_.exception('Failed remove recrawl_info, url:[%s]' % url)

  def upsert_start_url(self, channel, channel_data):
    if not channel:
      return False
    try:
      doc = self._starturl_collection.find({'channel': channel})
      doc = [i for i in doc]
      if doc:
        self.logger_.info('exist start url, channel: [%s]', channel)
        return False
      else:
        self._starturl_collection.insert(channel_data, continue_on_error=True)
        self.logger_.info('insert new start url, channel: [%s]', channel)
        return True
    except:
      self.logger_.exception('Failed upsert channel: [%s]', channel)
      return False

  def upsert_channel_info(self, channel_dict):
    if not channel_dict:
      return False
    try:
      self._channel_collection.update({'channel_id': channel_dict['channel_id']}, {'$set': channel_dict}, upsert=True)
      return True
    except:
      self.logger_.exception('Failed upsert channel_info channel: [%s]', channel_dict.get('channel_id', None))
      return False

  def _request_seen(self, url, dont_filter=False):
    if dont_filter:
      return False
    if not url:
      return True
    if self.deduper_.add(url):
      return True
    return self.url_filter_client_.url_seen(url)

  def _create_request(self, url, page_type, doc_type, schedule_doc_type=ScheduleDocType.NORMAL, meta=None, headers=None, dont_filter=True, in_doc=None, is_next=False):
    if self._request_seen(url, dont_filter):
      self.logger_.info('request duplicated, %s', url)
      return None
    meta = meta or {}
    headers = headers or {}

    crawl_doc = CrawlDoc()
    crawl_doc.url = url
    crawl_doc.discover_time = int(time.time())
    crawl_doc.page_type = page_type
    crawl_doc.doc_type = doc_type
    crawl_doc.schedule_doc_type = schedule_doc_type

    if in_doc and in_doc.in_links:
      in_links = in_doc.in_links
      in_links = copy.deepcopy(in_links)
    else:
      in_links = []
    referer = headers.get('Referer')
    if not is_next and referer:
      inlink_anchor = Anchor()
      inlink_anchor.url = self._strip_key(referer)
      if in_doc:
        inlink_anchor.discover_time = in_doc.discover_time
      inlink_anchor.doc_type = meta.get('doc_type', CrawlDocType.HUB_OTHER)
      inlink_anchor.location = Location()
      inlink_anchor.location.position = meta.get('position', 0)
      inlink_anchor.location.page_index = meta.get('page_index', 0)
      in_links.append(inlink_anchor)
    if in_links:
     crawl_doc.in_links = in_links
    meta['crawl_doc'] = crawl_doc
    crawl_status = CrawlStatus.DISCOVERED if schedule_doc_type == ScheduleDocType.NORMAL else CrawlStatus.RECRAWLED
    self.update_status(crawl_doc, CrawlStatus._VALUES_TO_NAMES.get(crawl_status))
    return Request(url,
                   callback=self.callback_map_[page_type],
                   meta=meta,
                   dont_filter=dont_filter)


  def start_requests(self):
    for item in self._starturl_collection.find({}):
      item.pop('_id', None)
      exmap = item
      source = item.get('source', None)
      exmap['source'] = source
      kind = item.get('kind', None)
      user = item.get('user', None)
      channel = item.get('channel', None)
      if source == 'youtube':
        if kind == 'channel':
          part = 'snippet'
          maxResults = 50
          api = 'https://www.googleapis.com/youtube/v3/playlists?part=%s&maxResults=%s&channelId=%s' % \
              (part, maxResults, channel)
          yield self._create_request(api, PageType.CHANNEL, CrawlDocType.HUB_HOME, meta={'extend_map': exmap})
      elif source in ['youtube_pop', 'custom', 'socialblade', 'related_channel']:
        part = 'snippet,statistics,contentDetails'
        if kind == 'user':
          api = 'https://www.googleapis.com/youtube/v3/channels?part=%s&forUsername=%s' % \
              (part, user)
        elif kind == 'channel':
          api = 'https://www.googleapis.com/youtube/v3/channels?part=%s&id=%s' % \
              (part, channel)
        yield self._create_request(api, PageType.HOME, CrawlDocType.HUB_HOME, meta={'extend_map': exmap})


  def parse_channel(self, response):
    try:
      items = []
      url = response.url.strip()
      headers = {'Referer': url}
      doc = response.meta.get('crawl_doc')
      #print 'parse_channel url:', url
      self.logger_.error('parse_channel url: %s' % url)
      page = response.body.decode(response.encoding)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED))
      #self.update_recrawl_info(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      extend_map = response.meta.get('extend_map', {})
      rep_dict = json.loads(page)
      datas = rep_dict.get('items', [])
      if not datas:
        self.logger_.error('parse channel failed, url: [%s]' % url)
        return None
      data = datas[0]
      exmap = {}
      exmap.update(extend_map)
      exmap['channel_dict'] = parse_channel_detail(data, extend_map)
      self.upsert_channel_info(exmap['channel_dict'])
      kind = exmap.get('kind', None)
      user = exmap.get('user', None)
      channel = data.get('id', None)
      exmap['channel'] = channel
      channel_title = data.get('snippet', {}).get('title', None)
      if kind == 'user' and channel:
        self._starturl_collection.update({'kind': 'user', 'user': user}, {'$set': {'channel': channel, 'channel_title': channel_title}})
      upload_playlist = data.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads', None)
      if not upload_playlist:
        return None
      exmap['playlist'] = upload_playlist 
      part = 'snippet'
      maxResults = 50
      api = u"https://www.googleapis.com/youtube/v3/playlistItems?part=%s&maxResults=%s&playlistId=%s" % \
          (part, maxResults, upload_playlist)
      items.append(self._create_request(api, PageType.HUB, CrawlDocType.HUB_TIME_HOME, meta={'extend_map': exmap}, headers=headers, in_doc=doc))
      """
      if channel:
        relatedchannel_api = u"https://www.googleapis.com/youtube/v3/channels?part=brandingSettings&id=%s" % channel
        items.append(self._create_request(api, PageType.RELATED_CHANNEL, CrawlDocType.HUB_CATEGORY, headers=headers in_doc=doc))
      """
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED))
      self.remove_recrawl_info(url)
      return items
    except Exception, e:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      self.logger_.exception('Failed parse_channel:%s, url:%s' % (msg, url))

  def parse_relatedchannel(self, responose):
    try:
      items = {}
      url = response.url.strip()
      headers = {'Referer': url}
      doc = response.meta.get('crawl_doc')
      self.logger_.error('parse_relatedchannel url: %s' % url)
      exmap = response.meta.get('extend_map', {})
      page = response.body.decode(response.encoding)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOAD))
      #self.update_recrawl_info(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      rep_dict = json.loads(page)
      datas = rep_dict.get('items', [])
      if not datas:
        self.logger_.error('parse channel failed, url: [%s]' % url)
        return None
      data = datas[0]
      featuredChannelsUrls = data.get('brandingSettings', {}).get('channel', {}).get('featuredChannelsUrls', [])
      if featuredChannelsUrls:
        for channelId in featuredChannelsUrls:
          part = 'contentDetails'
          api = 'https://www.googleapis.com/youtube/v3/channels?part=%s&id=%s' % \
              (part, channelId)
          items.append(self._create_request(api, PageType.HOME, CrawlDocType.HUB_TIME_HOME, meta={'extend_map': exmap}, headers=headers, in_doc=doc))
      self.update_status(doc, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED)})
      self.remove_recrawl_info(url)
      return items
    except:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      self.logger_.exception('Failed parse_relatedchannel, url:%s' % url)


  def parse_playlist(self, response):
    try:
      items = []
      url = response.url.strip()
      headers = {'Referer': url}
      doc = response.meta.get('crawl_doc')
      #print 'parse_playlist url:', url
      self.logger_.error('parse_playlist url: %s' % url)
      page = response.body.decode(response.encoding)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED))
      #self.update_recrawl_info(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      exmap = response.meta.get('extend_map', {})
      rep_dict = json.loads(page)
      data = rep_dict.get('items', [])
      if not data:
        self.logger_.error('parse playlist failed for no items url: [%s]' % url)
        return None
      nextPageToken = rep_dict.get('nextPageToken', None)
      if nextPageToken:
        part = 'snippet'
        maxResults = 50
        channel = exmap.get('channel', None)
        if channel:
          next_api = u"https://www.googleapis.com/youtube/v3/playlists?part=%s&maxResults=%s&pageToken=%s&channelId=%s" % \
                (part, maxResults, nextPageToken, channel)
          items.append(self._create_request(next_api, PageType.CHANNEL, CrawlDocType.HUB_HOME, meta={'extend_map': exmap}, headers=headers, in_doc=doc, is_next=True))
      for sub_data in data:
        playlist = sub_data.get('id')
        part = 'snippet'
        maxResults = 50
        api = u"https://www.googleapis.com/youtube/v3/playlistItems?part=%s&maxResults=%s&playlistId=%s" % \
                (part, maxResults, playlist)
        extend_map = {}
        extend_map['playlist'] = playlist
        extend_map.update(exmap)
        items.append(self._create_request(api, PageType.HUB, CrawlDocType.HUB_TIME_HOME,
                                            meta={'extend_map': extend_map, 'doc_type': CrawlDocType.HUB_TIME_HOME}, headers=headers, in_doc=doc))
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED))
      self.remove_recrawl_info(url)
      return items
    except Exception, e:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      self.log('Failed parse_channel:%s, url:%s' % (msg, url), log.ERROR)


  def parse_list(self, response):
    try:
      url = response.url.strip()
      headers = {'Referer': url}
      #print 'parse_list url:', url
      self.logger_.error('parse_list url: %s' % url)
      doc = response.meta.get('crawl_doc')
      page = response.body.decode(response.encoding)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED))
      #self.update_recrawl_info(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      doc_type = response.meta.get('doc_type', CrawlDocType.HUB_OTHER)
      page_index = response.meta.get('page_index', 1)
      exmap = response.meta.get('extend_map', {})
      source = exmap.get('source', None)
      rep_dict = json.loads(page)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED))
      self.remove_recrawl_info(url)
      nextPageToken = rep_dict.get('nextPageToken', None)
      if nextPageToken:
        playlist = exmap.get('playlist')
        part = 'snippet'
        maxResults = 50
        next_api = u"https://www.googleapis.com/youtube/v3/playlistItems?part=%s&maxResults=%s&pageToken=%s&playlistId=%s" % \
                (part, maxResults, nextPageToken, playlist)
        if page_index > 1:
          dont_filter = False
          doc_type = CrawlDocType.HUB_OTHER
        else:
          dont_filter = True
          doc_type = CrawlDocType.HUB_TIME_HOME
        yield self._create_request(next_api,
                                   PageType.HUB,
                                   doc_type,
                                   meta={'doc_type': doc_type,
                                         'page_index': page_index + 1,
                                         'extend_map': exmap},
                                   headers=headers,
                                   dont_filter=dont_filter,
                                   in_doc=doc,
                                   is_next=True)
      data = rep_dict.get('items', [])
      if not data:
        self.logger_.error('parse list failed for no items url: [%s]' % url)
      else:
        for position, sub_data in enumerate(data):
          videoId = sub_data.get('snippet', {}).get('resourceId', {}).get('videoId', None)
          extend_map = {}
          extend_map['video'] = videoId
          extend_map.update(exmap)
          if source == 'youtube':
            part = 'snippet'
          else:
            part = 'contentDetails,player,recordingDetails,snippet,statistics,status,topicDetails'
          api = u"https://www.googleapis.com/youtube/v3/videos?part=%s&id=%s" % \
                (part, videoId)
          yield self._create_request(api,
                                     PageType.PLAY,
                                     CrawlDocType.PAGE_PLAY,
                                     schedule_doc_type=doc.schedule_doc_type,
                                     meta={'doc_type':doc_type,
                                           'page_index': page_index,
                                           'position': position +1,
                                           'extend_map': extend_map},
                                     headers=headers,
                                     dont_filter=False,
                                     in_doc=doc)
    except Exception, e:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      self.log('Failed parse_channel:%s, url:%s' % (msg, url), log.ERROR)


  def parse_page(self, response):
    try:
      items = []
      url = response.url.strip()
      headers = {'Referer': url}
      doc = response.meta.get('crawl_doc')
      #print 'parse_video url:', url
      self.logger_.error('parse_video url: %s' % url)
      page = response.body.decode(response.encoding)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED))
      self.remove_recrawl_info(url)
      exmap = response.meta.get('extend_map', {})
      source = exmap.get('source', None)
      if source == 'youtube':
        rep_dict = json.loads(page)
        datas = rep_dict.get('items', [])
        if not datas:
          self.logger_.error('failed to pase data, url: [%s]', url)
          return
        data = datas[0]
        channel_id = data.get('snippet', {}).get('channelId', None)
        if not channel_id:
          self.logger_.error('failed to get channel_id, url: [%s]', url)
          return
        channel_data = {'channel': channel_id, 'kind': 'channel', 'source': 'youtube_pop'}
        if self.upsert_start_url(channel_id, channel_data):
          part = 'snippet,statistics,contentDetails'
          api = 'https://www.googleapis.com/youtube/v3/channels?part=%s&id=%s' % \
                (part, channel_id)
          items.append(self._create_request(api, PageType.HOME, CrawlDocType.HUB_HOME, meta={'extend_map': channel_data}, headers=headers, in_doc=doc))
      else:  
        youtube_item = crawldoc_to_youtube_item(doc, response)
        if youtube_item:
          items.append(youtube_item)
      self.update_status(doc, CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED))
      return items
    except Exception, e:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      self.log('Failed parse_page:%s, url:%s' % (msg, url), log.ERROR)

