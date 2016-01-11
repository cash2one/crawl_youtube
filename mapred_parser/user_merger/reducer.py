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


user_merge_field = set(['user_name', 'url', 'channel_id', 'channel_title', 'channel_desc', 
	'publish_time', 'thumbnails', 'thumbnail_list',  'portrait_url', 'country',
	'play_num', 'fans_num', 'video_num', 'comment_num', 'state'])


class MergeItem:
  def __init__(self):
    self.reset('')


  def reset(self, user_url=None):
    self._data = []
    self._user_url = user_url
    self._url = None # used only in which length of self._data is 1
    self._user = None
    self._user_category_dict = {}
    self._user_language_dict = {}
    self._video_total = 0
    self._user_dict = {}


  def get_user_url(self):
    return self._user_url


  def add_item(self, user_url, data_type, out_type, url, data_base64):
    if data_type == 'user':
      try:
        original_user = str2user(base64.b64decode(data_base64))
        if original_user and original_user.update_time:
          self._user_dict[original_user.update_time] = original_user
      except:
        sys.stderr.write('ERROR: failed in base64 decode. %s\n' % user_url)
    elif data_type == 'video':
      is_out_video = out_type == 'video'
      self._data.append((data_base64, is_out_video))
      self._url = url


  def _merge_user(self, datas):
    #test
    self._user_list.sort(cmp=lambda x, y: (y.update_time or 0) - (x.update_time or 0))
    user_list = sorted(self._user_dict.iteritems(), key=lambda d:d[1], reverse=True)
    
    new_user = OriginalUser()
    for k, v in new_user.__dict__.iteritems():
      for data in user_list:
        old_v = getattr(data[1].user, k)
        if old_v is not None:
          setattr(new_user, k, old_v)
          break
    new_user.update_time = int(time.time())
    self._user = new_user


  def _print_video(self, datas):
    for data in datas:
      data[0].user = self._user
      video_str = thrift2str(data[0])
      if not video_str:
        sys.stderr.write('ERROR: failed in thrift2str. %s\n' % data[0].url)
        continue
      video_base64 = base64.b64encode(video_str)
      if not video_base64:
        sys.stderr.write('ERROR: failed in base64 encode. %s\n' % data[0].url)
        continue
      print 'unique' + '\t' + data[0].url + '\t' + str(self._user_url) + '\t' + video_base64
      if data[1]:
        print 'video' + '\t' + data[0].url + '\t' + str(self._user_url) + '\t' + video_base64

  def _print_user_info(self):
    if not self._user:
      return
    user_str = thrift2str(self._user)
    user_base64 = base64.b64encode(user_str)
    if user_base64:
      print 'user_info' + '\t' + str(self._user_url) + '\t' + user_base64

  def count_video(self, video):
    if not video:
      return
    sys.stderr.write('reporter:counter:reduce,video_total,1\n')
    category = video.category
    if category:
      category = category.replace(' ', '_')
      sys.stderr.write('reporter:counter:reduce,%s,1\n' % category)
    else:
      sys.stderr.write('reporter:counter:reduce,not_category,1\n')
    content_timestamp = video.content_timestamp
    if not content_timestamp:
      sys.stderr.write('reporter:counter:reduce,not_content_timestamp,1\n')
    now = int(time.time())
    time_delta = now - content_timestamp
    if time_delta > 0 and time_delta < 3600:
      sys.stderr.write('reporter:counter:reduce,video_1h,1\n')
    if time_delta > 0 and time_delta < 7200:
      sys.stderr.write('reporter:counter:reduce,video_2h,1\n')
    if time_delta > 0 and time_delta < 86400:
      sys.stderr.write('reporter:counter:reduce,video_24h,1\n')
      if category:
        sys.stderr.write('reporter:counter:reduce,24h_%s,1\n' % category)
    if time_delta > 0 and time_delta < 172800:
      sys.stderr.write('reporter:counter:reduce,video_48h,1\n')

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
    if not self._data:
      return
    self._video_total = len(self._data)
    for idx, data_group in enumerate(self._data):
      try:
        data = str2mediavideo(base64.b64decode(data_group[0]))
        if data.user and data.user.update_time:
          self._user_dict[data.user.update_time] = data.user
        self.count_video(data)
        if data.category:
          self._user_category_dict[data.category] = self._user_category_dict.get(data.category, 0) + 1
        if data.language_type:
          self._user_language_dict[data.language_type] = self._user_language_dict.get(data.language_type, 0) + 1
      except:
        sys.stderr.write('ERROR: failed in base64 decode. %s\n' % self._user_url)
      self._data[idx] = (data, data_group[1])
    self._data = [item for item in self._data if item[0]]
    #self._data.sort(cmp=lambda x, y: (y[0].user.update_time or 0) - (x[0].user.update_time or 0))
    self._merge_user(self._data)
    if self._user_category_dict:
      self.process_user_category()
    if self._user_language_dict:
      self.process_user_language()
    self._print_video(self._data)
    self._print_user_info()


def main():
  merge_item = MergeItem()
  while 1:
    line = sys.stdin.readline()
    if not line:
      break

    line_data = line.strip().split('\t', 4)
    if len(line_data) != 5:
      sys.stderr.write(str(len(line_data)) + ' ' + str(line_data) + '\n')
      continue

    user_url, url, data_type, out_type, data_base64 = line_data
    if user_url == 'None':
      print 'unique' + '\t' + url + '\t' + user_url + '\t' + data_base64
      if out_type == 'video':
        print 'video' + '\t' + url + '\t' + user_url + '\t' + data_base64
      continue

    if user_url == merge_item.get_user_url():
      merge_item.add_item(user_url, data_type, out_type, url, data_base64)
    else:
      merge_item.print_item()
      merge_item.reset(user_url)
      merge_item.add_item(user_url, data_type, out_type, url, data_base64)
  merge_item.print_item()


if __name__ == '__main__':
  main()

