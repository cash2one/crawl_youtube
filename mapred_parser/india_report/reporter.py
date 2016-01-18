#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import os
import sys
import time
import logging
import commands
import threading

sys.path.append('../')
import hdfs_utils
import python_library.webpy as web
import python_library.utils as utils
import hdfs_utils

log_name = 'india_ranking.error'
logging.basicConfig(format="[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
                    filename=log_name, level=logging.DEBUG)

out_video_dir = '/user/search/short_video/out/video/'
out_user_dir = '/user/search/short_video/out/user_info/'

HTML_TEXT = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>India Ranking</title>
</head>
<body>
<h2>India Ranking</h2>
<h3>last updated: %s</h3>
<hr>
<br>
<table border = "1">
<tr><th></th><th>%s</th></tr>
%%s
</table>
</body>
</html>'''

def get_input_paths():
  paths = ''
  cmd = 'hadoop fs -ls %s | tail -n 1' % out_video_dir
  _, output = hdfs_utils.call_cmd(cmd)
  output = output.strip()
  time_str = output.split(' ')[-1].split('/')[-1][:8]
  paths += ' -input ' + out_video_dir + time_str + '*'
  paths += ' -input ' + out_video_dir + str(int(time_str) - 1) + '*'
  paths += ' -input ' + out_video_dir + str(int(time_str) - 2) + '*'
  #paths += ' -input ' + out_video_dir + str(int(time_str) - 3) + '*'

  cmd = 'hadoop fs -ls %s | tail -n 1' % out_user_dir
  _, output = hdfs_utils.call_cmd(cmd)
  output = output.strip()
  time_str = output.split(' ')[-1].split('/')[-1][:8]
  paths += ' -input ' + out_user_dir + time_str + '*'
  paths += ' -input ' + out_user_dir + str(int(time_str) - 1) + '*'
  paths += ' -input ' + out_user_dir + str(int(time_str) - 2) + '*'
  #paths += ' -input ' + out_user_dir + str(int(time_str) - 3) + '*'
  logging.info('input paths are %s', paths)
  return paths

class CacheManager:
  def __init__(self):
    logging.info('cache_manager init ...')
    self._cache = None
    self.job_out_dir_ = '/user/search/short_video/india_job_tmp'
    threading.Thread(target=self._load_data, args=()).start()


  def _load_data(self):
    logging.info('load data ...')
    utils.cycle_run(self._load_data_internal, 12 * 60 * 60)


  def run_job(self):
    hdfs_utils.rm_dir(self.job_out_dir_)
    input_paths = get_input_paths()
    reduce_amount = 1
    logging.info('out dir: %s', self.job_out_dir_)
    cmd = 'hadoop jar hadoop-streaming-2.6.0.jar ' \
          '-libjars custom.jar ' \
          '-archives hdfs://cluster/user/search/short_video/bin/mapred_parser.tar.gz#mapred_parser ' \
          '-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator ' \
          '-D mapreduce.job.reduces=%s ' \
          '-D mapreduce.job.name=youtube_statistic ' \
          '-D mapreduce.job.priority=HIGH ' \
          '-D mapreduce.output.fileoutputformat.compress=0 ' \
          '-D stream.num.map.output.key.fields=3 ' \
          '-D mapreduce.partition.keypartitioner.options=-k1,1 ' \
          '-D mapreduce.partition.keycomparator.options="-k1,3" ' \
          ' %s ' \
          '-output %s ' \
          '-mapper ./mapred_parser/india_report/mapper.py ' \
          '-reducer ./mapred_parser/india_report/reducer.py ' \
          '-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner ' \
          '-inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat ' \
          '-outputformat com.custom.MultipleTextOutputFormatByKey' % \
          (reduce_amount, input_paths, self.job_out_dir_)
    logging.info('start running statistic job...\nreduce job amount: [%s]\ncommand: %s', reduce_amount, cmd)
    status, output = commands.getstatusoutput(cmd)
    logging.info('Job %s, details:\n%s', 'succeeded' if status == 0 else 'failed', output)
    return status == 0


  def _load_data_internal(self):
    logging.info('load data internal ...')
    self.run_job()
    logging.info('finish run job ...')
    try:
      filename = 'part-00000'
      if os.path.isfile(filename):
        os.remove(filename)
      cmd = 'hadoop fs -get %s/india_video/%s' % (self.job_out_dir_, filename)
      logging.info('cmd: %s', cmd)
      commands.getoutput(cmd)
      logging.info('end to dump file')
      
      ranking_list_dict = {}
      last_category = ''
      logging.info('loading file...')
      counter = -1
      with open(filename) as f:
        for line in f:
          line_data = line.strip().split('\t')
          if len(line_data) != 6:
            logging.error('not len of line_data 6, line_data: %s', line_data)
          category, play_total, url, title, crawl_time, content_timestamp = line_data
          crawl_interval = int(crawl_time) - int(content_timestamp)
          if play_total == 'None':
            play_total = 0
          play_per_sec = float(play_total) / crawl_interval
          value = (url, title, play_total, play_per_sec)
          ranking_list_dict.setdefault(category, []).append(value)
      for category, ranking_list in ranking_list_dict.items():
        ranking_list_dict[category] = sorted(ranking_list, cmp=lambda x, y: cmp(y[1], x[1]))

      text = HTML_TEXT % (time.strftime('%Y-%m-%d %H:%M:%S'), '</th><th>'.join([ category for category, ranklist in ranking_list_dict.items() ]))
      content = ''
      for ranking_index in range(0, 100):
        line = '<tr><th>%s</th><th>%%s</th></tr>' % ranking_index
        values = []
        for category, item in ranking_list_dict.items():
          if ranking_index >= len(item):
            continue
          value = item[ranking_index]
          url_pattern = '<a href="%s" title="%s" target="_blank">%s</a><br>played: %s' % (value[0], value[1], value[1], value[2])
          values.append(url_pattern)
        if values:
          content += line % ('</th><th>'.join(values))
      self._cache = text % content
      logging.debug('end to load data.')
    except:
      logging.exception('failed to load data')


  def get(self):
    return self._cache



urls = ('/india_ranking', 'Monitor')

web.config.debug = True
app = web.application(urls, globals())
cache_manager = CacheManager()

class Monitor:
  def GET(self):
    s = cache_manager.get()
    if not s:
      return 'loading...'
    return s
    

if __name__ == '__main__':
  app.run()
