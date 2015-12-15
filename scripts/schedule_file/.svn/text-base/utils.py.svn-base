# encoding: utf8

import os, sys
import time
from datetime import datetime
from hadoop.io import Text, SequenceFile
import subprocess
import urllib

def call_cmd(cmd, timeout=300):
  p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
  t_beginning = time.time()
  seconds_passed = 0
  while True:
    if p.poll() is not None:
      break
    seconds_passed = time.time() - t_beginning
    if timeout and seconds_passed > timeout:
      p.terminate()
      return -1, None
    time.sleep(0.1)
  return p.returncode, p.stdout.read()

def cycle_run(func, seconds=60, times=-1):
  # times = -1 -> infinite times
  assert seconds > 0 and times > -2
  if not times:
    return
  while 1:
    stamp = time.time()
    func()
    spare = seconds - (time.time() - stamp)
    if spare > 0:
      time.sleep(spare)
    if times == -1:
      continue
    times -= 1
    if not times:
      break

def send_message(message, tel='13426031534'):
  api = 'http://10.182.63.85:8799/warn_messages'
  params = {'m': message, 'p':tel}
  params = urllib.urlencode(params)
  res_data = urllib.urlopen("%s?%s" % (api, params))

