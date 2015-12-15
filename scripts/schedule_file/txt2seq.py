#!/usr/bin/python
#coding=utf-8
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'
"""
this class is top abstract logic file writer,
support multi writer create

"""

import os, sys
import time
from datetime import datetime
import logging
import traceback
from logging.handlers import RotatingFileHandler
from multiprocessing import Pool, current_process, Queue, Manager
from utils import call_cmd, cycle_run, send_message


from hadoop.io import Text, SequenceFile
import subprocess
from utils import call_cmd, cycle_run 


TEL_LIST = ['13426031534', '18515029185', '15330025605']


class TxtToSequenceFileWriter(object):
  def __init__(self, path, logger, metadict=None):
    self._path = path
    self._tmppostfix = 'seqtmp'
    self._postfix = 'seq'
    self._raw_key, self._raw_value = Text(), Text()
    self._item_count = 0
    tmpdict = metadict or {}
    tmpdict['name'] = 'SequenceFileWriter'
    tmpdict['ver'] = '0.1'
    from hadoop.io.SequenceFile import Metadata
    self._logger = logger

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

  def _rename(self):
    """
    release resource, move tmp file to final file
    """
    try:
      tmp_path = self._gen_tmp_path()
      file_path = self._gen_file_path()
      os.rename(tmp_path, file_path)
    except Exception:
      self._logger.exception('rename failed %s to %s' % (tmp_path, file_path))

  def add(self, key, value):
    self._raw_key.set(key)
    self._raw_value.set(value)
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


class TxtToSequenceFile(object):
  def __init__(self, in_dir, out_dir, max_lines, queue, lock, p_name):
    self._in_dir = in_dir
    self._out_dir = out_dir
    self._max_lines = max_lines
    self.file_fp_ = None
    self.current_file_name_ = ''
    self.total_items_ = 0
    self.exit_ = False
    self._init_dir()
    self._line_failed_count = 0
    self._file_input_queue = queue
    self._queue_lock = lock
    self._p_name = p_name
    self._init_log()

  def _init_log(self):
    log_name = "txt2seq_%s.error" % self._p_name
    self._handler = RotatingFileHandler(log_name, mode='a', maxBytes=100 * 1024 * 1024, backupCount=2)
    self._handler.setFormatter(logging.Formatter('[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s'))
    self._logger = logging.getLogger(log_name)
    self._logger.addHandler(self._handler)
    self._logger.setLevel(logging.DEBUG)

  def __del__(self):
    self._handler.close()
    self._logger.removeHandler(self._handler)

  def _init_dir(self):
    if not os.path.exists(self._out_dir):
      os.mkdir(self._out_dir)

  def gen_random_str(self):
    import random
    return str(random.randint(1, 1000000)).zfill(7)

  def gen_filestr(self):
    return os.path.join(self._out_dir, '%s_%d_%s' % (time.strftime('%Y%m%d_%H%M%S', time.localtime()),
      os.getpid(), self.gen_random_str()))

  def finalize(self):
    self.exit_ = True
    if self.file_fp_:
      self.file_fp_.close()

  def _prepare_writer(self):
    if self.file_fp_:
      self._dump_file()
    self.current_file_name_ = self.gen_filestr()
    self._logger.debug('start gen seqfile, filename:[%s]', self.current_file_name_)
    #print 'start gen seqfile, filename:[%s]', self.current_file_name_
    self.file_fp_ = TxtToSequenceFileWriter(self.current_file_name_,
        self._logger,
        {'thrift_compack': 'true',
          'max_lines': '%s' % self._max_lines,
          'writer': 'CrawlDocWriter'})

  def _dump_file(self):
    try:
      if not self.file_fp_:
        return False
      self.file_fp_.close()
      self.file_fp_ = None
      return True
    except Exception:
      self._logger.exception('failed dump_file ....')
      return False

  def _delete_txt_file(self, file_path):
    try:
      os.remove(file_path)
      return True
    except Exception:
      self._logger.exception('failed delete file: %s' % file_path)
      return False

  def _gen_file_name(self):
    file_name = None
    self._queue_lock.acquire()
    if not self._file_input_queue.empty():
      file_name = self._file_input_queue.get(timeout=1)
    self._queue_lock.release()
    return file_name

  def run(self):
    while 1:
      file_name = self._gen_file_name()
      if not file_name:
        break
      if os.path.isdir(file_name):
        continue
      file_path = os.path.join(self._in_dir, file_name)
      source_file = open(file_path, 'r')
      self._logger.debug('start put txt file to seqfile, filename:[%s]', file_path)
      for line in source_file:
        line = line.strip()
        if not line:
          continue
        line_list = line.split('\t')
        if len(line_list) != 2:
          print 'line:%s' % line
          self._line_failed_count += 1
          self._logger.info('error line: %s' % line)
          self._logger.info('line failed count: [%s]' % self._line_failed_count)
          continue
        key,value = line_list
        if not self.file_fp_:
          self._prepare_writer()
        self.file_fp_.add(key, value)
        self.total_items_ += 1
        if self.file_fp_.item_size() >= self._max_lines:
          self._dump_file()
      self._logger.debug('finish put txt file to seqfile, filename:[%s]', file_path)
      if self._delete_txt_file(file_path):
        self._logger.debug('success delete txt file local, filename:[%s]', file_path)
      else:
        self._logger.error('failed delete txt file local, filename:[%s]', file_path)
    self._dump_file()


def run_txt2seq(in_dir, out_dir, max_lines, q, lock, p_name):
  txt2seq = TxtToSequenceFile(in_dir, out_dir, max_lines, q, lock, p_name)
  txt2seq.run()


def run_convert(in_dir, out_dir, max_lines, process_size=8):
  while 1:
    manager = Manager()
    file_input_queue = manager.Queue(10000)
    lock = manager.Lock()
    file_list = os.listdir(in_dir)
    file_list = [file_name for file_name in file_list if file_name.endswith('.txt')]
    if not file_list:
      break
    for file_name in file_list:
      file_input_queue.put(file_name)
    pool = Pool(process_size)
    for i in range(process_size):
      pool.apply_async(run_txt2seq, args=(in_dir, out_dir, max_lines, file_input_queue, lock, 'p%s' % i))
    print 'waiting for all txttosequence to finish ...'
    pool.close()
    pool.join()
    print 'finish all txttosequence .....'


def start_convert(in_dir='./in', out_dir='./out', max_lines=5000, interval=30):
  try:
    cycle_run(lambda: run_convert(in_dir, out_dir, max_lines), interval)
  except Exception:
    print traceback.format_exc()
    send_message('txt2seq failed ...', TEL_LIST)

def main():
  in_dir = './in'
  out_dir = './out'
  start_convert(in_dir, out_dir, 1000)


if __name__ == '__main__':
  main()


