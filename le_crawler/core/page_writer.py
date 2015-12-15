#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import time
import Queue
import threading

from scrapy.utils.misc import load_object
from scrapy.utils.project import get_project_settings


writer_handlers = '''
le_crawler.core.page_writer.PageWriterBase,
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
    self._init_writer()

  def exit(self):
    self.logger_.info('page writer manager receive exit')
    self.exit_ = True
    while not self.all_exited_:
      time.sleep(2)

  def _gen_writer(self, writer_clss):
    if not writer_clss:
      return None
    strlist = filter(lambda l: l != '', [s.strip() for s in writer_clss.split(',')])
    if not strlist or len(strlist) <= 0:
      self.logger_.info('writer string flag is empty[%s]', writer_clss)
    try:
      for w in strlist:
        cls = load_object(w)(self.spider_)
        self.writers_[cls.name] = cls
        self.logger_.info('gen writer[%s]', cls.name)
    except:
      self.logger_.exception('failed gen writer.')
      raise Exception("Failed Generate Crawl Doc Writer [%s]", w)

  def _init_writer(self):
    for name, writer in self.writers_.items():
      self.logger_.info('init writer[%s]', name)
      if not writer.initialize():
        raise Exception('init writer %s error' % name)

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


class PageWriterBase(object):
  def __init__(self, spider):
    self.spider_ = spider
    self.writer_name_ = 'DefaultPageWriter'
    self.exit_ = False

  def set_name(self, name):
    self.writer_name_ = name

  @property
  def exit_sig(self):
    return self.exit_

  @property
  def name(self):
    return self.writer_name_

  # return true or false
  @property
  def spider(self):
    return self.spider_

  def initialize(self):
    return True

  def finalize(self):
    self.exit_ = True

  # return current status
  def status(self):
    pass

  # process item should never be block
  def process_item(self, item):
    pass


class PageWriterWithBuff(PageWriterBase):
  def __init__(self, spider, bufsize=1024):
    super(PageWriterWithBuff, self).__init__(spider)
    self.data_queue_ = Queue.LifoQueue(maxsize=bufsize)
    self.set_name('PageWriterWithBuff')
    self.inner_writer_ = threading.Thread(target=self._writer_thread, args=())
    self.__timeout = 0
    self.__timeout_callback = None
    self.__write_count = 0

  def initialize(self):
    self.inner_writer_.start()
    return True

  # all extend class should call super finalize
  def finalize(self):
    super(PageWriterWithBuff, self).finalize()
    while not self.wthread_exit_:
      self.logger_.info('[%s] wait inner thread', self.name)
      time.sleep(3)
    self.logger_.info('[%s] total writer item %s' % (self.name, self.__write_count))

  def status(self):
    return "page writer [%s]'s queue size: %d, has processed: %d" % \
           (self.name, self.data_queue_.qsize(), self.__write_count)

  # if return false, will skip the item
  def accept(self, item):
    return True

  def _writer_thread(self):
    self.wthread_exit_ = False
    self.logger_.info('[%s] inner thread running...' % self.name)
    while not self.exit_sig or not self.data_queue_.empty():
      try:
        item = self.data_queue_.get(block=True, timeout=5)
        if not item:
          continue
        self.writer(item)
        self.__write_count += 1
      except Queue.Empty:
        continue
      except:
        self.logger_.exception('writer thread fails.')
    self.wthread_exit_ = True
    self.logger_.info('[%s] inner thread end', self.name)

  def process_item(self, item):
    if not item:
      self.spider.info('item is null %s', item)
      return
    while not self.exit_sig:
      try:
        if self.accept(item):
          self.data_queue_.put(item, block=True, timeout=5)
        return
      except:
        self.logger_.exception('writer buffer full, size %d', self.data_queue_.qsize())
        continue

  # TODO:write you own logic here, no more need buffer
  def writer(self, item):
    pass

  def timeout_callback_register(self, callback=None, timeout=0):
    if not callable(callback):
      raise Exception('Uncallable callback: %s' % callback)
    self.__timeout = timeout
    self.__timeout_callback = callback

