#!/usr/bin/python
# coding=utf8
# author=gaoqiang@letv.com

import commands

def get_job_detail(job_dir, job_name):
  data = commands.getoutput('hadoop fs -ls %s/_logs/history/*.xml' % job_dir)
  job_id = data[data.rfind('job'):data.find('_conf')]
  if job_id.endswith('director'):
    job_id = None
  job_tracker = 'http://10.140.60.180:50030/jobdetails.jsp?jobid=%s'
  print '-' * 100
  print '\n====>>>', job_name
  print 'job id: %s\njob tracker: %s' % (job_id, job_tracker % job_id)



if __name__ == '__main__':
  job_dir = commands.getoutput('hadoop fs -ls short_video | grep out_video_').split(' ')[-1]
  get_job_detail(job_dir + '/parse_job', 'parse_job')
  get_job_detail(job_dir + '/user_merge_job', 'user_merge_job')
  get_job_detail('short_video/out_tmp', 'file_merge_job')
  get_job_detail('short_video/statistic_out', 'statistic_job')



# shell:
# jobid=`hadoop fs -ls short_video/out_video/_logs/history/*.xml`
# echo ${jobid:107:23}
# echo 'http://10.140.60.180:50030/jobdetails.jsp?jobid='${jobid:107:23}

