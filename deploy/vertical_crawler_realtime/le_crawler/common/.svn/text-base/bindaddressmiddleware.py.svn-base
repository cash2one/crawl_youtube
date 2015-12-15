#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
"""
this middlewares is using for bind multi ip
now we can support random bind ip to create http only
"""

__author__ = 'guoxiaohe@letv.com (guo xiaohe)'

import random
import socket

from scrapy.settings import Settings
from scrapy import log


class BindaddressMiddleWare(object):
  def __init__(self, settings):
    if not settings['BINDIP_LOCAL']:
      self._ips = [settings['BIND_ADDRESS_IP']]
    else:
      self.__get_ips_auto()
    if not self._ips:
      raise Exception('Failed Got Bind ip(s)')
    self._port_min = 7025
    self._port_max = 65535
    self._base_port = 1025
    self._current_port = 1025
    self._port_step = 1
    self._ip_idx = 0

  def __get_ips_auto(self):
    import os
    cmd = "ifconfig | grep -A 3 eth0 | grep 'inet addr' | awk -F ' ' '{print $2}' | awk -F ':' '{print $2}'"
    self._ips = [ip.strip().replace('\n', '') for ip in os.popen(cmd).readlines()]
    print 'Got IP List: %s' % self._ips

  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings)

  def process_request(self, request, spider):
    if self._ips:
      if self._ip_idx >= len(self._ips):
        self._ip_idx = 0
      ip = self._ips[self._ip_idx]
      request.meta.update(bindaddress=(ip,
        self.get_useable_port(ip, spider)))
      self._ip_idx += 1

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

