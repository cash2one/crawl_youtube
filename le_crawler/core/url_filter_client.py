#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import time

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol

from ..proto.filter import UrlFilterService

class UrlFilterClient(object):
  def __init__(self, ip, port, logger):
    self.logger_ = logger
    self.server_ip = ip
    self.server_port = port
    self._create_client()


  def _create_client(self, try_num=5):
    for i in range(1, try_num):
      try:
        tsocket = TSocket.TSocket(self.server_ip, self.server_port)
        tsocket.setTimeout(10000)
        self.transport = TTransport.TBufferedTransport(tsocket)
        self.client_ = UrlFilterService.Client(TCompactProtocol.TCompactProtocol(self.transport))
        self.transport.open()
        self.logger_.info('create filter client: %s' % self.client_)
        break
      except:
        self.logger_.exception('failed create filter client [%s/%s].', i, try_num)
        time.sleep(1)
        continue


  def close(self):
    self._logger_.info('client receive exit signals, closing')
    self.transport.close()
    self.exit_sig_ = True


  def url_seen(self, url):
    try:
      return self.client_.url_seen(url)
    except:
      self.logger_.exception('failed query url existence, %s', url)
      self._create_client()
      return False

