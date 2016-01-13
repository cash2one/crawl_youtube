#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import logging
import commands
import urllib
import time
import sys
sys.path.append('../')

import hdfs_utils
import python_library.utils as utils


logging.basicConfig(format="[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
                    filename='auto_statistic.error', level=logging.DEBUG)

out_video_dir = '/user/search/short_video/out/video/'
out_user_dir = '/user/search/short_video/out/user_info/'



def get_input_paths():
  paths = ''
  cmd = 'hadoop fs -ls %s | tail -n 1' % out_video_dir
  _, output = hdfs_utils.call_cmd(cmd)
  output = output.strip()
  time_str = output.split(' ')[-1].split('/')[-1][:8]
  paths += ' -input ' + out_video_dir + time_str + '*'
  paths += ' -input ' + out_video_dir + str(int(time_str) - 1) + '*'
  #paths += ' -input ' + out_video_dir + str(int(time_str) - 2) + '*'

  cmd = 'hadoop fs -ls %s | tail -n 1' % out_user_dir
  _, output = hdfs_utils.call_cmd(cmd)
  output = output.strip()
  time_str = output.split(' ')[-1].split('/')[-1][:8]
  paths += ' -input ' + out_user_dir + time_str + '*'
  paths += ' -input ' + out_user_dir + str(int(time_str) - 1) + '*'
  #paths += ' -input ' + out_user_dir + str(int(time_str) - 2) + '*'
  logging.info('input paths are %s', paths)
  return paths


class StatisticWorker(object):

  def run(self):
    self.job_out_dir_ = '/user/search/short_video/statistic_job_tmp'
    hdfs_utils.rm_dir(self.job_out_dir_)
    input_paths = get_input_paths()
    reduce_amount = 10
    logging.info('out dir: %s', self.job_out_dir_)
    cmd = 'hadoop jar hadoop-streaming-2.6.0.jar ' \
          '-libjars custom.jar ' \
          '-archives hdfs://cluster/user/search/short_video/bin/mapred_parser.tar.gz#mapred_parser ' \
          '-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator ' \
          '-D mapreduce.job.reduces=%s ' \
          '-D mapreduce.job.name=youtube_statistic ' \
          '-D mapreduce.job.priority=HIGH ' \
          '-D mapreduce.output.fileoutputformat.compress=0 ' \
          '-D stream.num.map.output.key.fields=2 ' \
          '-D mapreduce.partition.keypartitioner.options=-k1,1 ' \
          '-D mapreduce.partition.keycomparator.options="-k1,2" ' \
          ' %s ' \
          '-output %s ' \
          '-mapper ./mapred_parser/user_statics/mapper.py ' \
          '-reducer ./mapred_parser/user_statics/reducer.py ' \
          '-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner ' \
          '-inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat ' \
          '-outputformat com.custom.MultipleTextOutputFormatByKey' % \
          (reduce_amount, input_paths, self.job_out_dir_)
    logging.info('start running statistic job...\nreduce job amount: [%s]\ncommand: %s', reduce_amount, cmd)
    status, output = commands.getstatusoutput(cmd)
    logging.info('Job %s, details:\n%s', 'succeeded' if status == 0 else 'failed', output)
    return status == 0



if __name__ == '__main__':
  try:
    worker = StatisticWorker()
    worker.run()
    #utils.cycle_run(worker.run, 60 * 60 * 12)
  except:
    logging.exception('failed run statistic.')

