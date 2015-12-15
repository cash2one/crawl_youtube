#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for dupefilter module.

A detailed description of dupefilter.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

import connection

from queue_cluster import StrDataQueueCluster
from queue import DataSet
from scrapy.dupefilter import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

DUPEFILTER_KEY = '%(spider)s:dupefilter'
DUPE_SHARD_DIST = [1]

class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""

    def __init__(self, servers, dupe_key, shard_dist):
        """Initialize duplication filter

        Parameters
        ----------
        servers  : list
            redis clent list
        dupe_key : str
            Where to store fingerprints
        """
        self.servers = servers
        self.dupe_key = dupe_key
        self.shard_dist = shard_dist

    def set_spider(self, spider):
      self.dupe_key = self.dupe_key % {'spider': spider.name}
      self.queue_cluster = StrDataQueueCluster(
          self.servers, self.dupe_key, DataSet, self.shard_dist)

    @classmethod
    def from_settings(cls, settings):
        servers = connection.from_settings(settings)
        dupefilter_key = settings.get('DUPEFILTER_KEY', DUPEFILTER_KEY)
        shard_dist = settings.get('DUPE_SHARD_DIST', DUPE_SHARD_DIST)
        return cls(servers, dupefilter_key, shard_dist)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        rets = self.queue_cluster.push(fp)
        return not rets

    def close(self, reason):
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        """Clears fingerprints data"""
        self.queue_cluster.clear()
