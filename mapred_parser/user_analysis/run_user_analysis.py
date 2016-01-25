#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import os
import sys
import time
import logging
import commands

sys.path.append('../')

import hdfs_utils


log_name = 'user_analysis.error'
logging.basicConfig(format="[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
                    filename=log_name, level=logging.DEBUG)


def run_job(input_path, out_path, mapper_path='./mapred_parser/user_analysis/mapper.py', reducer_path='./mapred_parser/user_analysis/reducer_test.py'):
  reduce_amount = 10
  cmd = 'hadoop jar hadoop-streaming-2.6.0.jar ' \
        '-libjars custom.jar ' \
        '-archives hdfs://cluster/user/search/short_video/bin/user_test/mapred_parser.tar.gz#mapred_parser ' \
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


if __name__ == '__main__':
  run_job('/user/search/short_video/full_user_info/out_user_20160124/*', 
          '/user/search/short_video/tmp/full_user_analysis/user_analysis_8',
          mapper_path='./mapred_parser/user_analysis/mapper_once.py'
          reducer_path='./mapred_parser/user_analysis/reducer_8.py')
  for i in range(7, 1, -1):
    input_path = '/user/search/short_video/tmp/full_user_analysis/user_analysis_%s/user_info/*' % (i + 1)
    out_path = '/user/search/short_video/tmp/full_user_analysis/user_analysis_%s' % i
    reducer_path = './mapred_parser/user_analysis/reducer_%s.py' % i
    run_job(input_path, out_path, reducer_path)

