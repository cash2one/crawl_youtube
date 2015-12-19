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
    self._prepare_writer()
    self.total_items_ = 0
    self.gen_file_max_time_threshold_ = gen_max_time  # 10min
    self.max_lines_per_file_ = file_max_nums
    self.data_queue_ = Queue.LifoQueue(maxsize=10240)
    thread = threading.Thread(target=self.file_writer_manger, args=())
    thread.start()

  def _prepare_writer(self):
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
      self.logger_.info('flush file [%s], [%s]', self.current_file_name_, self.file_fp_.item_size())
      self.file_fp_.close()
      self._prepare_writer()
    except:
      self.logger_.exception('failed dump file: [%s]', self.current_file_name_)

  def _add_item(self, key, value):
    if not key or not value:
      return
    # value = zlib.compress(value, zlib.Z_BEST_COMPRESSION)
    self.file_fp_.add(key, value)
    self.total_items_ += 1
    if self.file_fp_.item_size() > 0 and self.file_fp_.item_size() % 10 == 0:
      self.logger_.info('flush result with [%d]', self.file_fp_.item_size())
      self.file_fp_.flush()
    if self.file_fp_.item_size() >= self.max_lines_per_file_ or \
        (self.file_fp_.item_size() > 0 and (int(time.time()) - self.last_flush_time_) >= self.gen_file_max_time_threshold_):
      self._dump_file()

  def file_writer_manger(self):
    while not self.exit_ or not self.data_queue_.empty():
      item = None
      try:
        item = self.data_queue_.get(block=True, timeout=5)
      except:
        self.logger_.debug('get item from queue timeout.')
      doc = self.convert_item(item)
      # FIXME(gaoqiang): add PAGE_TIME doc support!!
      if not doc or not doc.response:
        continue
      self._add_item(doc.response.url + '&crawl', thrift_to_str(doc))
    self._dump_file()
    self.logger_.info('doc write manager exit normal.')

