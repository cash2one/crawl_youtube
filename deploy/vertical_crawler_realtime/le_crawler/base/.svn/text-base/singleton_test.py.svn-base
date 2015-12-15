#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

#base singleton class
from singleton import Singleton

class SingletonTest(Singleton):
  count_ = 0
  print 'test'
  def count(self):
    print 'before:%d' % self.count_
    SingletonTest.count_ += 1
    print 'after:%d' % self.count_
  def _init():
    print '--------------->'

class TestMain(object):
  def test(self):
    s1 = SingletonTest()
    s2 = SingletonTest()
    s3 = SingletonTest()
    s4 = SingletonTest()
    s5 = SingletonTest()
    s6 = SingletonTest()
    s1.count()
    s4.count()
    s3.count()
    s2.count()
    s5.count()
    s6.count()

if __name__ == '__main__':
  tests = TestMain()
  tests.test()



