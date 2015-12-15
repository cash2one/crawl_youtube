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
from le_crawler.core.page_writer import PageWriterBase
from le_crawler.base.thrift_util import thrift_to_str

class CrawlDocWriter(PageWriterBase):

  def __init__(self, spider):
    PageWriterBase.__init__(self, spider)
    if get_project_settings()['DEBUG_MODEL']:
      self._init(864000, 200, '/tmp/crawler_delta/')
      self.set_name('CrawlDocWriterDebug')
    else:
      self._init(86400, 300000, '/letv/crawler_delta/')
      self.set_name('CrawlDocWriter')

  def _init(self, gen_max_time = 86400, file_max_nums = 2000, data_dir = ""):
    if not os.path.isdir(data_dir):
      raise Exception('%s is not dir' % (data_dir))
    self.file_fp_ = None
    self.current_file_name_ = ''
    self.total_items_ = 0
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
      self.spider_.log('page writer que[%d]' % (self.data_queue_.qsize()), log.INFO)
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

  def gen_random_str(self):
    import random
    return str(random.randint(1, 1000000)).zfill(7)

  def gen_filestr(self):
    return os.path.join(self.data_dir_, '%s_%d_%s'%(time.strftime('%Y%m%d_%H%M%S', time.localtime()),
        os.getpid(), self.gen_random_str()))

  def convert_item(self, item, type = 'crawldoc'):
    if not item:
      return None
    try:
      if type == 'json':
        return item.to_jsonStr()
      elif type == 'crawldoc':
        return item.to_crawldoc()
    except:
      self.spider_.log('Failed decoding [%s] with [%s]' %(dict['url'],
        dict['page_encoding']), log.WARNING)
      dict['page'] = 'error decoding'
      return None

  def _prepare_writer(self):
    if self.file_fp_:
      self._dump_file()
    self.current_file_name_ = self.gen_filestr()
    from le_crawler.base.filewriter import SequenceFileWriter
    self.file_fp_ = SequenceFileWriter(self.current_file_name_,
        {'thrift_compack':'true',
          'max_lines':'%s' % self.max_lines_per_file_,
          'writer':'CrawlDocWriter'})

  def _dump_file(self):
    try:
      if not self.file_fp_:
        return False
      self.spider_.log('Flush File[%s],[%s]' % (self.current_file_name_,
        self.file_fp_.item_size()), log.INFO)
      self.file_fp_.close()
      self.last_flush_time_ = int(time.time())
      self.file_fp_ = None
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
        crawldoc = self.convert_item(item)
        if crawldoc:
          try:
          #line_zip = zlib.compress(line_str, zlib.Z_BEST_COMPRESSION)
            crawldoc_str = thrift_to_str(crawldoc)
            if crawldoc_str:
              # for some cause, we need filter by url, set sequence file key as
              # url, value as serialize of crawldoc thrift, so that we dont need
              # unserialize value to crawldoc then judge filter
              self.file_fp_.add(crawldoc.response.url, crawldoc_str)
              self.total_items_ += 1
              if self.file_fp_.item_size() > 0 and  self.file_fp_.item_size() %  1000 == 0:
                self.spider_.log('Flush result with [%d]' %
                    (self.file_fp_.item_size()), log.INFO)
                self.file_fp_.flush()
            else:
              self.spider_.log('Can not convert thrift to str: %s' %
                  (crawldoc), log.ERROR)
          except Exception, e:
            import traceback
            print traceback.format_exc()
            print e
            self.spider_.log('Error while write to file[%s]' % (self.current_file_name_))

      nows = int(time.time())
      if self.file_fp_.item_size() >= self.max_lines_per_file_ or (self.file_fp_.item_size() > 0
        and (nows - self.last_flush_time_) >= self.gen_file_max_time_threshold_):
      # flush file to disk
        if not self._dump_file():
          self.spider_.log('flush file error:[%s]' % self.current_file_name_,
            log.ERROR)
        else:
          self.spider_.log('flush file ok:[%s]' % self.current_file_name_,
              log.INFO)

    self.spider_.log('crawldoc write manager exit normal', log.INFO)
    self._dump_file()
