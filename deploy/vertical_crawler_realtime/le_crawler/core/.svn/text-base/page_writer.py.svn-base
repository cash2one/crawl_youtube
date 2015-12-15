#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'


import time
import Queue
import threading

from scrapy import log
from scrapy.utils.misc import load_object
from scrapy.utils.project import get_project_settings


writer_handlers = '''
le_crawler.core.page_writer.PageWriterBase,
le_crawler.common.page_local_writer.PageLocalWriter
'''
#le_crawler.common.today_tv_writer.TodayTvWriter
#le_crawler.common.page_local_writer.PageLocalWriter
class PageWriterManager(threading.Thread):
  def __init__(self, queue_max_size = 1024, spider = None):
    threading.Thread.__init__(self)
    self.data_queue_ = Queue.LifoQueue(maxsize = queue_max_size)
    self.exit_ = False
    # base on PageWriter
    self.writers_ = {}
    self.spider_ = spider
    self.process_exit_ = False
    self.all_exited_ = False
    # 'mysql.PageMysqlWriter, page_local_writer.PageDataWriter'
    self.writerstr_ = get_project_settings()['CRAWL_DOC_WRITERS'] or writer_handlers
    #'sle_crawler.common.page_local_writer.PageLocalWriter, sle_crawler.common.wc_page_writer.PageMysqlWriter'
    self._gen_writer(self.writerstr_)
    self._init_writer()

  def exit(self):
    self.spider_.log('page writer manager reciver exit', log.INFO)
    self.exit_ = True
    while not self.all_exited_:
      time.sleep(2)

  def _gen_writer(self, writer_clss):
    if not writer_clss:
      return None
    strlist = filter(lambda l: l != '', [s.strip() for s in  writer_clss.split(',')])
    if not strlist or len(strlist) <= 0:
      self.spider_.log('writer string flag is empty[%s]'%(writer_clss), log.INFO)
    try:
      for w in strlist:
        cls = load_object(w)(self.spider_)
        self.writers_[cls.name] = cls
        self.spider_.log('gen writer[%s]'%(cls.name), log.INFO)
    except Exception, e:
      import traceback
      print traceback.format_exc()
      raise Exception("Failed Generate Crawl Doc Writer [%s] : %s" % (w, e))

  def _init_writer(self):
    for (name, writer) in self.writers_.items():
      self.spider_.log('init writer[%s]'%(name), log.INFO)
      if not writer.initialize():
        raise Exception('Init writer %s error' % (name))

  def _finalize(self):
    for (name, writer) in self.writers_.items():
      self.spider_.log('finalize writer[%s]'%(name), log.INFO)
      writer.finalize()
      self.spider_.log('finished finalize writer[%s]'%(name), log.INFO)


  def add_item(self, item):
    if not item:
      return
    while True:
      try:
        self.data_queue_.put(item, block = True, timeout = 5)
        return
      except Exception, e:
        self.spider_.log('try to put item into queu error %s, size %d' % (e,
          self.data_queue_.qsize()))
        continue

  def run(self):
    consu_thread = threading.Thread(target = self.process_items, args = ()) 
    consu_thread.start()
    time_count = 0
    log_interval = 300
    while not self.process_exit_:
      #self.spider_.log('Writer Queue Size[%d]' % (self.data_queue_.qsize()),
      #    log.DEBUG)
      if time_count % log_interval == 0:
        time_count = 1
        for (name, writer) in self.writers_.items():
          tmpstr = writer.status()
          if tmpstr:
            self.spider_.log("[%s] says [%s]" % (name, tmpstr), log.INFO)
      time_count += 1
      time.sleep(1)

    self._finalize()
    self.spider_.log('Writer Manager Exit', log.INFO)
    self.all_exited_ = True

  def process_items(self):

    self.spider_.log('Page writer manager consumer start...', log.INFO)
    while not self.exit_ or not self.data_queue_.empty():
      item = None
      try:
        item = self.data_queue_.get(block = True, timeout = 10)
      except Exception, e:
        self.spider_.log('Page Writer Manager Got Nonthing From queue[%s]'
            %(e.message), log.DEBUG)
        continue
      if not item:
        continue
      for (name, writer) in self.writers_.items():
        try:
          writer.process_item(item)
        except Exception, e:
          self.spider_.log('Error while using [%s] writer[%s]' % (name,
            e.message), log.ERROR)
          continue
    self.process_exit_ = True
    self.spider_.log('Page writer manager exit normal', log.INFO)

class PageWriterBase(object):
  def __init__(self, spider):
    self.spider_ = spider
    self.writer_name_ ='DefaultPageWriter'
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

# 
class PageWriterWithBuff(PageWriterBase):
  def __init__(self, spider, bufsize = 1024):
    super(PageWriterWithBuff, self).__init__(spider)
    self.data_queue_ = Queue.LifoQueue(maxsize = bufsize)
    self.set_name('PageWriterWithBuff')
    self.inner_writer_ = threading.Thread(target = self._writer_thread, args =
        ())
    self.__timeout = 0
    self.__timeout_callback = None

  def initialize(self):
    self.inner_writer_.start()
    return True

  # all extend class should call super finalize
  def finalize(self):
    super(PageWriterWithBuff, self).finalize()
    while not self.wthread_exit_:
      self.spider_.log('[%s] wait iner thread' % (self.name), log.INFO)
      time.sleep(3)

  def status(self):
    return str('[%s]\'s queue size#: %d' % (self.name, self.data_queue_.qsize()))

  # if return false, will skip the item
  def accept(self, item):
    return True

  def _writer_thread(self):
    self.wthread_exit_ = False
    self.spider.log('[%s] iner thread running...' % (self.name), log.INFO)
    while not self.exit_sig or not self.data_queue_.empty():
      item = None
      try:
        item = self.data_queue_.get(block = True, timeout = 5)
        if not item:
          continue
        self.writer(item)
      except Exception, e:
        #self.spider_.log('I am starving[%d] with error[%s]'
        #    %((self.data_queue_.qsize()), e.message), log.INFO)
        continue

    self.wthread_exit_ = True
    self.spider_.log('[%s] iner thread end' % (self.name), log.INFO)

  def process_item(self, item):
    if not item:
      self.spider.log('item is null %s' % (item), log.INFO)
      return
    while not self.exit_sig:
      try:
        if self.accept(item):
          self.data_queue_.put(item, block = True, timeout = 5)
        return
      except Exception, e:
        self.spider_.log('PageWriterWithBuff writer buffer is full %s, size %d' % (e,
          self.data_queue_.qsize()), log.ERROR)
        continue

  # TODO:writer you own logic here, no more need buf
  def writer(self, item):
    pass

  def timeout_callback_register(self, callback = None, timeout = 0):
    if not callable(callback):
      raise Exception('Uncallable: %s' % callback)
    self.__timeout = timeout
    self.__timeout_callback = callback

class SpiderMock(object):
  def __init__(self):
    pass

  def log(self, object, level):
    print '%s' % (object)

# test mock case
if __name__ == '__main__':
  spider = SpiderMock()
  pgmgr = PageWriterManager(spider = spider)
  pgmgr.add_item('hello1')
  pgmgr.add_item('hello2')
  pgmgr.add_item('hello3')
  pgmgr.add_item('hello4')
  pgmgr.start()

