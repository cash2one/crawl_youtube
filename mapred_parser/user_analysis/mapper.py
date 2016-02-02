#!/usr/bin/python
# coding=utf8


import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')



from le_crawler.proto.video.ttypes import OriginalUser
from le_crawler.proto.crawl.ttypes import CountrySource, CountryCode
from le_crawler.common.utils import str2user 

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
    print user_url + '\t' + 'user' + '\t' + user_url + '\t' + data_base64

    try:
      original_user = str2user(base64.b64decode(data_base64))
    except:
      sys.stderr.write('reporter:counter:map,map_decode_failed,1\n')
      continue
    if original_user.out_related_user and original_user.country_source_list:
      for country_source_info in original_user.country_source_list:
        if CountrySource.YOUTUBE in country_source_info.source_list:
          if country_source_info.country_code == CountryCode.IN:
            sys.stderr.write('reporter:counter:map,india_user,1\n')
          if not country_source_info.country_code:
            continue
          for related_user in original_user.out_related_user:
            print related_user + '\t' + 'mined_countrys' + '\t' + user_url + '\t' + CountryCode._VALUES_TO_NAMES[country_source_info.country_code]


