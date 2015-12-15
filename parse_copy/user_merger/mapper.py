#!/usr/bin/python
# coding=utf-8

import sys

if __name__ == '__main__':
  while 1:
    line = sys.stdin.readline()
    if not line:
      break
    #file_name, user_url, url, data_type, data_base64 = line.strip().split('\t')
    #print user_url + '\t' + url + '\t' + data_type + '\t' + data_base64
    print line.strip()

