#!/usr/bin/python
# encoding: utf8
# Copyright 2015 LeTV Inc. All Rights Reserved.
# Author: gaoqiang@letv.com (Qiang Gao)

import os
import Queue
import random
import time
import threading

from scrapy.utils.project import get_project_settings

from page_writer_base import PageWriterBase
from txt_file_writer import TxtFileWriter
from thrift_util import thrift_to_str

class CrawlDocWriter(PageWriterBase):
  def _initialize(self):
    if get_project_settings()['DEBUG_MODE']:
      gen_max_time = 60
      file_max_nums = 20
      self.data_dir_ = '/tmp/crawler_delta/'
    else:
      gen_max_time = 300
      file_max_nums = 200
      self.data_dir_ = '/letv/crawler_delta/'
    self.set_name('CrawlDocWriter')
    if not os.path.isdir(self.data_dir_):
      raise Exception('%s is not dir' % self.data_dir_)
    self.file_fp_ = None
    #self._prepare_writer()
    self.total_items_ = 0
    self.gen_file_max_time_threshold_ = gen_max_time  # 10min
    self.max_lines_per_file_ = file_max_nums
    self.last_flush_time_ = int(time.time())
    self.data_queue_ = Queue.LifoQueue(maxsize=10240)
    thread = threading.Thread(target=self.file_writer_manger, args=())
    thread.start()

  def _prepare_writer(self):
    if self.file_fp_:
      self._dump_file()
    self.current_file_name_ = self.gen_file_name()
    self.logger_.info('prepare file: [%s]', self.current_file_name_)
    self.file_fp_ = TxtFileWriter(self.current_file_name_)
    self.last_flush_time_ = int(time.time())

  def finalize(self):
    self.exit_ = True
    while not self.data_queue_.empty():
      self.logger_.info('page writer queue: [%d]', self.data_queue_.qsize())
      time.sleep(1)

  def process_item(self, item):
    if not item:
      return
    while True:
      try:
        self.data_queue_.put(item, block=True, timeout=2)
        return
      except:
        self.logger_.exception('failed to put item into queue, size %d', self.data_queue_.qsize())
        continue

  def status(self):
    return 'total item wrote: %s' % self.total_items_

  def gen_random_str(self):
    return str(random.randint(1, 1000000)).zfill(7)

  def gen_file_name(self):
    file_name = '%s_%d_%s' % (time.strftime('%Y%m%d_%H%M%S', time.localtime()), os.getpid(), self.gen_random_str())
    return os.path.join(self.data_dir_, file_name)

  def convert_item(self, item, type='crawldoc'):
    if not item:
      return None
    if type == 'json':
      return item.to_json_str()
    elif type == 'crawldoc':
      return item.to_crawldoc()

  def _dump_file(self):
    try:
      if not self.file_fp_:
        return  False
      self.logger_.info('flush file [%s], [%s]', self.current_file_name_, self.file_fp_.item_size())
      self.file_fp_.close()
      #self._prepare_writer()
      self.file_fp_ = None
      return True
    except:
      self.logger_.exception('failed dump file: [%s]', self.current_file_name_)


  def file_writer_manger(self):
    while not self.exit_ or not self.data_queue_.empty():
      item = None
      try:
        item = self.data_queue_.get(block=True, timeout=10)
      except Exception, e:
        self.logger_.debug('get item from queue timeout')
        item = None
      while not self.file_fp_:
        self._prepare_writer()
        self.logger_.info('prepare file ptr:[%s]', self.current_file_name_)
        time.sleep(1)

      if item:
        crawldoc = self.convert_item(item)
        if crawldoc:
          try:
            crawldoc_str = thrift_to_str(crawldoc)
            if crawldoc_str:
              self.file_fp_.add(crawldoc.response.url + '&crawl', crawldoc_str)
              self.total_items_ += 1
              if self.file_fp_.item_size() > 0 and self.file_fp_.item_size() % 100 == 0:
                self.logger_.info('Flush result with [%d]', self.file_fp_.item_size())
                self.file_fp_.flush()
            else:
              self.logger_.error('Can not convert thrift to str: %s', crawldoc)
          except Exception, e:
            import traceback
            print traceback.format_exc()
            print e
            self.logger_.exception('Error while write to file[%s]', self.current_file_name_)

      nows = int(time.time())
      if self.file_fp_.item_size() >= self.max_lines_per_file_ or (self.file_fp_.item_size() > 0
                                                                   and (
            nows - self.last_flush_time_) >= self.gen_file_max_time_threshold_):
        # flush file to disk
        if not self._dump_file():
          self.logger_.error('flush file error:[%s]', self.current_file_name_)
        else:
          self.logger_.info('flush file ok:[%s]', self.current_file_name_)

    self.logger_.info('crawldoc write manager exit normal')
    self._dump_file()
