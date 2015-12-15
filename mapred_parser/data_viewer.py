#!/usr/bin/python
# coding=utf8

import re
import sys
import base64
from le_crawler.common.utils import str2mediavideo


def test_print(video):
    print '=' * 40
    for k, v in sorted(video.__dict__.iteritems()):
      if v:
        if k == 'crawl_history':
          v = len(v.crawl_history)
        elif k == 'play_trends':
          v = len(v.split(';'))
        print '%-20s ->' % k, v
    print '=' * 40


def main():
  count = 100
  while count:
    line = sys.stdin.readline()
    if not line:
      break
    line_data = line.strip().split('\t', 1)
    if len(line_data) != 2:
      sys.stderr.write('reporter:counter:map_error,map_input_not_2,1\n')
      continue
    url, data_base64 = line_data
    try:
      data_str = base64.b64decode(data_base64)
    except:
      sys.stderr.write('reporter:counter:map_error,map_decode_failed,1\n')
      continue
    test_print(str2mediavideo(data_str))
    continue


if __name__ == '__main__':
  main()

