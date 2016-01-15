#!/usr/bin/python
# coding=utf-8

import sys
import os
import re
import base64
import time

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')
from le_crawler.common.utils import str2mediavideo, thrift2str, str2user

def get_url_type(url):
  if not url:
    return None
  url_type_reg = {'video': [r'www\.youtube\.com\/watch'],
                  'user':  [r'www\.youtube\.com\/channel',
                            r'www\.googleapis\.com\/youtube\/v3\/channels']}
  for (url_type, reg_list) in url_type_reg.items():
    for reg in reg_list:
      if re.search(reg, url):
        return url_type
  return None
  
def count_video(video):
  if not video:
    return
  category = video.category
  if category:
    category = category.replace(' ', '_')
    sys.stderr.write('reporter:counter:statistic,%s,1\n' % category)
  else:
    sys.stderr.write('reporter:counter:statistic,not_category,1\n')
  content_timestamp = video.content_timestamp
  if not content_timestamp:
    sys.stderr.write('reporter:counter:statistic,not_content_timestamp,1\n')
  now = int(time.time())
  time_delta = now - content_timestamp
  if time_delta > 0 and time_delta < 3600:
    sys.stderr.write('reporter:counter:statistic,video_1h,1\n')
    if time_delta > 0 and time_delta < 7200:
      sys.stderr.write('reporter:counter:statistic,video_2h,1\n')
    if time_delta > 0 and time_delta < 86400:
      sys.stderr.write('reporter:counter:statistic,video_24h,1\n')
      if category:
        sys.stderr.write('reporter:counter:statistic,24h_%s,1\n' % category)
    if time_delta > 0 and time_delta < 172800:
      sys.stderr.write('reporter:counter:statistic,video_48h,1\n')

if __name__ == '__main__':
  while 1:
    line = sys.stdin.readline()
    if not line:
      break
    #file_name, user_url, url, data_type, data_base64 = line.strip().split('\t')
    #print user_url + '\t' + url + '\t' + data_type + '\t' + data_base64
    line_data = line.strip().split('\t')
    url = line_data[0]
    data_type = get_url_type(url)
    if data_type == 'video':
      if len(line_data) != 3:
        sys.stderr.write('reporter:counter:map,not_len_video_data_3,1\n')
        continue
      user_url = line_data[1]
      data_base64 = line_data[2]
      if user_url == 'None':
        sys.stderr.write('reporter:counter:statistic,video_not_user,1\n')
        #sys.stderr.write('reporter:counter:statistic,video_total,1\n')
        """
        try:
          video = str2mediavideo(base64.b64decode(data_base64))
          count_video(video)
        except:
          sys.stderr.write('reporter:counter:map,failed_2_video,1\n')
        """
      else:
        print user_url + '\t1_video\t' + url + '\t' + data_base64
    elif data_type == 'user':
      if len(line_data) != 2:
        sys.stderr.write('reporter:counter:map,not_len_usr_data_2,1\n')
        continue
      data_base64 = line_data[1]
      print url + '\t0_user\t' + url + '\t' + data_base64
    else:
      sys.stderr.write('reporter:counter:map,error_data_type,1\n')

