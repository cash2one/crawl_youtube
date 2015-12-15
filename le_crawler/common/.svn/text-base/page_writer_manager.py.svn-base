#!/usr/bin/python
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import Queue
import threading
import time

from scrapy.utils.misc import load_object
from scrapy.utils.project import get_project_settings


writer_handlers = '''
le_crawler.common.page_local_writer.PageLocalWriter
'''

# le_crawler.common.today_tv_writer.TodayTvWriter
# le_crawler.common.page_local_writer.PageLocalWriter
class PageWriterManager(threading.Thread):
  def __init__(self, queue_max_size=1024, spider=None):
    threading.Thread.__init__(self)
    self.data_queue_ = Queue.LifoQueue(maxsize=queue_max_size)
    self.exit_ = False
    # base on PageWriter
    self.writers_ = {}
    self.spider_ = spider
    self.logger_ = spider.logger_
    self.process_exit_ = False
    self.all_exited_ = False
    self._gen_writer(get_project_settings()['CRAWL_DOC_WRITERS'] or writer_handlers)

  def exit(self):
    self.logger_.info('page writer manager receive exit')
    self.exit_ = True
    while not self.all_exited_:
      time.sleep(2)

  def _gen_writer(self, writer_clss):
    if not writer_clss:
      return None
    writers = filter(lambda l: l != '', [s.strip() for s in writer_clss.split(',')])
    if not writers:
      self.logger_.info('writer string flag is empty[%s]', writer_clss)
    for w in writers:
      obj = load_object(w)(self.spider_)
      self.writers_[obj.name] = obj
      obj._initialize()
      self.logger_.info('create writer [%s]', obj.name)


  def _finalize(self):
    for name, writer in self.writers_.items():
      self.logger_.info('finalize writer[%s]', name)
      writer.finalize()
      self.logger_.info('finished finalize writer[%s]', name)


  def add_item(self, item):
    if not item:
      return
    while 1:
      try:
        self.data_queue_.put(item, block=True, timeout=5)
        return
      except:
        self.logger_.exception('failed to enqueue item, size %d', self.data_queue_.qsize())
        continue

  def run(self):
    consu_thread = threading.Thread(target=self.process_items, args=())
    consu_thread.start()
    time_count = 0
    log_interval = 300
    while not self.process_exit_:
      if time_count % log_interval == 0:
        time_count = 1
        for name, writer in self.writers_.items():
          writer_status = writer.status()
          if writer_status:
            self.logger_.info("[%s] status: [%s]", name, writer_status)
      time_count += 1
      time.sleep(1)

    self._finalize()
    self.logger_.info('Writer Manager Exit')
    self.all_exited_ = True

  def process_items(self):
    self.logger_.info('Page writer manager consumer start...')
    while not self.exit_ or not self.data_queue_.empty():
      try:
        item = self.data_queue_.get(block=True, timeout=10)
      except Queue.Empty:
        continue
      if not item:
        continue
      for name, writer in self.writers_.items():
        try:
          writer.process_item(item)
        except:
          self.logger_.exception('error while using [%s] writer', name)
          continue
    self.process_exit_ = True
    self.logger_.info('Page writer manager exit normal')

