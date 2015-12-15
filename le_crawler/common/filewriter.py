#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'
"""
this class is top abstract logic file writer,
support multi writer create

"""

from hadoop.io import Text, SequenceFile
import base64


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
    import os

    try:
      os.rename(self._gen_tmp_path(), self._gen_file_path())
    except Exception, e:
      import traceback

      print 'final file failed: %s' % (e)
      print traceback.format_exc()

  def size(self):
    pass

  def close(self):
    pass

  def next(self):
    pass

  def add(self, key, value):
    pass


class SequenceFileWriter(FileBase):
  def __init__(self, path, metadict=None):
    FileBase.__init__(self, path)
    self._tmppostfix = 'seqtmp'
    self._postfix = 'seq'
    self._raw_key, self._raw_value = Text(), Text()
    self._item_count = 0
    tmpdict = metadict or {}
    tmpdict['name'] = 'SequenceFileWriter'
    tmpdict['ver'] = '0.1'
    from hadoop.io.SequenceFile import Metadata

    meta = Metadata()
    for k, v in tmpdict.items():
      meta.set(k, v)
    self._writer = SequenceFile.createWriter(self._gen_tmp_path(), Text, Text,
                                             metadata=meta,
                                             compression_type=SequenceFile.CompressionType.BLOCK)
    assert self._writer, "Failed Create Writer File handler"

  def _gen_tmp_path(self):
    return '%s.%s' % (self._path, self._tmppostfix)

  def _gen_file_path(self):
    return '%s.%s' % (self._path, self._postfix)

  def add(self, key, value):
    self._raw_key.set(key)
    self._raw_value.set(base64.b64encode(value))
    self._writer.append(self._raw_key, self._raw_value)
    self._item_count += 1

  def close(self):
    self._writer.close()
    self._rename()

  def item_size(self):
    return self._item_count

  def size(self):
    return self._writer.getLength()

  def set_meta(self, key, value):
    pass

  def flush(self):
    self._writer.sync()
