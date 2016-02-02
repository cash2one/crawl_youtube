#!/usr/bin/python
# coding=utf-8

import os
import sys
import time
import base64

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

from le_crawler.proto.video.ttypes import OriginalUser
from le_crawler.proto.crawl.ttypes import CategoryProportion, LanguageProportion, LanguageType
from le_crawler.common.utils import str2mediavideo, thrift2str, str2user


class MergeItem:
  def __init__(self):
    self.reset('')

  def reset(self, user_url=None):
    self._user_url = user_url
    self._user_b64 = None
    self._related_country_dict = {}

  def get_user_url(self):
    return self._user_url

  def add_item(self, user_url, data_type, related_user_url, data):
    if data_type == 'user':
      self._user_b64 = data
    elif data_type == 'mined_countrys':
      if not data:
        return
      countrys = data.split(';')
      if not countrys:
        return
      for country in countrys:
        self._related_country_dict[country] = self._related_country_dict.get(country, 0) + 1


  def print_item(self):
    if not self._user_url or not self._user_b64:
      return
    sys.stderr.write('reporter:counter:reduce,user_total,1\n')
    if not self._related_country_dict:
      print 'user_info' + '\t' + self._user_url + '\t' + self._user_b64
      return

    mined_countrys = []
    for key, value in self._related_country_dict.items():
      if value >= 2:
        mined_countrys.append(key)
    if not mined_countrys:
      print 'user_info' + '\t' + self._user_url + '\t' + self._user_b64
      return

    try:
      original_user = str2user(base64.b64decode(self._user_b64))
    except:
      sys.stderr.write('reporter:counter:reduce,reduce_decode_failed,1\n')
      print 'user_info' + '\t' + self._user_url + '\t' + self._user_b64
      return

    if not original_user:
      sys.stderr.write('reporter:counter:reduce,not_user,1\n')
      return

    country_source_list = original_user.country_source_list
    for country in mined_countrys:
      country_source_list = merge_country_source(country_source_list, 
          CountryCode._NAMES_TO_VALUES.get(country, CountryCode.UNKNOWN), [CountrySource.MINED])
    original_user.country_source_list = country_source_list

    user_str = thrift2str(original_user)
    if not user_str:
      sys.stderr.write('reporter:counter:reduce,failed_user2str,1\n')
      return
    user_base64 = base64.b64encode(user_str)
    if not user_base64:
      sys.stderr.write('reporter:counter:reduce,failed_encodeuserb64,1\n')
      return

    sys.stderr.write('reporter:counter:reduce,mined_country_user,1\n')
    print 'user_info' + '\t' + self._user_url + '\t' + user_base64
    print 'mined_country_user' + '\t' + self._user_url + '\t' + user_base64
    if 'IN' in mined_countrys:
      sys.stderr.write('reporter:counter:reduce,mined_india_user,1\n')
      print 'india_mined_user' + '\t' + self._user_url + '\t' + user_base64
    return


def main():
  merge_item = MergeItem()
  while 1:
    line = sys.stdin.readline()
    if not line:
      break

    line_data = line.strip().split('\t')
    if len(line_data) !=4:
      sys.stderr.write('reporter:counter:reduce,not_len_line_4,1\n')
      continue

    user_url, data_type, related_user_url, data = line_data

    if user_url == merge_item.get_user_url():
      merge_item.add_item(user_url, data_type, related_user_url, data)
    else:
      merge_item.print_item()
      merge_item.reset(user_url)
      merge_item.add_item(user_url, data_type, related_user_url, data)
  merge_item.print_item()


if __name__ == '__main__':
  main()

