#!/usr/bin/python
# encoding=utf8
# Copyright 2015 LeTV Inc. All Rights Reserved.

__author__ = 'zhaojincheng@letv.com'

import traceback
from scrapy import log
import json
import copy

from ..core.page_writer import PageWriterWithBuff



class LejianWriter(PageWriterWithBuff):
  def __init__(self, spider):
    super(LejianWriter, self).__init__(spider)
    self.set_name('LejianWriter')
    self.total_save_count = 0
    self.failed_save_count = 0
    self.total_update_count = 0
    self.failed_updata_count = 0
    self.retry_time_max = 10
    self.write_client = open('data.txt', 'wb')


  def status(self):
    return 'total_save:%s, total_update:%s, %s' % (self.total_save_count, self.total_update_count, super(LejianWriter, self).status())

  def writer(self, item):
    if not item:
      return
    #item['page'] = None
    #line = item.to_json_str()
    line = json.dumps(dict(item), ensure_ascii=False).encode('utf-8')
    self.write_client.write(line)
    self.write_client.write('\n')
