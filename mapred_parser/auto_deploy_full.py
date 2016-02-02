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


class ExtractWorker(object):

  def get_last_unique_dir(self):
    cmd = 'hadoop fs -ls /user/search/short_video/full | grep out_video_'
    _, output = hdfs_utils.call_cmd(cmd)
    output = output.strip()
    last_dir = output.split(' ')[-1] + '/'
    logging.info('last unique directory is %s', last_dir)
    return last_dir


  def get_last_user_dir(self):
    cmd = 'hadoop fs -ls /user/search/short_video/full_user_info | grep out_user_'
    _, output = hdfs_utils.call_cmd(cmd)
    output = output.strip()
    last_dir = output.split(' ')[-1] + '/'
    logging.info('last unique directory is %s', last_dir)
    return last_dir


  def run_job(self):
    cur_job_dir = self.cur_cycle_dir_ + '/parse_job/'
    logging.info('\n>> last unique directory is %s\n>> current job directory is %s',
            self.last_unique_dir_, cur_job_dir)

    input_path = ' -input /user/search/short_video/out/video/' + self.merge_day + '*'
    input_path += ' -input /user/search/short_video/out/user_info/' + self.merge_day + '*'

    input_file_count = hdfs_utils.count_file(self.last_unique_dir_)
    if input_file_count:
      input_path += ' -input ' + self.last_unique_dir_ 
    
    input_file_count = hdfs_utils.count_file(self.last_user_dir_)
    if input_file_count:
      input_path += ' -input ' + self.last_user_dir_ 

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
      raise Exception('hadoop parse job of short video failed')
    return status == 0


  def prepare_input(self):
    logging.info('preparing input data...')
    today = time.strftime('%Y%m%d')
    self.last_unique_dir_ = self.get_last_unique_dir()
    self.last_user_dir_ = self.get_last_user_dir()
    self.last_day = self.last_unique_dir_.strip('/').split('_')[-1]
    self.merge_day = (datetime.strptime(self.last_day, '%Y%m%d') + timedelta(days=1)).strftime('%Y%m%d')
    self.cur_cycle_dir_ = '/user/search/short_video/tmp/full_job_%s' % self.merge_day
    if self.merge_day < today:
      logging.info('merge_day less today, merge_day: %s, today: %s', self.merge_day, today)
    else:
      logging.info('merge_day not less today, merge_day: %s, today: %s', self.merge_day, today)
      return False
    logging.debug('finished preparing input data.')

    logging.info('creating current job directory...')
    hdfs_utils.rm_dir(self.cur_cycle_dir_)
    hdfs_utils.mkdir(self.cur_cycle_dir_)
    logging.info('current job directory is %s' % self.cur_cycle_dir_)
    return True

  def run_user_job(self, 
                   input_path, 
                   out_path, 
                   mapper_path='./mapred_parser/user_analysis/mapper.py', 
                   reducer_path='./mapred_parser/user_analysis/reducer.py'):
    reduce_amount = 10
    cmd = 'hadoop jar hadoop-streaming-2.6.0.jar ' \
          '-libjars custom.jar ' \
          '-archives hdfs://cluster/user/search/short_video/bin/mapred_parser.tar.gz#mapred_parser ' \
          '-D mapreduce.job.reduces=%s ' \
          '-D mapreduce.job.name=short_video_user_analysis ' \
          '-D mapreduce.job.priority=HIGH ' \
          '-input %s ' \
          '-output %s ' \
          '-mapper %s ' \
          '-reducer %s ' \
          '-inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat ' \
          '-outputformat com.custom.MultipleSequenceFileOutputFormatByKey' % \
          (reduce_amount, input_path,  out_path, mapper_path, reducer_path)
    logging.info('start running analysis job...\nreduce job amount: [%s]\ncommand: %s', reduce_amount, cmd)
    status, output = commands.getstatusoutput(cmd)
    logging.info('Job %s, details:\n%s', 'succeeded' if status == 0 else 'failed', output)
    if status:
      #hdfs_utils.rm_dir(self.cur_cycle_dir_)
      raise Exception('hadoop user analysis job of short video failed')
    return status == 0


  def run_user_analysis(self):
    user_input = self.cur_cycle_dir_ + '/parse_job/user_info'
    user_outpath = '%s/user_analysis_job' % self.cur_cycle_dir_
    mapper_path='./mapred_parser/user_analysis/mapper.py'
    reducer_path='./mapred_parser/user_analysis/reducer.py'
    self.run_user_job(user_input, user_outpath, mapper_path, reducer_path)
    return True


  def gen_output(self):
    logging.info('moving output data into final folder...')

    out_final_dir = '/user/search/short_video/full/out_video_%s' % self.merge_day
    out_user_dir = '/user/search/short_video/full_user_info/out_user_%s' % self.merge_day
    hdfs_utils.mv(self.cur_cycle_dir_ + '/parse_job/unique', out_final_dir)
    hdfs_utils.mv(self.cur_cycle_dir_ + '/user_analysis_job/user_info', out_user_dir)
    return True


  def run(self):
    logging.info('starting new cycle.')
    self.prepare_input() and self.run_job() and self.run_user_analysis() and self.gen_output()
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

