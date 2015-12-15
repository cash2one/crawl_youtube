#!/usr/bin/python
# encoding: utf8
# Copyright 2015 LeTV Inc. All Rights Reserved.
# Author: gaoqiang@letv.com (Qiang Gao)

import base64
from qpid.messaging import Connection, Message
from scrapy.utils.project import get_project_settings
from page_writer_base import PageWriterBase
from thrift_util import thrift_to_str
from ..proto.crawl.ttypes import CrawlDocType

class FreshDocWriter(PageWriterBase):
  def _initialize(self):
    self.set_name('FreshDocWriter')
    if get_project_settings()['DEBUG_MODE']:
      self._push_message = self._push_message_debug
    else:
      self._create_client()

  def _create_client(self):
    try:
      self.connection_ = Connection(url='10.100.151.13:5672', heartbeat=4, reconnect=True,
                                    reconnect_limit=10, reconnect_interval=4)
      self.connection_.open()
      self.sender_ = self.connection_.session().sender('leso.exchange.fresh_video')
    except:
      self.connection_ = None
      self.logger_.exception('failed to connect to message queue server.')

  def finalize(self):
    if self.connection_:
      self.connection_.close()
    PageWriterBase.finalize(self)

  def _push_message_debug(self, doc):
    pass

  def _push_message(self, doc):
    doc.video.doc_id = doc.id
    doc.video.id = str(doc.id)
    doc.video.crawl_time = doc.video.create_time = doc.crawl_time
    doc.video.discover_time = doc.discover_time
    doc.video.url = doc.url
    doc.video.domain = doc.domain
    doc.video.domain_id = doc.domain_id
    doc.video.in_links = doc.in_links
    msg_body = thrift_to_str(doc.video)
    if not msg_body:
      return
    self.sender_.send(Message(content=doc.url + '\t' + base64.b64encode(msg_body), durable=True))
    self.logger_.info('send message successfully, %s', doc.url)

  def process_item(self, item):
    if not item:
      return
    doc = item.to_crawldoc()
    if doc.doc_type != CrawlDocType.PAGE_TIME:
      return
    try:
      self._push_message(doc)
    except:
      self.logger_.exception('failed to send message, %s', doc.url)

