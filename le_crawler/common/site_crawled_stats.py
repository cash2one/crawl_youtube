#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.

__author__ = 'guoxiaohe@letv.com'

"""
Extension for collecting core stats like items scraped and start/finish times
"""

import os
import time
import cPickle as pickle

from scrapy import signals
from scrapy.statscollectors import StatsCollector
from scrapy import log

from url_filter import UrlFilter


class DiskableStateCollector(StatsCollector):
  def __init__(self, crawler):
    super(DiskableStateCollector, self).__init__(crawler)
    self._stats_dir = crawler.settings.get('JOBDIR', '../data/')
    # default every 23min dump
    self._stats_dump_inv_ = crawler.settings.getint('STATS_DUMP_INTERVAL', 1380)
    if not os.path.exists(self._stats_dir):
      os.makedirs(self._stats_dir)
    assert os.path.isdir(self._stats_dir), '%s is not dir' % self._stats_dir
    self._stats_nick = 'statscollector.global'
    self._exit_sig = False

  def open_spider(self, spider):
    super(DiskableStateCollector, self).open_spider(spider)
    nick_stats = os.path.join(self._stats_dir, self._stats_nick)
    if not os.path.isfile(nick_stats):
      return
    fp = open(nick_stats, 'rb')
    self._stats = pickle.load(fp)
    spider.log('Restore stats from disk %s' % self._stats_dir, log.INFO)

  def close_spider(self, spider, reason):
    super(DiskableStateCollector, self).close_spider(spider, reason)
    self._exit_sig = True
    fp = open(os.path.join(self._stats_dir, self._stats_nick), 'wb')
    pickle.dump(self._stats, fp, 2)
    spider.log('Dump stats to disk %s' % self._stats_dir, log.INFO)
    fp.close()

  # dump stats every time interval
  def dump_thread(self):
    seconds_count = 0
    while not self._exit_sig:
      if seconds_count >= self._stats_dump_inv_:
        fp = open(os.path.join(self._stats_dir, self._stats_nick), 'wb')
        pickle.dump(self._stats, fp, 2)
        fp.close()
        seconds_count = 0
      seconds_count += 3
      time.sleep(3)


class SiteCrawledStats(object):
    def __init__(self, stats):
        self.stats = stats
        self.url_filter_ = UrlFilter.get_instance()

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(o.item_dropped, signal=signals.item_dropped)
        return o

    def spider_opened(self, spider):
      pass

    def spider_closed(self, spider, reason):
      pass

    def __get_flag(self, url):
      if not url:
        return None
      domain = self.url_filter_.get_allowed_domain_from_url(url)
      if not domain:
        domain = 'othres.site'
      return domain

    def item_scraped(self, item, spider):
      if not item:
        return None
      domain = '%s(crawled)' % (self.__get_flag(item.get('url', None)))
      self.stats.inc_value(domain, spider=spider)

    def item_dropped(self, item, spider, exception):
      if not item:
        return None
      reason = exception.__class__.__name__
      domain = '%s(droped)' % (self.__get_flag(item.get('url', None)))
      self.stats.inc_value(domain, spider=spider)
      self.stats.inc_value('%s/%s' %( domain, reason), spider=spider)
 # for domain exception statistic


class DomainExceptionStats(object):
    def __init__(self, stats):
        self.stats = stats
        self.url_filter_ = UrlFilter.get_instance()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def process_exception(self, request, exception, spider):
        ex_class = "%s.%s" % (exception.__class__.__module__, exception.__class__.__name__)
        self.stats.inc_value('downloader/exception_type_count/%s[%s]' % (
            ex_class, self.url_filter_.get_flag(request.url)), spider=spider)
