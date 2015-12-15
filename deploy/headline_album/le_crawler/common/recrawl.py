#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for test module.

A detailed description of test.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

import sys
import le_crawler.signals
import scrapy.signals
import scrapy.log
import connection
import scrapy_redis.connection
from scrapy.http import Request
from queue import DataSet
from queue_manager import QueueManager
from queue_cluster import StrDataQueueCluster

try:
    import cPickle as pickle
except ImportError:
    import pickle

RECRAWL_KEY = 'recrawl_list'
RECRAWL_SHARD_DIST = [1]
PRIORITY_QUEUE_TAG = 'priority_queue'
RECRAWL_LIST_TAG = 'recrawl_list'

class Recrawl(object):
  def __init__(self, servers, key, shard_dist, crawler):
    """Initialize Recrawler

    Parameters
    ----------
    server : Redis instance
    key : str
        Where to store fingerprints
    """
    self.queues = QueueManager()
    self.crawler = crawler
    data_queue = StrDataQueueCluster(servers, key, DataSet, shard_dist)
    self.queues.add(RECRAWL_LIST_TAG, data_queue)

  @classmethod
  def from_crawler(cls, crawler):
    servers = connection.from_settings(crawler.settings)
    key = crawler.settings.get('RECRAWL_LIST_KEY', RECRAWL_KEY)
    shard_dist = crawler.settings.get('RECRAWL_SHARD_DIST', RECRAWL_SHARD_DIST)
    recrawl = cls(servers, key, shard_dist, crawler)
    crawler.signals.connect(
        recrawl.setup_recrawl, signal=scrapy.signals.spider_opened)
    return recrawl

  def setup_recrawl(self, spider):
    self.crawler.signals.connect(
        self.recrawl, signal=le_crawler.signals.hourly_timeout)

  def recrawl(self):
    recrawl_list = list(self.queues.list_members(RECRAWL_LIST_TAG))
    for url in recrawl_list:
      req = Request(url, dont_filter=True)
      self.queues.push(PRIORITY_QUEUE_TAG, req)

