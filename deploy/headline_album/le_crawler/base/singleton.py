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
  @staticmethod
  def get_instance(*kargs, **kwargs):
    pass

  # inherited this function
  # add your code here

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



