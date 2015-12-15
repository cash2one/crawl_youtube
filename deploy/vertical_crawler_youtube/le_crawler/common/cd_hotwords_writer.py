#!/usr/bin/python
#-*-coding:utf8-*-
#
# Copyright 2015 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
"""
this pipeline using for fetch content from html
"""
import json

from le_crawler.common.cdesktop_writer import CDesktopWriter

class CDHotwordsWriter(CDesktopWriter):
  def __init__(self, spider):
    super(CDHotwordsWriter, self).__init__(spider)
    self.set_name('CDesktopHotwordsWriter')
    self.type_c = 'http'

  def get_tags_name(self, item):
    item_type = item.get('item_type', None)
    cate_id = item.get('cate_id', None)
    if not item_type or not cate_id:
      self.spider.log('Failed get tags name:%s' % (item))
      return None
    if u'热搜' in item_type and u'热门搜索' in cate_id:
      return 'hot_search_all'
    if u'热搜' in item_type and u'世说新词' in cate_id:
      return 'hot_search_word'
    if u'人物' in item_type and u'热点人物' in cate_id:
      return 'hot_people'
    if u'人物' in item_type and u'娱乐名人' in cate_id:
      return 'hot_famous'
    if u'人物' in item_type and u'美女' in cate_id:
      return 'hot_beauty'
    if u'人物' in item_type and u'帅哥' in cate_id:
      return 'hot_handsome'
    if u'人物' in item_type and u'女演员' in cate_id:
      return 'hot_female_star'
    if u'人物' in item_type and u'男演员' in cate_id:
      return 'hot_male_star'
    if u'人物' in item_type and u'女歌手' in cate_id:
      return 'hot_female_singer'
    if u'人物' in item_type and u'男歌手' in cate_id:
      return 'hot_male_singer'
    if u'人物' in item_type and u'主持人' in cate_id:
      return 'hot_dj'
    if u'人物' in item_type and u'选秀歌手' in cate_id:
      return 'hot_show_singer'
    if u'人物' in item_type and u'欧美明星' in cate_id:
      return 'hot_useu_star'
    if u'人物' in item_type and u'体坛人物' in cate_id:
      return 'hot_sports_people'
    if u'人物' in item_type and u'财经人物' in cate_id:
      return 'hot_finance_people'
    if u'人物' in item_type and u'互联网人物' in cate_id:
      return 'hot_internet_people'
    if u'人物' in item_type and u'历史人物' in cate_id:
      return 'hot_history_people'
    if u'人物' in item_type and u'名家人物' in cate_id:
      return 'hot_scholar'
    if u'热点' in item_type and u'实时热点' in cate_id: 
      return 'hot_instant_topic'
    if u'热点' in item_type and u'今日热点' in cate_id:
      return 'hot_today_topic'
    if u'热点' in item_type and u'七日热点' in cate_id: 
      return 'hot_week_topic'
    if u'热点' in item_type and u'民生热点' in cate_id: 
      return 'hot_life_topic'
    if u'热点' in item_type and u'娱乐热点' in cate_id: 
      return 'hot_ent_topic'
    if u'热点' in item_type and u'体育热点' in cate_id: 
      return 'hot_sports_topic'
    if u'娱乐' in item_type and u'电影' in cate_id:
      return 'movie_all'
    if u'娱乐' in item_type and u'电视剧' in cate_id:
      return 'tv_all' 
    if u'娱乐' in item_type and u'综艺' in cate_id:
      return 'show_all'
    if u'娱乐' in item_type and u'动漫' in cate_id:
      return 'comic_all'
    if u'娱乐' in item_type and u'音乐' in cate_id:
      return 'music_all'
    return None

  def writer(self, item):
    tmpvalue = self.get_tags_name(item)
    if not tmpvalue:
      return
    tmpdict = {}
    tmpdict['tagsTopic'] = tmpvalue
    tmpdict['tags'] = item['extend_map']
    datastr = json.dumps(tmpdict)
    try_time = 0
    # will retry 10 times, if not drop
    while try_time < self.retry_time_max:
      if not self._send_data(datastr):
        try_time += 1
        continue
      break
    self.total_send_count += 1
