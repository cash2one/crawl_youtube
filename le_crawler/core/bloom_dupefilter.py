#!python
#
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.cn'

import traceback

# from thrift.Thrift import TException
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TCompactProtocol
from scrapy.dupefilters import BaseDupeFilter

from le_crawler.proto.util import BloomFilterRdService
from le_crawler.proto.util.ttypes import FilterStatus


class BloomRedisClient(object):
  def __init__(self, host, port):
    self._client = None
    self.host = host
    self.port = port
    self.get_connection()
    self.max_retry = 100

  def get_connection(self, new=False):
    if new:
      try:
        self.close()
        self.log('close bloom service and create new connection.')
      except:
        # self.spider_.log('failed to close bloom client, detailed: %s' % traceback.format_exc(), log.ERROR)
        print traceback.format_exc()
    elif self._client:
      return self._client
    try:
      tsocket = TSocket.TSocket(self.host, self.port)
      tsocket.setTimeout(10000)
      self.transport_ = TTransport.TBufferedTransport(tsocket)
      self.transport_.open()
      self._client = BloomFilterRdService.Client(TCompactProtocol.TCompactProtocol(self.transport_))
    except:
      # self.spider_.log("Failed creat connection to  bloom filter service: %s" % traceback.format_exc(), log.ERROR)
      print traceback.format_exc()
      self._client = None
      raise Exception('Failed connect to bloom filter service')

  def is_element_present(self, key):
    if self._client:
      return self._client.IsElementPresent(key)
    raise Exception("Failed IsElementPresent operator for key:%s" % key)

  def fill_element(self, key):
    if self._client:
      return self._client.FillElement(key)
    raise Exception("Failed FillElement operator for key:%s" % key)

  def close(self):
    self.transport_.close()
    # self._client.close()
    self._client = None

class BloomDupeFilter(BaseDupeFilter):
  """bloom Redis-based request duplication filter"""
  def __init__(self, bloom_host, bloom_port):
    """Initialize duplication filter
    Parameters
    ----------
    server : bloom filter server
    key : str
    Where to store fingerprints
    """
    self.client = BloomRedisClient(bloom_host, bloom_port)

  @classmethod
  def from_settings(cls, settings):
    bloom_host = settings.get("BLOOM_DUPE_HOST")
    bloom_port = settings.get("BLOOM_DUPE_PORT")
    return cls(bloom_host, bloom_port)

  @classmethod
  def from_crawler(cls, crawler):
    return cls.from_settings(crawler.settings)

  def request_seen(self, request):
   # fp = request_fingerprint(request)
   # NOTE(xiaohe): this we will using request url for dupe, not the request
   # if this method is not adjust our reqired, replace with request_fingerprint
   ret = self.client.fill_element(request.url)
   if ret == FilterStatus.BLOOM_EXIST:
     return True
   elif ret == FilterStatus.BLOOM_NOT_EXIST:
     return False
   else:
     raise Exception('Failed operation with bloom filter')

  def close(self, reason):
    """Delete data on close. Called by scrapy's scheduler"""
    self.client.close()
    self.clear()

  def clear(self):
    pass

if __name__ == '__main__':
  client = BloomRedisClient('127.0.0.1', 8099)
  print client.is_element_present('hello world')
  print client.is_element_present('key hello world')
  print client.fill_element('key hello world')
  print client.is_element_present('key hello world')
