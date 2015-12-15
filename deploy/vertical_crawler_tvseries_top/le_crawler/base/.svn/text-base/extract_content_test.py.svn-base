#-*-coding:utf8-*-
#!/usr/bin/python
# encoding = utf8
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# this class inherited from singleton

from extract_content import ContentExtractor
import urllib2
def main(url):
  res = urllib2.urlopen(url)
  try:
    encoding = res.info().get('content-type', '').split(';')[1].split('=')[1].strip()
  except Exception:
    encoding = 'gb2312'
  html = res.read().decode(encoding, 'replace')
  extra = ContentExtractor()
  readcon = extra.analyse(html, encode_type = encoding)[0]
  print '==' * 20,  'pure text:', '==' * 20
  print readcon
  rest = extra.extract_with_paragraph(html, encode_type = encoding)
  print '==' * 20,  'paragraph:', '==' * 20
  for l in range(0, len(rest[-1])):
    print '%s: ' % l, rest[-1][l]
  print '==' * 20,  'imgs:', '==' * 20
  for l in range(0, len(rest[0])):
    print '%s: ' % l, rest[0][l]
  print '==' * 20,  'links:', '==' * 20
  for l in range(0, len(rest[1])):
    print '%s: ' % l, rest[1][l]

  print '==' * 20,  'title:', '==' * 20
  print '%s: ' % rest[-2]

if __name__ == '__main__':
  import sys
  if len(sys.argv) < 2:
    print 'Usage: input url'
    sys.exit(1)
  main(sys.argv[1])

