#!/usr/bin/python
# coding=utf-8

import sys
import time
import base64
# try:
#   import cPickle as pickle
# except:
#   import pickle

from le_crawler.proto.video.ttypes import OriginalUser
from le_crawler.proto.crawl.ttypes import CrawlHistory, HistoryItem
from le_crawler.common.utils import str2mediavideo, thrift2str, multi_key_fields, compress_play_trends, str2user, merge_country_source  #, int_typeids
from le_crawler.common.parse_youtube import youtube_category_dict

merged_fields = set(['crawl_history', 'play_trends', 'in_links', 'user', 'page_state', 'inlink_history'])
direct_merged = set(['title', 'poster'])
need_cal_merged = set(['play_total', 'voteup_count', 'votedown_count'])
time_fields = set(['content_timestamp', 'showtime'])

class MergeItem:
  def __init__(self):
    self.reset('')

  def reset(self, url=None):
    self._data = []
    self._url = url
    self.merged_ = False
    self.crawled_ = True
    self._user_url = None
    self._data_type = None

  def get_url(self):
    return self._url


  def add_item(self, user_url, data_source, data_type, data_str):
    if self._data_type is None:
      self._data_type = data_type
    if self._data_type != data_type:
      sys.stderr.write('reporter:counter:reduce,data_type_error,1\n')
      return

    if not self._url:
      sys.stderr.write('reporter:counter:reduce,reduce_url_empty,1\n')
      return

    if self.crawled_ and data_source != 'crawl':
      self.crawled_ = False

    if user_url != 'None':
      self._user_url = user_url
    self._data.append(data_str)


  def _merge_history_trends(self, videos):
    history_items = {}
    for video in videos:
      if video.crawl_history and video.crawl_history.crawl_history:
        crawl_history = video.crawl_history.crawl_history
        for item in crawl_history:
          if item.crawl_time:
            history_items[item.crawl_time] = item.play_count

    crawl_history_new = CrawlHistory()
    crawl_history_new.crawl_history = []
    history_list = compress_play_trends(history_items)
    # print history_list
    history_list.reverse()
    #history_list = sorted(history_items.iteritems(), reverse=True)
    history_len = len(history_list)
    for idx, c_item in enumerate(history_list):
      item = HistoryItem()
      item.crawl_time = c_item[0]
      item.play_count = c_item[1]
      if idx + 1 < history_len:
        item.crawl_interval = c_item[0] - history_list[idx + 1][0]
      crawl_history_new.crawl_history.append(item)
      # history_list[idx] = (str(c_item[0]), str(c_item[1]))
    crawl_history_new.update_time = int(time.time())
    videos[0].crawl_history = crawl_history_new
    # videos[0].play_trends = ';'.join('|'.join(x) for x in history_list if x[1] != 'None')


  def _merge_in_links(self, videos):
    if len(videos) < 2 or not videos[0].in_links or not videos[1].in_links:
      return
    latest_anchor = videos[0].in_links[-1]
    in_links = videos[1].in_links
    for idx, anchor in enumerate(in_links):
      if latest_anchor.url == anchor.url:
        in_links[idx] = latest_anchor
        break
    else:
      in_links.append(latest_anchor)
    videos[0].in_links = in_links


  def _merge_inlink_history(self, videos):
    if len(videos) < 2 or not videos[1].inlink_history:
      return
    if not videos[0].inlink_history:
      videos[0].inlink_history = videos[1].inlink_history
      return
    inlink_history = videos[1].inlink_history
    latest_inlink = videos[0].inlink_history[0]
    latest_link_list = [anchor.url for anchor in latest_inlink]
    is_exist = False
    for inlinks in inlink_history:
      link_list = [anchor.url for anchor in inlinks]
      if latest_link_list == link_list:
        is_exist = True
        break
    if is_exist:
      return False
    inlink_history.append(latest_inlink)
    videos[0].inlink_history = inlink_history

  def _merge_country_list(self, country_list_des, country_list_src):
    if not country_list_src:
      return country_list_des
    for country_info in country_list_src:
      country_list_des = merge_country_source(country_list_des, country_info.country_code, country_info.source_list)
    return country_list_des

  def _merge_user(self, users):
    if not users:
      return
    new_user = OriginalUser()
    for k, v in new_user.__dict__.iteritems():
      if k == 'country_source_list':
        country_source_list = []
        for user in users:
          old_v = getattr(user, k)
          if not old_v:
            continue
          country_source_list = self._merge_country_list(old_v, country_source_list)
        if country_source_list:
          setattr(new_user, k, country_source_list)
      else:
        for user in users:
          old_v = getattr(user, k)
          if old_v is not None:
            setattr(new_user, k, old_v)
            break
    return new_user


  def _merge_data(self, src, dst):
    merged = False
    for k, v in dst.__dict__.iteritems():
      src_v = getattr(src, k)
      if k in merged_fields or v == src_v:
        continue
      if not v:
        setattr(dst, k, src_v)
      elif k in time_fields:
        if src_v:  # use the old timestamp to maintain accuracy
          setattr(dst, k, src_v)
        else:
          merged = True
      elif k in direct_merged:
        merged = True
      elif k in multi_key_fields:
        v_set = set(v.split(';'))
        src_v_set = set((src_v or '').split(';'))
        if v_set - src_v_set:
          setattr(dst, k, ';'.join(list(v_set | src_v_set)))
          if k == 'category_list':
            merged = True
      elif k in need_cal_merged:
        src_v = src_v or 1
        if (v - src_v) * 1.0 / src_v > 0.1 and (v - src_v) >= 20:
          merged = True
    return merged


  def _merge_video(self, videos):
    self._merge_history_trends(videos)
    self._merge_in_links(videos)
    self._merge_inlink_history(videos)
    # first merge crawled data
    for video in videos[1:-1]:
      self._merge_data(video, videos[0])
    # then merge the latest video and the original video
    self.merged_ = self._merge_data(videos[-1], videos[0])

    #TODO to delete
    if self._user_url:
      videos[0].user = None

    if self.merged_:
      sys.stderr.write('reporter:counter:reduce,video_updated,1\n')
      videos[0].update_time = int(time.time())


  def _print_user(self, user):
    user_str = thrift2str(user)
    if not user_str:
      sys.stderr.write('reporter:counter:reduce,reduce_thrift2str_failed,1\n')
      return
    user_base64 = base64.b64encode(user_str)
    if not user_base64:
      sys.stderr.write('reporter:counter:reduce,reduce_base64encode_failed,1\n')
      return
    sys.stderr.write('reporter:counter:reduce,user_total,1\n')
    print 'user_info' + '\t' + self._url + '\t' + user_base64


  def _print_video(self, video):
    video_str = thrift2str(video)
    if not video_str:
      sys.stderr.write('reporter:counter:reduce,reduce_thrift2str_failed,1\n')
      return
    video_base64 = base64.b64encode(video_str)
    if not video_base64:
      sys.stderr.write('reporter:counter:reduce,reduce_base64encode_failed,1\n')
      return
    sys.stderr.write('reporter:counter:reduce,video_total,1\n')
    user_url = self._user_url if self._user_url else 'None'
    print 'unique' + '\t' + self._url + '\t' + user_url + '\t' + video_base64
    if self.crawled_:
      sys.stderr.write('reporter:counter:statistic,video_new,1\n')
      print 'video' + '\t' + self._url + '\t' + user_url + '\t' + video_base64
    return


  def print_item(self):
    if not self._data:
      return
    if len(self._data) == 1:
      if self._data_type == 'video':
        sys.stderr.write('reporter:counter:reduce,video_total,1\n')
        user_url = self._user_url if self._user_url else 'None'
        print 'unique' + '\t' + self._url + '\t' + user_url + '\t' + self._data[0]
        if self.crawled_:
          print 'video' + '\t' + self._url + '\t' + user_url + '\t' + self._data[0]
        #print '%s\t%s' % (self._user_url, str2mediavideo(base64.b64decode(self._data[0])))
        if self.crawled_:
          sys.stderr.write('reporter:counter:statistic,video_new,1\n')
      elif self._data_type == 'user':
        sys.stderr.write('reporter:counter:reduce,user_total,1\n')
        print 'user_info' + '\t' + self._url + '\t' + self._data[0]
      return

    for idx, data_str in enumerate(self._data):
      try:
        data = base64.b64decode(data_str)
      except:
        sys.stderr.write('reporter:counter:reduce,reduce_json_failed,1\n')
      if self._data_type == 'video':
        data = str2mediavideo(data)
        if not data:
          sys.stderr.write('reporter:counter:reduce,reduce_str_to_video,1\n')
        self._data[idx] = data
      elif self._data_type == 'user':
        data = str2user(data)
        if not data:
          sys.stderr.write('reporter:counter:reduce,reduce_str_to_user,1\n')
        self._data[idx] = data
      else:
        sys.stderr.write('reporter:counter:reduce,data_type_error,1\n')
        return
    self._data = [item for item in self._data if item]
    if not self._data:
      sys.stderr.write('reporter:counter:reduce,not_datas,1\n')
      return
    if self._data_type == 'video':
      self._data.sort(cmp=lambda x, y: (y.create_time or 0) - (x.create_time or 0))
      self._merge_video(self._data)
      self._print_video(self._data[0])
    elif self._data_type == 'user':
      self._data.sort(cmp=lambda x, y: (y.update_time or 0) - (x.update_time or 0))
      self._data[0] = self._merge_user(self._data)
      self._print_user(self._data[0])


def main():
  merge_item = MergeItem()
  url = ''
  while 1:
    line = sys.stdin.readline()
    if not line:
      break

    line_data = line.strip().split('\t', 4)
    if len(line_data) != 5:
      sys.stderr.write('reporter:counter:reduce,reduce_input_not_len_5,1\n')
      continue

    url, user_url, data_source, data_type, data = line_data
    if not url:
      sys.stderr.write('reporter:counter:reduce,miss_url,1\n')
      continue
    if url == merge_item.get_url():
      merge_item.add_item(user_url, data_source, data_type, data)
    else:
      merge_item.print_item()
      merge_item.reset(url)
      merge_item.add_item(user_url, data_source, data_type, data)
  merge_item.print_item()


if __name__ == '__main__':
  main()

