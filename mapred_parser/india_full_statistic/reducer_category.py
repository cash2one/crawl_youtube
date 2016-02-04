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
from le_crawler.common.parse_youtube import get_url_param



class MergeItem:
  def __init__(self):
    self.reset('')


  def reset(self, user_url=None):
    self._user_url = user_url
    self._user = None
    self._url = None
    self._user_category_dict = {}
    self._user_language_dict = {}
    self._video_total = 0


  def get_user_url(self):
    return self._user_url


  def add_item(self, user_url, data_type, url, data_base64):
    if data_type == 'user':
      try:
        original_user = str2user(base64.b64decode(data_base64))
        self._user = original_user
      except:
        sys.stderr.write('reporter:counter:statistic,failed_2_user,1\n')
    elif data_type == 'video':
      if not self._user:
        return
      if url != self._url:
        self._url = url
        try:
          video = str2mediavideo(base64.b64decode(data_base64))
        except:
          return
          sys.stderr.write('reporter:counter:reduce,failed_2_video,1\n')
        self._video_total += 1
        if video.category:
          self._user_category_dict[video.category] = self._user_category_dict.get(video.category, 0) + 1
        if video.language_type:
          self._user_language_dict[video.language_type] = self._user_language_dict.get(video.language_type, 0) + 1

  def process_user_category(self):
    if not self._user_category_dict or not self._video_total:
      return
    category_list =  sorted(self._user_category_dict.items(), key=lambda x: x[1], reverse=True)
    category_proportion_li = []
    count = 0
    idx = 0
    for key, value in category_list:
      idx += 1
      if idx > 3:
        break
      count += value
      category_proportion = CategoryProportion()
      category_proportion.category = key
      category_proportion.proportion = float(value)/self._video_total
      category_proportion_li.append(category_proportion)
    if float(count)/self._video_total < 0.9:
      return
    self._user.category_proportion_list = category_proportion_li

    
  def process_user_language(self):
    if not self._user_language_dict:
      return
    language_list =  sorted(self._user_language_dict.items(), key=lambda x: x[1], reverse=True)
    language_proportion_li = []
    count = 0
    idx = 0
    for key, value in language_list:
      idx += 1
      if idx > 3:
        break
      count += value
      language_proportion = LanguageProportion()
      language_proportion.language_type = key
      language_proportion.proportion = float(value)/self._video_total
      language_proportion_li.append(language_proportion)
    if float(count)/self._video_total < 0.9:
      return
    self._user.language_proportion_list = language_proportion_li
    

  def print_item(self):
    if not self._user:
      return
    self.process_user_category()
    self.process_user_language()
    user_str = thrift2str(self._user)
    user_base64 = base64.b64encode(user_str)
    if user_base64:
      print 'user_info' + '\t' + self._user_url + '\t' + user_base64


def main():
  merge_item = MergeItem()
  while 1:
    line = sys.stdin.readline()
    if not line:
      break

    line_data = line.strip().split('\t', 3)
    if len(line_data) != 4:
      sys.stderr.write('reporter:counter:reduce,not_len_data_4,1\n')
      continue

    user_url, data_type, url, data_base64 = line_data
    data_type = data_type.split('_')[-1]
    if user_url == merge_item.get_user_url():
      merge_item.add_item(user_url, data_type, url, data_base64)
    else:
      merge_item.print_item()
      merge_item.reset(user_url)
      merge_item.add_item(user_url, data_type, url, data_base64)
  merge_item.print_item()


if __name__ == '__main__':
  main()

