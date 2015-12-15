#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import logging
logging.basicConfig(format="[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
                    filename='statistic.error', level=logging.DEBUG)
import commands
import json
import os
import urllib
import time

import hdfs_utils
import python_library.utils as utils


category_rank = ['news', 'sports', 'finance', 'ent', 'fun', 'tech', 'car', 'beauty']

domain_list = ['youku.com', 'tudou.com', 'iqiyi.com', 'qq.com', 'sohu.com', 
               'ifeng.com', 'wasu.cn', '56.com', 'fun.tv', 'cztv.com', '163.com',
               'hunantv.com', 'people.com.cn', 'sina.com.cn', 'hexun.com', 'pptv.com']

MAIL_TEXT = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<title>Crawler Monitor</title>
</head>
<body>
<h2>Crawler Statistics within 24h</h2>
<hr>
<br>
<table border = "1">
<tr><th></th><th>%s</th><th>Total</th></tr>
%%s
</table>
</body>
</html>'''

def send_message(alert_msg):
  for tel in ['13426031534', '18515029185', '15330025605', '18686863062']:
    api = 'http://10.182.63.85:8799/warn_messages?%s'
    urllib.urlopen(api % urllib.urlencode({'m': alert_msg, 'p': tel}))

def get_last_unique_dir():
  cmd = 'hadoop fs -ls short_video | grep out_video_ | tail -n 2 | head -n 1'
  _, output = commands.getstatusoutput(cmd)
  last_dir = output.split(' ')[-1] + '/'
  print 'last unique directory is %s' % last_dir
  logging.info('last unique directory is %s', last_dir)
  return last_dir

class StatisticWorker(object):
  def __init__(self):
    self.last_time_ = time.time()

  def run(self):
    self.statistic_out_dir_ = 'short_video/statistic_out'
    hdfs_utils.rm_dir(self.statistic_out_dir_)
    last_dir = get_last_unique_dir()
    logging.info('last unique dir is: %s', last_dir)
    input_path = last_dir + 'parse_job/unique/*'
    input_file_count = hdfs_utils.count_file(last_dir + 'user_merge_job/unique/')
    if input_file_count:
      input_path += ' -input ' + last_dir + 'user_merge_job/unique/*'
    reduce_amount = 1
    logging.info('out dir: %s', self.statistic_out_dir_)
    cmd = 'hadoop jar /letv/search/hadoop-1.1.2/contrib/streaming/hadoop-streaming-1.1.2.jar ' \
          '-libjars custom.jar ' \
          '-archives hdfs://webdm-cluster/user/search/short_video/bin/statistic/mapred_parser.tar.gz#mapred_parser ' \
          '-D mapred.reduce.tasks=%s ' \
          '-D mapred.job.name=short_video_statistic ' \
          '-D mapred.job.priority=VERY_HIGH ' \
          '-D mapred.output.compress=0 ' \
          '-input %s ' \
          '-output %s ' \
          '-mapper ./mapred_parser/statistic_mapper.py ' \
          '-reducer ./mapred_parser/statistic_reducer.py ' \
          '-inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat ' \
          '-outputformat com.custom.MultipleTextOutputFormatByKey' % \
          (reduce_amount, input_path, self.statistic_out_dir_)
    logging.info('start running parse job...\nreduce job amount: [%s]\ncommand: %s', reduce_amount, cmd)
    status, output = commands.getstatusoutput(cmd)
    logging.info('Job %s, details:\n%s', 'succeeded' if status == 0 else 'failed', output)
    if status:
      send_message('statistic job failed.')
    else:
      self.statistic(output)
    return status == 0

  def statistic(self, result):
    job_id = [x for x in result.split('\n') if 'Job complete:' in x][0].split()[-1]
    _, output = commands.getstatusoutput('mapred job -status %s' % job_id)
    logging.info('\n==>>>>> job status [%s]:\n%s', job_id, output)
    data = {y.split('=')[0]: y.split('=')[1] for y in
            [x.strip() for x in output.split('\n') if '=' in x.strip()]}
    data['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
    self.dump(data)
    logging.info('dump complete.')
    now_time = time.time()
    if now_time - self.last_time_ > 0:
      data = self._load_status_data()
      self._send_status_mail(data)
      self.last_time_ = now_time
      logging.info('sent mail, job id: %s', job_id)

  def dump(self, data):
    out = json.dumps(data, indent=4, sort_keys=True)
    logging.info('Job statistic:\n%s', out)
    if not os.path.isdir('.statistic'):
      os.mkdir('.statistic')
    with open('.statistic/' + time.strftime('%Y%m%d_%H%M%S'), 'w') as f:
      f.write(out)

  def _load_status_data(self):
    cmd = 'hadoop fs -get ' + self.statistic_out_dir_ + '/status/part-00000'
    status, output = commands.getstatusoutput(cmd)
    if status:
      logging.error('get hadoop status file failed')
      return None
    else:
      data = {}
      with open('part-00000', 'r') as f:
        for line in f:
          line_data = line.strip().split('\t')
          if len(line_data) != 2:
            logging.error('status line length not 2: %s' % line)
            continue
          data[line_data[0]] = line_data[1]
      os.remove('part-00000')
      return data

  def _send_status_mail(self, data):
    if not data:
      return None
    content = ''
    for category in category_rank:
      if not category in data:
        continue
      line = '<tr><th>%s</th><th>%%s</th></tr>' % category
      values = []
      for domain in domain_list:
        values.append(data.get(category + '_' + domain, ''))
      values.append(data.get(category, ''))
      content += line % ('</th><th>'.join(values))
    domains = list(x.split('.')[0] for x in domain_list)
    mail_text = MAIL_TEXT % '</th><th>'.join(domains)
    to_address = ['gaoqiang@letv.com', 'zhaojincheng@letv.com', 'fangjing1@letv.com', 'wangziqing@letv.com', 'xiezhi@letv.com', 
                  'hexingwei@letv.com', 'guantao@letv.com', 'liqiang1@letv.com', 'liqiang5@letv.com', 'liye@letv.com', 'kezhendong@letv.com',
                  'lvfeifei@letv.com', 'xiangkun@letv.com', 'sunzheng@letv.com', 'liushu1@letv.com', 'jiaowei@letv.com', 'tianrong@letv.com',
                  'taojianliang@letv.com', 'yinfei@letv.com', 'yaohongjiao@letv.com']
    utils.send_mail('crawler@letv.com', to_address, 'Crawler Statistics within 24h', mail_text % content, subtype='html', charset='utf-8')


if __name__ == '__main__':
  try:
    worker = StatisticWorker()
    utils.cycle_run(worker.run, 60 * 60)
  except:
    logging.exception('failed run statistic.')
    send_message('statistic job failed.')

