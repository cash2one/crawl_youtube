#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import os
import time
import base64
import commands
import threading
from datetime import datetime

from le_crawler.common.utils import *

import python_library.webpy as web
import python_library.utils as utils

log_name = 'crawler_monitor.error'
logging.basicConfig(format="[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
                    filename=log_name, level=logging.DEBUG)

fields = ['title', 'update_time', 'play_total', 'poster', 'history_count', 'content_timestamp', 'category', 'duration', 'create_time']

text = '''
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Crawler Monitor</title>
</head>
<body>
<h2>Crawler Monitor</h2>
<hr>
<br>
<table border = "1">
<tr><th>%s</th></tr>
%%s
</table>
</body>
</html>''' % '</th><th>'.join(fields)

class CacheManager:
  def __init__(self):
    self._cache = None
    self._filename = None
    threading.Thread(target=self._load_data, args=()).start()


  def _load_data(self):
    utils.cycle_run(self._load_data_internal, 60 * 10)


  def _load_data_internal(self):
    logging.debug('begin to load data.')
    cmd = 'hadoop fs -ls short_video/out/video'
    logging.debug('cmd: %s', cmd)
    filename = commands.getoutput(cmd).split('\n')[-1].split()[-1].split('/')[-1]
    logging.debug('get file %s', filename)

    if self._filename != filename:
      if self._filename and os.path.isfile(self._filename):
        logging.debug('remove file %s', self._filename)
        os.remove(self._filename)
      self._filename = filename

    if not os.path.isfile(filename):
      logging.debug('begin to dump file...')
      cmd = 'hadoop fs -text short_video/out/video/%s > %s' % (filename, filename)
      logging.debug('cmd: %s', cmd)
      commands.getoutput(cmd)
      logging.debug('end to dump file')
    else:
      if self._cache:
        logging.info('nothing changed, skip load.')
        return
      logging.info('file exists, skip dump.')
    
    cache = []
    logging.debug('loading file...')
    counter = 0; limit = 10000
    with open(filename) as f:
      for line in f:
        cache.append(str2mediavideo(base64.b64decode(line.split()[1])))
        counter += 1
        if counter >= limit:
          break
    logging.info('video total: %s', len(cache))
    # logging.debug('sorting...')
    # cache.sort(lambda x, y: y.play_total - x.play_total)
    # logging.debug('sort completed.')
    content = ''
    for obj in cache:
      line = '<tr><th>%s</th></tr>'
      values = []
      for k in fields:
        value = str(getattr(obj, k, ''))
        url_pattern = '<a href="%s" title="%s" target="_blank">%s</a>'
        if k == 'title':
          value = url_pattern % (getattr(obj, 'url', ''), value, value)
        elif k == 'poster':
          value = url_pattern % (value, 'poster', 'poster') if value else None
        elif k in ['create_time', 'update_time', 'content_timestamp'] and value and value != 'None':
          try:
            value = datetime.fromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
          except:
            pass
        elif k == 'history_count':
          value = str(len(obj.crawl_history.crawl_history) if obj.crawl_history and obj.crawl_history.crawl_history else 0)
        elif k== 'play_total':
          value = str(obj.crawl_history.crawl_history[0].play_count)
        values.append(value)
      if values:
        content += line % ('</th><th>'.join(values))
    self._cache = text % content
    logging.debug('end to load data.')


  def get(self):
    return self._cache


cache_manager = CacheManager()

urls = ('/crawler_monitor', 'Monitor')

web.config.debug = False
app = web.application(urls, globals())

class Monitor:
  def GET(self):
    s = cache_manager.get()
    if not s:
      return 'loading...'
    return s
    

if __name__ == '__main__':
  app.run()
