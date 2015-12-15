__author__ = 'zhaojincheng'

import traceback
import urlparse
import logging
import time
import re

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from pybloom import ScalableBloomFilter

from ..common.logutil import Log
from ..core.items import YoutubeItem
from ..common.url_filter import UrlFilter
from ..proto.crawl.ttypes import CrawlDocType, ScheduleDocType, PageType, Location, Anchor, CrawlDocState, CrawlStatus, SourceType
from ..proto.crawl_doc.ttypes import CrawlDoc
from ..common.utils import safe_eval
from ..core.url_filter_client import UrlFilterClient


#key = 'AIzaSyADAw1LV8-DmiqJNvYD7qxTRn7VclazxAE'


class YouTubeCrawler(Spider):
  name = 'youtube'
  allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')

  def __init__(self, *a, **kw):
    super(YouTubeCrawler, self).__init__(*a, **kw)
    self._logger = Log('spider', log_path='../log/spider.log', log_level=logging.INFO).log
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
                                              self._logger)

  def _init_client(self):
    try:
      client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')
      self._db = client.admin
      self._db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
      if get_project_settings()['DEBUG_MODEL']:
        self._collection = self._db.debug_schedule_info
        self._starturl_collection = self._db.debug_starturl_info
        self._recrawl_collection = self._db.debug_recrawl_info
      else:
        self._collection = self._db.schedule_info
        self._starturl_collection = self._db.starturl_info
        self._recrawl_collection = self._db.recrawl_info
      self._ensure_indexs()
    except Exception, e:
      self._collection = None
      self._logger.exception('failed to connect to mongodb...')

  def _ensure_indexs(self):
    #index_info = self._collection.index_information()
    #if not index_info or 'url_1' not in index_info or 'update_time_-1' not in index_info:
    from pymongo import IndexModel, ASCENDING, DESCENDING
    self._collection.create_index('url', unique=True)
    self._collection.create_index([('update_time', DESCENDING)])
    self._recrawl_collection.create_index('url', unique=True)

  def _strip_key(self, url):
    if not url:
      self._logger.error('empty url ......')
      return None
    return self._sub_key_pattern.sub('', url)

  def update_status(self, url, data):
    url = self._strip_key(url)
    if not url:
      return
    data.update({'update_time': int(time.time())})
    try:
      self._collection.update({'url': url}, {'$set': data}, upsert=True)
    except Exception, e:
      self._logger.exception('Failed update status:[%s]' % url)
      raise

  def update_recrawl_info(self, url, data):
    url = self._strip_key(url)
    if not url:
      return
    data.update({'update_time': int(time.time())})
    #print 'update recrawl info, url: %s' % url
    try:
      self._recrawl_collection.update({'url': url}, {'$set': data}, upsert=True)
    except Exception, e:
      self._logger.exception('Failed update recrawl info:[%s]' % url)

  def remove_recrawl_info(self, url):
    url = self._strip_key(url)
    if not url:
      return
    #print 'remove recrawl info, url: %s' % url
    try:
      self._recrawl_collection.remove({'url': url})
    except Exception, e:
      self._logger.exception('Failed remove recrawl_info, url:[%s]' % url)

  def _request_seen(self, url, dont_filter=False):
    if dont_filter:
      return False
    if not url:
      return True
    if self.deduper_.add(url):
      return True
    return self.url_filter_client_.url_seen(url)

  def _create_request(self, url, page_type, doc_type, schedule_doc_type=ScheduleDocType.NORMAL, meta=None, headers=None, dont_filter=True):
    if self._request_seen(url, dont_filter):
      self._logger.info('request duplicated, %s', url)
      return None
    meta = meta or {}
    headers = headers or {}

    crawl_doc = CrawlDoc()
    crawl_doc.url = url
    crawl_doc.discover_time = int(time.time())
    crawl_doc.page_type = page_type
    crawl_doc.doc_type = doc_type
    crawl_doc.schedule_doc_type = schedule_doc_type

    referer = headers.get('Referer')
    if referer:
      inlink_anchor = Anchor()
      inlink_anchor.url = self._strip_key(referer)
      inlink_anchor.discover_time = crawl_doc.discover_time
      inlink_anchor.doc_type = meta.get('doc_type', CrawlDocType.HUB_OTHER)
      inlink_anchor.location = Location()
      inlink_anchor.location.position = meta.get('position', 0)
      inlink_anchor.location.page_index = meta.get('page_index', 0)
      crawl_doc.in_links = [inlink_anchor]
    meta['crawl_doc'] = crawl_doc
    self.update_status(url, {'doc_type': CrawlDocType._VALUES_TO_NAMES.get(doc_type),
      'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DISCOVERED)})
    return Request(url,
                   callback=self.callback_map_[page_type],
                   meta=meta,
                   dont_filter=dont_filter)


  def start_requests(self):
    #items = []
    source_dict = {'youtube': SourceType.YOUTUBE,
                   'custom':SourceType.CUSTOM, 
                   'socialblade': SourceType.SOCIALBLADE, 
                   'related_channel': SourceType.RELATED_CHANNEL}
    for item in self._starturl_collection.find({}):
      item.pop('_id', None)
      exmap = item
      source = item.get('source', None)
      source = source_dict.get(source, None)
      exmap['source'] = source
      kind = item.get('kind', None)
      user = item.get('user', None)
      channel = item.get('channel', None)
      if source == SourceType.YOUTUBE:
        if kind == 'channel':
          part = 'snippet'
          maxResults = 50
          api = 'https://www.googleapis.com/youtube/v3/playlists?part=%s&channelId=%s&maxResults=%s' % \
              (part, channel, maxResults)
          yield self._create_request(api, PageType.CHANNEL, CrawlDocType.HUB_HOME, meta={'extend_map': exmap})
      elif source in [SourceType.CUSTOM, SourceType.SOCIALBLADE, SourceType.RELATED_CHANNEL]:
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
      #print 'parse_channel url:', url
      self._logger.error('parse_channel url: %s' % url)
      page = response.body.decode(response.encoding)
      self.update_status(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      #self.update_recrawl_info(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      exmap = response.meta.get('extend_map', {})
      rep_dict = safe_eval(page)
      datas = rep_dict.get('items', [])
      if not datas:
        self._logger.error('parse channel failed, url: [%s]' % url)
        return None
      data = datas[0]
      exmap['channel_dict'] = data
      exmap['channel_dict']['update_time'] = int(time.time())
      kind = exmap.get('kind', None)
      user = exmap.get('user', None)
      channel = data.get('id', None)
      channel_title = data.get('snippet', {}).get('title', None)
      if kind == 'user' and channel:
        self._starturl_collection.update({'kind': 'user', 'user': user}, {'$set': {'channel': channel, 'channel_title': channel_title}})
      upload_playlist = data.get('contentDetails', {}).get('relatedPlaylists', {}).get('uploads', None)
      if not upload_playlist:
        return None
      exmap['playlist'] = upload_playlist 
      part = 'snippet'
      maxResults = 50
      api = u"https://www.googleapis.com/youtube/v3/playlistItems?part=%s&playlistId=%s&maxResults=%s" % \
          (part, upload_playlist, maxResults)
      items.append(self._create_request(api, PageType.HUB, CrawlDocType.HUB_TIME_HOME, meta={'extend_map': exmap}))
      """
      if channel:
        relatedchannel_api = u"https://www.googleapis.com/youtube/v3/channels?part=brandingSettings&id=%s" % channel
        items.append(self._create_request(api, PageType.RELATED_CHANNEL, CrawlDocType.HUB_CATEGORY))
      """
      self.update_status(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED)})
      self.remove_recrawl_info(url)
      return items
    except Exception, e:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      self._logger.exception('Failed parse_channel:%s, url:%s' % (msg, url))

  def parse_relatedchannel(self, responose):
    try:
      items = {}
      url = response.url.strip()
      self._logger.error('parse_relatedchannel url: %s' % url)
      page = response.body.decode(response.encoding)
      self.update_status(url, {'status', CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOAD)})
      #self.update_recrawl_info(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      rep_dict = safe_eval(page)
      datas = rep_dict.get('items', [])
      if not datas:
        self._logger.error('parse channel failed, url: [%s]' % url)
        return None
      data = datas[0]
      featuredChannelsUrls = data.get('brandingSettings', {}).get('channel', {}).get('featuredChannelsUrls', [])
      if featuredChannelsUrls:
        for channelId in featuredChannelsUrls:
          part = 'contentDetails'
          api = 'https://www.googleapis.com/youtube/v3/channels?part=%s&id=%s' % \
              (part, channelId)
          items.append(self._create_request(api, PageType.HOME, CrawlDocType.HUB_TIME_HOME, meta={'extend_map': exmap}))
      self.update_status(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED)})
      self.remove_recrawl_info(url)
      return items
    except:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      self._logger.exception('Failed parse_relatedchannel, url:%s' % url)


  def parse_playlist(self, response):
    try:
      items = []
      url = response.url.strip()
      #print 'parse_playlist url:', url
      self._logger.error('parse_playlist url: %s' % url)
      page = response.body.decode(response.encoding)
      self.update_status(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      #self.update_recrawl_info(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      exmap = response.meta.get('extend_map', {})
      rep_dict = safe_eval(page)
      data = rep_dict.get('items', [])
      if not data:
        self._logger.error('parse playlist failed for no items url: [%s]' % url)
        return None
      nextPageToken = rep_dict.get('nextPageToken', None)
      if nextPageToken:
        part = 'snippet'
        maxResults = 50
        channel = exmap.get('channel', None)
        if channel:
          next_api = u"https://www.googleapis.com/youtube/v3/playlists?part=%s&channelId=%s&maxResults=%s&pageToken=%s" % \
                (part, channel, maxResults, nextPageToken)
          items.append(self._create_request(next_api, PageType.CHANNEL, CrawlDocType.HUB_HOME, meta={'extend_map': exmap}))
      for sub_data in data:
        playlist = sub_data.get('id')
        part = 'snippet'
        maxResults = 50
        api = u"https://www.googleapis.com/youtube/v3/playlistItems?part=%s&playlistId=%s&maxResults=%s" % \
                (part, playlist, maxResults)
        extend_map = {}
        extend_map['playlist'] = playlist
        extend_map.update(exmap)
        items.append(self._create_request(api, PageType.HUB, CrawlDocType.HUB_TIME_HOME,
                                            meta={'extend_map': extend_map, 'doc_type': CrawlDocType.HUB_TIME_HOME}))
      self.update_status(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED)})
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
      #print 'parse_list url:', url
      self._logger.error('parse_list url: %s' % url)
      page = response.body.decode(response.encoding)
      self.update_status(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      #self.update_recrawl_info(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      doc_type = response.meta.get('doc_type', CrawlDocType.HUB_OTHER)
      page_index = response.meta.get('page_index', 1)
      exmap = response.meta.get('extend_map', None)
      current_crawl_doc = response.meta.get('crawl_doc')
      rep_dict = safe_eval(page)
      self.update_status(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED)})
      self.remove_recrawl_info(url)
      nextPageToken = rep_dict.get('nextPageToken', None)
      if nextPageToken:
        playlist = exmap.get('playlist')
        part = 'snippet'
        maxResults = 50
        next_api = u"https://www.googleapis.com/youtube/v3/playlistItems?part=%s&playlistId=%s&maxResults=%s&pageToken=%s" % \
                (part, playlist, maxResults, nextPageToken)
        if page_index > 2:
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
                                   dont_filter=dont_filter)
      data = rep_dict.get('items', [])
      if not data:
        self._logger.error('parse list failed for no items url: [%s]' % url)
      else:
        for position, sub_data in enumerate(data):
          videoId = sub_data.get('snippet', {}).get('resourceId', {}).get('videoId', None)
          extend_map = {}
          extend_map['video'] = videoId
          extend_map.update(exmap)
          part = 'contentDetails,player,recordingDetails,snippet,statistics,status,topicDetails'
          api = u"https://www.googleapis.com/youtube/v3/videos?part=%s&id=%s" % \
                (part, videoId)
          yield self._create_request(api,
                                     PageType.PLAY,
                                     CrawlDocType.PAGE_PLAY,
                                     schedule_doc_type=current_crawl_doc.schedule_doc_type,
                                     meta={'doc_type':doc_type,
                                           'page_index': page_index,
                                           'position': position +1,
                                           'extend_map': extend_map},
                                     headers={'Referer': url},
                                     dont_filter=False)
    except Exception, e:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      self.log('Failed parse_channel:%s, url:%s' % (msg, url), log.ERROR)


  def parse_page(self, response):
    try:
      url = response.url.strip()
      #print 'parse_video url:', url
      self._logger.error('parse_video url: %s' % url)
      page = response.body.decode(response.encoding)
      self.update_status(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      #self.update_recrawl_info(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.DOWNLOADED)})
      urlparse_ret = urlparse.urlparse(url)
      url_query = urlparse.parse_qs(urlparse_ret.query)
      videoId = url_query.get('id', [''])[0]
      if not videoId:
        self._logger.error('parse page failed for no videoId, url: [%s]' % url)
        return
      video_url = 'https://www.youtube.com/watch?v=' + videoId
      response.meta['crawl_doc'].url = video_url
      youtube_item = YoutubeItem()
      youtube_item.fill_item(response)
      self.update_status(url, {'status': CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED)})
      self.remove_recrawl_info(url)
      return youtube_item
    except Exception, e:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      self.log('Failed parse_page:%s, url:%s' % (msg, url), log.ERROR)
