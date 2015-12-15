#!/usr/bin/python
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

class PageWriterBase(object):
  def __init__(self, spider):
    self.spider_ = spider
    self.logger_ = spider.logger_
    self.exit_ = False
    self._initialize()

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

  def _initialize(self):
    self.writer_name_ = 'DefaultPageWriter'
    return True

  def finalize(self):
    self.exit_ = True

  # return current status
  def status(self):
    pass

  # process item should never be block
  def process_item(self, item):
    pass

