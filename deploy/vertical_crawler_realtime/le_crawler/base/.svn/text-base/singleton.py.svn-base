#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

#base singleton class
import threading

class Singleton(object):
  _instance = None
  _instance_lock = threading.Lock()
  _common_lock = threading.Lock()
  __init_finished = False

  def __init__(self, *args, **kwargs):
    """
    disable Singleton's __init__
    """
    self.init_multi()
    self._common_lock.acquire()
    if self.__init_finished:
      self._common_lock.release()
      return
    self.__init_finished = True
    self.init_onece()
    self._common_lock.release()
    
  def __new__(class_, *args, **kwargs):
    class_._instance_lock.acquire()
    try:
      if not isinstance(class_._instance, class_):
        class_._instance = object.__new__(class_, *args, **kwargs)
    finally:
      class_._instance_lock.release()
      return class_._instance
  # inherited this function
  # add your code here
  def init_onece(self, *args, **kwargs):
    pass

  def init_multi(self, *args, **kwargs):
    pass

#class TestA(Singleton):
#  def __init__(self):
#    print 'int testA init'
#
#a = TestA()
#print a
#if __name__ == '__main__':
#  b = TestA()
#  print b
#  c = TestA()
#  print c
#  import time
#  def create_a():
#    count = 0
#    while count < 1000:
#      tmp = TestA()
#      print tmp
#      time.sleep(0.1)
#      count += 1
#  def create_b():
#    count = 0
#    import time
#    while count < 1000:
#      tmp = TestA()
#      print tmp
#      time.sleep(0.1)
#      count += 1
#  t1 = threading.Thread(target = create_a, args = ())
#  t2 = threading.Thread(target = create_b, args = ())
#  t1.start()
#  t2.start()
#
#



