#!/usr/bin/python
# coding=utf8


import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')



from le_crawler.proto.video.ttypes import OriginalUser
from le_crawler.common.utils import str2mediavideo, thrift2str, multi_key_fields, compress_play_trends, str2user #, int_typeids

if __name__ == '__main__':
  while 1:
    line = sys.stdin.readline()
    if not line:
      break
    line_data = line.strip().split('\t')
    if len(line_data) != 2:
      sys.stderr.write('reporter:counter:map,map_input_not_2,1\n')
      continue
    user_url, data_base64 = line_data

    try:
      user_str = base64.b64decode(data_base64)
      original_user = str2user(base64.b64decode(data_base64))
    except:
      sys.stderr.write('reporter:counter:map,map_decode_failed,1\n')
      continue
    if original_user.country == 'IN':
      sys.stderr.write('reporter:counter:map,india_user_total,1\n')
      print 'india_user' + '\t' + user_url + '\t' + data_base64


