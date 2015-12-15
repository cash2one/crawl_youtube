#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for queue_manager module.

A detailed description of queue_manager.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

import sys
from scrapy import log
from le_crawler.common.le_exceptions import QueueTagNotExisted

def singleton(cls):
  instances = {}
  def _singleton(*args, **kw):
    if not cls in instances:
      instances[cls] = cls(*args, **kw)
    return instances[cls]
  return _singleton

@singleton
class QueueManager(object):
  def __init__(self):
    self.queue_list = {}

  def tag_existed(self, queue_tag):
    return self.queue_list.has_key(queue_tag)

  def add(self, queue_tag, queue):
    if self.queue_list.has_key(queue_tag):
      log.msg("the queye tag %s has existed" % queue_tag, log.INFO)
    else:
      self.queue_list[queue_tag] = queue

  def get(self, queue_tag):
    return self.queue_list.get(queue_tag, None)

  def push(self, queue_tag, request):
    if not self.queue_list.has_key(queue_tag):
      raise QueueTagNotExisted
    return self.queue_list[queue_tag].push(request)

  def pop(self, queue_tag, timeout=0):
    if not self.queue_list.has_key(queue_tag):
      raise QueueTagNotExisted
    return self.queue_list[queue_tag].pop(timeout)

  def list_members(self, queue_tag):
    if not self.queue_list.has_key(queue_tag):
      raise QueueTagNotExisted
    return self.queue_list[queue_tag].list_members()


  def clear(self, queue_tag):
    if not self.queue_list.has_key(queue_tag):
      raise QueueTagNotExisted
    return self.queue_list[queue_tag].clear()

  def len(self, queue_tag):
    if not self.queue_list.has_key(queue_tag):
      raise QueueTagNotExisted
    return len(self.queue_list[queue_tag])

