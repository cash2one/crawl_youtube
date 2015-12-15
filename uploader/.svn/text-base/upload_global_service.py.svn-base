#!/usr/bin/env python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import commands
import time
import os
from threading import Thread

from base.logutil import Log


"""
this module is using to upload all crawler server's data to
hdfs, that is to say it's a center scheduler
"""
class UploaderService(Thread):
  def __init__(self, cfpath = '../conf/config.cfg'):
    Thread.__init__(self)
    self.__parse_config(cfpath)
    self._log = Log('upload_log', self._log_path)
    self._log.log.info('Got ip: %s' % self._ips)
    self._exit = False

  def __parse_config(self, cf_path):
    import ConfigParser
    cf = ConfigParser.ConfigParser()
    cf.read(cf_path)
    # global para
    self._hdfs_dir = cf.get("global", "hdfs_dir")
    self._hdfs_subdir = cf.get("global", "hdfs_subdir")
    self._batch_num = cf.getint("global", "batch_num")
    self._max_ideal_times = cf.getint("global", "max_ideal_times")
    self._hadoop_bin = cf.get("global", "hadoop_bin")
    self._log_path = cf.get("global", "log_path")
    self._check_interval = cf.getint('global', 'check_interval')
    # crawler para
    self._crawler_data_dir = cf.get("crawler", "data_dir")
    self._crawler_data_backup_dir = cf.get("crawler", "backup_dir")
    self._crawler_upload_bin = cf.get("crawler", "upload_bin")
    ipstr = cf.get("crawler", "ips")
    self._ips = [ ip.strip() for ip in str.split(ipstr, ',') if ip and ip != '']
    #self._ips = filter(lambda ip : ip != '' and ip is not None, ips)
    self._upload_bin = cf.get("crawler", "upload_bin")
    # local para
    self._last_update_time = int(time.time())

  # return files dict if the file count more than the dest
  # return {ip:[f,f1, f3]}
  def _prepare_remote_files(self):
    files = {}
    file_count = 0
    for ip in self._ips:
      cmd = "ssh search@%s ls %s" % (ip, self._crawler_data_dir)
      status, result = commands.getstatusoutput(cmd)
      if status != 0:
        self._log.log.info('Failed exe:%s with %s, %s' % (cmd, status, result))
        continue
      for f in str.split(result, '\n'):
        if f.endswith('tmp') or f == '' or f is None:
          continue
        files.setdefault(ip, []).append(f)
        file_count += 1
    now_times = int(time.time())
    if file_count == 0:
      return None
    elif file_count >= self._batch_num:
      return files
    elif self._max_ideal_times > 0 and self._max_ideal_times <= (now_times - self._last_update_time):
      return files
    self._log.log.info('Not enough files to uploading[%s < %s]' % (file_count, self._batch_num))
    return None

  def _hdfs_exist(self, dest_path):
    if not dest_path:
      return False
    cmd = '%s fs -ls %s' % (self._hadoop_bin, dest_path)
    status, result = commands.getstatusoutput(cmd)
    if status != 0 or 'No such file or directory' in result:
      return False
    return True

  def _hdfs_mkdir(self, dest_dir):
    if not dest_dir:
      return False
    cmd = '%s fs -mkdir %s' % (self._hadoop_bin, dest_dir)
    status, result = commands.getstatusoutput(cmd)
    if status != 0:
      self._log.log.error('Failed mkdir : %s, %s, %s' % (cmd, status, result))
      return False
    return True

  def _hdfs_mvdir(self, old_dir, new_dir):
    if not old_dir:
      return False
    if not self._hdfs_exist(new_dir):
      if not self._hdfs_mkdir(new_dir):
        return False
    cmd = '%s fs -mv %s/* %s/' % (self._hadoop_bin, old_dir, new_dir)
    status, result = commands.getstatusoutput(cmd)
    if status != 0:
      self._log.log.error('Failed mv dir : %s, %s, %s' % (cmd, status, result))
      return False
    self._log.log.info('ok, mv dir : %s, %s, %s' % (cmd, status, result))
    return True

  def _command_remote_backup(self, ip, filelist, backup_dir):
    if not ip or not filelist or not backup_dir:
      return False
    abs_path = [ os.path.join(self._crawler_data_dir, f) for f in filelist]
    sub_cmd = 'mv %s %s' % (' '.join(abs_path), backup_dir)
    cmd = "ssh search@%s \'%s\'" % (ip, sub_cmd)
    self._log.log.info('begin exe:%s' % (cmd))
    status, result = commands.getstatusoutput(cmd)
    self._log.log.info('end exe:%s' % (cmd))
    if status == 0:
      return True
    else:
      self._log.log.error('Failed exe:%s with: %s, %s' % (cmd, status, result))
      return False

  def _command_remote_uploader(self, ip, filelist, hdfs_dir):
    if not ip or not filelist or not hdfs_dir:
      return False
    abs_path = [ os.path.join(self._crawler_data_dir, f) for f in filelist]
    sub_cmd = '%s fs -put %s %s' % (self._crawler_upload_bin, ' '.join(abs_path),
        hdfs_dir)
    cmd = "ssh search@%s \'%s\'" % (ip, sub_cmd)
    self._log.log.info('Begin: %s' % cmd)
    status, result = commands.getstatusoutput(cmd)
    self._log.log.info('End: %s' % cmd)
    if status == 0:
      return True
    else:
      self._log.log.error('Failed exe:%s with: %s, %s' % (cmd, status, result))
      return False
  # return the final upload file dict
  # return (hdfs_dir, filedict)
  def _prepare_upload_files(self):
    all_files = self._prepare_remote_files()
    if not all_files:
      return None, None
    flist = []
    for k, v in all_files.items():
      if v:
        flist += v
    # order by file name
    if not flist:
      return None, None
    flist.sort()
    dest_hdfs_dir = '_'.join(str.split(flist[0], '_')[0:2])
    selected_f = flist[0 : self._batch_num]
    upload_dict = {}
    for k, v in all_files.items():
      tmplist = list(set(v).intersection(selected_f))
      if tmplist:
        upload_dict[k] = tmplist
    return dest_hdfs_dir, upload_dict

  def exit_service(self, num, fram):
    self._exit = True

  def _upload(self, filedict, hdfs_dir, hdfs_dir_tmp):
    if not filedict:
      return False
    dest_tmp_dir = hdfs_dir_tmp
    if not self._hdfs_exist(dest_tmp_dir):
      if not self._hdfs_mkdir(dest_tmp_dir):
        return False
    self._log.log.info('upload file to %s' % (dest_tmp_dir))
    sucfiles = 0
    for k, v in filedict.items():
      # TODO(xiaohe):concurrent upload
      if self._command_remote_uploader(k, v, dest_tmp_dir):
        sucfiles += 1
        while not self._command_remote_backup(k, v,
            self._crawler_data_backup_dir):
          time.sleep(1)
    if sucfiles > 0:
      while not self._hdfs_mvdir(dest_tmp_dir, hdfs_dir):
        time.sleep(1)
    return sucfiles > 0


  def run(self):
    last_check_time = 0
    self._log.log.info('upload service is running...')
    while not self._exit:
      nowt = int(time.time())
      time.sleep(1)
      if nowt - last_check_time >= self._check_interval:
        dest_hdfs_dir, upload_files = self._prepare_upload_files()
        self._log.log.info('ready: %s, %s' % (dest_hdfs_dir, upload_files))
        last_check_time = nowt
        if not dest_hdfs_dir or not upload_files:
          self._log.log.info('not enouth files')
          continue
        hdfs_dir = os.path.join(self._hdfs_dir, self._hdfs_subdir, dest_hdfs_dir)
        hdfs_dir_tmp = os.path.join(self._hdfs_dir, self._hdfs_subdir, 'upload_tmp')
        if not self._upload(upload_files, hdfs_dir, hdfs_dir_tmp):
          self._log.log.error('Failed upload data: %s, to %s, %s' % (upload_files,
            hdfs_dir_tmp, hdfs_dir))
    self._log.log.info('upload service is end.')

import signal
uploader = UploaderService()
signal.signal(signal.SIGINT, uploader.exit_service)
signal.signal(signal.SIGTERM, uploader.exit_service)
if __name__ == '__main__':
  uploader.setDaemon(True)
  print 'upload service start...'
  uploader.start()
  while uploader.isAlive():
    time.sleep(10)
  print 'upload service end.'
