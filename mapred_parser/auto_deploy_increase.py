#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import logging
logging.basicConfig(format="[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
                    filename='auto_deploy_increase.error', level=logging.DEBUG)

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
in_tmp_dir = '/user/search/short_video/in_tmp/'
out_md5_dir = '/user/search/short_video/out_md5/'
out_video_dir = '/user/search/short_video/out/video/'
out_user_dir = '/user/search/short_video/out/user_info/'


class ExtractWorker(object):
  def __init__(self):
    self.job_data_ = {}


  def run_job(self):
    cur_job_dir = self.cur_cycle_dir_ + 'parse_job/'
    logging.info('\n>> current job directory is %s', cur_job_dir)
    input_path = ' -input ' + in_tmp_dir + '*'
    reduce_amount = 5
          #'-D mapreduce.task.io.sort.mb=1024 ' \
          #'-D mapreduce.map.memory.mb=2048 ' \
          #'-D mapreduce.reduce.memory.mb=1024 ' \
          #'-D mapreduce.tasktracker.reduce.tasks.maximum=6 ' \
          #'-D mapreduce.tasktracker.map.tasks.maximum=8 ' \
    cmd = 'hadoop jar hadoop-streaming-2.6.0.jar ' \
          '-libjars custom.jar ' \
          '-archives hdfs://cluster/user/search/short_video/bin/mapred_parser.tar.gz#mapred_parser ' \
          '-D mapred.reduce.tasks=%s ' \
          '-D mapred.job.name=short_video_parser ' \
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
      hdfs_utils.mv(in_tmp_dir + '*.seq', in_dir)
      send_message('hadoop parse job failed, please take a look ASAP!')
      #utils.send_mail('crawler_parse_report@letv.com', 'gaoqiang@letv.com', 'Schedule Parser Failed', 'schedule parser failed, details: \n%s' % output)
      raise Exception('hadoop parse job of short video failed')
    return status == 0


  def prepare_input(self):
    logging.info('preparing input data...')
    # hdfs_utils.ensure_dir(in_tmp_dir)
    files = hdfs_utils.list_files(in_dir + '*.seq')
    if not files:
      logging.info('no data found')
      return False
    if len(files) >= 500:
      # if amount of files greater than 2000, split into groups to run parse job
      timeflag = files[0].split('/')[-1][:11]
      len_total = len_tmp = hdfs_utils.count_file(in_tmp_dir)
      while len_total < 500:
        hdfs_utils.mv(in_dir + timeflag + '*.seq', in_tmp_dir)
        timeflag = (datetime.strptime(timeflag, '%Y%m%d_%H') + timedelta(hours=1)).strftime('%Y%m%d_%H')
        tmp_files = [f for f in files if f.split('/')[-1] < timeflag]
        len_total = len_tmp + len(tmp_files)
    else:
      hdfs_utils.mv(in_dir + '*.seq', in_tmp_dir)
    logging.debug('finished preparing input data.')
    logging.info('creating current job directory...')
    hdfs_utils.mkdir(self.cur_cycle_dir_)
    logging.info('current job directory is %s' % self.cur_cycle_dir_)
    return True


  def gen_output(self):
    logging.info('moving output data into final folder...')
    hdfs_utils.ensure_dir(done_dir)
    hdfs_utils.ensure_dir(out_md5_dir)
    hdfs_utils.mv(in_tmp_dir + '*.seq', done_dir)
    hdfs_utils.cp_or_mv_with_timestamp(self.cur_cycle_dir_ + 'parse_job/video/*', out_video_dir, 'mv')
    hdfs_utils.cp_or_mv_with_timestamp(self.cur_cycle_dir_ + 'parse_job/user_info/*', out_user_dir, 'mv')
    hdfs_utils.cp_or_mv_with_timestamp(self.cur_cycle_dir_ + 'parse_job/no_md5/*', out_md5_dir, 'mv')
    logging.info('finished moving.')
    return True


  def run(self):
    logging.info('starting new cycle.')
    self.cur_cycle_dir_ = '/user/search/short_video/job_tmp/out_video_%s/' % time.strftime('%Y%m%d_%H%M%S')
    self.prepare_input() and self.run_job() and self.merge_user() and self.merge_file() and self.gen_output()
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

