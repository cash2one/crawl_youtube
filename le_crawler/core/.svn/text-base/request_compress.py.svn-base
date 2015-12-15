#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.

# remove some un-using data field, reduce redis mem cost
__author__ = 'guoxiaohe@letv.com'


class RequestDeCompress(object):

  REDUCE_REQUEST = False

  #TODO(xiaohe): make more common
  @staticmethod
  def reduce_request_dict(req_dict):
    if not RequestDeCompress.REDUCE_REQUEST:
      return req_dict
    ndict = {}
    if req_dict.has_key('url'):
      ndict['u'] = req_dict['url']
    if req_dict.has_key('callback'):
      ndict['c'] = req_dict['callback']
    if req_dict.has_key('method'):
      ndict['m'] = req_dict['method']
    if req_dict.has_key('meta'):
      tmpm = req_dict['meta']
      if tmpm.has_key('link_text'):
        tmpm.pop('link_text')
      ndict['me'] = tmpm
    if req_dict.has_key('_encoding'):
      ndict['e'] = req_dict['_encoding']
    if req_dict.has_key('dont_filter'):
      ndict['d'] = req_dict['dont_filter']
    ndict['v'] = 'v'
    return ndict

  @staticmethod
  def restore_request_dict(req_dict):
    if not req_dict.has_key('v'):
      return req_dict
    ndict = {}
    if req_dict.has_key('u'):
      ndict['url'] = req_dict['u']
    if req_dict.has_key('c'):
      ndict['callback'] = req_dict['c']
    if req_dict.has_key('m'):
      ndict['method'] = req_dict['m']
    if req_dict.has_key('me'):
      tmpm = req_dict['me']
      ndict['meta'] = tmpm
    if req_dict.has_key('e'):
      ndict['_encoding'] = req_dict['e']
    if req_dict.has_key('d'):
      ndict['dont_filter'] = req_dict['d']
    # fill nonusing word
    ndict['body'] = ''
    ndict['errback'] = None 
    ndict['headers'] = None
    ndict['cookies'] = None
    ndict['priority'] = 0
    return ndict

