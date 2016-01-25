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
  
if __name__ == '__main__':
  while 1:
    line = sys.stdin.readline()
    if not line:
      break
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
      else:
        print user_url + '\t1_video\t' + url + '\t' + data_base64
        #print user_url + '\t1_video\t' + url + '\t' + '~'
    elif data_type == 'user':
      if len(line_data) != 2:
        sys.stderr.write('reporter:counter:map,not_len_usr_data_2,1\n')
        continue
      data_base64 = line_data[1]
      print url + '\t0_user\t' + url + '\t' + data_base64
    else:
      sys.stderr.write('reporter:counter:map,error_data_type,1\n')

