# encoding: utf8

import time
import logging
import os
import traceback
from logging.handlers import RotatingFileHandler
from multiprocessing import Pool, current_process, Queue, Manager
from utils import call_cmd, cycle_run, send_message


TEL_LIST = ['13426031534', '18515029185', '15330025605']

class HadoopUploader(object):
  def __init__(self, local_out, hadoop_dir, queue, lock, p_name):
    self._local_out = local_out
    self._hadoop_dir = hadoop_dir
    self._file_upload_queue = queue
    self._queue_lock = lock
    self._p_name = p_name
    self._init_log()

  def _init_log(self):
    log_name = "hadoop_uploader_%s.error" % self._p_name
    self._handler = RotatingFileHandler(log_name, mode='a', maxBytes=100 * 1024 * 1024, backupCount=2)
    self._handler.setFormatter(logging.Formatter('[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s'))
    self._logger = logging.getLogger(log_name)
    self._logger.addHandler(self._handler)
    self._logger.setLevel(logging.DEBUG)


  def __del__(self):
    self._handler.close()
    self._logger.removeHandler(self._handler)

  def _delete_seqfile_local(self, filename):
    try:
      os.remove('%s/%s' % (self._local_out, filename))
      return True
    except Exception:
      self._logger.exception('failed to delete %s' % filename)
      return False

  def _put_to_hadoop(self, filename):
    cmd = 'hadoop fs -put %s/%s %s' % (self._local_out, filename, self._hadoop_dir)
    logging.debug('excute cmd:%s', cmd)
    sta, result = call_cmd(cmd)
    return True if sta == 0 else False

  def _gen_file_name(self):
    filename = None
    self._queue_lock.acquire()
    if not self._file_upload_queue.empty():
      filename = self._file_upload_queue.get(timeout=1)
    self._queue_lock.release()
    return filename

  def run(self):
    while 1:
      filename = self._gen_file_name()
      if not filename:
        break
      if os.path.isdir(filename):
        continue
      if not filename.endswith('.seq'):
        self._logger.error('except file not seq filename:[%s]', filename)
        continue
      if self._put_to_hadoop(filename):
        self._logger.info('success put file to hadoop, filename:[%s]', filename)
        if self._delete_seqfile_local(filename):
          self._logger.info('success delete sequence file local, filename:[%s]', filename)
        else:
          self._logger.error('failed delete sequence file local, filename:[%s]', filename)
      else:
        self._logger.error('failed put file to hadoop, filename:[%s]', filename)


def run_upload(local_out, hadoop_dir, file_upload_queue, lock, p_name):
  hadoop_uploader = HadoopUploader(local_out, hadoop_dir, file_upload_queue, lock, p_name)
  hadoop_uploader.run()

def run_pool(local_out='./out', hadoop_dir='short_video/in', process_size=4):
  while 1:
    manager = Manager()
    file_upload_queue = manager.Queue(10000)
    lock = manager.Lock()
    file_list = os.listdir(local_out)
    file_list = [filename for filename in file_list if filename.endswith('.seq')]
    if not file_list:
      break
    for filename in file_list:
      file_upload_queue.put(filename)
    pool = Pool(process_size)
    for i in range(process_size):
      pool.apply_async(run_upload, args=(local_out, hadoop_dir, file_upload_queue, lock, 'p%s' % i))
    print 'waiting for all upload to finish ...'
    pool.close()
    pool.join()
    print 'finish all upload .....'


def start_up(local_out='./out', hadoop_dir='short_video/in', interval=60):
  try:
    cycle_run(lambda: run_pool(local_out, hadoop_dir), interval)
  except Exception, e:
    print traceback.format_exc()
    send_message('txt2seq failed ...', TEL_LIST)


def main():
  local_out = './out'
  hadoop_dir='short_video/in'
  start_up(local_out, hadoop_dir)

if __name__ == "__main__":
  main()
