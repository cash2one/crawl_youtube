#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# this class inherited from singleton

import threading
import hashlib

# simple class using for file monitor, if the file state is changed,
# a callback will be called
class FileMonitor(object):
  def __init__(self):
    self._monitor_files = None
    self._file_chg_cb = set()
    self._file_md5 = None
    self._mf_cb_dict = {}
    self._file_stats = {}

  @property
  def file_stats_dict(self):
    return self._file_stats

  @property
  def callback_dict(self):
    return self._mf_cb_dict

  @property
  def monitor_file(self):
    return self._monitor_files

  def register_callback(self, filep, callback):
    import os

    if not os.path.isfile(filep):
      print '%s is not file' % filep
      return False
    if not callable(callback):
      print '%s is not callable' % callback
      return False
    if not self._mf_cb_dict.has_key(filep):
      self._mf_cb_dict[filep] = set()
    self._mf_cb_dict[filep].add(callback)

  @staticmethod
  def str_md5(inputstr):
    return hashlib.md5(inputstr).hexdigest()

  @staticmethod
  def md5_checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
      data = fh.read(8192)
      if not data:
        break
      m.update(data)
    fh.close()
    return m.hexdigest()


class FileMonitorBlock(FileMonitor, threading.Thread):
  def __init__(self, monitor_inv=180):
    super(FileMonitorBlock, self).__init__()
    threading.Thread.__init__(self)
    self.__exit = False
    self.__monitor_invr = monitor_inv

  def quit(self):
    self.__exit = True

  def __is_file_changes(self, filep):
    import os, copy

    nst = copy.copy(os.stat(filep))
    prest = None
    if self.file_stats_dict.has_key(filep):
      prest = self.file_stats_dict[filep]
    if nst != prest:
      self.file_stats_dict[filep] = nst
      return True
    return False

  def run(self):
    import time

    timecount = self.__monitor_invr
    print 'start monitor...'
    first_time = True
    while first_time or not self.__exit:
      if timecount >= self.__monitor_invr:
        timecount = 0
        for (f, c) in self.callback_dict.items():
          if self.__is_file_changes(f):
            for cb in c:
              cb()
      first_time = False
      timecount += 1
      time.sleep(1)  # 1min
    print 'end monitor'

  def start_monitor(self):
    self.start()


class FileMonitorNonBlock(FileMonitor):
  pass

# test
if __name__ == '__main__':
  import time

  ftmp = '/tmp/file_monitor.tst'
  fp = open(ftmp, 'w')
  fp.write('')
  fm = FileMonitorBlock(1)

  def hello():
    print 'file changes'

  fm.register_callback(ftmp, hello)
  fm.start_monitor()
  time.sleep(4)
  fp.write('hello wold1')
  fp.flush()
  time.sleep(4)
  fp.write('hello wold2')
  fp.flush()
  time.sleep(4)
  fm.quit()
