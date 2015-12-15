#!/usr/bin/python
#coding=utf-8
#author=gaoqiang@letv.com
#
# Copyright 2015 LeTV Inc. All Rights Reserved.

import time
import threading

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol

from ..proto.scheduler import SchedulerService

"""
this sheduler is using for thrift RPC, read more about:
  search2/crawler_ver2/le_crawler/proto/scheduler_service.thrift
"""

class SchedulerClient(object):
  def __init__(self, server_ip="localhost", server_port=8088):
    self.server_ip_ = server_ip
    self.server_port_ = server_port
    self.exit_sig_ = False
    self.client_ = None
    self.lock_ = threading.Lock()


  def open(self, logger):
    self._logger = logger
    self._create_scheduler_client(self.server_ip_, self.server_port_)


  def _create_scheduler_client(self, host, port, try_num=5):
    self.lock_.acquire()
    for i in range(1, try_num):
      try:
        tsocket = TSocket.TSocket(host, port)
        tsocket.setTimeout(10000)
        self.transport = TTransport.TBufferedTransport(tsocket)
        self.client_ = SchedulerService.Client(TCompactProtocol.TCompactProtocol(self.transport))
        self.transport.open()
        self._logger.info('create scheduler client: %s' % self.client_)
        break
      except:
        self._logger.exception('failed create scheduler client [%s/%s].', i, try_num)
        time.sleep(1)
        continue
    self.lock_.release()


  def close(self):
    self._logger.info('client receive exit signals, closing')
    self.transport.close()
    self.exit_sig_ = True


  def get_crawldocs_local(self, required_num=40):
    while 1:
      try:
        return self.client_.get_crawldocs(required_num)
      except:
        self._logger.exception('failed get crawl_docs.')
        self._create_scheduler_client(self.server_ip_, self.server_port_)
      time.sleep(2)


  # return bool
  def set_crawldocs_local(self, docs):
    while 1:
      try:
        self.client_.set_crawldocs(docs)
        self._logger.info('pushed crawl_doc to scheduler: %s', len(docs))
        return True
      except:
        self._logger.exception('failed set crawl_docs.')
        self._create_scheduler_client(self.server_ip_, self.server_port_)
      time.sleep(1)

