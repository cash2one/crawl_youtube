#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import os
"""
the original thinking is: give input url patten str
return the status and real replace url
(stats, [])
"""
def extend_url(url_pattern, from_str, to_str, pattern_len = 0, add_num_tail = True):
  """
  usage: http://www.a.com/(*).zip 0 100 4
  will get:
  http://www.a.com/0000.zip
  http://www.a.com/0001.zip
  ...
  http://www.a.com/0099.zip
  """
  if not url_pattern:
    return (False, [])
  if not '(*)' in url_pattern:
    return (True, [url_pattern])
  if not from_str or not to_str:
    return (False, [])
  ifp = 0
  itp = 0
  char_gen = False
  if from_str.isalpha() and to_str.isalpha():
    if len(from_str) != 1 or len(to_str) != 1:
      return (False, [])
    char_gen = True
    ifp = ord(from_str)
    itp = ord(to_str)
  else:
    ifp = int(from_str)
    itp = int(to_str)
  rets = []
  for i in range(ifp, itp + 1):
    if not char_gen:
      tmpstr = str(i).zfill(int(pattern_len))
    else:
      tmpstr = str(chr(i)).zfill(int(pattern_len))
    if add_num_tail:
      rets.append(url_pattern.replace('(*)', tmpstr) + '|%s' % i )
    else:
      rets.append(url_pattern.replace('(*)', tmpstr))
  return (True, rets)


def extend_url_with_time(url_pattern, time_format = '%Y%m%d', add_num_tail = True):
  import time
  tstr = time.strftime(time_format, time.localtime())
  return url_pattern.replace('(*today*)', tstr)

# parser the first pattern,
# return (new_url, begin_str, end_str, pattern_len)
def __replace_extend_str(url):
  bi = url.find('(*')
  ei = url.find('*)')
  if bi == -1 or ei == -1:
    return ()
  blstr = url[bi + 2 : ei]
  pattern = blstr.split(',')
  if len(pattern) != 2:
    return ()
  ftstr = pattern[0].split('-')
  if len(ftstr) != 2:
    return ()
  rbs = ftstr[0].strip()
  res = ftstr[1].strip()
  rls = pattern[1].strip()
  newurl = url[:bi] + '(*)' + url[ei + 2 :]
  return (newurl, rbs, res, rls)

# return all the extends urls
def __full_extend_url(url_pa, add_num_tail = False):
  rets = __replace_extend_str(url_pa)
  if not rets:
    return [url_pa]
  urlexts = extend_url(rets[0], rets[1], rets[2],rets[3], add_num_tail)
  returls = []
  if urlexts[0]:
    for u in urlexts[1]:
      returls.extend(__full_extend_url(u))
  else:
    raise Exception('fully extend url error')
  return returls

def extend_url_en(url, add_num_tail = False):
  return __full_extend_url(extend_url_with_time(url), add_num_tail)

# line define as: http://a.b/(*0-100,4*)/(*today*).html id
# line define as: http://a.b/(*0-100,4*)/list.html id
# line define as: http://a.b/(*0-100,4*)/(*A-Z,0*)list.html id
# line define as: http://a.b/(*0-100,4*)/(*A-Z,0*)/(*today*).html id
# http://ent.ifeng.com/listpage/236/list_(*1-100,0*)--/list.shtml IFENG_NEWS
# http://ent.ifeng.com/listpage/236/list_/list.shtml IFENG_NEWS
def load_lines_with_extend(fpath, random_sort = False):
  if not fpath or not os.path.exists(fpath):
    return []
  flist = []
  returls = []
  if os.path.isfile(fpath):
    flist.append(fpath)
  else:
    flist = [os.path.join(fpath, f) for f in os.listdir(fpath) ]
  from url_filter import UrlFilter
  for f in flist:
    tmplines = UrlFilter.load_lines(f)
    for line in tmplines:
      exus = extend_url_en(line)
      if not exus:
          raise Exception('Failed extend urls: %s' % line)
      else:
        returls.extend(exus)
  if random_sort:
    import random
    random.shuffle(returls)
  return returls

if __name__ == "__main__":
  # test
  test_url_pa1 = 'http://ifeng.com/(*1-3, 0*)/test.html'
  test_url_pa1_except = [
      'http://ifeng.com/1/test.html',
      'http://ifeng.com/2/test.html',
      'http://ifeng.com/3/test.html',
      ]
  test_ret = extend_url_en(test_url_pa1)
  assert cmp(test_ret, test_url_pa1_except) == 0, '%r, %r' % (test_ret,
      test_url_pa1_except)
  # test 2
  test_url_pa1 = 'http://ifeng.com/(*1-3, 0*)/test_(*1-2,0*).html'
  test_url_pa1_except = [
      'http://ifeng.com/1/test_1.html',
      'http://ifeng.com/1/test_2.html',
      'http://ifeng.com/2/test_1.html',
      'http://ifeng.com/2/test_2.html',
      'http://ifeng.com/3/test_1.html',
      'http://ifeng.com/3/test_2.html',
      ]
  test_ret = extend_url_en(test_url_pa1)
  assert cmp(test_ret, test_url_pa1_except) == 0, '%r, %r' % (test_ret,
      test_url_pa1_except)
  # test3 
  test_url_pa1 = 'http://ifeng.com/(*today*)/test_(*1-2,0*).html'
  import time
  tdstr = time.strftime('%Y%m%d', time.localtime())
  test_url_pa1_except = [
      'http://ifeng.com/%s/test_1.html' % (tdstr),
      'http://ifeng.com/%s/test_2.html' % (tdstr),
      ]
  test_ret = extend_url_en(test_url_pa1)
  assert cmp(test_ret, test_url_pa1_except) == 0, '%r, %r' % (test_ret,
      test_url_pa1_except)
  # test4 
  test_url_pa1 = 'http://ifeng.com/(*today*)/test.html'
  import time
  tdstr = time.strftime('%Y%m%d', time.localtime())
  test_url_pa1_except = [
      'http://ifeng.com/%s/test.html' % (tdstr),
      ]
  test_ret = extend_url_en(test_url_pa1)
  assert cmp(test_ret, test_url_pa1_except) == 0, '%r, %r' % (test_ret,
      test_url_pa1_except)
