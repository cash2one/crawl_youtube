#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for queue_cluster module.

A detailed description of queue_cluster.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

import hashlib
from operator import itemgetter

import le_crawler.core.signals

from le_crawler.core.queue import Base
from le_crawler.common.le_exceptions import ServerNumNotEnough
from scrapy.http.request import Request
from scrapy.utils.request import request_fingerprint
from scrapy.signalmanager import SignalManager
from threading import Timer

FLUSH_CACHE_INTERVAL = 1

class ClusterBase(Base):
  def __init__(self, servers, key, shard_dist):
    Base.__init__(self, servers, key)
    if not isinstance(self.server, list):
      self.server = [self.server]
    if (len(shard_dist) > len(self.server)):
      raise ServerNumNotEnough
    self.queues = []
    self.shard_dist = shard_dist

  def __len__(self):
    length = 0
    for q in self.queues:
      length = length + len(q)
    return length

  def _get_push_shard_id(self, data):
    raise NotImplementedError

  def _get_pop_shard_ids(self, num):
    len_dict = {idx:len(self.queues[idx]) for idx in range(len(self.queues))}
    len_list = sorted(len_dict.iteritems(), key=itemgetter(1), reverse=True)
    len_min = len_list[-1][1]
    request_num = num
    result = {}
    for pair in len_list[:-1]:
      diff = pair[1] - len_min
      if diff <= 0:
        break
      result[pair[0]] = diff < request_num and diff or request_num
      request_num -= result[pair[0]]
      if request_num <= 0:
        break
    if request_num:
      remain_ave = request_num / len(self.queues)
      remain_ext = request_num % len(self.queues)
      for idx in range(len(self.queues)):
        result[idx] = result.setdefault(idx, 0) + remain_ave
        if idx < remain_ext:
          result[idx] += 1
    return result

  def _push_single_internal(self, data):
    shard_id = self._get_push_shard_id(data)
    return self.queues[shard_id].push(data)

  def _push_list_internal(self, datas):
    data_dict = {}
    {data_dict.setdefault(
        self._get_push_shard_id(data), []).append(data) for data in datas}
    for shard_id in data_dict:
      self.queues[shard_id].push_list(data_dict[shard_id])

  def pop_list(self, size):
    shard_id_dict = self._get_pop_shard_ids(size)
    result = []
    for shard_id, num in shard_id_dict.items():
      result.extend(self.queues[shard_id].pop_list(num))
    return result


  def pop(self, timeout=0):
    shard_id_dict = self._get_pop_shard_ids(1)
    shard_id = 0
    for k, v in shard_id_dict.items():
      if v > 0:
        return self.queues[k].pop(timeout)

  def list_members(self):
    result = []
    for q in self.queues:
      result.extend(q.list_members())
    return result

  def clear(self):
    for q in self.queues:
      q.clear()

class StrDataQueueCluster(ClusterBase):
  def __init__(self, servers, key, queue_cls, shard_dist):
    ClusterBase.__init__(self, servers, key, shard_dist)
    shard_id = 0
    for i in range(len(shard_dist)):
      for j in range(shard_dist[i]):
        self.queues.append(queue_cls(servers[i], key + "_%d" % shard_id))
        shard_id += 1

  def _get_push_shard_id(self, data):
    if not isinstance(data, str):
      raise TypeError, TypeError("Only accept str type data")
    fp = hashlib.sha1(data).hexdigest()
    return int(fp[-4:], 16) % len(self.queues)

class RequestQueueCluster(ClusterBase):
  def __init__(self, servers, key, queue_cls, shard_dist, spider):
    ClusterBase.__init__(self, servers, key, shard_dist)
    shard_id = 0
    for i in range(len(shard_dist)):
      for j in range(shard_dist[i]):
        self.queues.append(queue_cls(servers[i], spider, key + "_%d" % shard_id))
        shard_id += 1

  def _get_push_shard_id(self, request):
    if not isinstance(request, Request):
      raise TypeError, TypeError("Only accept Request type data")
    fp = request_fingerprint(request)
    return int(fp[-4:], 16) % len(self.queues)

class CachedRequestQueueCluster(RequestQueueCluster):
  def __init__(self, servers, key, queue_cls, shard_dist,
               spider, cache_size=1024, auto_flush=True):
    RequestQueueCluster.__init__(self, servers, key, queue_cls, shard_dist, spider)
    self.cache_size = cache_size
    self._in_cache = []
    self._out_cache = []
    self.timer = None
    self.auto_flush = auto_flush
    if self.auto_flush:
      self.timer = Timer(FLUSH_CACHE_INTERVAL, self.flush_put_cache)
      self.timer.daemon = True
      self.timer.start()

  def flush_put_cache(self):
    if self.timer:
      self.timer.cancel()
    RequestQueueCluster._push_list_internal(self, self._in_cache)
    self._in_cache = []
    if self.auto_flush:
      self.timer = Timer(FLUSH_CACHE_INTERVAL, self.flush_put_cache)
      self.timer.start()

  def _push_list_internal(self, datas):
    self._in_cache.extend(datas)
    if len(self._in_cache) >= self.cache_size:
      self.flush_put_cache()
      self._in_cache = []

  def _push_single_internal(self, data):
    self._push_list_internal([data])

  def pop_list(self, size):
    pop_size = size - len(self._out_cache)
    pop_size = pop_size > 0 and pop_size or 0
    if pop_size:
      self._out_cache.extend(
          RequestQueueCluster.pop_list(self, pop_size + self.cache_size))
    result = self._out_cache[0:size]
    self._out_cache = self._out_cache[size:]
    return result

  def pop(self, timeout=0):
    result = self.pop_list(1)
    if result and len(result) > 0:
      return result[0]

  def clear(self):
    if self.timer:
      self.timer.cancel()
    RequestQueueCluster.clear(self)



