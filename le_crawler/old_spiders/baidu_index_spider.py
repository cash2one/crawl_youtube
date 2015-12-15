#!/usr/bin/python
# -*- encoding: utf-8 -*-
# Copyright 2015 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

''' short way for scrapy baidu index '''

import urllib2
import urllib
import cookielib

cj = cookielib.CookieJar()
cookies = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookies)
urllib2.install_opener(opener)

request_url = 'http://www.datadriver.info/scrapdata/'
ua = "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0"
from_d = "20110101"
to_d = "20150310"
email = "guest@datadriver.info"
pwd = "demo"
headers = {
    'Host' : 'www.datadriver.info',
    'User-Agent' : ua, 
    'Accept' :  'application/json, text/javascript, */*; q=0.01',
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip, deflate',
    'Content-Type' :  'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With' :  'XMLHttpRequest',
    'Referer' : 'http://www.datadriver.info/scrapdata/',
    'Connection' : 'keep-alive',
    'Pragma' : ' no-cache',
    }
def _open_url():
  response = urllib2.urlopen(url = request_url)
  lines = response.info()
  allines = lines.get('set-cookie').split(';')
  for i in allines:
    if 'csrftoken' in i:
      kv = i.split('=')
      return kv[1]


  #print response.read()
  print cj

def _build_task_request(query, from_d, to_data, ckie, path = 'startscrap/',
    extrac_data = {}):
  data = {
      'csrfmiddlewaretoken' : ckie,
      'req-url' : request_url,
      'your_email' : 'guest@datadriver.info',
      'your_pw' : 'demo',
      'param_01' : 'BID',
      'param_02' : query,
      'param_03' : from_d,
      'param_04' : to_d,
      'param_05' : '0',
      'param_01' : 'BID',
      }
  data.update(extrac_data)
  request = urllib2.Request(url = '%s%s' % (request_url, path), headers = headers,
    data = urllib.urlencode(data))
  return request

def _send_request(query, ckie):
  import time
  to_date = time.strftime("%Y%m%d", time.localtime())
  request = _build_task_request(query,
      from_d, to_date, ckie = ckie, path = 'startscrap/')
  response = opener.open(request)
  print response.info()
  rspjsonstr = response.read().strip()
  import json
  sta = json.loads(rspjsonstr)
  if sta.get('status', '') != "Ready":
    print "Failed get query:", query
    return None
  taskid = sta.get('task_id')
  gen_time = sta.get('gen_time')
# wait for taskid
  while True:
    query_r = _build_task_request(query, from_d, to_date,
        ckie = ckie, path = 'updatescrap/', extrac_data = {'task_id' : taskid,
          'gen_time' : gen_time})
    response = opener.open(query_r)
    jstr = response.read().strip()
    jobs = json.loads(jstr)
    if jobs.get('status', '') != 'SUCCESS':
      print jobs
      time.sleep(2)
      continue
    print 'result status:', jobs
    break

def main():
  ck = _open_url()
  _send_request('google.com', ckie = ck)

if __name__ == '__main__':
  main()
