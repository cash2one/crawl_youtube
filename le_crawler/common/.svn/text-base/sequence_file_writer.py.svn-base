#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import os
import time
import Queue
import random
import threading

from scrapy.utils.project import get_project_settings

from filewriter import SequenceFileWriter
from thrift_util import thrift_to_str
from ..core.page_writer import PageWriterBase


class CrawlDocWriter(PageWriterBase):
  def __init__(self, spider):
    PageWriterBase.__init__(self, spider)
    if get_project_settings()['DEBUG_MODE']:
      self._init(1800, 20000, '/tmp/crawler_delta/')
      self.set_name('CrawlDocWriterDebug')
    else:
      self._init(3600, 30000, '/letv/crawler_delta/')
      self.set_name('CrawlDocWriter')

  def _init(self, gen_max_time=86400, file_max_nums=2000, data_dir=""):
    if not os.path.isdir(data_dir):
      raise Exception('%s is not dir' % (data_dir))
    self.file_fp_ = None
    self.current_file_name_ = ''
    self.total_items_ = 0
    self.gen_file_max_time_threshold_ = gen_max_time  # 10min
    self.max_lines_per_file_ = file_max_nums
    self.last_flush_time_ = int(time.time())
    self.data_dir_ = data_dir
    self.data_queue_ = Queue.LifoQueue(maxsize=10240)
    thread = threading.Thread(target=self.file_writer_manger, args=())
    thread.start()

  def finalize(self):
    self.exit_ = True
    while not self.data_queue_.empty():
      self.logger_.info('page writer queue size: [%d]', self.data_queue_.qsize())
      time.sleep(1)

  def process_item(self, item):
    self.add_item(item)

  def add_item(self, item):
    if not item:
      return
    while True:
      try:
        self.data_queue_.put(item, block=True, timeout=5)
        return
      except:
        self.logger_.exception('failed enqueue item, size %d', self.data_queue_.qsize())
        continue

  def status(self):
    return 'total item wrote: %s' % self.total_items_

  def gen_random_str(self):
    return str(random.randint(1, 1000000)).zfill(7)

  def gen_filestr(self):
    return os.path.join(self.data_dir_, '%s_%d_%s' % \
                        (time.strftime('%Y%m%d_%H%M%S', time.localtime()),
                         os.getpid(),
                         self.gen_random_str()))

  def convert_item(self, item, type='crawldoc'):
    if not item:
      return None
    if type == 'json':
      return item.to_json_str()
    elif type == 'crawldoc':
      return item.to_crawldoc()

  def _prepare_writer(self):
    if self.file_fp_:
      self._dump_file()
    self.current_file_name_ = self.gen_filestr()
    self.file_fp_ = SequenceFileWriter(self.current_file_name_,
                                       {'thrift_compack': 'true',
                                        'max_lines': '%s' % self.max_lines_per_file_,
                                        'writer': 'CrawlDocWriter'})

  def _dump_file(self):
    try:
      if not self.file_fp_:
        return False
      self.logger_.info('flush file [%s], [%s]', self.current_file_name_, self.file_fp_.item_size())
      self.file_fp_.close()
      self.last_flush_time_ = int(time.time())
      self.file_fp_ = None
      return True
    except:
      self.logger_.exception('error while dump file:[%s]', self.current_file_name_)
      return False

  def file_writer_manger(self):
    while not self.exit_ or not self.data_queue_.empty():
      try:
        item = self.data_queue_.get(block=True, timeout=10)
      except:
        self.logger_.exception('failed to get item from queue')
        item = None
      while not self.file_fp_:
        self._prepare_writer()
        self.logger_.info('prepare file: [%s]', self.current_file_name_)
        time.sleep(1)
      if item:
        crawldoc = self.convert_item(item)
        if crawldoc:
          try:
            # line_zip = zlib.compress(line_str, zlib.Z_BEST_COMPRESSION)
            crawldoc_str = thrift_to_str(crawldoc)
            if crawldoc_str:
              # for some case, we need filter by url, set sequence file key as
              # url, value as serialize of crawldoc thrift, so that we don't need
              # unserialize value to crawldoc then judge filter
              self.file_fp_.add(crawldoc.response.url, crawldoc_str)
              self.total_items_ += 1
              if self.file_fp_.item_size() > 0 and self.file_fp_.item_size() % 1000 == 0:
                self.logger_.info('flush result with [%d]', self.file_fp_.item_size())
                self.file_fp_.flush()
            else:
              self.logger_.error('Can not convert thrift to str: %s', crawldoc)
          except:
            self.logger_.exception('Error while write to file[%s]' % (self.current_file_name_))

      nows = int(time.time())
      if self.file_fp_.item_size() >= self.max_lines_per_file_ or \
              (self.file_fp_.item_size() > 0 and (nows - self.last_flush_time_) >= self.gen_file_max_time_threshold_):
        if not self._dump_file():
          self.logger_.error('flush file error: [%s]', self.current_file_name_)
        else:
          self.logger_.info('flush file ok: [%s]', self.current_file_name_)

    self.spider_.info('crawl doc write manager exit normal')
    self._dump_file()
