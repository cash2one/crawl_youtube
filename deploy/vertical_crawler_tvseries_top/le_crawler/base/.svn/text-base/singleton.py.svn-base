#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

#base singleton class
"""
this is weak example template class
can not be inherited
"""
import threading

class Singleton(object):
  _instance = {}
  _instance_lock = threading.Lock()

  @staticmethod
  def get_instance(*kargs, **kwargs):
    Singleton._instance_lock.acquire()
    singleton_id = kwargs['singleton_id'] if 'singleton_id' \
        in kwargs else Singleton.__name__
    if singleton_id not in Singleton._instance:
      Singleton._instance[singleton_id] = Singleton(*kargs, **kwargs)
    Singleton._instance_lock.release()
    return Singleton._instance[singleton_id]
  def __init__(self, *kargs, **kwargs):
    print 'init Singleton class'


class TestSingleton(Singleton):
  def __init__(self, *kargs, **kwargs):
    print 'init inherited class'
  # inherited this function
  # add your code here

if __name__ == '__main__':
  s1 = Singleton.get_instance()
  s2 = Singleton.get_instance()
  st1 = TestSingleton.get_instance()
  st2 = TestSingleton.get_instance()
  print id(s1)
  print id(s2)
  print id(st2)
  print id(st1)
