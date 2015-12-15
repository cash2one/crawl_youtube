#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for scheduler module.

A detailed description of scheduler.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

import connection

from scrapy.utils.misc import load_object
from le_crawler.core.dupefilter import RFPDupeFilter
from le_crawler.core.queue_manager import QueueManager
from le_crawler.core.queue_cluster import CachedRequestQueueCluster
from le_crawler.core.queue_cluster import RequestQueueCluster

from le_crawler.base.url_normalize import UrlNormalize


# default values
SCHEDULER_PERSIST = False
INPUT_QUEUE_KEY = '%(spider)s:input_requests'
INPUT_QUEUE_CLASS = 'scrapy_redis.core.queue.SpiderPriorityQueue'
INPUT_QUEUE_SHARD_DIST = [1]
INPUT_QUEUE_TAG = 'input_request_queue'
OUTPUT_QUEUE_KEY = '%(spider)s:output_requests'
OUTPUT_QUEUE_CLASS = 'scrapy_redis.core.queue.SpiderPriorityQueue'
OUTPUT_QUEUE_SHARD_DIST = [1]
OUTPUT_QUEUE_TAG = 'output_request_queue'
PRIORITY_QUEUE_KEY = '%(spider)s:requests'
PRIORITY_QUEUE_CLASS = 'le_crawler.core.queue.SpiderStack'
PRIORITY_QUEUE_SHARD_DIST = [1]
PRIORITY_QUEUE_TAG = 'priority_queue'
DUPEFILTER_KEY = '%(spider)s:dupefilter'
RECRAWL_KEY = 'recrawl_list'
IDLE_BEFORE_CLOSE = 0


class Scheduler(object):
    """Redis-based scheduler"""

    def __init__(self, servers, persist, input_queue_key, input_queue_cls,
                 input_queue_shard_dist, output_queue_key, output_queue_cls,
                 output_queue_shard_dist, priority_queue_key,
                 priority_queue_cls, priority_queue_shard_dist, recrawl_key,
                 dupefilter_key, dupe_filter_ins, idle_before_close):
        """Initialize scheduler.

        Parameters
        ----------
        servers : list of Redis instance
        persist : bool
        queue_key : str
        queue_cls : queue class
        dupe_filter_cls : dupefilter class
        dupefilter_key : str
        idle_before_close : int
        """
        self.persist = persist
        self.input_queue_key = input_queue_key
        self.input_queue_cls = input_queue_cls
        self.input_queue_shard_dist = input_queue_shard_dist
        self.output_queue_key = output_queue_key
        self.output_queue_cls = output_queue_cls
        self.output_queue_shard_dist = output_queue_shard_dist
        self.priority_queue_key = priority_queue_key
        self.priority_queue_cls = priority_queue_cls
        self.priority_queue_shard_dist = priority_queue_shard_dist
        self.dupefilter_key = dupefilter_key
        self.df = dupe_filter_ins
        self.recrawl_key = recrawl_key
        self.idle_before_close = idle_before_close
        self.stats = None
        self.servers = servers
        self.queues = QueueManager()
        self.url_normalize = UrlNormalize()

    def __len__(self):
        return self.queues.len(PRIORITY_QUEUE_TAG) +\
               self.queues.len(OUTPUT_QUEUE_TAG)

    @classmethod
    def from_settings(cls, settings):
        persist = settings.get('SCHEDULER_PERSIST', SCHEDULER_PERSIST)
        input_queue_key = settings.get(
          'INPUT_QUEUE_KEY', INPUT_QUEUE_KEY)
        input_queue_cls = load_object(settings.get(
          'INPUT_QUEUE_CLASS', INPUT_QUEUE_CLASS))
        input_queue_shard_dist = settings.get(
          'INPUT_QUEUE_SHARD_DIST', INPUT_QUEUE_SHARD_DIST)
        output_queue_key = settings.get(
          'OUTPUT_QUEUE_KEY', OUTPUT_QUEUE_KEY)
        output_queue_cls = load_object(settings.get(
          'OUTPUT_QUEUE_CLASS', OUTPUT_QUEUE_CLASS))
        output_queue_shard_dist = settings.get(
          'OUTPUT_QUEUE_SHARD_DIST', OUTPUT_QUEUE_SHARD_DIST)
        priority_queue_key = settings.get(
          'PRIORITY_QUEUE_KEY', PRIORITY_QUEUE_KEY)
        priority_queue_cls = load_object(settings.get(
          'PRIORITY_QUEUE_CLASS', PRIORITY_QUEUE_CLASS))
        priority_queue_shard_dist = settings.get(
          'PRIORITY_QUEUE_SHARD_DIST', PRIORITY_QUEUE_SHARD_DIST)
        dupefilter_key = settings.get('DUPEFILTER_KEY', DUPEFILTER_KEY)
        idle_before_close = settings.get('SCHEDULER_IDLE_BEFORE_CLOSE', IDLE_BEFORE_CLOSE)
        servers = connection.from_settings(settings)
        dupefilter_ins = load_object(
            settings['DUPEFILTER_CLASS']).from_settings(settings)
        recrawl_key = settings.get('RECRAWL_LIST_KEY', RECRAWL_KEY)
        return cls(servers, persist, input_queue_key, input_queue_cls,
                   input_queue_shard_dist, output_queue_key, output_queue_cls,
                   output_queue_shard_dist, priority_queue_key,
                   priority_queue_cls, priority_queue_shard_dist, recrawl_key,
                   dupefilter_key, dupefilter_ins, idle_before_close)

    @classmethod
    def from_crawler(cls, crawler):
        instance = cls.from_settings(crawler.settings)
        # FIXME: for now, stats are only supported from this constructor
        instance.stats = crawler.stats
        return instance

    def open(self, spider):
        self.spider = spider
        input_queue = CachedRequestQueueCluster(
            self.servers,
            self.input_queue_key,
            self.input_queue_cls,
            self.input_queue_shard_dist,
            self.spider)
        output_queue = CachedRequestQueueCluster(
            self.servers,
            self.output_queue_key,
            self.output_queue_cls,
            self.output_queue_shard_dist,
            self.spider)
        priority_queue = RequestQueueCluster(
            self.servers,
            self.priority_queue_key,
            self.priority_queue_cls,
            self.priority_queue_shard_dist,
            self.spider)
        self.queues.add(INPUT_QUEUE_TAG, input_queue)
        self.queues.add(OUTPUT_QUEUE_TAG, output_queue)
        self.queues.add(PRIORITY_QUEUE_TAG, priority_queue)
        if self.idle_before_close < 0:
            self.idle_before_close = 0
        # notice if there are requests already in the queue to resume the crawl
        if len(input_queue):
            spider.log("Resuming crawl (%d requests scheduled)" % len(input_queue))
        if isinstance(self.df, RFPDupeFilter):
          self.df.set_spider(spider)

    def close(self, reason):
        if not self.persist:
            self.df.clear()
            self.queues.clear(INPUT_QUEUE_TAG)
            self.queues.clear(OUTPUT_QUEUE_TAG)
            self.queues.clear(PRIORITY_QUEUE_TAG)

    def enqueue_request(self, request):
        if not request:
          return
        # TODO(Xiaohe): move url normalize to some better place
        # process request, url normalize
        # some place we dont need normalize url in process request or response
        tmpurl = self.url_normalize.get_unique_url(request.url)
        if not tmpurl:
          raise Exception('Bad request url:%s' % (request.url))
          return
        new_meta = request.meta.copy() or {}
        new_meta['Rawurl'] = request.url
        nrequest = request.replace(url = tmpurl, meta = new_meta)
        if not request.dont_filter and self.df.request_seen(request):
          return
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        self.queues.push(INPUT_QUEUE_TAG, nrequest)

    def next_request(self):
        block_pop_timeout = self.idle_before_close
        request = self.queues.pop(PRIORITY_QUEUE_TAG, block_pop_timeout)
        if request is None:
          request = self.queues.pop(OUTPUT_QUEUE_TAG, block_pop_timeout)
        if request and self.stats:
            self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
        if request and not request.meta.has_key('Rawurl'):
          tmpurl = self.url_normalize.get_unique_url(request.url)
          if not tmpurl:
            raise Exception('Bad request url:%s' % (request.url))
          nrequest = request.replace(url = tmpurl)
          return nrequest
        return request

    def has_pending_requests(self):
        return len(self) > 0
