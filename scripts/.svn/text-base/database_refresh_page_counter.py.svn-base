#!/usr/bin/python
# coding=utf-8
# Copyright 2015 LeTV Inc. All Rights Reserved.
# Author=gaoqiang@letv.com

import os
import sys

import leveldb

if __name__ == '__main__':
  path = sys.argv[1]
  print path
  for dir_name in os.listdir(path):
    db = leveldb.LevelDB(os.path.join(path, dir_name))
    count = 0
    for kv in db.RangeIter():
      if kv[0].startswith('000002'):
        count += 1
      else:
        break
    print '%-20s: %s' % (dir_name, count)

