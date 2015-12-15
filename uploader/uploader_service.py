#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

import os
import sys
import commands
import time
import signal
import threading
import gzip
import commands

from logutil import Log

hadoop_bin = 'hadoop'
LOCAL_DATA_DIR = [
    '/letv/crawler_delta/',
    ]
HDFS_DEST_DIR = 'crawler_upload/'
LOCAL_DATA_BACKUP_DIR = '/letv/crawler_backup/'
BATCH_FILE_NUMS = 5
MAX_TIMEUPLOAD_SDS = 86400

def gen_dir_with_times(src_dir):
  return time.strftime('%s_%%Y%%m%%d%%H%%M%%S' % (src_dir), time.localtime())

def hdfs_mkdir(dest_dir):
  cmdstr = '%s fs -mkdir %s' %(hadoop_bin, dest_dir)
  sta, out = commands.getstatusoutput(cmdstr)
  loger.get_log().info('exec:[%s], [%s], [%s]' %(cmdstr, sta, out))
  return sta == 0

def hdfs_upload(files, dest_dir):
  if not files:
    return True
  filestr = ' '.join(files)
  cmdstr = '%s fs -put %s %s' %(hadoop_bin, filestr, dest_dir)
  sta, out = commands.getstatusoutput(cmdstr)
  loger.get_log().info('exec:[%s], [%s]' %(cmdstr, out))
  loger.get_log().info(out)
  return sta == 0

class UploadFilesToHdfs(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.exit_ = False
    self.batch_num_ = BATCH_FILE_NUMS
    self.backup_dir_ = LOCAL_DATA_BACKUP_DIR
    self.gzip_before_upload_ = True
    if not os.path.isdir(self.backup_dir_):
      msg = '%s is not dir' % self.backup_dir_
      loger.get_log().error(msg)
      assert False, msg
    self.local_filedirs_ =  LOCAL_DATA_DIR

    self.dest_hdfs_dir_ = HDFS_DEST_DIR
    #self.dest_hdfs_dir_ = 'crawler_tmp/'
    self.max_not_meet_seconds_ = MAX_TIMEUPLOAD_SDS
    self.up_meet_times_= int(time.time())

  def set_gzip_before_upload(self, flag = True):
    self.gzip_before_upload_ = flag

  def __gzip_file(self, inputf, outputf):
    cmd = str('tar -czvf %s %s' % (outputf, inputf))
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
      loger.get_log().error('Failed exec [%s] with [%s, %s]' % (cmd, status, output))
      return False
    return True

  def prepare_upload_batch_file(self, src_dir):
    rets = []
    if not os.path.isdir(src_dir):
      loger.get_log().info('%s is not exists' % src_dir)
      assert False, '% is not dir' %(src_dir)
      return []
    
    fis = filter(lambda f: self.is_ok_file(f),  os.listdir(src_dir))
    if not fis or len(fis) <= 0:
      loger.get_log().info('empty file in dir')
      return []
    nows = int(time.time())
    diff = nows - self.up_meet_times_;
    if len(fis) < self.batch_num_ and diff < self.max_not_meet_seconds_:
      loger.get_log().info('now count [%d] < [%d] under [%s]' % (len(fis),
        self.batch_num_, diff))
      return []
    fis.sort()
    self.up_meet_times_ = nows
    uploadf = fis[0 : self.batch_num_]
    loger.get_log().info('begin compress dest file [%s]' %(uploadf))
    for l in uploadf:
      l = os.path.join(src_dir, l)
      nwf = l
      if self.gzip_before_upload_ and not l.endswith('.gz'):
        nwf = '%s.gz' % (l)
        try:
          loger.get_log().info('compress [%s] to [%s]' %(l, nwf))
          # remove the orignal file
          if self.__gzip_file(l, nwf):
            os.remove(l)
            rets.append(nwf)
          else:
            loger.get_log().error('gen gzip file error[%s], [%s]' %(l, nwf))
        except Exception, e:
          loger.get_log().error('gen gzip file error[%s], [%s]' %(l,
            e.message))
      elif l.endswith('.gz') and os.path.isfile(l):
        # upload with gz
        rets.append(nwf)
      else:
        loger.get_log().error('unkown file[%s]' %(l))
    return rets

  def is_ok_file(self, filen):
    return not filen.endswith('.tmp')

  def gen_upload_dir(self, filens):
    filens.sort()
    tmpstr = filens[0]
    dirn = os.path.basename(tmpstr).split('_')
    if not dirn or len(dirn) < 2:
      raise Exception('bad filename:[%s]' % filens)
      return None
    pid = os.getpid()
    return '%s_%s_%d' %(dirn[0], dirn[1], pid)

  def backup_files_to_local(self, files, dest_dir):
    import shutil
    for f in files:
      if not os.path.isfile(f):
        continue
      #loger.get_log().info('move %s'% (f))
      #os.remove(f)
      shutil.move(f, dest_dir)

  def start_upload_files(self, local_dir, hdfs_dir):
    loger.get_log().info('begin upload %s to %s' %(local_dir, hdfs_dir))

    tmpf = self.prepare_upload_batch_file(local_dir)
    if not tmpf or len(tmpf) <= 0:
      loger.get_log().info('empty file list')
      return False
    batchf = [tmpf]
    loger.get_log().info('%s, %s' %(local_dir, batchf) )
    for bf in batchf:
      tmp_dir = self.gen_upload_dir(bf)
      if not tmp_dir:
        raise Exception('bad dir name %s' % tmp_dir)
        return False
      redir = gen_dir_with_times(os.path.join(hdfs_dir, tmp_dir))
      while not hdfs_mkdir(redir):
        loger.get_log().error('error while try to mkdir %s' %  redir)
        if self.exit_:
          return False
        time.sleep(5)
        redir = gen_dir_with_times(os.path.join(hdfs_dir, tmp_dir))
      while not hdfs_upload(bf, redir):
        loger.get_log().error('error while try to upload [%s] to [%s]' % (bf, redir))
        if self.exit_:
          return False
        time.sleep(5)
      self.backup_files_to_local(bf, self.backup_dir_)
    loger.get_log().info('Success upload files to hdfs')

  def exit(self, num, frame):
    self.exit_ = True

  def run(self):
    inverts = 60 * 5
    secs = inverts
    while not self.exit_:
      if secs == inverts:
        secs = 0
        for di in self.local_filedirs_:
          self.start_upload_files(di, self.dest_hdfs_dir_)
      time.sleep(1)
      secs += 1
    loger.get_log().info('upload service exit normaly')

loger = Log(logf = '../log/uploader.log')
uploader = UploadFilesToHdfs()

signal.signal(signal.SIGINT, uploader.exit)
signal.signal(signal.SIGTERM, uploader.exit)

if __name__ == '__main__':
  uploader.setDaemon(True)
  uploader.start()
  loger.get_log().info('uploader service is running..')
  while uploader.isAlive():
    time.sleep(10)
  loger.get_log().info('uploader service main end')
