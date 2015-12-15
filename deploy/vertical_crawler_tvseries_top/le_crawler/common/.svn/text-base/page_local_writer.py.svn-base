#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'


import time
import os
import Queue
import threading

from scrapy import log
from scrapy.utils.project import get_project_settings
from ..core.page_writer import PageWriterBase
"""
for json format data writer
"""

class PageLocalWriter(PageWriterBase):

  def __init__(self, spider):
    PageWriterBase.__init__(self, spider)
    if get_project_settings()['DEBUG_MODEL']:
      self._init(86400, 1000, '/tmp/crawler_delta/')
      self.set_name('PageLocalJsonWriterTest')
    else:
      self._init(
          get_project_settings().getint('LOCAL_PAGE_WRITER_DATA_TIME_LIMIT', 86400),
          get_project_settings().getint('LOCAL_PAGE_WRITER_DATA_FLUSH_LIMIT', 20000),
          get_project_settings().get('LOCAL_PAGE_WRITER_DATA_DIR', '/letv/crawler_delta/')
          )
      self.set_name('PageLocalJsonWriter')

  def _init(self, gen_max_time = 86400, file_max_nums = 2000, data_dir = ""):
    if not os.path.isdir(data_dir):
      raise Exception('%s is not dir' % (data_dir))
    self.file_fp_ = None
    self.current_file_name_ = ''
    self.total_items_ = 0
    self.current_nums_ = 0
    self.gen_file_max_time_threshold_ = gen_max_time # 10min
    self.max_lines_per_file_ = file_max_nums
    self.last_flush_time_ = int(time.time())
    self.data_dir_ = data_dir
    self.data_queue_ = Queue.LifoQueue(maxsize = 10240)
    thread = threading.Thread(target = self.file_writer_manger, args = ())
    thread.start()

  def finalize(self):
    self.exit_ = True
    while not self.data_queue_.empty():
      self.spider_.log('page page_local_writer que[%d]' % (self.data_queue_.qsize()), log.INFO)
      time.sleep(1)

  def process_item(self, item):
    self.add_item(item)

  def add_item(self, item):
    if not item:                                                                                                                   
       return
    while True:
      try:
        self.data_queue_.put(item, block = True, timeout = 5)
        return
      except Exception, e:
        self.spider_.log('try to put item into queu error %s, size %d' % (e, self.data_queue_.qsize()))
        continue

  def status(self):
    return 'total item wrote: %s' % (self.total_items_)

  def gen_filestr(self):
    return os.path.join(self.data_dir_, '%s_%d'%(time.strftime('%Y%m%d_%H%M%S',
      time.localtime()),
        os.getpid()))

  def gen_json_str(self, item):
    if not item:
      return None
    try:
      return item.to_json_str()
    except:
      self.spider_.log('Failed decoding [%s] with [%s]' %(dict['url'],
        dict['page_encoding']), log.WARNING)
      dict['page'] = 'error decoding'
      return None

  def _prepare_writer(self):
    if self.file_fp_:
      self._dump_file()
    self.current_file_name_ = self.gen_filestr()
    self.file_fp_ = open(self.current_file_name_ + '.tmp', 'w+')
    self.current_nums_ = 0

  def _dump_file(self):
    try:
      if not self.file_fp_:
        return False
      self.file_fp_.close()
      self.last_flush_time_ = int(time.time())
      self.file_fp_ = None
      os.rename(self.current_file_name_ + '.tmp', self.current_file_name_ + '.json')
      return True
    except Exception, e:
      print e
      self.spider_.log('Error while dump file:[%s]' % self.current_file_name_,
            log.ERROR)
      return False

  def file_writer_manger(self):
    while not self.exit_ or not self.data_queue_.empty():
      item = None
      try:
        item = self.data_queue_.get(block = True, timeout = 10)
      except Exception, e:
        self.spider_.log('get item from queu timeout[%s]' %(e), log.DEBUG)
        item = None
      while not self.file_fp_:
        self._prepare_writer()
        self.spider_.log('prepare file ptr:[%s]' % self.current_file_name_,
            log.INFO)
        time.sleep(1)

      if item:
        line_str = self.gen_json_str(item)
        if line_str:
          try:
          #line_zip = zlib.compress(line_str, zlib.Z_BEST_COMPRESSION)
            self.file_fp_.write(line_str)
            self.file_fp_.write('\n')
            self.current_nums_ += 1
            self.total_items_ += 1
            if self.current_nums_ > 0 and self.current_nums_ %  1000 == 0:
              self.spider_.log('Flush result with [%d]' % (self.current_nums_), log.INFO)
              self.file_fp_.flush()
          except Exception, e:
            print time.localtime()
            print e
            self.spider_.log('Error while write to file[%s]' % (self.current_file_name_))
      nows = int(time.time())
      if self.current_nums_ >= self.max_lines_per_file_ or (self.current_nums_ > 0
        and (nows - self.last_flush_time_) >= self.gen_file_max_time_threshold_):
      # flush file to disk
        if not self._dump_file():
          self.spider_.log('flush file error:[%s]' % self.current_file_name_,
            log.ERROR)
        self.spider_.log('flush:[ %s ] with [%d]' %(self.current_file_name_,
         self.current_nums_), log.INFO)

    self.spider_.log('page_local_writer manager exit normal', log.INFO)
    self._dump_file()
