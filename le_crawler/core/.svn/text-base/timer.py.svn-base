#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for timmer module.

A detailed description of timmer.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

import scrapy
import le_crawler.core.signals
from threading import Timer


class TimerDispatcher(object):
  def __init__(self, crawler):
    self.crawler = crawler
    self.timer_list = []

  def send_singal(self, send_singal, next_timeout, idx):
    self.crawler.core.signals.send_catch_log(signal=send_singal)
    if idx >= 0:
      self.timer_list.pop(idx).cancel()
    t = Timer(next_timeout, self.send_singal,
              (send_singal, next_timeout, len(self.timer_list)))
    self.timer_list.append(t)
    t.start()

  def start_timer(self):
    self.send_singal(le_crawler.core.signals.minutely_timeout, 60, -1)
    self.send_singal(le_crawler.core.signals.hourly_timeout, 60*60, -1)
    self.send_singal(le_crawler.core.signals.minutely_timeout, 60*60*24, -1)
    for k, v in self.crawler.settings.get("CUSTOM_TIMERS", {}).items():
      sig = getattr(le_crawler.core.signals, k, None)
      if sig:
        self.send_singal(sig, v, -1)

  def clear(self):
    for timer in self.timer_list:
      timer.cancel()
    self.timer_list = []

  @classmethod
  def from_crawler(cls, crawler):
    timer = cls(crawler)
    crawler.core.signals.connect(
        timer.start_timer, signal=scrapy.signals.spider_opened)
    crawler.signals.connect(
        timer.clear, signal=scrapy.signals.spider_closed)
    return timer
