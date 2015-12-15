#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com (Guo XiaoHe)'
"""
gen docid from base url(normalized)
simple say: using fringerprint(the hash module tranlate from c++ base lib)
"""
import letvbase

# importaint thrift only include int64 non unsigned type,
# so we convert uint64 to int64
def gen_docid(url):
  return letvbase.get_fingerprint_i64(url)
