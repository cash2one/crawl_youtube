#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com (Guo XiaoHe)'

import re
number_spell = re.compile(r'(\d+)')
tail_str = re.compile(r'([^\d]+$)')

def get_number(num_str, default_value = None):
  if not num_str: return default_value
  numls = number_spell.findall(num_str)
  if not numls: return default_value
  num_1 = ''.join(numls)
  num_1 = num_1.strip()
  destr = tail_str.search(num_str)
  if not destr:
    return int(num_1)
  destr = destr.groups()[0].strip()
  if destr == u'万':
    return int(num_1) * 10000
  elif destr == u'十万':
    return int(num_1) * 100000
  elif destr == u'百万':
    return int(num_1) * 1000000
  elif destr == u'千万':
    return int(num_1) * 10000000
  elif destr == u'亿':
    return int(num_1) * 100000000
  elif destr == u'十亿':
    return int(num_1) * 1000000000
  elif destr == u'百亿':
    return int(num_1) * 10000000000
  else:
    raise('Undefine:%s' % (destr))

if __name__ == '__main__':

  excep = 100
  test_str = format(excep, ',')
  assert excep == get_number(test_str)
  excep = 100000000
  test_str = format(excep, ',')
  assert excep == get_number(test_str)
  excep = 100000
  test_str = format(excep, ',')
  assert excep == get_number(test_str)
  excep = 1000000000
  test_str = format(excep, ',')
  assert excep == get_number(test_str)
  assert 1000 != get_number(test_str)
  assert 10000 == get_number(u'1万')
  assert 100000 == get_number(u'10万')
  assert 900000 == get_number(u'9十万')
  assert 3000000 == get_number(u'3百万')
  assert 50000000 == get_number(u'5千万')
