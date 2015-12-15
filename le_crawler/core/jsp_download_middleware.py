#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import os
import re
import time
import subprocess
from threading import current_thread

from scrapy import log
from scrapy.http import HtmlResponse

from ..proto.crawl.ttypes import PageType

"""
using for extract content page with some necessary data_receiver_ip
generate by js
NOTE: this download middleware will slow your crawler progress for
js extract, so using it on your own judgment
"""

DEFAULT_JS_PATH = 'js_dep/get_html.js'

def cmd_call(cmd, timeout=15):
  threadName = current_thread().getName()
  fdout = open('.' + threadName + '.out', 'w+')
  fderr = open('.' + threadName + '.err', 'w+')
  #p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
  p = subprocess.Popen(cmd, stderr=fderr, stdout=fdout, shell=True)
  t_beginning = time.time()
  seconds_passed = 0
  while True:
    if p.poll() is not None:
      break
    seconds_passed = time.time() - t_beginning
    if timeout and seconds_passed > timeout:
      p.terminate()
      return -1, None, None
    time.sleep(0.1)
  fdout.flush()
  fdout.seek(0)
  result = fdout.read()
  fderr.flush()
  fderr.seek(0)
  err_result = fderr.read()
  return p.returncode, result, err_result

class JSPDownloadMiddleWare(object):
  def __init__(self, settings):
    self.enable_js = settings.get('ENABLE_JS_DOWNLOAD', False)
    self.js_request_url_pat = settings.getdict('JS_DOWNLOADER_URL_PATTERT', {})
    self.uagent = settings.get('USER_AGENT')
    self.js_bin_path = settings.get('JS_DOWNLOAD_ENGIN_PATH',
    'js_dep/letv_crawler_ptj')
    self.types_ = [PageType.HOME, PageType.CHANNEL, PageType.HUB]
    assert os.path.isfile(self.js_bin_path), self.js_bin_path


  def _using_js_downloader(self, url):
    if not self.enable_js:
      return None
    for pat, js_path in self.js_request_url_pat.iteritems():
      if re.search(pat, url):
        return js_path
    return None


  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings)


  def _get_js_path(self, page_type, js_list):
    path = None
    if isinstance(js_list, list):
      if page_type == PageType.ORDER_TYPE:
        page_type = PageType.HUB
      for i, type_ in enumerate(self.types_):
        if page_type == type_:
          path = js_list[i]
    else:
      path = js_list

    if path == 'N': # not using js
      return None
    elif path == 'D': # using default js
      return DEFAULT_JS_PATH
    return path


  def process_request(self, request, spider):
    js_path_list = self._using_js_downloader(request.url)
    if not js_path_list:
      return None

    crawl_doc = request.meta.get('crawl_doc')
    if not crawl_doc:
      spider.log('CrawlDoc in JSPDownloadMiddleWare is EMPTY!!!!', log.ERROR)
      return None
    js_path = self._get_js_path(crawl_doc.page_type, js_path_list)
    if js_path is None:
      return None
    htmlbody, redirected_url = self._download_with_phantomjs(request.url, crawl_doc, spider, js_path)

    if not htmlbody:
      spider.log('failed download page with js engine: %s' % request.url, log.ERROR)
      return None
    resp_url = request.url
    if redirected_url and redirected_url.startswith('http://'):
      resp_url = redirected_url
    return HtmlResponse(resp_url, body=htmlbody, encoding='utf8')


  def _download_with_phantomjs(self, url, crawl_doc, spider, js_path, timeout=15):
    #TODO:make bind ip enable, make js bin run in memory,
    # instead of load every request from disk
    cmd = '%s --output-encoding=unicode --load-images=false --disk-cache=true %s \"%s\" \"%s\" '\
        % (self.js_bin_path, js_path, url, self.uagent)
    max_times = 3
    if crawl_doc.page_type == PageType.HUB or crawl_doc.page_type == PageType.ORDER_TYPE:
      timeout = 180
    for try_time in range(max_times):
      sta, result, err_result = cmd_call(cmd, timeout)
      if sta == 0:
        regex_match = re.search('redirected url: (.*)', err_result)
        if regex_match:
          return result, regex_match.group(1)
        return result, None
      spider.log('Download Page Failed(PJS): %s, with: %s' % (url, result), log.ERROR)
    spider.log('Download Page Failed(PJS) for try maxtimes: %s, with: %s' % (url, result), log.ERROR)
    return None, None

