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
    self._is_india_user = False
    self._url = None


  def get_user_url(self):
    return self._user_url


  def add_item(self, user_url, data_type, url, data_base64):
    if data_type == 'user':
      try:
        original_user = str2user(base64.b64decode(data_base64))
        self._user = original_user
        if self._user:
          if (self._user.country == 'IN') or (self._user.display_countrys and 'IN' in self._user.display_countrys):
            self._is_india_user = True
      except:
        sys.stderr.write('reporter:counter:statistic,failed_2_user,1\n')
    elif data_type == 'video':
      if url != self._url:
        self._url = url
        try:
          if not self._user:
            sys.stderr.write('reporter:counter:statistic,video_not_user,1\n')
          video = str2mediavideo(base64.b64decode(data_base64))
          self.count_video(video)
        except:
          sys.stderr.write('reporter:counter:reduce,failed_2_video,1\n')


  def count_video(self, video):
    if not video:
      return
    sys.stderr.write('reporter:counter:statistic,video_total,1\n')
    if self._is_india_user:
      sys.stderr.write('reporter:counter:statistic,india_video_total,1\n')

    category = video.category
    if category:
      category = category.replace(' ', '_')
      sys.stderr.write('reporter:counter:statistic,%s,1\n' % category)
      if self._is_india_user:
        sys.stderr.write('reporter:counter:statistic,india_%s,1\n' % category)
    else:
      sys.stderr.write('reporter:counter:statistic,not_category,1\n')
      if self._is_india_user:
        sys.stderr.write('reporter:counter:statistic,india_not_category,1\n')
    content_timestamp = video.content_timestamp
    if not content_timestamp:
      sys.stderr.write('reporter:counter:statistic,not_content_timestamp,1\n')
      if self._is_india_user:
        sys.stderr.write('reporter:counter:statistic,india_not_content_timestamp,1\n')
    now = int(time.time())
    time_delta = now - content_timestamp
    if time_delta > 0 and time_delta < 3600:
      sys.stderr.write('reporter:counter:statistic,video_1h,1\n')
      if self._is_india_user:
        sys.stderr.write('reporter:counter:statistic,india_video_1h,1\n')
    if time_delta > 0 and time_delta < 7200:
      sys.stderr.write('reporter:counter:statistic,video_2h,1\n')
      if self._is_india_user:
        sys.stderr.write('reporter:counter:statistic,india_video_2h,1\n')
    if time_delta > 0 and time_delta < 86400:
      sys.stderr.write('reporter:counter:statistic,video_24h,1\n')
      if self._is_india_user:
        sys.stderr.write('reporter:counter:statistic,india_video_24h,1\n')
      if category:
        sys.stderr.write('reporter:counter:statistic,24h_%s,1\n' % category)
        if self._is_india_user:
          sys.stderr.write('reporter:counter:statistic,india_24h_%s,1\n' % category)
    if time_delta > 0 and time_delta < 172800:
      sys.stderr.write('reporter:counter:statistic,video_48h,1\n')
      if self._is_india_user:
        sys.stderr.write('reporter:counter:statistic,india_video_48h,1\n')


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
      merge_item.reset(user_url)
      merge_item.add_item(user_url, data_type, url, data_base64)


if __name__ == '__main__':
  main()

