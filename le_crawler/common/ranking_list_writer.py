#!/usr/bin/python
# encoding: utf8
# Copyright 2015 letv Inc. All Rights Reserved.
# Author: wangziqing@letv.com(Ziqing Wang)

import time

from scrapy.utils.project import get_project_settings
from scrapy import log

from crawl_doc_writer import CrawlDocWriter
from page_writer_base import PageWriterBase
from ..proto.crawl.ttypes import RankingList, RankingListType
from thrift_util import thrift_to_str

class RankingListWriter(CrawlDocWriter):
  def __init__(self, spider):
    PageWriterBase.__init__(self, spider)
    if get_project_settings()['DEBUG_MODE']:
      self._init(300, 20000, '/tmp/crawler_baidu_hot/')
      self.set_name('RankingListWriterDebug')
    else:
      self._init(3600, 30000, '/letv/crawler_baidu_hot/')
      self.set_name('RankingListWriter')

    self._rank_type_map = {'实时热点': RankingListType.BaiduHotRealTime,
                           '今日热点': RankingListType.BaiduHotToday,
                           '七日热点': RankingListType.BaiduHot7Days,
                           '民生热点': RankingListType.BaiduHotLife,
                           '娱乐热点': RankingListType.BaiduHotPlay,
                           '体育热点': RankingListType.BaiduHotSports,
                           '百度电视剧榜': RankingListType.BaiduHotDrama,
                           '百度电影榜': RankingListType.BaiduHotMovie,
                           '百度动漫榜': RankingListType.BaiduHotComic,
                           '百度综艺榜': RankingListType.BaiduHotVariety
                          }
    self._ranking_lists = []
    self._is_wrote = []
    for i in range(len(self._rank_type_map.keys())):
      self._ranking_lists.append(RankingList())
      self._is_wrote.append(False)


  def write_rankinglist(self, rl):
    print 'start write %s RankingList with %s items' % (rl.rank_list_type, len(rl.ranking_items))
    try:
      rankinglist_str = thrift_to_str(rl)
      if rankinglist_str:
        # for some cause, we need filter by url, set sequence file key as
        # url, value as serialize of crawldoc thrift, so that we dont need
        # unserialize value to crawldoc then judge filter
        self.file_fp_.add(rl.url, rankinglist_str)
        self.total_items_ += 1
        self.spider_.log('Flush result with [%d]' %
                          (self.file_fp_.item_size()), log.INFO)
        self.file_fp_.flush()
        #self.spider_.log('wrote RankingList: %s' % (rl), log.INFO)
      else:
        self.spider_.log('Can not convert thrift to str: %s' % (rl), log.ERROR)
    except:
      self.spider_.exception('Error while write to file[%s]' % (self.current_file_name_))


  def file_writer_manger(self):
    while not self.exit_ or not self.data_queue_.empty():
      item = None
      try:
        item = self.data_queue_.get(block=True, timeout=10)
      except:
        self.spider_.exception('get item from queue timeout.')
        item = None
      while not self.file_fp_:
        self._prepare_writer()
        self.spider_.log('prepare file ptr:[%s]' % self.current_file_name_,
                         log.INFO)
        time.sleep(1)

      if item:
        ranking_item = item.to_rankingitem()
        if ranking_item:
          ext_map = item.get('extend_map', None)
          if ext_map:
            category = ext_map.get('category', None)
          else:
            continue
          url = item.get('referer', None)
          if category:
            rank_type = self._rank_type_map.get(category.encode('utf8'), None)
          else:
            continue
          down_time = item.get('down_time', None)

          rl = self._ranking_lists[rank_type - 1]
          if not rl.ranking_items: # init this RankingList
            rl.rank_list_type = int(rank_type)
            rl.ranking_items = []
            if down_time:
              rl.crawl_time = int(down_time)
            if url:
              rl.url = url.encode('utf8')
            rl.ranking_list_name = category.encode('utf8')

          rl.ranking_items.append(ranking_item)
          if not rl.crawl_time:
            rl.crawl_time = down_time
          if not rl.url:
            rl.url = url

          if len(rl.ranking_items) >= 50: # write the RankingList to file
            self.write_rankinglist(rl)
            self._is_wrote[rank_type - 1] = True

    # for those RankingList whose items number is less than 50
    for i in range(len(self._rank_type_map.keys())):
      if not self._is_wrote[i] and self._ranking_lists[i].ranking_items:
        self.write_rankinglist(self._ranking_lists[i])

    self.spider_.log('RankingList write manager exit normal', log.INFO)
    # flush file to disk
    if not self._dump_file():
      self.spider_.log('flush file error:[%s]' % self.current_file_name_,
                       log.ERROR)
    else:
      self.spider_.log('flush file ok:[%s]' % self.current_file_name_,
                       log.INFO)

