#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
setup Letv C++ base lib
"""

try:
  from setuptools import setup, Extension
except ImportError:
  from distutils.core import setup, Extension
extra_compile_args = ['-fPIC', '-Wall', '-O2', '-I"."']
setup(
  name='letvbase',
  version='1.0',
  maintainer='guoxiaohe',
  maintainer_email='guoxiaohe@letv.com',
  url='http://crawler.letv.cn',
  description='Python bindings for Letv base algorithm',
  ext_modules=[
    Extension('letvbase',
              sources=[
                'base/hash.cc',
                'base/string_piece.cc',
                'base/python_base_lib.cc',
              ],
              extra_compile_args=extra_compile_args
              )
  ]
)



