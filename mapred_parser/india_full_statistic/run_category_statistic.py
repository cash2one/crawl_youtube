#!/usr/bin/python
# coding=utf-8
# author=zhaojincheng@letv.com

import os
import sys
import time
import logging
import commands
import threading

sys.path.append('../')
import hdfs_utils


log_name = 'category_statistic.error'
logging.basicConfig(format="[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
                    filename=log_name, level=logging.DEBUG)

def run_job():
  input_path = '-input /user/search/short_video/full_user_info/out_user_20160202 -input /user/search/short_video/full/out_video_20160202'
  out_path = '/user/search/short_video/tmp/category_statistic '
  reduce_amount = 100
  cmd = 'hadoop jar hadoop-streaming-2.6.0.jar ' \
        '-libjars custom.jar ' \
        '-archives hdfs://cluster/user/search/short_video/bin/test/mapred_parser.tar.gz#mapred_parser ' \
        '-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator ' \
        '-D mapreduce.job.reduces=%s ' \
        '-D mapreduce.job.name=category_statistic ' \
        '-D mapreduce.job.priority=HIGH ' \
        '-D mapreduce.output.fileoutputformat.compress=0 ' \
        '-D stream.num.map.output.key.fields=3 ' \
        '-D mapreduce.partition.keypartitioner.options=-k1,1 ' \
        '-D mapreduce.partition.keycomparator.options="-k1,3" ' \
        ' %s ' \
        '-output %s ' \
        '-mapper ./mapred_parser/india_full_statistic/mapper.py ' \
        '-reducer ./mapred_parser/india_full_statistic/reducer_category.py ' \
        '-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner ' \
        '-inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat ' \
        '-outputformat com.custom.MultipleTextOutputFormatByKey' % \
        (reduce_amount, input_path, out_path)
  logging.info('start running statistic job...\nreduce job amount: [%s]\ncommand: %s', reduce_amount, cmd)
  status, output = commands.getstatusoutput(cmd)
  logging.info('Job %s, details:\n%s', 'succeeded' if status == 0 else 'failed', output)
  return status == 0

if __name__ == '__main__':
  run_job()
