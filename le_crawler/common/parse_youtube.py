#!/usr/bin/python
# coding=utf-8
#
# Copyright 2015 LeTV Inc. All Rights Reserved.
# encoding = utf8

__author__ = 'zhaojincheng@letv.com'

import json
import time
import urlparse
import traceback

from time_parser import TimeParser
from ..proto.crawl.ttypes import Thumbnail

time_parser = TimeParser()

youtube_category_dict = {'1': 'Film & Animation',
                         '2': 'Autos & Vehicles',
                         '10': 'Music',
                         '15': 'Pets & Animals',
                         '17': 'Sports',
                         '18': 'Short Movies',
                         '19': 'Travel & Events',
                         '20': 'Gaming',
                         '21': 'Videoblogging',
                         '22': 'People & Blogs',
                         '23': 'Comedy',
                         '24': 'Entertainment',
                         '25': 'News & Politics',
                         '26': 'Howto & Style',
                         '27': 'Education',
                         '28': 'Science & Technology',
                         '29': 'Nonprofits & Activism',
                         '30': 'Movies',
                         '31': 'Anime/Animation',
                         '32': 'Action/Adventure',
                         '33': 'Classics',
                         '34': 'Comedy',
                         '35': 'Documentary',
                         '36': 'Drama',
                         '37': 'Family',
                         '38': 'Foreign',
                         '39': 'Horror',
                         '40': 'Sci-Fi/Fantasy',
                         '41': 'Thriller',
                         '42': 'Shorts',
                         '43': 'Shows',
                         '44': 'Trailers'}


def parse_channel_detail(channel_data, extend_map=None):
  ret_dict = {}
  channel_id = channel_data.get('id', None)
  if channel_id is not None:
    ret_dict['channel_id'] = channel_id
  else:
    return None
  ret_dict['url'] = 'https://www.youtube.com/channel/%s' % ret_dict['channel_id']
  
  channel_title = channel_data.get('snippet', {}).get('title', None)
  if channel_title is not None:
    ret_dict['channel_title'] = channel_title

  channel_desc = channel_data.get('snippet', {}).get('description', None)
  if channel_desc is not None:
    ret_dict['channel_desc'] = channel_desc
    
  publish_time = channel_data.get('snippet', {}).get('publishedAt', None)
  if publish_time is not None:
    ret_dict['publish_time'] = time_parser.timestamp(publish_time)

  thumbnails = channel_data.get('snippet', {}).get('thumbnails', None)
  if thumbnails is not None:
    ret_dict['thumbnails'] = thumbnails
  portrait_url = thumbnails.get('default', {}).get('url', None)
  if portrait_url is not None:
    ret_dict['portrait_url'] = portrait_url

  country = channel_data.get('snippet', {}).get('country', None)
  if country is not None:
    ret_dict['country'] = country

  video_num = channel_data.get('statistics', {}).get('videoCount', None)
  if video_num is not None:
    ret_dict['video_num'] = int(video_num)

  play_num = channel_data.get('statistics', {}).get('viewCount', None)
  if play_num is not None:
    ret_dict['play_num'] = int(play_num)

  fans_num = channel_data.get('statistics', {}).get('subscriberCount', None)
  if fans_num is not None:
    ret_dict['fans_num'] = int(fans_num)

  comment_num = channel_data.get('statistics', {}).get('commentCount', None)
  if comment_num is not None:
    ret_dict['comment_num'] = int(comment_num)

  if extend_map:
    if extend_map.get('user', None):
      ret_dict['user'] = extend_map['user']
    if extend_map.get('source', None):
      ret_dict['source'] = extend_map['source']
    if extend_map.get('country', None) and ret_dict.get('country', None):
      ret_dict['country'] = extend_map['country']

  ret_dict['is_parse'] = True
  ret_dict['update_time'] = int(time.time())
  return ret_dict
  
  
def gen_youtube_video_url(request_url):
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


def parse_channel_id(url):
  if not url:
    return None
  if not url.startswith('https://www.googleapis.com/youtube/v3/channels'):
    return None
  try:
    urlparse_ret = urlparse.urlparse(url)
    url_query = urlparse.parse_qs(urlparse_ret.query)
    channel_id = url_query.get('id', [''])[0]
    return channel_id
  except Exception, e:
    msg = e.message
    msg += traceback.format_exc()
    print msg


    
 
def parse_thumbnail_list(thumbnail_dict):
  if not thumbnail_dict:
    return
  thumbnail_list = []
  try:
    for key, value in thumbnail_dict.items():
      thumbnail = Thumbnail()
      thumbnail.scale = key.encode('utf-8')
      thumbnail.height = value.get('height', None)
      thumbnail.width = value.get('width', None)
      url = value.get('url', None)
      if not url:
        return
      thumbnail.url = url.encode('utf-8')
      thumbnail_list.append(thumbnail)
    return thumbnail_list
  except:
    print traceback.format_exc()
    return
