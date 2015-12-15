#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import logging
logging.basicConfig(format="[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
                    filename='auto_deploy_full.error', level=logging.DEBUG)

import os
import json
import time
import urllib
import commands
import traceback
from datetime import datetime
from datetime import timedelta

import hdfs_utils
import python_library.utils as utils


def send_message(alert_msg):
  return
  #for tel in ['13426031534', '18515029185', '15330025605', '18686863062']:
  for tel in ['13426031534']:
    api = 'http://10.182.63.85:8799/warn_messages?%s'
    urllib.urlopen(api % urllib.urlencode({'m': alert_msg, 'p': tel}))


in_dir = '/user/search/short_video/in/'
done_dir = '/user/search/short_video/done/'
merge_dir = '/user/search/short_video/out_tmp/'
in_tmp_dir = '/user/search/short_video/in_tmp/'
out_md5_dir = '/user/search/short_video/out_md5/'
out_final_dir = '/user/search/short_video/out/video/'
day_tmp_dir = '/user/search/short_video/day_tmp/'


class ExtractWorker(object):
  def __init__(self):
    self.last_unique_dir_ = self.get_last_unique_dir()
    self.last_day = self.last_unique_dir_.strip('/').split('_')[-1]
    self.merge_day = (datetime.strptime(self.last_day, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')
    logging.info('last_day: %s, merge_day: %s', self.last_day, self.merge_day)
    self.job_data_ = {}


  def get_last_unique_dir(self):
    cmd = 'hadoop fs -ls /user/search/short_video/full | grep out_video_'
    _, output = commands.getstatusoutput(cmd)
    output = hdfs_utils.strip_first_line(output)
    last_dir = output.split(' ')[-1] + '/'
    logging.info('last unique directory is %s', last_dir)
    return last_dir


  def run_job(self):
    cur_job_dir = self.cur_cycle_dir_ + 'parse_job/'
    logging.info('\n>> last unique directory is %s\n>> current job directory is %s',
            self.last_unique_dir_, cur_job_dir)
    if not hdfs_utils.count_file(day_tmp_dir):
      return False
    input_path = ' -input ' + day_tmp_dir + '*'
    input_file_count = hdfs_utils.count_file(self.last_unique_dir_ + 'parse_job/unique/')
    if input_file_count:
      input_path += ' -input ' + self.last_unique_dir_ + 'parse_job/unique/*' 
    input_file_count = hdfs_utils.count_file(self.last_unique_dir_ + 'user_merge_job/unique/')
    if input_file_count:
      input_path += ' -input ' + self.last_unique_dir_ + 'user_merge_job/unique/*'

    #add
    input_file_count = hdfs_utils.count_file('/user/search/short_video/old_tmp/')
    if input_file_count:
      input_path += ' -input /user/search/short_video/old_tmp/* ' 
    
    reduce_amount = 100
    cmd = 'hadoop jar hadoop-streaming-2.6.0.jar ' \
          '-libjars custom.jar ' \
          '-archives hdfs://cluster/user/search/short_video/bin/mapred_parser.tar.gz#mapred_parser ' \
          '-D mapred.reduce.tasks=%s ' \
          '-D mapred.job.name=short_video_full_parser ' \
          '-D mapred.job.priority=VERY_HIGH ' \
          ' %s ' \
          '-output %s ' \
          '-mapper ./mapred_parser/mapper.py ' \
          '-reducer ./mapred_parser/reducer.py ' \
          '-inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat ' \
          '-outputformat com.custom.MultipleSequenceFileOutputFormatByKey' % \
          (reduce_amount, input_path,  cur_job_dir)
    logging.info('start running parse job...\nreduce job amount: [%s]\ncommand: %s', reduce_amount, cmd)
    status, output = commands.getstatusoutput(cmd)
    logging.info('Job %s, details:\n%s', 'succeeded' if status == 0 else 'failed', output)
    if status:
      hdfs_utils.rm_dir(self.cur_cycle_dir_)
      hdfs_utils.rm_file(day_tmp_dir + '*')
      send_message('hadoop parse job failed, please take a look ASAP!')
      #utils.send_mail('crawler_parse_report@letv.com', 'gaoqiang@letv.com', 'Schedule Parser Failed', 'schedule parser failed, details: \n%s' % output)
      raise Exception('hadoop parse job of short video failed')
    """
    else:
      self.statistic(output)
    """
    return status == 0


  def merge_user(self):
    cur_job_dir = self.cur_cycle_dir_ + 'user_merge_job/'
    logging.info('\n>> current input directory is %s\n>> current job directory is %s',
            self.cur_cycle_dir_ + 'parse_job/user_merge/', cur_job_dir)
    input_file_count = hdfs_utils.count_file(self.cur_cycle_dir_ + 'parse_job/user_merge/')
    if not input_file_count:
      return True
    reduce_amount = input_file_count if input_file_count > 0 and input_file_count < 1000 else 1000
    reduce_amount = 100
    cmd = 'hadoop jar hadoop-streaming-2.6.0.jar ' \
          '-libjars custom.jar ' \
          '-archives hdfs://cluster/user/search/short_video/bin/mapred_parser.tar.gz#mapred_parser ' \
          '-D mapred.reduce.tasks=%s ' \
          '-D mapred.job.name=short_video_full_user_merger ' \
          '-D mapred.job.priority=VERY_HIGH ' \
          '-D mapreduce.reduce.memory.mb=8192 ' \
          '-input %s ' \
          '-output %s ' \
          '-mapper ./mapred_parser/user_merger/mapper.py ' \
          '-reducer ./mapred_parser/user_merger/reducer.py ' \
          '-inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat ' \
          '-outputformat com.custom.MultipleSequenceFileOutputFormatByKey' % \
          (reduce_amount, self.cur_cycle_dir_ + 'parse_job/user_merge/*', cur_job_dir)
    logging.info('start merging user...\nreduce job amount: [%s]\ncommand: %s', reduce_amount, cmd)
    status, output = commands.getstatusoutput(cmd)
    logging.info('Job %s, details:\n%s', 'succeeded' if status == 0 else 'failed', output)
    if status:  # job failed
      send_message('hadoop user merge of short video failed, please come back ASAP!')
      hdfs_utils.rm_dir(self.cur_cycle_dir_)
      hdfs_utils.rm_file(day_tmp_dir + '*')
      raise Exception('hadoop user merge of short video failed')
    return  status == 0


  def statistic(self, result):
    job_id = [x for x in result.split('\n') if 'Job complete:' in x][0].split()[-1]
    _, output = commands.getstatusoutput('mapred job -status %s' % job_id)
    logging.info('job status [%s]:\n%s', job_id, output)
    
    #self.job_data_ = {y.split('=')[0]: y.split('=')[1] for y in [x.strip() for x in output.split('\n') if '=' in x.strip()]}
    self.job_data_ = {}
    tmp_data = [x.strip() for x in output.split('\n') if '=' in x.strip()]
    for y in tmp_data:
      k, v = y.split('=')
      self.job_data_[k] = v
    self.job_data_['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.dump()
    logging.info('dump complete.')


  def prepare_input(self):
    logging.info('preparing input data...')
    today = time.strftime('%Y%m%d')
    if self.merge_day < today:
      logging.info('merge_day less today, merge_day: %s, today: %s', self.merge_day, today)
      hdfs_utils.cp('/user/search/short_video/out/video/' + self.merge_day + '*', day_tmp_dir)
    else:
      logging.info('merge_day not less today, merge_day: %s, today: %s', self.merge_day, today)
      return False
    if not hdfs_utils.count_file(day_tmp_dir):
      return False
    logging.debug('finished preparing input data.')

    logging.info('creating current job directory...')
    hdfs_utils.mkdir(self.cur_cycle_dir_)
    logging.info('current job directory is %s' % self.cur_cycle_dir_)
    return True


  def gen_output(self):
    logging.info('moving output data into final folder...')

    #add
    hdfs_utils.rm_file(day_tmp_dir + '*')
    hdfs_utils.rm_file('/user/search/short_video/old_tmp/*')
    
    self.last_unique_dir_ = self.cur_cycle_dir_
    self.last_day = self.last_unique_dir_.strip('/').split('_')[-1]
    self.merge_day = (datetime.strptime(self.last_day, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')
    return True


  def load(self):
    filename = '.cache.' + time.strftime('%Y-%m-%d_%H%M')
    if not os.path.isfile('.cache/' + filename):
      logging.error('load cache failed.')
      return {}
    with open('.cache/' + filename, 'r') as f:
      s = f.read()
    return json.loads(s) if s else {}


  def dump(self):
    out = json.dumps(self.job_data_, indent=4, sort_keys=True)
    logging.info('Job statistic:\n%s', out)
    if not os.path.isdir('.cache'):
      os.mkdir('.cache')
    with open('.cache/.cache.' + time.strftime('%Y%m%d_%H%M'), 'w') as f:
      f.write(out)


  def run(self):
    logging.info('starting new cycle.')
    self.cur_cycle_dir_ = '/user/search/short_video/full/out_video_%s/' % self.merge_day
    self.prepare_input() and self.run_job() and self.merge_user() and self.gen_output()
    logging.info('finished one cycle.')


if __name__ == '__main__':
  try:
    worker = ExtractWorker()
    """
    logging.info('begin to deploy...')
    status, output = commands.getstatusoutput('sh scripts_uploader.sh')
    logging.info(output)
    if status:
      logging.error('failed to deploy')
      exit(1)
    logging.info('deploy complete.')
    """
    utils.cycle_run(worker.run, 30 * 60)
  except:
    logging.exception('failed deploy hadoop job')
    send_message('hadoop parse job failed, please take a look ASAP!')
    #utils.send_mail('crawler_parse_report@letv.com', 'gaoqiang@letv.com', 'Schedule Parser Crash', 'schedule parser crash, details: \n%s' % traceback.format_exc())

