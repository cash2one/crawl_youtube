#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for middlewares module.

A detailed description of middlewares.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

import random
import socket

from scrapy.settings import Settings
from scrapy import log


class BindaddressMiddleWare(object):
  def __init__(self, settings):
    self._ip = settings['BIND_ADDRESS_IP']
    self._port = settings['BIND_ADDRESS_PORT']
    self._port_min = 1025
    self._port_max = 65535
    self._base_port = 1025
    self._current_port = 1025
    self._port_step = 3

  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings)

  def process_request(self, request, spider):
    if self._ip and self._port:
      request.meta.update(bindaddress=(self._ip,
        self.get_useable_port(self._ip, spider)))

  def get_random_port(self, first_time = False):
    if first_time:
      self._current_port = random.randint(self._port_min, self._port_max)
      return self._current_port
    else:
      self._current_port += self._port_step
      if self._current_port > self._port_max:
        self._current_port = self._port_min
    return self._current_port

  def get_useable_port(self, ip, spider):
    port = self.get_random_port(True)
    failed_count = 0
    while True:
      try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.close()
        break
      except socket.error:
        failed_count += 1
        spider.log('Failed Bind Port:[%d] for [%d] times' %(port, failed_count), log.ERROR)
        port = self.get_random_port(False)
    return port

