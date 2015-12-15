#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.

import sys
import logging
import json
import subprocess
import time
from threading import current_thread

import utils
from xpather import Xpather
reload(sys)


def cmd_call(cmd):
  threadName = current_thread().getName()
  fdout = open('.'+threadName+'.out', 'w+')
  fderr = open('.'+threadName+'.err', 'w')
  #p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
  p = subprocess.Popen(cmd, stderr=fderr, stdout=fdout, shell=True)
  t_beginning = time.time()
  timeout = 30
  seconds_passed = 0
  while True:
    if p.poll() is not None:
      break
    seconds_passed = time.time() - t_beginning
    if timeout and seconds_passed > timeout:
      p.terminate()
      return -1, None
    time.sleep(0.1)
  fdout.flush()
  fdout.seek(0)
  result = fdout.read()
  return p.returncode, result

def download_with_phantomjs(url):
  import commands
  js_bin_path = './js_dep/letv_crawler_ptj'
  # ===== edit js_script_path to use different js script =====
  js_script_path = './js_dep/get_html.js'
  # ==========================================================
  #uagent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
  uagent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36'
  cmd = '%s --output-encoding=unicode --load-images=false --disk-cache=true %s \"%s\" \"%s\" '\
      % (js_bin_path, js_script_path, url, uagent)
  print 'cmd========', cmd
  max_times = 3
  for try_time in range(max_times):
    sta, result = cmd_call(cmd)
    if sta == 0:
      print 'finish download_with_phantomjs..............'
      return result
    else:
      print 'Download Page Failed(PJS):%s, with:%s' % (url, result)
  print 'Download Page Failed(PJS) for try maxtimes:%s, with:%s' % (url, result)
  return None

def main(argv):
  logging.getLogger().setLevel(10)
  xpather = Xpather()
  xpather.load_templates('./templates/')
  result = {}
  if len(argv) == 1:
    result = xpather.parse_from_url('http://www.youku.com/v_showlist/c86.html')
  else:
    # ===== to choose either downloading with js engine or not =====
    #html = utils.FetchHTML(argv[1])
    html = download_with_phantomjs(argv[1])
    # ==============================================================
    result = xpather.parse(argv[1], html)
  for k, v in result.items():
    print '%s %s length=%s' %(k, type(v), len(v))
    for vi in v:
      if isinstance(vi, dict):
        print json.dumps(vi, ensure_ascii=False).encode('utf-8')
      else:
        if isinstance(vi, unicode):
            vi = vi.encode('utf-8')
        print vi


if __name__ == '__main__':
  main(sys.argv)
