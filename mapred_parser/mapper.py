#!/usr/bin/python
# coding=utf8

import re
import sys
import time
import base64
import letvbase
import copy

from le_crawler.extractors.video_adaptor import VideoAdaptor
from le_crawler.proto.crawl.ttypes import PageType, CrawlDocState, Anchor
from le_crawler.common.url_normalize import get_abs_url, UrlNormalize
from le_crawler.common.utils import massage_data, thrift2str, str2crawldoc, build_video, str2mediavideo, build_user

play_page_merged_keys = ['domain', 'domain_id']
url_normalizer = UrlNormalize.get_instance()


def get_url_type(url):
  if not url:
    return None
  url_type_reg = {'video': [r'www\.youtube\.com\/watch',
                            r'www\.googleapis\.com\/youtube\/v3\/search.*relatedToVideoId'],
                  'user':  [r'www\.youtube\.com\/channel',
                            r'www\.googleapis\.com\/youtube\/v3\/channels']}
  for (url_type, reg_list) in url_type_reg.items():
    for reg in reg_list:
      if re.search(reg, url):
        return url_type
  return None
  

def print_video(data_source, data, crawl_doc):
  if not data_source:
    sys.stderr.write('reporter:counter:map,invalid_data,1\n')
    return
  massage_data(data, printable=False)
  video = build_video(data, crawl_doc)

  original_user = video.user
  if original_user:
    video.user = None
    print_user(data_source, original_user)
  user_url = video.user_url

  url = video.url
  data = thrift2str(video)
  if not data:
    sys.stderr.write('reporter:counter:map,map_thrift2str,1\n')
    return
  if not user_url:
    user_url = 'None'
  print url + '\t' + user_url + '\t' + data_source + '\t' + 'video' + '\t' + base64.b64encode(data)


def print_user(data_source, original_user):
  if not data_source or not original_user:
    sys.stderr.write('reporter:counter:map,invalid_user,1\n')
    return
  user_url = original_user.url
  if not user_url:
    sys.stderr.write('reporter:counter:map,miss_user_url,1\n')
    return
  user_str = thrift2str(original_user)
  if not user_str:
    sys.stderr.write('reporter:counter:map,map_user2str,1\n')
    return
  print user_url + '\t' + user_url + '\t' + data_source + '\t' + 'user' + '\t' + base64.b64encode(user_str)


def process_old_video(data_source, data_str, url, user_url, url_type):
  if data_source is not None:  # not from old video data
    return False
  if url_type == 'user':
    sys.stderr.write('reporter:counter:map,old_user,1\n')
  elif url_type == 'video':
    sys.stderr.write('reporter:counter:map,old_video,1\n')
  print url + '\t' + user_url + '\t' + 'old_data' + '\t' + url_type + '\t' + data_str 
  return True


if __name__ == '__main__':
  video_adaptor = VideoAdaptor('templates')
  while 1:
    line = sys.stdin.readline()
    if not line:
      break
    user_url = 'None'
    line_data = line.strip().split('\t', 2)
    if len(line_data) == 3:
      user_url = line_data.pop(1)
    if len(line_data) != 2:
      sys.stderr.write('reporter:counter:map,map_input_not_2,1\n')
      continue

    url, data_base64 = line_data
    data_source = None
    if url.endswith('&crawl'):
      data_source = 'crawl'
      url = url.replace('&crawl', '')

    url_type = get_url_type(url)
    if not url_type:
      sys.stderr.write('reporter:counter:map,url_type_error,1\n')
      continue

    if process_old_video(data_source, data_base64, url, user_url, url_type):
      continue

    try:
      data_str = base64.b64decode(data_base64)
    except:
      sys.stderr.write('reporter:counter:map,map_decode_failed,1\n')
      continue

    if data_source == 'crawl':
      sys.stderr.write('reporter:counter:map,crawl_page,1\n')

    try:
      crawl_doc = str2crawldoc(data_str)
    except:
      sys.stderr.write('reporter:counter:map,map_error_crawldoc,1\n')
      continue

    parsed_data = video_adaptor.get_static(crawl_doc)
    if not parsed_data:
      sys.stderr.write('reporter:counter:map,map_parse_failed,1\n')
      continue

    if url_type == 'user':
      original_user = build_user(parsed_data)
      if not original_user:
        sys.stderr.write('reporter:counter:map,build_user,1\n')
      print_user(data_source, original_user)
    elif url_type == 'video':
      print_video(data_source, parsed_data, crawl_doc)

