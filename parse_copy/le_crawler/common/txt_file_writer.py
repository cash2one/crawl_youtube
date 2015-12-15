#!/usr/bin/python
# coding=utf-8
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import base64
import threading
from file_base import FileBase

class TxtFileWriter(FileBase):
  def __init__(self, path):
    FileBase.__init__(self, path)
    self._tmppostfix = 'txttmp'
    self._postfix = 'txt'
    self._item_count = 0
    self.lock_ = threading.Lock()
    self._writer = open(self._gen_tmp_path(),'w')

  def _gen_tmp_path(self):
    return '%s.%s' % (self._path, self._tmppostfix)

  def _gen_file_path(self):
    return '%s.%s' % (self._path, self._postfix)

  def add(self, key, value, isbase64=True):
    #line = '%s\t%s\n' % (key,value)
    #self._writer.write('%s\t%s\n' % (key,value))
    with self.lock_:
      self._writer.write(key)
      self._writer.write('\t')
      if isbase64:
        self._writer.write(base64.b64encode(value))
      else:
        self._writer.write(value)
      self._writer.write('\n')
      self._item_count += 1

  def close(self):
    with self.lock_:
      self._writer.close()
      self._rename()

  def item_size(self):
    return self._item_count

  def size(self):
    return None

  def set_meta(self, key, value):
    pass

  def flush(self):
    with self.lock_:
      self._writer.flush()

