#!/usr/bin/env python
#-*-coding:utf-8-*-

__author__ = 'zhaojincheng'

import re
import sys
import string

reload(sys)
sys.setdefaultencoding('utf8')

ISO8601_PERIOD_REGEX = re.compile(
  r"P(?!\b)"
  r"((?P<days>[0-9]+)([,.][0-9]+)?D)?"
  r"((?P<separator>T)((?P<hours>[0-9]+)([,.][0-9]+)?H)?"
  r"((?P<minutes>[0-9]+)([,.][0-9]+)?M)?"
  r"((?P<seconds>[0-9]+)([,.][0-9]+)?S)?)?$")

re_list = [
  re.compile(ur"[^\d]*(?P<seconds>\d{1,})(秒)?$"),
  re.compile(ur"[^\d]*?((?P<hours>\d{1,2})(:|时|小时))?((?P<minutes>\d{1,2})(:|分|分钟))((?P<seconds>\d{1,2})(秒)?)?$"),
  ISO8601_PERIOD_REGEX]


def duration_format(duration_str, duration_encode='utf-8'):
  # duration_str = duration_str.lower()
  duration_str = duration_str.decode(duration_encode)
  duration_str = duration_str.strip()
  return duration_str

def duration2int(duration_str, duration_encode='utf-8'):
  try:
    ret = 0
    if not duration_str:
      return ret
    duration_str = duration_format(duration_str, duration_encode)
    parse_groups = {}
    for re_pattern in re_list:
      duration_dict_rematch = re_pattern.match(duration_str)
      if duration_dict_rematch:
        parse_groups = duration_dict_rematch.groupdict()
        break
    if parse_groups.get('seconds', None):
      ret += int(parse_groups['seconds'])
    if parse_groups.get('minutes', None):
      ret += int(parse_groups['minutes']) * 60
    if parse_groups.get('hours', None):
      ret += int(parse_groups['hours']) * 3600
    if parse_groups.get('days', None):
      ret += int(parse_groups['days']) * 86400
    return ret
  except:
    return 0

if __name__ == '__main__':
  duration_map = {
    '时长：1小时1分10秒':3670,
    '时长：10:51':651,
    '1时1分':3660,
    '01:57:01':7021,
    '2秒':2,
    '03:02':182,
    '3分10秒':190,
    '102':102,
    'PT1M53S': 113,
  }
  duration_str = '1小时1分'
  print duration2int(duration_str)
  for i in duration_map:
    print 'duration_str:%s, duration_int:%s' % (i, duration2int(i))
    assert duration_map[i] == duration2int(i)
  print 'duration_parser finish........'
