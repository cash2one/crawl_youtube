#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'
"""
using for extract content page with some neccessay data_reciver_ip
generate by js
NOTE: this download middleware will slow your crawler progress for
js extract, so using it on your own judgment
"""
class JSPDownloadMiddleWare(object):
  def __init__(self, settings):
    self.enable_js = settings.get('ENABLE_JS_DOWNLOAD', False)
    js_request_url_pat = settings.getlist('JS_DOWNLOADER_URL_PATTERT', [])
    self.uagent = settings.get('USER_AGENT')
    import re
    self.js_url_reg = [re.compile(x, re.I | re.S) for x in js_request_url_pat]
    self.js_bin_path = settings.get('JS_DOWNLOAD_ENGIN_PATH',
    '../js_dep/letv_crawler_ptj')
    self.js_script_path = settings.get('JS_DOWNOAD_ENGIN_JS',
        '../js_dep/get_html.js')
    import os
    assert os.path.isfile(self.js_bin_path)
    assert os.path.isfile(self.js_script_path)

  def __using_js_downloader(self, url):
    if not self.enable_js:
      return False
    for r in self.js_url_reg:
      if r.search(url):
        return True
    return False
  @classmethod
  def from_crawler(cls, crawler):
    return cls(crawler.settings)
  def process_request(self, request, spider):
    if not self.__using_js_downloader(request.url):
      return None

  def __download_with_phantomjs(self, request):
    #TODO(xiaohe):make bind ip enable, make js bin run in memory,
    # instead of load every request from disk
    import commands
    cmd = '%s %s %s %s'\
        % (self.js_bin_path, self.js_script_path, request.url, self.uagent)
    sta, result = commands.getstatusoutput()

