#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import sys

if __name__ == '__main__':
  while 1:
    line = sys.stdin.readline()
    if not line:
      break
    #datas = line.strip().split('\t')
    #if len(datas) == 3:
    #  line = datas[0] + '\t' + datas[2]
    print line.strip()

