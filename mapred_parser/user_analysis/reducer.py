#!/usr/bin/python
# coding=utf-8

import os
import sys
import time


if __name__ == '__main__':
  while 1:
    line = sys.stdin.readline()
    if not line:
      break
    print line.strip()

