# encoding: utf8
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.

import time
import os
import Queue
import threading
import traceback
import json

from scrapy import log
from scrapy.utils.project import get_project_settings

from txt_file_writer import TxtFileWriter
from thrift_util import thrift_to_str
from ..core.page_writer import PageWriterBase
from ..proto.crawl.ttypes import RankingList, RankingListType, PageType
from ..extractors.video_adaptor import VideoAdaptor
from txt_file_writer import CrawlDocWriter


class UgcItemWriter(CrawlDocWriter):
  def __init__(self, spider):
    PageWriterBase.__init__(self, spider)
    self.video_adaptor = VideoAdaptor('video_templates')
    self.list_adaptor = VideoAdaptor('list_templates')
    if get_project_settings()['DEBUG_MODE']:
      self._init(300, 200, '/tmp/crawler_delta/')
      self.set_name('UgcItemWriterDebug')
    else:
      self._init(3600, 30000, '/letv/crawler_tudou_ugc/')
      self.set_name('UgcItemWriter')

  def file_writer_manger(self):
    while not self.exit_ or not self.data_queue_.empty():
      item = None
      try:
        item = self.data_queue_.get(block=True, timeout=10)
      except Exception, e:
        self.spider_.log('get item from queue timeout[%s]' % (e), log.DEBUG)
        item = None
      while not self.file_fp_:
        self._prepare_writer()
        self.spider_.log('prepare file ptr:[%s]' % self.current_file_name_,
                         log.INFO)
        time.sleep(1)
      if item:
        crawldoc = self.convert_item(item)
        video = crawldoc.video
        if video:
          category = video.category_list
        if crawldoc and crawldoc.response:
          try:
            id = crawldoc.id
            if crawldoc.page_type == PageType.PLAY:
              parsed_data = self.video_adaptor.get_static(crawldoc)
            else:
              continue
            if parsed_data:
              showtime = parsed_data.get('showtime', "")
              if showtime:
                x = time.localtime(float(showtime))
                showtime = time.strftime('%Y-%m-%d', x)
              current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
              if showtime != current_time:
                continue
              url = parsed_data.get('url',"")
              if url:
                url = url.encode('utf8')
              key = url
              value = {}
              title = parsed_data.get('title', "")
              value['title'] = title
              tags = parsed_data.get('tags', "")
              value['tags'] = tags
              desc = parsed_data.get('desc', "")
              value['desc'] = desc
              duration = parsed_data.get('duration', "")
              value['duration'] = duration
              create_time = parsed_data.get('crawl_time', "")
              if create_time:
                x = time.localtime(float(create_time))
                create_time = time.strftime('%Y-%m-%d %H:%M:%S',x)
              value['crawl_time'] = create_time
              value['category'] = category
              value['id'] = crawldoc.id
              value = json.dumps(value, ensure_ascii=False)
              self.file_fp_.add(key, value, False)
              self.total_items_ += 1
              if self.file_fp_.item_size() > 0 and self.file_fp_.item_size() % 1000 == 0:
                self.spider_.log('Flush result with [%d]' %
                                 (self.file_fp_.item_size()), log.INFO)
                self.file_fp_.flush()
            else:
              self.spider_.log('Can not convert parsed_data failed: %s' %
                             (crawldoc), log.ERROR)
          except:
            self.spider_.log('Error while write to file[%s]' % (self.current_file_name_), log.ERROR)

    nows = int(time.time())
    if self.file_fp_.item_size() >= self.max_lines_per_file_ or (self.file_fp_.item_size() > 0
                                                                 and (
          nows - self.last_flush_time_) >= self.gen_file_max_time_threshold_):
      # flush file to disk
      if not self._dump_file():
        self.spider_.log('flush file error:[%s]' % self.current_file_name_,
                         log.ERROR)
      else:
        self.spider_.log('flush file ok:[%s]' % self.current_file_name_,
                         log.INFO)

    self.spider_.log('crawldoc write manager exit normal', log.INFO)
    self._dump_file()
