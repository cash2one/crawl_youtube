#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import sys
# from statistic_mapper import category_mapping, domain_set

if __name__ == '__main__':
  counter = {}

  while 1:
    line = sys.stdin.readline()
    if not line:
      break
    data = line.split('\t')
    if len(data) != 2:
      sys.stderr.write('reporter:counter:reduce_error,reduece_input_not_2,1\n')
      continue
    counter[data[0]] = counter.get(data[0], 0) + int(data[1])

  for k, v in counter.iteritems():
    print 'status' + '\t' + k + '\t' + str(v)

