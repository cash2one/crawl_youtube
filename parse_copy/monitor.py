#!/usr/bin/python
# coding: utf-8

import sys
import os
import time
import json
import traceback
import urllib
import logging
import datetime
from logging.handlers import RotatingFileHandler

from python_library import utils


log_name = 'monitor.error'
_handler = RotatingFileHandler(log_name, mode='a', maxBytes=100*1024*1024, backupCount=2)
_handler.setFormatter(logging.Formatter('[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s'))
_logger = logging.getLogger(log_name)
_logger.addHandler(_handler)
_logger.setLevel(logging.DEBUG)

TEL_LIST = ['13426031534', '18515029185', '15330025605']
#TEL_LIST = ['13426031534']

def str2timestamp(time_str, format='%Y-%m-%d %H:%M:%S'):
  try:
    if not time_str:
      return 0
    _timetuple = time.strptime(time_str, format)
    _timestamp = time.mktime(_timetuple)
    return int(_timestamp)
  except:
    _logger.exception('str2timestamp failed, time_str: %s' % time_str)
    return 0

def get_lasttime():
  data = {}
  if not os.path.exists('.cache'):
    _logger.error('not exists .cahce .....')
    return 0
  if not os.listdir('.cache'):
    _logger.error('.cache not exist file .......')
    return 0
  file_list = [f for f in os.listdir('.cache') if not f.endswith('swp')]
  file_name = max(file_list)
  time_str = file_name.split('.')[-1]
  create_time = str2timestamp(time_str, format='%Y%m%d_%H%M')
  return create_time

def _send_message(message, tel='13426031534'):
  api = 'http://10.182.63.85:8799/warn_messages'
  params = {'m': message, 'p':tel}
  params = urllib.urlencode(params)
  res_data = urllib.urlopen("%s?%s" % (api, params))

def _monitor(delta_time=3600):
  now_time = int(time.time())
  last_time = get_lasttime()
  _logger.error('last_time: %s' % last_time)
  #print 'last_time:', last_time
  if now_time - last_time > delta_time:
    message = 'monitor: hadoop job failed!\n it need you!'
    for tel in TEL_LIST:
      _send_message(message, tel)
    _logger.error('monitor:hadoop job failed!')

def start_monitor(interval = 1800):
  try:
    utils.cycle_run(lambda: _monitor(), interval)
  except:
    ex = traceback.format_exc()
    _send_message(('monitor failed:\n%s' % ex))
    _logger.exception('monitor failed:\n%s' % ex)
  

if __name__ == '__main__':
  start_monitor()
