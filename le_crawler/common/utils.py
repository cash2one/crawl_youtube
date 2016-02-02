#!/usr/bin/python
# coding=utf-8
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import os
import sys
import gzip
import time
import json
import base64
import letvbase
import logging
import urllib2
import StringIO
import traceback
from lxml import etree

try:
  import cPickle as pickle
except:
  import pickle

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.Thrift import TType
from time_parser import TimeParser
from duration_parser import duration2int
from parse_youtube import parse_thumbnail_list
from ..proto.crawl_doc.ttypes import CrawlDoc
from ..proto.video.ttypes import MediaVideo, State, OriginalUser
from ..proto.crawl.ttypes import CrawlDocType, Request, Response, HistoryItem, CrawlHistory, PageType, UserState, CountrySourceInfo, CountryCode

def str_unzip(buf):
  f = gzip.GzipFile(fileobj = StringIO.StringIO(buf), mode = 'rb')
  html = f.read()
  f.close()
  return html


def str_gzip(content):
  buf = StringIO.StringIO()
  f = gzip.GzipFile(mode = 'wb', fileobj = buf)
  f.write(content)
  f.close()
  return buf.getvalue()


def del_repeat(li):
  if not li:
    return li
  unique_li = set(li)
  return list(unique_li)

def FetchHTML(url, timeout=30, header={}, data=None, check_redirect=False):
  if not url:
    return (None, None) if check_redirect else None
  for i in range(2):
    ret = _fetch_html(url, timeout, True, header, data, check_redirect)
    if ret:
      return ret
    time.sleep(1)
  logging.debug('failed to get html of url, %s', url)
  return (None, None) if check_redirect else None

def _fetch_html(url, timeout, check_charset=True, header={}, post_data=None, check_redirect=False):
  def get_charset(s):
    s = s.replace(" ", "").lower()
    index = s.find("charset=")
    if index != -1:
      s = s[index + len("charset="):]
      index = s.find(">")
      if index != -1:
        s = s[:index]
      s = s.strip("\",; /")
      return s
  try:
    req = urllib2.Request(url)
    ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153'
    req.add_header("User-Agent", ua)

    if isinstance(header, dict):
      req.headers.update(header)
    f = urllib2.urlopen(req, data=post_data, timeout=timeout)
    encoding = None
    if "content-encoding" in f.info().dict:
      encoding = f.info().dict["content-encoding"]
    if encoding and encoding != "gzip":
      logging.warning("invalid compress encoding [%s] for url [%s]" % (encoding, url))
      return (None, None) if check_redirect else None
    html = f.read()
    if encoding:
      html = Decompress(html)

    charset = None
    if "content-type" in f.info().dict:
      charset = get_charset(f.info().dict["content-type"])
    if charset is None and check_charset:
      charset = GetCharset(html)
    if charset not in [None, 'utf8', 'utf-8']:
      html = html.decode(charset, "ignore").encode('utf8')
    return (html, f.url) if check_redirect and html else html
  except:
    logging.debug("failed to get html, %s", url)
    return (None, None) if check_redirect else None
  else:
    f.close()

def Decompress(buf):
  f = gzip.GzipFile(fileobj=StringIO.StringIO(buf), mode='rb')
  html = f.read()
  f.close()
  return html

def GetCharset(html):
  charset = None
  rules = ["substring-after(/html/head/meta"
           "[contains(@content, 'charset')]/@content, 'charset=')",
           "/html/head/meta/@charset"]
  try:
    for rule in rules:
      datas = etree.HTML(html).xpath(rule)
      if isinstance(datas, str) and len(datas) > 0:
        charset = datas
      elif isinstance(datas, list) and len(datas) > 0 and len(datas[0]) > 0:
        charset = datas[0]
      else:
        continue
      break
  except Exception:
    logging.exception('failed to retrieve charset info')
    return None
  return charset

def atoi(num_str):
  if num_str is None:
    return None
  if isinstance(num_str, (int, float, long)):
    return num_str
  if not isinstance(num_str, basestring):
    return None
  try:
    return int(num_str)
  except:
    return None

  try:
    num_str = num_str if isinstance(num_str, unicode) \
      else num_str.decode('utf-8', 'ignore')
    num_str = erase_all(num_str, [',', u'，', ' '])
    digit_list = [unicode(i) for i in range(0, 10)]
    digit_list.append(u'.')
    multiple = {u'亿': 100000000, u'万': 10000, u'千': 1000, u'K': 1000, u'k': 1000, u'百': 100, u'十': 10}
    digit_map = {}
    for k, v in zip(list(u'零一二三四五六七八九'), range(0, 10)):
      digit_map[k] = str(v)
    result = 0
    clip_num = ''
    clip_decimal = None
    skip_multiple = False
    num_len = len(num_str)
    for idx, char in enumerate(num_str):
      if char == u'.' or char == u'点':
        skip_multiple = False
        clip_decimal = ''
        if idx < num_len - 1:
          continue
      if char in digit_list or char in digit_map:
        skip_multiple = False
        char = digit_map[char] if char in digit_map else char
        if clip_decimal is None:
          clip_num += char
        else:
          clip_decimal += char
        if idx < num_len - 1:
          continue
      elif char not in multiple and char not in digit_list:
        return None
      if skip_multiple:
        continue
      factor = 1
      while idx < num_len and num_str[idx] in multiple:
        factor *= multiple[num_str[idx]]
        idx += 1
        skip_multiple = True
      clip_num = '0' if not clip_num else clip_num
      clip_decimal = '0' if not clip_decimal else clip_decimal
      result += int(clip_num) * factor + \
                int(clip_decimal) * factor * 1.0 / (10 ** len(clip_decimal))
      clip_decimal = None
      clip_num = ''
      result_int = int(result)
    return result_int if result_int == result else result
  except:
    logging.exception('failed to parse string to int/float, %s', num_str)
    return None

def erase_all(string, erase_list, from_idx=0):
  clip = reduce(lambda x, y: x.replace(y, ''), erase_list, string)
  return clip if not from_idx else string[:from_idx] + clip



time_parser = TimeParser()

def gen_video_fields():
  data = {}
  for x in MediaVideo.thrift_spec:
    if x:
      data[x[2]] = x[1]
  return data

video_fields = gen_video_fields()  # {name: type_id}
int_typeids = set([TType.DOUBLE, TType.I16, TType.I32, TType.I64])
#{x[2]: x[1] for x in MediaVideo.thrift_spec if x}

source_set = {'baomihua.com': 1,
              'ifeng.com': 2,
              'ku6.com': 3,
              'qq.com': 4,
              'sohu.com': 5,
              'youku.com': 6,
              'letv.com': 7,
              'people.com.cn': 8,
              'fun.tv': 9,
              '163.com': 10,
              'sina.com.cn': 11,
              'v1.cn': 12,
              'iqiyi.com': 13,
              'tudou.com': 14,
              'uusee.com': 15,
              'autohome.com.cn': 16,
              'bitauto.com': 17,
              '56.com': 18,
              'cntv.cn': 19,
              'kankan.com': 20,
              'pptv.com': 21,
              'zol.com.cn': 22,
              'wasu.cn': 23,
              'smgbb.cn': 24,
              'hunantv.com': 25,
              'cztv.com':26,
              'toutiao.com':27,
              'youtube.com':28,
              'hexun.com': 29,
              'soku.com':30
}

#multi_key_fields = set(['tags', 'category', 'actor', 'director', 'collects', 'category_list'])
multi_key_fields = set(['actor', 'director', 'collects'])

required_fields = set(['id', 'title', 'url', 'poster', 'showtime'])
important_fields = required_fields - set(['id', 'title', 'url', 'poster'])

video_fields_flags = {
    'title':        1,
    'poster':       2,
    'showtime':     4,
    'play_total':   8
}

def thrift2str(thrift_obj):
  if thrift_obj is None:
    return None
  try:
    thrift_obj.validate()
    trans = TTransport.TMemoryBuffer()
    prot = TBinaryProtocol.TBinaryProtocol(trans)
    thrift_obj.write(prot)
    values = trans.getvalue()
    if values:
      return values
  except:
    logging.exception('thrift2str: %s', thrift_obj)
    return None


def str2crawldoc(thrift_str):
  if thrift_str is None:
    return None
  try:
    trans = TTransport.TMemoryBuffer(thrift_str)
    prot = TBinaryProtocol.TBinaryProtocol(trans)
    thrift_ob = CrawlDoc()
    thrift_ob.read(prot)
    thrift_ob.validate()
    return thrift_ob
  except:
    logging.exception('str2thrift failed: %s', thrift_str)
  return None


def str2mediavideo(thrift_str):
  if not thrift_str:
    return None
  try:
    trans = TTransport.TMemoryBuffer(thrift_str)
    prot = TBinaryProtocol.TBinaryProtocol(trans)
    thrift_ob = MediaVideo()
    thrift_ob.read(prot)
    thrift_ob.validate()
    return thrift_ob
  except:
    logging.exception('str2mediavideo failed: %s', thrift_str)
    return None


def str2user(thrift_str):
  if not thrift_str:
    return None
  try:
    trans = TTransport.TMemoryBuffer(thrift_str)
    prot = TBinaryProtocol.TBinaryProtocol(trans)
    thrift_ob = OriginalUser()
    thrift_ob.read(prot)
    thrift_ob.validate()
    return thrift_ob
  except:
    logging.exception('str2user failed: %s', thrift_str)
    return None


def gen_docid(url):
  return letvbase.get_fingerprint_i64(url)


def GetKey(js_dict, key, type_need=str):
  try:
    if js_dict.has_key(key):
      if isinstance(js_dict[key], type_need):
        return True, js_dict[key]
      else:
        return True, type_need(js_dict[key])
  except:
    pass
    # logging.error('GetKey ' + str(Exception) + ':' + str(e))
  return False, None


def json2crawlerdoc(js_dict):
  if js_dict is None:
    logging.error('js_dict is None')
    return None
  try:
    # base
    crawldoc = CrawlDoc()
    crawldoc.request = Request()
    crawldoc.response = Response()
    # docid generate from response url
    if js_dict.has_key('url'):
      crawldoc.docid = gen_docid(js_dict['url'])
      crawldoc.response.url = js_dict['url']
    else:
      logging.error('json2crawlerdoc url is None' + js_dict)
      return None
    crawldoc.doctype = CrawlDocType.RESPONSEDOC
    isset, crawldoc.crawl_time = GetKey(js_dict, 'down_time', int)
    isset, crawldoc.original_code = GetKey(js_dict, 'page_encoding')
    isset, crawldoc.content = GetKey(js_dict, 'page')
    isset, crawldoc.refer_url = GetKey(js_dict, 'referer')
    # response
    resta, crawldoc.response.header = GetKey(js_dict, 'http_header')
    isset = isset or resta
    resta, crawldoc.response.meta = GetKey(js_dict, 'meta')
    isset = isset or resta
    resta, crawldoc.response.return_code = GetKey(js_dict, 'status', int)
    isset = isset or resta
    if not isset:
      crawldoc.response = None
    # request
    isset = False
    resta, crawldoc.request.raw_url = GetKey(js_dict, 'rawurl')
    isset = isset or resta
    if not isset:
      crawldoc.request = None
    # base
    return crawldoc
  except Exception, e:
    logging.error('json2crawlerdoc ' + str(Exception) + ':' + str(e) + js_dict)
    return None


def get_video_attr_state(video):
  if not video:
    return 0
  attr_state = 0
  for key, flag in video_fields_flags.iteritems():
    if getattr(video, key):
      attr_state |= flag
  return attr_state


def build_video(data, crawl_doc):
  if not data:
    return None
  video = crawl_doc.video or MediaVideo()
  url = data.get('url')
  dead_link = data.get('page_state') == State.DEAD_LINK

  history_item = HistoryItem()
  history_item.crawl_time = data.get('crawl_time')
  history_item.play_count = data.get('play_total')
  history_item.doc_type = crawl_doc.doc_type
  crawl_history = CrawlHistory()
  crawl_history.update_time = int(time.time())
  crawl_history.crawl_history = [history_item]
  video.crawl_history = crawl_history

  for key, type_id in video_fields.items():
    if key == 'crawl_history':
      continue
    value = data.get(key)
    if value is None:
      if dead_link:
        continue
      # if key in important_fields:
      #   sys.stderr.write('reporter:counter:build_video,build_missed_%s_%s,1\n' % (data.get('domain', 'domain'), key))
      if key == 'poster' and crawl_doc.page_type == PageType.PLAY:
        continue
      if key in required_fields and not getattr(video, key):
        logging.debug('%s is MISSING, %s, page_type: %s',
                      key, url, PageType._VALUES_TO_NAMES.get(crawl_doc.page_type))
      continue
    try:
      if type_id == TType.BOOL:
        value = bool(value)
      elif isinstance(value, basestring) and \
           type_id in int_typeids and \
           not value.replace('.', '').isdigit():
        continue
      elif type_id == TType.DOUBLE:
        value = float(value)
      elif type_id in [TType.I16, TType.I32, TType.I64]:
        value = int(value)
    except:
      logging.exception('failed convert %s, %s to %s, %s', url, key, type_id, value)
      #print 'failed convert %s, %s to %s, %s', (url, key, type_id, value)
      # if key in important_fields:
      #   sys.stderr.write('reporter:counter:build_video,build_convert_%s,1\n' % key)
      continue
    if value is not None:
      setattr(video, key, value)
  video.update_time = int(time.time())
  return video


def merge_list_video(list_data, video):
    for k, v in list_data.items():
      if not v or k not in video_fields:
        continue
      video_v = getattr(video, k)
      if not video_v:
        setattr(video, k, v)


def str2dict(s):
  dic = {}
  if not s:
    return dic
  for item in s.split(';'):
    k, v = item.split('|')
    dic[k] = v
  return dic


def dict2str(dic):
  if not dic:
    return None
  s = []
  for k, v in dic.items():
    s.append(str(k) + '|' + str(v))
  return ';'.join(s)


def drop_noise(data, noise_list, splitter=';'):
  attrs = set(data.split(splitter))
  for token in noise_list:
    if token in attrs:
      attrs.remove(token)
  return splitter.join(list(attrs)).strip(splitter)


def massage_data(data, printable=True):
  if not data:
    return None
  url = data.get('url')
  if not url:
    return None
  for key, type_id in video_fields.items():
    value = data.get(key)
    if value is None:
      if key in data:
        del data[key]
      continue
    if key in ['play_total', 'voteup_count', 'votedown_count']:
      value = atoi(value)
      if value is not None:
        data[key] = value
      else:
        del data[key]
    elif key == 'showtime':
      content_timestamp = time_parser.timestamp(value, refer_time=data.get('create_time'))
      if content_timestamp:
        data['content_timestamp'] = content_timestamp
      elif printable:
        print url + '\t' + 'debug' + '\t' + 'debug' + '\t' + key + ';' + base64.b64encode(pickle.dumps(data)) + '\t' + '~'
    elif key == 'duration':
      duration = duration2int(value)
      if duration:
        data['duration_seconds'] = duration
      elif printable:
        print url + '\t' + 'debug' + '\t' + 'debug' + '\t' + key + ';' + base64.b64encode(pickle.dumps(data)) + '\t' + '~'
    if type_id == TType.STRING:
      data[key] = value.encode('utf-8')
    # if not value and key in important_fields:
    #   sys.stderr.write('reporter:counter:build_video,build_convert_%s,1\n' % key)
  return data


def massage_youtube_data(data):
  if not data:
    return None
  url = data.get('url')
  if not url:
    return None
  for key, type_id in video_fields.items():
    value = data.get(key)
    if value is None:
      if key in data:
        del data[key]
      continue
    if type_id == TType.STRING:
      data[key] = value.encode('utf-8')
  return data


def safe_eval(input_str):
  if not input_str:
    return None
  try:
    return eval(input_str, {"__builtins__": None},
                {'false': False, 'true': True, 'null': None})
  except:
    sys.stderr.write(traceback.format_exc())
    return None


def reverse_kv(dic):
  if not dic:
    return dic
  result = {}
  for k, v in dic.items():
    result[v] = k
  return result


def list2dict(data):
  dic = {}
  for idx, value in enumerate(data):
    dic[str(idx)] = value
  return dic


def obj2dict(obj):
  if isinstance(obj, dict):
    data = {}
    for (k, v) in obj.items():
      data[k] = obj2dict(v)
    return data
  elif hasattr(obj, "_ast"):
    return obj2dict(obj._ast())
  elif hasattr(obj, "__iter__"):
    return [obj2dict(v) for v in obj]
  elif hasattr(obj, "__dict__"):
    data = dict([(key, obj2dict(value)) for key, value in obj.__dict__.iteritems()
                 if not callable(value) and not key.startswith('_')])
    return data
  else:
    return obj


category_list = set(['电影', '电视剧', '动漫', '综艺', '娱乐', '体育', '新闻', '原创',
                     '其他', '音乐', '搞笑', '综艺', '教育', '生活', '汽车', '电视节目',
                     '纪录片', '公开课', '乐视制造', '时尚', '游戏', '财经', '旅游',
                     '教育', '热点', '曲艺', '戏曲', '亲子', '宠物', '广告', '女人',
                     '科技', '美女', '军事', '社会', '国际', '世界杯', '搜狐出品',
                     '头条'])

categoryid_set = list2dict(category_list)

category_set = reverse_kv(categoryid_set)


def get_slope(i, j, p_list):
  dy = float(p_list[j][1] - p_list[i][1])
  dx = p_list[j][0] - p_list[i][0]
  return dy / dx



def compress_play_trends(dict_trends):
  if not dict_trends:
    return None

  list_trends = sorted(dict_trends.iteritems(), key=lambda t: t[0])
  if len(list_trends) < 3:
    return list_trends

  # check trends' value
  trends = [list_trends[0]]
  v = list_trends[0][1]
  for i in range(1, len(list_trends)-1):
    if list_trends[i][1] > v:
      trends.append(list_trends[i])
      v = list_trends[i][1]
  if trends[-1][0] != list_trends[-1][0]:
    trends.append(list_trends[-1])

  if len(trends) < 10:
    return trends

  import math
  # smooth the trends curve
  diff_range = math.tan(math.radians(5)) # 5/360 degree difference
  cur_i = 0
  list_trends = [trends[0]]
  if not trends[0][1]:
    list_trends.append(trends[1])
    cur_i = 1
  cur_slope = get_slope(cur_i, cur_i+1, trends)
  for i in range(cur_i+2, len(trends)-1):
    slope = get_slope(cur_i, i, trends)
    if math.fabs(slope - cur_slope) > diff_range:
      list_trends.append(trends[i-1])
      cur_i = i - 1
      cur_slope = get_slope(i-1, i, trends)
  list_trends.append(trends[-1]) # add the last point
  return list_trends


def history2dict(history):
  if not history:
    return None

  h_list = []
  for item in history.crawl_history:
    d = {}
    d['crawl_time'] = item.crawl_time
    d['crawl_interval'] = item.crawl_interval
    d['play_count'] = item.play_count
    h_list.append(d)
  h_dict = {}
  h_dict['crawl_history'] = h_list
  h_dict['update_time'] = history.update_time
  return h_dict 

def gen_next_schedule_time(crawl_history):
  if not crawl_history:
    return None
  now = int(time.time())
  if len(crawl_history) == 1:
    return now + 60*60
  incr_count_hourly = ((crawl_history[0].get('play_count') or 0) - (crawl_history[1].get('play_count') or 0)) * 60 * 60 \
      / ((crawl_history[0].get('crawl_time') or 0) - (crawl_history[1].get('crawl_time') or 0) or 1)
  schedule_interval = crawl_history[0]['crawl_interval'] / 2 if incr_count_hourly > 1000 \
      else crawl_history[0]['crawl_interval'] * 2
  return now + schedule_interval

def merge_country_source(country_source_list, code, source_list_src):
  if code is None or source is None:
    return country_source_list
  if country_source_list is None:
    country_source_list = []
  for source_info in country_source_list:
    if source_info.country_code == code:
      source_list = source_info.source_list
      if source_list is not None and source_list_src is not None:
        source_info.source_list = list(set(source_list) + set(source_list_src))
      return country_source_list
  source_info = CountrySourceInfo()
  source_info.country_code = code
  source_info.source_list = source_list_src
  country_source_list.append(source_info)
  return country_source_list


def build_user(channel_dict):
  if not channel_dict:
    return None
  original_user = OriginalUser()
  channel_id = channel_dict.get('channel_id', None)
  if not channel_id:
    return
  original_user.channel_id = channel_id.encode('utf-8')
  channel_url = 'https://www.youtube.com/channel/%s' % channel_id
  original_user.url = channel_url.encode('utf-8')

  original_user.user_name = channel_dict.get('user_name', None)
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

  
  country_source_list = []
  country = channel_dict.get('country', None)
  if country:
    country_source_list = merge_country_source(country_source_list, 
        CountryCode._NAMES_TO_VALUES.get('country', CountryCode.UNKNOWN), [CountrySource.YOUTUBE])
  
  popular_countrys = channel_dict.get('popular_countrys', None)
  if popular_countrys:
    for country in popular_countrys:
      country_source_list = merge_country_source(country_source_list, 
          CountryCode._NAMES_TO_VALUES.get(country, CountryCode.UNKNOWN), [CountrySource.POPULAR])

  product_countrys = channel_dict.get('popular_countrys', None)
  if product_countrys:
    for country in product_countrys:
      country_source_list = merge_country_source(country_source_list, 
          CountryCode._NAMES_TO_VALUES.get(country, CountryCode.UNKNOWN), [CountrySource.PRODUCT])

  original_user.country_source_list = country_source_list

  original_user.video_num = int(channel_dict.get('video_num', '0'))
  original_user.play_num = int(channel_dict.get('play_num', '0'))
  original_user.fans_num = int(channel_dict.get('fans_num', '0'))
  original_user.comment_num = int(channel_dict.get('comment_num', '0'))
  original_user.update_time = channel_dict.get('update_time', None)
  
  out_related_user = channel_dict.get('out_related_user', [])
  if out_related_user:
    original_user.out_related_user = [related_user.encode('utf-8') for related_user in out_related_user]

  original_user.state = UserState.DISABLE if channel_dict.get('disabled', False) else UserState.NORMAL

  return original_user


