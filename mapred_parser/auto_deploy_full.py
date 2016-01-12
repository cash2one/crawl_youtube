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


out_final_dir = '/user/search/short_video/out/video/'
day_tmp_dir = '/user/search/short_video/day_tmp/'


class ExtractWorker(object):

  def get_last_unique_dir(self):
    cmd = 'hadoop fs -ls /user/search/short_video/full | grep out_video_'
    _, output = hdfs_utils.call_cmd(cmd)
    #output = hdfs_utils.strip_first_line(output)
    last_dir = output.split(' ')[-1] + '/'
    logging.info('last unique directory is %s', last_dir)
    return last_dir


  def get_last_user_dir(self):
    cmd = 'hadoop fs -ls /user/search/short_video/full_user_info | grep out_video_'
    _, output = call_cmd(cmd)
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

    input_file_count = hdfs_utils.count_file(self.last_unique_dir_)
    if input_file_count:
      input_path += ' -input ' + self.last_unique_dir_ 
    
    input_file_count = hdfs_utils.count_file(self.last_user_dir_)
    if input_file_count:
      input_path += ' -input ' + self.last_unique_dir_ 

    reduce_amount = 100
    cmd = 'hadoop jar hadoop-streaming-2.6.0.jar ' \
          '-libjars custom.jar ' \
          '-archives hdfs://cluster/user/search/short_video/bin/mapred_parser.tar.gz#mapred_parser ' \
          '-D mapred.reduce.tasks=%s ' \
          '-D mapred.job.name=short_video_full_parser ' \
          '-D mapred.job.priority=VERY_HIGH ' \
          '-D mapreduce.map.memory.mb=1024 ' \
          '-D mapreduce.reduce.memory.mb=1024 ' \
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
      raise Exception('hadoop parse job of short video failed')
    return status == 0


  def prepare_input(self):
    logging.info('preparing input data...')
    today = time.strftime('%Y%m%d')
    self.last_unique_dir_ = self.get_last_unique_dir()
    self.last_user_dir_ = self.get_last_user_dir()
    self.last_day = self.last_unique_dir_.strip('/').split('_')[-1]
    self.merge_day = (datetime.strptime(self.last_day, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')
    self.cur_cycle_dir_ = '/user/search/short_video/tmp/full_job_%s/' % self.merge_day
    if self.merge_day < today:
      logging.info('merge_day less today, merge_day: %s, today: %s', self.merge_day, today)
      hdfs_utils.cp('/user/search/short_video/out/video/' + self.merge_day + '*', day_tmp_dir)
      hdfs_utils.cp('/user/search/short_video/out/user_info/' + self.merge_day + '*', day_tmp_dir)
    else:
      logging.info('merge_day not less today, merge_day: %s, today: %s', self.merge_day, today)
      return False
    if not hdfs_utils.count_file(day_tmp_dir):
      return False
    logging.debug('finished preparing input data.')

    logging.info('creating current job directory...')
    hdfs_utils.rm_dir(self.cur_cycle_dir_)
    hdfs_utils.mkdir(self.cur_cycle_dir_)
    logging.info('current job directory is %s' % self.cur_cycle_dir_)
    return True


  def gen_output(self):
    logging.info('moving output data into final folder...')

    hdfs_utils.rm_file(day_tmp_dir + '*')
    out_final_dir = '/user/search/short_video/full/out_video_%s' % self.merge_day
    out_user_dir = '/user/search/short_video/full_user_info/out_user_%s' % self.merge_day
    hdfs_utils.mv(self.cur_cycle_dir_ + 'unique', out_final_dir)
    hdfs_utils.mv(self.cur_cycle_dir_ + 'user_info', out_user_dir)
    return True


  def run(self):
    logging.info('starting new cycle.')
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

