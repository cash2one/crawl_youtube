#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.

"""
get base crawler items to fill
using unicode as middle code
decoing item with utf8
in crawler we recommend using coding unicode
when output data should using utf8
"""

__author__ = 'guoxiaohe@letv.com (Guo XiaoHe)'

import json
import traceback
import base64
import time
import logging
import urlparse

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from ..common.thrift_util import thrift_to_str
from ..proto.crawl.ttypes import Request, Response, RedirectInfo, SourceType, CrawlHistory, HistoryItem, PageType, CrawlDocType
from ..proto.video.ttypes import MediaVideo, OriginalUser
from ..common.utils import safe_eval, build_video, source_set, massage_youtube_data, str2mediavideo, history2dict
from ..common.url_domain_parser import query_domain_from_url
from ..common.time_parser import to_iso8601_time
from ..common.duration_parser import parse_iso_duration
from docid_generator import gen_docid
from ..common.url_normalize import UrlNormalize


url_normalize_ = UrlNormalize.get_instance()


# all item should first alig to unicode,
# output should encod utf8
class ItemType(object):
  CRAWL_DOC = 0X11
  WEB_PAGE = 0x12
  PICS_DOC = 0x13
  IMAGE = 0x14


def crawldoc_to_item(crawl_doc, response=None):
  if not crawl_doc:
    print 'Empty crawl_doc !!!!'
    return

  if response:
    crawl_doc.request = Request()
    crawl_doc.request.raw_url = response.request.meta.get('Rawurl')

    crawl_doc.response = Response()
    crawl_doc.response.url = url_normalize_.get_unique_url(response.url) or response.url
    crawl_doc.response.body = response.body.decode(response.encoding, 'ignore').encode('utf-8')
    crawl_doc.response.header = response.headers.to_string()
    crawl_doc.response.return_code = response.status
    crawl_doc.response.redirect_info = RedirectInfo()
    crawl_doc.response.redirect_info.redirect_urls = response.meta.get('redirect_urls')

  item = CrawlerItem()
  item['crawl_doc'] = encode_item(crawl_doc)
  return item


def encode_item(obj):
  if isinstance(obj, unicode):
    return obj.encode('utf-8')
  if isinstance(obj, dict):
    for (k, v) in obj.items():
      obj[encode_item(k)] = encode_item(v)
  if hasattr(obj, '__iter__'):
    for idx, v in enumerate(obj):
      obj[idx] = encode_item(v)
  if hasattr(obj, "__dict__"):
    for key, value in obj.__dict__.iteritems():
      if not callable(value):
        setattr(obj, key, encode_item(value))
  return obj


# post item process
def process_item(item, encoding):
  if not item:
    return item
  try:
    for k in item.keys():
      if isinstance(item[k], str) or k == 'page':
        item[k] = item[k].decode(encoding, 'ignore')
  except:
    print traceback.format_exc(), 'with encoding:%s' % encoding
  return item


class CrawlerItem(Item):
  crawl_doc = Field()

  def to_json_str(self, include_empty=False, encodeing='utf8'):
    try:
      return json.dumps(dict(self), ensure_ascii=False).encode(encodeing)
    except:
      print 'Failed encoding json: %s, %s' % (self, traceback.format_exc())
      return None

  def get_key(self, key, type_need=str):
    try:
      if self.get(key):
        if isinstance(self[key], type_need):
          return True, self[key]
        elif type_need == str:
          return True, self[key].encode('utf-8')
        else:
          return True, type_need(self[key])
    except:
      print traceback.format_exc()
    return False, None

  def to_crawldoc(self):
    self.get('crawl_doc').crawl_time = int(time.time())
    return self['crawl_doc']


source_dict = {'youtube_pop': SourceType.YOUTUBE,
               'custom': SourceType.CUSTOM, 
               'socialblade': SourceType.SOCIALBLADE, 
               'related_channel': SourceType.RELATED_CHANNEL}


class YoutubeItem(Item):
  channel = Field()
  channel_title = Field()
  category = Field()
  user = Field()
  url = Field()
  title = Field()
  doc_id = Field()
  playlist = Field()
  crawl_doc = Field()
  video = Field()
  source = Field()
  category_id = Field()
  content_timestamp = Field()
  channel_dict = Field()
  request_url = Field()
  crawl_history = Field()
  doc_type = Field()
  page_type = Field()

  def gen_video_url(self, request_url):
    if not request_url:
      return None
    try:
      urlparse_ret = urlparse.urlparse(request_url)
      url_query = urlparse.parse_qs(urlparse_ret.query)
      videoId = url_query.get('id', [''])[0]
      if not videoId:
        return None
      video_url = 'https://www.youtube.com/watch?v=' + videoId
      return video_url
    except Exception, e:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      

  def fill_item(self, response, except_key=[]):
    crawl_doc = response.meta.pop('crawl_doc')
    if not crawl_doc:
      print 'Empty crawl_doc !!!!'
      return

    self['request_url'] = crawl_doc.url
    crawl_doc.url = self.gen_video_url(crawl_doc.url)
    self['url'] = crawl_doc.url
    self['doc_id'] = gen_docid(crawl_doc.url)
    crawl_doc.id = self['doc_id']
    crawl_doc.crawl_time = int(time.time())
    self['doc_type'] = CrawlDocType._VALUES_TO_NAMES.get(crawl_doc.doc_type)
    self['page_type'] = PageType._VALUES_TO_NAMES.get(crawl_doc.page_type)

    extend_map = response.meta.get('extend_map', {})
    self['category'] = extend_map.get('category', None)
    self['channel_dict'] = extend_map.get('channel_dict', None)
    self['user'] = extend_map['user'].lower() if extend_map.get('user', None) else None
    self['playlist'] = extend_map.get('playlist', None)
    self['source'] = source_dict.get(extend_map.get('source', None), None)

    page = response.body.decode(response.encoding, 'ignore')

    #html_data = self.parse_video(self, page, crawl_doc)
    #self['video'] = build_video(html_data, crawl_doc)
    self['video'] = self.parse_video(page, crawl_doc)
    self['crawl_history'] = history2dict(self['video'].crawl_history)

    crawl_doc.request = Request()
    crawl_doc.request.raw_url = response.request.meta.get('Rawurl')

    crawl_doc.response = Response()
    crawl_doc.response.url = crawl_doc.url
    crawl_doc.response.body = page.encode('utf-8')
    crawl_doc.response.header = response.headers.to_string()
    crawl_doc.response.return_code = response.status
    crawl_doc.response.redirect_info = RedirectInfo()
    crawl_doc.response.redirect_info.redirect_urls = response.meta.get('redirect_urls')
    crawl_doc.response.meta = '%s' % response.meta

    self['crawl_doc'] = encode_item(crawl_doc)

  def parse_video(self, page, crawl_doc):
    if not page:
      return None
    html_data = {}
    rep_dict = json.loads(page)
    if not rep_dict:
      return
    datas = rep_dict.get('items', [])
    if not datas:
      return
    data = datas[0]

    html_data['category'] = self['category']
    html_data['category_list'] = self['category']
    #html_data['channel'] = self['channel']
    #html_data['user'] = self['user']
    html_data['playlist'] = self['playlist']
    html_data['source_type'] = self['source']

    html_data['doc_id'] = crawl_doc.id
    html_data['id'] = str(crawl_doc.id)
    html_data['crawl_time'] = html_data['create_time'] = crawl_doc.crawl_time
    html_data['discover_time'] = crawl_doc.discover_time
    html_data['url'] = crawl_doc.url
    html_data['domain'] = query_domain_from_url(html_data['url'])
    html_data['domain_id'] = source_set[html_data['domain']]
    html_data['in_links'] = crawl_doc.in_links
    html_data['page_state'] = crawl_doc.page_state

    original_user = OriginalUser()

    snippet = data.get('snippet', None)
    if snippet:
      channel_id = snippet.get('channelId', None)
      if channel_id:
        original_user.channel_id = channel_id
        original_user.url = 'https://www.youtube.com/channel/%s' % channel_id
      self['channel'] = original_user.channel_id
      
      html_data['showtime'] = snippet.get('publishedAt', None)
      html_data['content_timestamp'] = int(to_iso8601_time(html_data['showtime']))
      self['content_timestamp'] = html_data['content_timestamp']
      html_data['title'] = snippet.get('title', None)
      self['title'] = html_data['title']
      html_data['desc'] = snippet.get('description', None)
      html_data['thumbnails'] = json.dumps(snippet.get('thumbnails', {}), ensure_ascii=False)
      html_data['poster'] = snippet.get('thumbnails', {}).get('default', {}).get('url', None)
      html_data['channel_title'] = snippet.get('channelTitle', None)
      self['channel_title'] = html_data['channel_title']
      html_data['tags'] = ';'.join(snippet.get('tags', [])).strip(';')
      html_data['category_id'] = snippet.get('categoryId', None)
      self['category_id'] = html_data['category_id']
      
    contentDetails = data.get('contentDetails', None)
    if contentDetails:
      html_data['duration'] = contentDetails.get('duration', None)
      html_data['duration_seconds'] = parse_iso_duration(html_data['duration'])
      html_data['dimension'] = contentDetails.get('dimension', None)
      html_data['quality'] = contentDetails.get('definition', None)
      html_data['caption'] = contentDetails.get('caption', False)

    statistics = data.get('statistics', None)
    if statistics:
      html_data['play_total'] = int(statistics.get('viewCount', '0'))
      html_data['voteup_count'] = int(statistics.get('likeCount', '0'))
      html_data['votedown_count'] = int(statistics.get('dislikeCount', '0'))
      html_data['comment_num'] = int(statistics.get('commentCount', '0'))
    
    html_data['player'] = data.get('player', {}).get('embedHtml', None)

    if self['channel_dict']:
      original_user.update_time = self['channel_dict'].get('update_time', None)
      original_user.channel_id = self['channel_dict'].get('channel_id', None)
      original_user.user_name = self['channel_dict'].get('user', None)
      original_user.channel_title = self['channel_dict'].get('channel_title', None)
      original_user.channel_desc = self['channel_dict'].get('channel_desc', None)
      original_user.publish_time = self['channel_dict'].get('publish_time', None)
      original_user.thumbnails = self['channel_dict'].get('thumbnails', None)
      original_user.portrait_url = self['channel_dict'].get('portrait_url', None)
      original_user.country = self['channel_dict'].get('country', None)
      original_user.video_num = int(self['channel_dict'].get('video_num', '0'))
      original_user.play_num = int(self['channel_dict'].get('play_num', '0'))
      original_user.fans_num = int(self['channel_dict'].get('fans_num', '0'))
      original_user.comment_num = int(self['channel_dict'].get('comment_num', '0'))

    html_data['user'] = original_user

    #if html_data.get('play_total', 0) and html_data.get('crawl_time', 0):
    #  html_data['play_trends'] = '%s|%s' % (html_data['crawl_time'], html_data['play_total'])
    html_data['play_trends'] = '%s|%s' % (html_data['crawl_time'], html_data['play_total'])

    html_data = massage_youtube_data(html_data)
    video = build_video(html_data, crawl_doc)
    return video


  def merge_video(self, merge_data):
    #TODO
    try:
      merge_data = base64.b64decode(merge_data)
      merge_data = str2mediavideo(merge_data)
      if not merge_data:
        logging.error('failed to convert merge_data ...')
        return
      history_items = {}
      if self['video'] and self['video'].crawl_history and self['video'].crawl_history.crawl_history:
        for sub_history in self['video'].crawl_history.crawl_history:
          if sub_history.crawl_time:
            history_items[sub_history.crawl_time] = sub_history.play_count
      if merge_data.crawl_history and merge_data.crawl_history.crawl_history:
        for sub_history in merge_data.crawl_history.crawl_history:
          if sub_history.crawl_time:
            history_items[sub_history.crawl_time] = sub_history.play_count
      crawl_history_new = CrawlHistory()
      crawl_history_new.crawl_history = []
      history_list = sorted(history_items.iteritems(), reverse=True)
      if len(history_list) > 10:
        history_list = history_list[:10]
      history_len = len(history_list)
      for idx, c_item in enumerate(history_list):
        item = HistoryItem()
        item.crawl_time = c_item[0]
        item.play_count = c_item[1]
        if idx + 1 < history_len:
          item.crawl_interval = c_item[0] - history_list[idx + 1][0]
        crawl_history_new.crawl_history.append(item)
        history_list[idx] = (str(c_item[0]), str(c_item[1]))
      crawl_history_new.update_time = int(time.time())
      self['video'].crawl_history = crawl_history_new
      self['video'].play_trends = ';'.join('|'.join(x) for x in history_list if x[1] != 'None')
      for k, v in self['video'].__dict__.iteritems():
        if v is None or k == 'user':
          src_v = getattr(merge_data, k)
          if src_v is not None:
            setattr(self['video'], k, src_v)
    except Exception, e:
      msg = e.message
      msg = traceback.format_exc()
      print msg
      return


  def convert_item(self):
    try:
      data = {}
      data['doc_id'] = str(self['doc_id'])
      data['url'] = self['url']
      data['request_url'] = self['request_url']
      data['category'] = self['category']
      data['channel'] = self['channel']
      data['channel_title'] = self['channel_title']
      data['playlist'] = self['playlist']
      data['user'] = self['user']
      data['title'] = self['title']
      data['source'] = SourceType._VALUES_TO_NAMES.get(self['source'])
      data['category_id'] = self['category_id']
      data['content_timestamp'] = self['content_timestamp']
      self['crawl_history'] = history2dict(self['video'].crawl_history)
      data['crawl_history'] = self['crawl_history']
      video_str = thrift_to_str(encode_item(self['video']))
      if video_str:
        data['video'] = base64.b64encode(video_str)
      else:
        logging.error('fail to convert media_video to str, url:%s' % self['url'])
        data['video'] = None
      craw_doc_str = thrift_to_str(self['crawl_doc'])
      data['crawl_doc'] = base64.b64encode(craw_doc_str)
      return data
    except Exception, e:
      msg = e.message
      msg += traceback.format_exc()
      print msg
      return None


class CrawlerLoader(ItemLoader):
  default_item_class = CrawlerItem
  default_input_processor = MapCompose(lambda s: s.strip())
  default_output_processor = TakeFirst()
  description_out = Join()

