#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
import os,sys
import commands

from scrapy import log

from ..core.page_writer import PageWriterWithBuff
class CDesktopWriter(PageWriterWithBuff):
  def __init__(self, spider):
    super(CDesktopWriter, self).__init__(spider)
    self.set_name('CDesktopWriter')
    self.data_reciver_ip = '10.180.92.206'
    self.data_port = 10086
    import socket
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect((self.data_reciver_ip, self.data_port))
    self.total_send_count = 0

  def __send_with_socket(self, datastr):
    self.s.sendall(datastr + '\n')

  def __writer_data(self, datastr):
    cmd = 'echo \'%s\' | nc %s %s' % (datastr,
        self.data_reciver_ip,
        self.data_port)
    self.spider.log('send data:%s' % (cmd), log.DEBUG)
    sta, result = commands.getstatusoutput(cmd)
    if sta != 0:
      msg = 'Failed to send data:[%s]%s' % (sta, result)
      self.spider.log(msg, log.ERROR)
      raise Exception(msg)

  def writer(self, item):
    datastr = item.to_json_str()
    self.__send_with_socket(datastr)
    self.total_send_count += 1
    #self.__writer_data(datastr)
