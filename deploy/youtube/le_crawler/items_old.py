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

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from ..common.thrift_util import thrift_to_str
from ..proto.crawl.ttypes import Request, Response, RedirectInfo, SourceType
from ..proto.video.ttypes import MediaVideo, OriginalUser
from ..common.utils import safe_eval, build_video, source_set, massage_youtube_data, str2mediavideo
from ..common.url_domain_parser import query_domain_from_url
from ..common.time_parser import to_iso8601_time
from ..common.duration_parser import parse_iso_duration
from docid_generator import gen_docid

# all item should first alig to unicode,
# output should encod utf8
class ItemType(object):
  CRAWL_DOC = 0X11
  WEB_PAGE = 0x12
  PICS_DOC = 0x13
  IMAGE = 0x14


def fill_base_item(response, item, except_key=[]):
  crawl_doc = response.meta.get('crawl_doc')
  if not crawl_doc:
    print 'Empty crawl_doc !!!!'
    return

  crawl_doc.request = Request()
  crawl_doc.request.raw_url = response.request.meta.get('Rawurl')

  crawl_doc.response = Response()
  crawl_doc.response.url = crawl_doc.url
  crawl_doc.response.body = response.body.decode(response.encoding, 'ignore').encode('utf-8')
  crawl_doc.response.header = response.headers.to_string()
  crawl_doc.response.return_code = response.status
  crawl_doc.response.redirect_info = RedirectInfo()
  crawl_doc.response.redirect_info.redirect_urls = response.meta.get('redirect_urls')

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


  def __init__(self):
    self._source_dict = {'youtube_pop': SourceType.YOUTUBE,
                         'custom': SourceType.CUSTOM, 
                         'socialblade': SourceType.SOCIALBLADE, 
                         'related_channel': SourceType.RELATED_CHANNEL}


  def fill_item(self, response, except_key=[]):
    crawl_doc = response.meta.pop('crawl_doc')
    if not crawl_doc:
      print 'Empty crawl_doc !!!!'
      return

    self['url'] = crawl_doc.url
    self['doc_id'] = gen_docid(crawl_doc.url)
    crawl_doc.id = self['doc_id']
    crawl_doc.crawl_time = int(time.time())

    extend_map = response.meta.get('extend_map')
    self['category'] = extend_map.get('category', None)
    self['channel_dict'] = extend_map.get('channel_dict', None)
    self['user'] = extend_map['user'].lower() if extend_map.get('user', None) else None
    self['playlist'] = extend_map.get('playlist', None)
    self['source'] = self._source_dict.get(extend_map.get('source', None), None)

    page = response.body.decode(response.encoding, 'ignore')

    #html_data = self.parse_video(self, page, crawl_doc)
    #self['video'] = build_video(html_data, crawl_doc)
    self['video'] = self.parse_video(page, crawl_doc)

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
    rep_dict = safe_eval(page)
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
      html_data['comment_count'] = int(statistics.get('commentCount', '0'))

    if self['channel_dict']:
      original_user.update_time = self['channel_dict'].get('update_time', None)
      original_user.channel_id = self['channel_dict'].get('id', None)
      original_user.user_name = self['user']
      original_user.channel_title = self['channel_dict'].get('snippet', {}).get('title', None)
      original_user.channel_desc = self['channel_dict'].get('snippet', {}).get('description', None)
      original_user.publish_time = int(to_iso8601_time(self['channel_dict'].get('snippet', {}).get('publishedAt', None)))
      original_user.thumbnails = json.dumps(self['channel_dict'].get('snippet', {}).get('thumbnails', {}), ensure_ascii=False)
      original_user.portrait_url = self['channel_dict'].get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', None)
      original_user.country = self['channel_dict'].get('snippet', {}).get('country', None)
      original_user.video_num = int(self['channel_dict'].get('statistics', {}).get('videoCount', None))
      original_user.play_num = int(self['channel_dict'].get('statistics', {}).get('viewCount', None))
      original_user.fans_num = int(self['channel_dict'].get('statistics', {}).get('subscriberCount', None))
      original_user.comment_num = int(self['channel_dict'].get('statistics', {}).get('commentCount', None))

    html_data['user'] = original_user

    #if html_data.get('play_total', 0) and html_data.get('crawl_time', 0):
    #  html_data['play_trends'] = '%s|%s' % (html_data['crawl_time'], html_data['play_total'])
    html_data['play_trends'] = '%s|%s' % (html_data['crawl_time'], html_data['play_total'])

    html_data = massage_youtube_data(html_data)
    video = build_video(html_data, crawl_doc)

    """
    video.user = OriginalUser()

    if self['channel_dict']:
      video.user.channel_id = self['channel_dict'].get('id', None)
      video.user.user_name = self['user']
      video.user.channel_title = self['channel_dict'].get('snippet', {}).get('title', None)
      video.user.channel_desc = self['channel_dict'].get('snippet', {}).get('description', None)
      video.user.publish_time = int(to_iso8601_time(self['channel_dict'].get('snippet', {}).get('publishedAt', None)))
      video.user.thumbnails = json.dumps(self['channel_dict'].get('snippet', {}).get('thumbnails', {}), ensure_ascii=False)
      video.user.portrait_url = self['channel_dict'].get('snippet', {}).get('thumbnails', {}).get('default', None)
      video.user.country = self['channel_dict'].get('snippet', {}).get('country', None)
      video.user.video_num = self['channel_dict'].get('statistics', {}).get('videoCount', None)
      video.user.play_num = self['channel_dict'].get('statistics', {}).get('viewCount', None)
      video.user.fans_num = self['channel_dict'].get('statistics', {}).get('subscriberCount', None)
      video.user.comment_num = self['channel_dict'].get('statistics', {}).get('commentCount', None) 
    """

    return video


  def merge_video(self, video_base64):
    #TODO
    return


  def convert_item(self):
    try:
      data = {}
      data['doc_id'] = str(self['doc_id'])
      data['url'] = self['url']
      data['category'] = self['category']
      data['channel'] = self['channel']
      data['channel_title'] = self['channel_title']
      data['playlist'] = self['playlist']
      data['user'] = self['user']
      data['title'] = self['title']
      data['source'] = SourceType._VALUES_TO_NAMES.get(self['source'])
      data['category_id'] = self['category_id']
      data['content_timestamp'] = self['content_timestamp']
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

