#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for spiders module.

A detailed description of le_spiders.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider

from le_crawler.core.queue_cluster import StrDataQueueCluster
from le_crawler.core.queue import DataSet
from le_crawler.core.connection import from_settings

PRIORITY_QUEUE_SHARD_DIST = [1]

class RedisMixin(object):
    """Mixin class to implement reading urls from a redis queue."""
    redis_key = None  # use default '<spider>:start_urls'

    def setup_redis(self):
        """Setup redis connection and idle signal.

        This should be called after the spider has set its crawler object.
        """
        if not self.redis_key:
            self.redis_key = '%s:start_urls' % self.name

        servers = from_settings(self.crawler.settings)
        # idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        self.log("Reading URLs from redis list '%s'" % self.redis_key)
        queue_shard_dist = self.crawler.settings.get(
          'PRIORITY_QUEUE_SHARD_DIST', PRIORITY_QUEUE_SHARD_DIST)
        self.queues = StrDataQueueCluster(
            servers, self.redis_key, DataSet, queue_shard_dist)

    def next_request(self):
        """Returns a request to be scheduled or none."""
        url = self.queues.pop()
        if url:
            return self.make_requests_from_url(url)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        req = self.next_request()
        if req:
            self.crawler.engine.crawl(req, spider=self)
        raise DontCloseSpider

class RedisSpider(RedisMixin, Spider):
    """Spider that reads urls from redis queue when idle."""

    def set_crawler(self, crawler):
        super(RedisSpider, self).set_crawler(crawler)
        self.setup_redis()
