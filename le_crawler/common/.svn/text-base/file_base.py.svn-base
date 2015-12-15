#!/usr/bin/python
# coding=utf-8
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'
"""
this class is top abstract logic file writer,
support multi writer create

"""

import os
import traceback

class FileBase(object):
  def __init__(self, path):
    self._path = path

  def _gen_tmp_path(self):
    return '%s.%s' % (self._path, 'tmp')

  def _gen_file_path(self):
    return '%s.%s' % (self._path, '')

  def _rename(self):
    """
    release resource, move tmp file to final file
    """
    try:
      os.rename(self._gen_tmp_path(), self._gen_file_path())
    except:
      print 'final file failed: %s' % traceback.format_exc()

  def size(self):
    pass

  def close(self):
    pass

  def next(self):
    pass

  def add(self, key, value):
    pass

