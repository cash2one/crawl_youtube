#!/usr/bin/python
# coding=utf-8

import sys
import json
import time
from static_extractor import StaticExtractor
from ..common.utils import multi_key_fields, source_set, safe_eval
from ..common.parse_youtube import youtube_category_dict, parse_thumbnail_list
from ..proto.video.ttypes import MediaVideo, State, OriginalUser
from ..proto.crawl.ttypes import SourceType, RegionStrategy, LanguageType
from ..common.langdetect import detect, detect_langs

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

  def GetStatic(self, crawl_doc):
    url = crawl_doc.url
    valid, url_type = self._is_invalid_page(url)
    if not valid:
      return None
    html_data = self.parse_page(crawl_doc)
    if not html_data:
      return
    self.parse_meta(crawl_doc, html_data)

    html_data['doc_id'] = crawl_doc.id
    html_data['id'] = str(crawl_doc.id)
    html_data['crawl_time'] = html_data['create_time'] = crawl_doc.crawl_time
    html_data['discover_time'] = crawl_doc.discover_time
    html_data['url'] = crawl_doc.url
    html_data['domain'] = self._web_name
    html_data['domain_id'] = source_set[self._web_name]
    html_data['in_links'] = crawl_doc.in_links
    if html_data['in_links']:
      html_data['inlink_history'] = [crawl_doc.in_links]
    html_data['page_state'] = crawl_doc.page_state

    return self._filter_long_video(html_data, url_type)

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
    video_la = detect_text(title)
    if not video_la or video_la == 'EN':
      desc_la = detect_text(desc)
      if desc_la:
        video_la = desc_la
    if not video_la:
      return None
    return LanguageType._NAMES_TO_VALUES.get(video_la, LanguageType.UNKNOWN)

  def parse_page(self, crawl_doc):
    page = crawl_doc.response.body
    rep_dict = json.loads(page)
    if not rep_dict:
      return
    datas = rep_dict.get('items', [])
    if not datas:
      return
    data = datas[0]

    html_data = {}

    if data.get('id', None):
      html_data['external_id'] = data['id']

    snippet = data.get('snippet', None)
    if snippet:
      html_data['channel_id'] = snippet.get('channelId', None)
      # if html_data['channel_id']:
      #   user_url = 'https://www.youtube.com/channel/%s' % html_data['channel_id']
      #   video = MediaVideo()
      #   # video.user = OriginalUser(url=user_url.encode('utf-8'), channel_id=html_data['channel_id'].encode('utf-8'), update_time=crawl_doc.crawl_time)
      #   crawl_doc.video = video

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


  def parse_meta(self, crawl_doc, html_data):
    rep_meta = self.load_meta(crawl_doc.response.meta)
    if not rep_meta:
      return
    extend_map = rep_meta.get('extend_map', None)
    if not extend_map:
      return
    if extend_map.get('playlist', None):
      html_data['playlist'] = extend_map['playlist']
    html_data['source_type'] = self._source_dict.get(extend_map.get('source', None), None)
    channel_dict = extend_map.get('channel_dict', None)
    if channel_dict:
      original_user = OriginalUser()
      channel_id = channel_dict.get('channel_id', None)
      if not channel_id:
        return
      original_user.channel_id = channel_id.encode('utf-8')
      channel_url = 'https://www.youtube.com/channel/%s' % channel_id
      original_user.url = channel_url.encode('utf-8')

      original_user.user_name = channel_dict.get('user', None)
      if original_user.user_name:
        original_user.user_name = original_user.user_name.encode('utf-8')

      original_user.channel_title = channel_dict.get('channel_title', None)
      if original_user.channel_title:
        original_user.channel_title = original_user.channel_title.encode('utf-8')

      original_user.channel_desc = channel_dict.get('channel_desc', None)
      if original_user.channel_desc:
        original_user.channel_desc = original_user.channel_desc.encode('utf-8')

      original_user.publish_time = channel_dict.get('publish_time', None)

      thumbnails = channel_dict.get('thumbnails', None)
      if thumbnails:
        original_user.thumbnails = json.dumps(thumbnails, ensure_ascii=False).encode('utf-8')
      thumbnail_list = parse_thumbnail_list(thumbnails)
      if thumbnail_list:
        original_user.thumbnail_list = thumbnail_list

      
      portrait_url = channel_dict.get('portrait_url', None)
      if portrait_url:
        original_user.portrait_url = portrait_url.encode('utf-8')

      original_user.country = channel_dict.get('country', None)
      if original_user.country:
        original_user.country = original_user.country.encode('utf-8')

      display_countrys = channel_dict.get('display_countrys', None)
      if display_countrys:
        original_user.display_countrys = [country.encode('utf-8') for country in display_countrys]

      original_user.video_num = int(channel_dict.get('video_num', '0'))
      original_user.play_num = int(channel_dict.get('play_num', '0'))
      original_user.fans_num = int(channel_dict.get('fans_num', '0'))
      original_user.comment_num = int(channel_dict.get('comment_num', '0'))
      original_user.update_time = channel_dict.get('update_time', None)

      #TODO to delete
      # in_related_user = channel_dict.get('in_related_user', [])
      # if in_related_user:
      #   original_user.in_related_user = [related_user.encode('utf-8') for related_user in in_related_user]
      

      out_related_user = channel_dict.get('out_related_user', [])
      if out_related_user:
        original_user.out_related_user = [related_user.encode('utf-8') for related_user in out_related_user]

      video = MediaVideo()
      video.user = original_user
      crawl_doc.video = video

