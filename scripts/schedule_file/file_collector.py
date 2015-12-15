# encoding: utf8

import os
import time
import logging
import traceback
from logging.handlers import RotatingFileHandler
from multiprocessing import Pool, current_process
from utils import call_cmd, cycle_run, send_message

class FileCollector(object):
  def __init__(self, remote_ip, remote_dir='/letv/crawler_delta', local_dir='./in'):
    self._remote_ip = remote_ip
    self._remote_dir = remote_dir
    self._local_dir = local_dir
    self._init_dir()
    self._init_log()

  def _init_dir(self):
    if not os.path.exists(self._local_dir):
      os.mkdir(self._local_dir)

  def _init_log(self):
    log_name = "file_collector_%s.error" % self._remote_ip
    self._handler = RotatingFileHandler(log_name, mode='a', maxBytes=100 * 1024 * 1024, backupCount=2)
    self._handler.setFormatter(logging.Formatter('[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s'))
    #self._handler.setLevel(logging.DEBUG)
    self._logger = logging.getLogger(log_name)
    self._logger.addHandler(self._handler)
    self._logger.setLevel(logging.DEBUG)

  def __del__(self):
    self._handler.close()
    self._logger.removeHandler(self._handler)

  def _ls_file_list(self):
    cmd = 'ssh %s ls %s' % (self._remote_ip, self._remote_dir)
    #self._logger.debug('excute cmd:%s', cmd)
    sta, result = call_cmd(cmd)
    #print sta, result
    if sta == 0:
      #self._logger.debug('success get filelist:\n%s', result)
      return result.split()
    else:
      return None

  def _scp_file(self, filename, filename_tmp):
    cmd = 'scp search@%s:%s/%s %s/%s' % (self._remote_ip, self._remote_dir, filename, self._local_dir, filename_tmp)
    #self._logger.debug('excute cmd:%s', cmd)
    sta, result = call_cmd(cmd)
    return True if sta==0 else False

  def _delete_file_remote(self, filename):
    cmd = 'ssh search@%s rm %s/%s' % (self._remote_ip, self._remote_dir, filename)
    #self._logger.debug('excute cmd:%s', cmd)
    sta, result = call_cmd(cmd)
    return True if sta == 0 else False

  def _rename_file(self, filename, filename_tmp):
    if not filename or not filename_tmp:
      return
    local_filename = '%s/%s' % (self._local_dir, filename)
    local_filename_tmp = '%s/%s' % (self._local_dir, filename_tmp)
    try:
      os.rename(local_filename_tmp, local_filename)
    except Exception:
      self._logger.exception('failed to rename %s to %s' % (local_filename_tmp, local_filename))

  def run(self):
    file_list = self._ls_file_list()
    if not file_list:
      return
    for filename in file_list:
      if not filename.endswith('.txt'):
        continue
      filename_tmp = '%s_copying' % filename
      if self._scp_file(filename, filename_tmp):
        self._rename_file(filename, filename_tmp)
        self._logger.debug('success scp file filename:[%s]', filename)
        if self._delete_file_remote(filename):
          self._logger.debug('success delete remote file filename:[%s]', filename)
        else:
          self._logger.error('failed delete remote file filename:[%s]', filename)

def start_collect(ip, remote_dir, local_dir, interval=30):
  try:
    cycle_run(lambda: FileCollector(ip, remote_dir, local_dir).run(), interval)
  except Exception:
    print traceback.format_exc()
    send_message('file_collector failed ...', TEL_LIST)

ip_list = [
    '10.154.29.76',
    '10.154.29.75',
    '10.154.29.74',
    '10.154.29.73',
    '10.154.29.72',
    '10.154.29.71',
    '10.154.29.70',
    '10.154.29.69',
    '10.154.30.21',
    '10.154.30.25',
    '10.154.30.71',
    '10.154.30.80',
    '10.154.30.81',
    '10.154.30.89',
    '10.154.30.104',
    '10.154.30.105'
    ]
def main():
  pool = Pool(len(ip_list))
  for ip in ip_list:
    pool.apply_async(start_collect, (ip, '/letv/crawler_delta', './in'))
  print 'waiting for all file collector to finish...'
  pool.close()
  pool.join()

def test():
  pool = Pool(len(ip_list))
  for ip in ip_list:
    pool.apply_async(start_collect, (ip, '/letv/crawler_delta', './test_in'))
  print 'waiting for all file collector to finish...'
  pool.close()
  pool.join()
def unit_test():
  ip = '10.154.29.76'
  remote_dir = '/letv/crawler_delta'
  local_dir = './in'
  FileCollector(ip, remote_dir, local_dir).run()

if __name__ == "__main__":
  main()
