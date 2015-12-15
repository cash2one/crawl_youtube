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
def extend_url(url_pattern, from_str, to_str, pattern_len = 0):
  """
  usage: http://www.a.com/(*).zip 0 100 4
  will get: 
  http://www.a.com/0000.zip
  http://www.a.com/0001.zip
  .
  .
  .
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
  for i in range(ifp, itp):
    if not char_gen:
      tmpstr = str(i).zfill(int(pattern_len))
    else:
      tmpstr = str(chr(i)).zfill(pattern_len)
    rets.append(url_pattern.replace('(*)', tmpstr))
  return (True, rets)

# line define as: http://a.b/(*0-100,4*)/list.html id
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
      if '(*' in line and '*)' in line:
        bi = line.index('(*')
        ei = line.index('*)')
        url_pa = line[:bi] + '(*)' + line[(ei + 2):]
        tmpstr = line[(bi + 2) : ei]
        pattern = tmpstr.split(',')
        ftl = pattern[0].split('-')
        urlexts = extend_url(url_pa, ftl[0], ftl[1], pattern[-1])
        if not urlexts[0]:
          raise Exception('Failed extend urls: %s' % line)
        returls += [ u for u in urlexts[1] ]
      else:
        returls.append(line)
  if random_sort:
    import random
    random.shuffle(returls)
  return returls

if __name__ == "__main__":
  url_p = "http://ent.ifeng.com/listpage/236/(*)/list.shtml"
  f = 1
  t = 330
  print extend_url(url_p, '0', '10', 3)
  url_p = "http://ent.ifeng.com/listpage/236/1/list.shtml"
  print extend_url(url_p, '0', '10', 3)
  url_p = "http://ent.ifeng.com/listpage/236/(*)/list.shtml"
  print extend_url(url_p, 'a', 'z')
  print load_lines_with_extend('/tmp/test.txt', True)

