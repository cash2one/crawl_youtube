#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import urllib2, urllib
import socket

from scrapy import log
from scrapy.utils.project import get_project_settings

from le_crawler.core.page_writer import PageWriterWithBuff

class CDesktopWriter(PageWriterWithBuff):
  def __init__(self, spider):
    super(CDesktopWriter, self).__init__(spider)
    self.set_name('CDesktopWriter')
    self.data_reciver_ip = '10.180.92.206'
    self.data_port = 10086
    self.total_send_count = 0
    self.type_c = get_project_settings().get('CD_WRITE_TYPE', 'http')
    self.post_url = get_project_settings().get('CD_WRITE_POST_URL',
        'http://10.180.92.206:9998/bigdata/post/webpage')
    self.connection = None
    self.__create_data_pipe()
    self.retry_time_max = 10

  def __create_data_pipe(self):
    try:
      if self.connection:
        self.connection.close()
      if self.type_c == 'http':
        self.headers = \
            {'Content-Type' : 'application/json', 'Referer': 'crawler@search2'}
      else:
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.data_reciver_ip, self.data_port))
    except Exception, e:
      self.spider_.log('failed create connect for %s' % (self.type_c), log.ERROR)
      raise e

  def _send_data(self, datastr):
    try:
      err_msg = ''
      if self.type_c == 'http':
        response = urllib2.urlopen(urllib2.Request(url = self.post_url,
          data = datastr,
          headers = self.headers))
        err_msg = '[%s], %s' %(response.getcode(), response.read())
        if response.getcode() != 200:
          self.spider.log('Failed Send data with pos:%s' % (err_msg), log.ERROR)
          return False
      else:
        self.connection.sendall(datastr + '\n')
      return True
    except Exception, e:
      import traceback
      self.spider_.log('send data with error:%s, %s' % (e.message,
        traceback.format_exc()), log.ERROR)
      self.__create_data_pipe()
      return False

  def status(self):
    return '%s, %s' %(self.total_send_count, PageWriterWithBuff.status(self)) 

  def writer(self, item):
    datastr = item.to_json_str()
    try_time = 0
    # will retry 10 times, if not drop
    while try_time < self.retry_time_max:
      if not self._send_data(datastr):
        try_time += 1
        continue
      break
    self.total_send_count += 1
