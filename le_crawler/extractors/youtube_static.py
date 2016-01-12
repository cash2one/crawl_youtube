#!/usr/bin/python
# coding=utf-8

import sys
import json
import time
import re
import urlparse
from static_extractor import StaticExtractor
from ..common.utils import multi_key_fields, source_set, safe_eval, build_user
from ..common.parse_youtube import youtube_category_dict, parse_thumbnail_list, parse_channel_detail, get_url_param
from ..proto.video.ttypes import MediaVideo, State, OriginalUser
from ..proto.crawl.ttypes import SourceType, RegionStrategy, LanguageType
from ..common.langdetect import detect, detect_langs
from ..core.docid_generator import gen_docid


try:
  import cPickle as pickle
except:
  import pickle


class YoutubeStatic(StaticExtractor):
  def __init__(self, xpather, deadlinks):
    StaticExtractor.__init__(self, xpather, deadlinks)
    self._web_name = 'youtube.com'
    self._source_dict = {'youtube_pop': SourceType.YOUTUBE,
                         'youtube': SourceType.YOUTUBE,
                         'custom': SourceType.CUSTOM,
                         'socialblade': SourceType.SOCIALBLADE, 
                         'related_channel': SourceType.RELATED_CHANNEL,
                         'related_video': SourceType.RELATED_VIDEO}
    self._users = [r'www\.youtube\.com\/channel',
                   r'www\.googleapis\.com\/youtube\/v3\/channels']


  def GetStatic(self, crawl_doc):
    url = crawl_doc.url
    valid, url_type = self._is_invalid_page(url)
    if not valid:
      return None

    if url_type == 'user':
      if url.startswith('https://www.youtube.com/channel/'):
        html_data = self.parse_user_html(crawl_doc)
        html_data['url'] = url
        html_data['channel_id'] = self.parse_channel_id(url)
      elif url.startswith('https://www.googleapis.com/youtube/v3/channels'):
        channel_id = get_url_param(url, 'id')
        html_data = self.parse_user_api(crawl_doc)
        if html_data:
          if not html_data.get('channel_id', None):
            channel_id = get_url_param(url, 'id')
            if not channel_id:
              return
            html_data['channel_id'] = channel_id
            html_data['url'] = 'https://www.youtube.com/channel/' + channel_id
          url = crawl_doc.url = html_data['url']
    elif url_type == 'video':
      html_data = self.parse_page(crawl_doc)
    else:
      return

    if not html_data:
      return
    html_data['url_type'] = url_type
    crawl_doc.id = gen_docid(crawl_doc.url)
    html_data['doc_id'] = crawl_doc.id
    html_data['id'] = str(crawl_doc.id)
    html_data['global_id'] = '202_' + html_data['id']
    html_data['crawl_time'] = html_data['create_time'] = crawl_doc.crawl_time
    html_data['discover_time'] = crawl_doc.discover_time
    html_data['domain'] = self._web_name
    html_data['domain_id'] = source_set[self._web_name]
    html_data['page_state'] = crawl_doc.page_state
    return self._filter_long_video(html_data, url_type)


  def parse_channel_id(self, channel_url):
    if not channel_url:
      return
    urlparse_ret = urlparse.urlparse(channel_url)
    path_list = urlparse_ret.path.strip('/').split('/')
    if not path_list:
      return
    if 'channel' != path_list[0]:
      return
    channel_id = path_list[1]
    return channel_id


  def parse_user_html(self, crawl_doc):
    if not crawl_doc or not crawl_doc.url or not crawl_doc.response:
      return
    html_data = self._xpather.parse(crawl_doc.url, crawl_doc.response.body)
    if html_data.get('out_related_user', None):
      related_channel_urls = []
      for related_user in html_data['out_related_user']:
        if 'http' not in related_user:
          related_user = 'https://www.youtube.com/channel/' + related_user
        related_channel_urls.append(related_user)
      html_data['out_related_user'] = related_channel_urls
    return html_data

  def parse_user_api(self, crawl_doc):
    if not crawl_doc or not crawl_doc.url or not crawl_doc.response:
      return
    page = crawl_doc.response.body
    if not page:
      return
    rep_data = json.loads(page)
    html_data = parse_channel_detail(rep_data)
    extend_map = self.parse_extend_map(crawl_doc)
    if extend_map:
      if extend_map.get('display_countrys', None):
        html_data['display_countrys'] = extend_map['display_countrys']
      if extend_map.get('user_name', None):
        html_data['user_name'] = extend_map['user_name']

    return html_data

  def detect_video_language(self, title, desc):
    def detect_text(video_text):
      if not video_text:
        return
      try:
        lang_li = detect_langs(video_text)
        la = lang_li[0].lang
        if la == 'EN' and len(lang_li) > 1:
          la = lang_li[1].lang
        return la
      except:
        return
    def preprocess_text(video_text):
      if not video_text:
        return
      return re.sub(r"https?://\S*(\s|$)", "", video_text)

    video_la = detect_text(title)
    if not video_la or video_la == 'EN':
      desc = preprocess_text(desc)
      desc_la = detect_text(desc)
      if desc_la:
        video_la = desc_la
    if not video_la:
      return None
    return LanguageType._NAMES_TO_VALUES.get(video_la, LanguageType.UNKNOWN)

  def parse_page(self, crawl_doc):
    html_data = {}
    if crawl_doc.in_links:
      html_data['in_links'] = crawl_doc.in_links
      html_data['inlink_history'] = [crawl_doc.in_links]

    extend_map = self.parse_extend_map(crawl_doc)
    if extend_map:
      if extend_map.get('playlist', None):
        html_data['playlist'] = extend_map['playlist']
      html_data['source_type'] = self._source_dict.get(extend_map.get('source', None), None)
      channel_dict = extend_map.get('channel_dict', None)
      if channel_dict:
        original_user = build_user(channel_dict)
        video = MediaVideo()
        video.user = original_user
        crawl_doc.video = video

    page = crawl_doc.response.body
    rep_dict = json.loads(page)
    if not rep_dict:
      html_data['dead_link'] = True
      return html_data
    datas = rep_dict.get('items', [])
    if not datas:
      html_data['dead_link'] = True
      return html_data
    data = datas[0]

    if data.get('id', None):
      html_data['external_id'] = data['id']
      html_data['url'] = 'https://www.youtube.com/watch?v=' + data['id']
    else:
      return

    snippet = data.get('snippet', None)
    if snippet:
      html_data['channel_id'] = snippet.get('channelId', None)
      if html_data['channel_id']:
        html_data['user_url'] = 'https://www.youtube.com/channel/' + html_data['channel_id']
      html_data['showtime'] = snippet.get('publishedAt', None)
      html_data['title'] = snippet.get('title', None)
      html_data['desc'] = snippet.get('description', None)
      language_type = self.detect_video_language(html_data['title'], html_data['desc'])
      if language_type is not None:
        html_data['language_type'] = language_type

      thumbnails = snippet.get('thumbnails', {})
      if thumbnails:
        html_data['thumbnails'] = json.dumps(thumbnails, ensure_ascii=False).encode('utf-8')
        html_data['thumbnail_list'] = parse_thumbnail_list(thumbnails)
        html_data['poster'] = thumbnails.get('default', {}).get('url', None)

      html_data['channel_title'] = snippet.get('channelTitle', None)
      html_data['tags'] = ';'.join(snippet.get('tags', [])).strip(';')
      html_data['category_id'] = snippet.get('categoryId', None)
      html_data['category'] = youtube_category_dict.get(html_data['category_id'], None)
      html_data['category_list'] = html_data['category']
      html_data['language'] = snippet.get('defaultLanguage', None)

    contentDetails = data.get('contentDetails', None)
    if contentDetails:
      html_data['duration'] = contentDetails.get('duration', None)
      html_data['dimension'] = contentDetails.get('dimension', None)
      html_data['quality'] = contentDetails.get('definition', None)
      #html_data['caption'] = True if contentDetails.get('caption', 'false') == 'true' else False
      html_data['caption'] = 1 if contentDetails.get('caption', 'false') == 'true' else 0
      region_restriction = contentDetails.get('regionRestriction', None)
      if region_restriction:
        region_strategy = RegionStrategy()
        allowed_list = region_restriction.get('allowed', None)
        if allowed_list is not None:
          region_strategy.region_allowed = [region.encode('utf-8') for region in allowed_list]
        blocked_list = region_restriction.get('blocked', None)
        if blocked_list is not None:
          region_strategy.region_blocked = [region.encode('utf-8') for region in blocked_list]
        html_data['region_strategy'] = region_strategy

    statistics = data.get('statistics', None)
    if statistics:
      html_data['play_total'] = int(statistics.get('viewCount', '0'))
      html_data['voteup_count'] = int(statistics.get('likeCount', '0'))
      html_data['votedown_count'] = int(statistics.get('dislikeCount', '0'))
      html_data['comment_num'] = int(statistics.get('commentCount', '0'))
    
    html_data['player'] = data.get('player', {}).get('embedHtml', None)
    
    return html_data

  
  def load_meta(self, meta_str):
    if not meta_str:
      return
    try:
      rep_meta = json.loads(meta_str)
      if not rep_meta:
        return
      if not isinstance(rep_meta, dict):
        return
      return rep_meta
    except:
      sys.stderr.write('reporter:counter:map,map_meta_jsonload_error_url,1\n')
      return


  def parse_extend_map(self, crawl_doc):
    rep_meta = self.load_meta(crawl_doc.response.meta)
    if not rep_meta:
      return
    extend_map = rep_meta.get('extend_map', None)
    return extend_map

