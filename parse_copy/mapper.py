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
from le_crawler.common.lejian_video_settings import ACCEPT_URL_REG as url_regs
from le_crawler.common.utils import massage_data, thrift2str, str2crawldoc, build_video, str2mediavideo

play_page_merged_keys = ['domain', 'domain_id']
url_normalizer = UrlNormalize.get_instance()


def print_list(base_url, data_source, data, crawl_doc):
  blocks = []
  for item in data.keys():
    if 'items' in item:
      blocks.extend(data.pop(item))
  if not blocks:
    return
  domain = data.get('domain')
  in_links = crawl_doc.in_links or []
  in_links = copy.deepcopy(in_links)
  inlink = Anchor(url=crawl_doc.url, doc_type=crawl_doc.doc_type, discover_time=crawl_doc.discover_time)
  re_obj_list = url_regs.get(domain)
  for block in blocks:
    for k, v in block.items():
      block[k] = v[0]
    # filtering out the video block whose url does not match the regex
    url = get_abs_url(base_url,  block.get('url'))
    if not url:
      #sys.stderr.write('failed get absolute url, %s, base url: %s\n' % (block.get('url'), base_url))
      continue
    #url = block['url'] = url_normalizer.get_unique_url(url) or url
    url = block['url'] = url
    if not url or not url.startswith('http://'):
      #sys.stderr.write('invalid block url, %s, domain: %s\n' % (url, domain))
      sys.stderr.write('reporter:counter:map_error,map_block_invalid_url,1\n')
      continue
    if re_obj_list:
      for re_obj in re_obj_list:
        if re_obj.search(url):
          break
      else:
        continue
    block['doc_id'] = letvbase.get_fingerprint_i64(url)
    block['id'] = str(block['doc_id'])
    block['discover_time'] = block['crawl_time'] = block['create_time'] = int(time.time())
    in_links.append(inlink)
    block['in_links'] = in_links
    if in_links:
      block['inlink_history'] = [in_links]
    for k, v in data.items():
      if crawl_doc.page_type == PageType.PLAY and k not in play_page_merged_keys:
        continue
      if v and not block.get(k):
        block[k] = v
    print_video(data_source, block, url, crawl_doc)


def print_video(data_source, data, url, crawl_doc, data_type='video', data_base64=None):
  if not url or not data_source:
    sys.stderr.write('reporter:counter:map_error,invalid_data,1\n')
    return
  page_state = data.get('page_state')
  if page_state and page_state & CrawlDocState.NO_MD5 != 0:
    data_type = 'no_md5'
  massage_data(data, printable=False)
  if data_source == 'crawl':
    video = build_video(data, crawl_doc)
    user_url = 'None'
    if video.user and video.user.url:
      user_url = video.user.url
    data = thrift2str(video)
    if not data:
      sys.stderr.write('reporter:counter:map_error,map_thrift2str,1\n')
      return
  print url + '\t' + user_url + '\t' + data_source + '\t' + data_type + '\t' + base64.b64encode(data) + '\t' + '~'  # (data_base64 or '~')
  #print '%s\t%s\t%s\t%s\t%s\t~' % (url, user_url, data_source, data_type, video)
  #print '%s\t%s' % (url, str2mediavideo(data))


def print_error(url, data_base64):
  #sys.stderr.write('parse failed, %s\n' % url)
  sys.stderr.write('reporter:counter:map_error,map_parse_failed,1\n')
  print '%s\tNone\terror\terror\t~\t%s' % (url, data_base64)


def dump_html(html):
  with open('raw.html', 'w') as f:
    f.write(html)
  exit(1)


def process_old_video(data_source, data_str, url, user_url):
  if data_source is not None:  # not from old video data
    return False
  sys.stderr.write('reporter:counter:map,old_data,1\n')
  print url + '\t' + user_url + '\t' + 'old_data' + '\t' + 'video' + '\t' + data_str + '\t' + '~'
  return True


if __name__ == '__main__':
  video_adaptor = VideoAdaptor('video_templates')
  list_adaptor = VideoAdaptor('list_templates')
  for k, v in url_regs.iteritems():
    for i, reg in enumerate(v):
      v[i] = re.compile(reg)

  while 1:
    line = sys.stdin.readline()
    if not line:
      break
    user_url = 'None'
    line_data = line.strip().split('\t', 2)
    if len(line_data) == 3:
      user_url = line_data.pop(1)
    if len(line_data) != 2:
      sys.stderr.write('reporter:counter:map_error,map_input_not_2,1\n')
      continue
    key, data_base64 = line_data
    url_type = key.split('&')
    url = '&'.join(url_type[:-1]) if len(url_type) >= 2 else key
    data_source = url_type[-1] if len(url_type) >= 2 else None
    # url = url_normalizer.get_unique_url(url) or url

    if process_old_video(data_source, data_base64, url, user_url):
      continue

    try:
      data_str = base64.b64decode(data_base64)
    except:
      sys.stderr.write('reporter:counter:map_error,map_decode_failed,1\n')
      continue

    if data_source == 'crawl':
      sys.stderr.write('reporter:counter:map,crawl_page,1\n')

    try:
      crawl_doc = str2crawldoc(data_str)
    except:
      sys.stderr.write('reporter:counter:map_error,map_error_crawldoc,1\n')
      continue
    # dump_html(crawl_doc.response.body)

    parsed_data = None
    if crawl_doc.page_type == PageType.PLAY:
      parsed_data = video_adaptor.get_static(crawl_doc)
    else:
      parsed_data = list_adaptor.get_static(crawl_doc)
    if not parsed_data:
      print_error(url, data_base64)
      continue
    temp_video = crawl_doc.video
    crawl_doc.video = None
    print_list(url, data_source, parsed_data, crawl_doc)
    crawl_doc.video = temp_video

    if crawl_doc.page_type == PageType.PLAY:
      print_video(data_source, parsed_data, url, crawl_doc, data_base64=data_base64)

