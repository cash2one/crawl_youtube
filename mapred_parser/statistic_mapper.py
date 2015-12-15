#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import base64
import sys
import time
from datetime import datetime

from le_crawler.proto.video.ttypes import State
from le_crawler.common.utils import str2mediavideo, video_fields, important_fields


category_mapping = {'news': ['资讯', '新闻', '社会', '台湾', '热点'],
                    'sports': ['体育', 'NBA'],
                    'tech': ['科技'],
                    'ent': ['娱乐'],
                    'fun': ['搞笑'],
                    'finance': ['财经', '股市'],
                    'car': ['汽车'],
                    'beauty': ['美女']}

domain_set = set(['iqiyi.com', 'ifeng.com', 'youku.com', 'tudou.com', 'hunantv.com', 
                  'sohu.com', 'wasu.cn', 'pptv.com', '56.com', 'fun.tv', 'people.com.cn', 
                  'qq.com', 'sina.com.cn', '163.com', 'hexun.com', 'cztv.com'])


def statistic(item, counter):
  data = str2mediavideo(base64.b64decode(item))
  domain = getattr(data, 'domain')
  sys.stderr.write('reporter:counter:statistic,video_%s,1\n' % domain)
  if getattr(data, 'page_state') == State.DEAD_LINK:
    sys.stderr.write('reporter:counter:statistic,dead_link,1\n')
    return
  for key in video_fields.keys():
    if getattr(data, key) is None and key in important_fields:
      sys.stderr.write('reporter:counter:statistic,missed_%s,1\n' % key)
  showtime = data.content_timestamp
  if not showtime:
    sys.stderr.write('reporter:counter:statistic,showtime_None,1\n')
    return
  if data.content_timestamp > data.crawl_time:
    sys.stderr.write('reporter:counter:statistic,crawl_before_content_time,1\n')
  try:
    showtime = int(showtime)
    datetime.fromtimestamp(showtime)
  except:
    sys.stderr.write('reporter:counter:statistic,showtime_wrong,1\n')
    return
  else:
    data.tags = (data.tags or '') + (data.category_list or '') + (data.crumbs or '')
    time_now = int(time.time())
    if (time_now - showtime) > 0 and (time_now - showtime) < 86400:
      sys.stderr.write('reporter:counter:statistic,24h_%s,1\n' % data.domain)
      sys.stderr.write('reporter:counter:statistic,24h,1\n')
      for category, key_words in category_mapping.iteritems():
        for key in key_words:
          if key in data.tags and data.domain in domain_set:
            k = '%s_%s' % (category, data.domain)
            if data.poster:
              counter[k] = counter.get(k, 0) + 1
            else:
              counter[k + '_no_poster'] = counter.get(k + '_no_poster', 0) + 1
            counter[category] = counter.get(category, 0) + 1
            break
      if 'NBA' in data.tags and data.domain == 'qq.com':
        counter['NBA_qq'] = counter.get('NBA_qq', 0) + 1
        if not data.poster:
          counter['NBA_qq_no_poster'] = counter.get('NBA_qq_no_poster', 0) + 1
    if (time_now - showtime) > 0 and (time_now - showtime) < 172800:
      sys.stderr.write('reporter:counter:statistic,48h,1\n')
    if (time_now - showtime) > 0 and (time_now - showtime) < 259200:
      sys.stderr.write('reporter:counter:statistic,72h,1\n')
    if (time_now - showtime) > 0 and (time_now - showtime) < 2592000:
      sys.stderr.write('reporter:counter:statistic,30d,1\n')
    sys.stderr.write('reporter:counter:statistic,showtime_correct,1\n')


if __name__ == '__main__':
  counter = {} 

  while 1:
    line = sys.stdin.readline()
    if not line:
      break
    data = line.strip().split('\t', 2)
    if len(data) != 2 and len(data) != 3:
      sys.stderr.write('reporter:counter:map_error,map_input_not_2_or_3,1\n')
      continue
    statistic(data[-1], counter)

  for k, v in counter.iteritems():
    print k + '\t' + str(v)

