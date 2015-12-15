#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe
__author__ = 'guoxiaohe@letv.com'

import traceback
import logging

from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol
from thrift.protocol import TJSONProtocol
from thrift.transport import TTransport

SERIALIZE_TYPE_FAST = 1
SERIALIZE_TYPE_COMPACT = 2
SERIALIZE_TYPE_JSON = 3


def thrift_to_str(thrift_obj, ser_type=SERIALIZE_TYPE_FAST):
  if thrift_obj is None:
    return None
  try:
    thrift_obj.validate()
    trans = TTransport.TMemoryBuffer()
    if ser_type == SERIALIZE_TYPE_FAST:
      prot = TBinaryProtocol.TBinaryProtocol(trans)
    elif ser_type == SERIALIZE_TYPE_COMPACT:
      prot = TCompactProtocol.TCompactProtocol(trans)
    elif ser_type == SERIALIZE_TYPE_JSON:
      prot = TJSONProtocol.TSimpleJSONProtocol(trans)
    else:
      raise Exception('Unsupport thrift serialize type: %s' % (ser_type))
    thrift_obj.write(prot)
    values = trans.getvalue()
    if values:
      return values
  except:
    logging.exception('thrift to string failed, object:\n%s\n', thrift_obj)
  return None


def str_to_thrift(thrift_str, thrift_ob, ser_type=SERIALIZE_TYPE_FAST):
  if thrift_str is None or thrift_ob is None:
    return False
  try:
    trans = TTransport.TMemoryBuffer(thrift_str)
    if ser_type == SERIALIZE_TYPE_FAST:
      prot = TBinaryProtocol.TBinaryProtocol(trans)
    elif ser_type == SERIALIZE_TYPE_COMPACT:
      prot = TCompactProtocol.TCompactProtocol(trans)
    elif ser_type == SERIALIZE_TYPE_JSON:
      prot = TJSONProtocol.TSimpleJSONProtocol(trans)
    else:
      raise Exception('Unsupport thrift serialize type: %s' % (ser_type))
    thrift_ob.read(prot)
    thrift_ob.validate()
    return True
  except:
    print traceback.format_exc()
    return False
