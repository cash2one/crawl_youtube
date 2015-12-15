#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import gzip
import StringIO

def str_unzip(buf):
  f = gzip.GzipFile(fileobj = StringIO.StringIO(buf), mode = 'rb')
  html = f.read()
  f.close()
  return html

def str_gzip(content):
  buf = StringIO.StringIO()
  f = gzip.GzipFile(mode = 'wb', fileobj = buf)
  f.write(content)
  f.close()
  return buf.getvalue()


