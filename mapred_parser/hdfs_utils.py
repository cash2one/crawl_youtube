#!/usr/bin/python
# coding=utf-8
# author=gaoqiang@letv.com

import time
import commands
import logging
import subprocess

fs_cmd = 'hadoop fs %s'

def call_cmd(cmd):
  pro = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return pro.returncode, pro.stdout.read()

def strip_first_line(output):
  line_list = output.split('\n')
  line_list = line_list[1:]
  output = '\n'.join(line_list)
  return output

def list_files(path):
  cmd = fs_cmd % '-ls ' + path
  logging.debug('listing files: %s', cmd)
  status, files = call_cmd(cmd)
  #files = strip_first_line(files)
  if status:
    logging.error('failed to run command [%s]', fs_cmd % '-ls ' + path)
    return []
  if not files:
    logging.error('hadoop input path is empty, [%s]', path)
    return []
  files = [x.split()[-1] for x in files.split('\n')
           if not x.startswith('Found ') and not x.endswith(' items')]
  logging.debug('files in [%s]:\n\t%s', path, files)
  return files


def file_exists(file_path):
  cmd = fs_cmd % '-test -e ' + file_path
  logging.debug('checking file: %s', cmd)
  return call_cmd(cmd)[0] == 0


def dir_exists(path):
  cmd = fs_cmd % 'test -d ' + path
  logging.debug('checking directory: %s', cmd)
  return call_cmd(cmd)[0] == 0


def rm_file(file_path):
  cmd = fs_cmd % '-rm ' + file_path
  logging.debug('removing file: %s', cmd)
  call_cmd(cmd)


def rm_dir(path):
  cmd = fs_cmd % '-rm -r %s' % path
  logging.debug('deleting directory: %s', cmd)
  call_cmd(cmd)


def mv(filename, path_or_filename):
  cmd = fs_cmd % '-mv %s %s' % (filename, path_or_filename)
  logging.debug('moving [%s] to [%s]: %s', filename, path_or_filename, cmd)
  call_cmd(cmd)


def cp(filename, path_or_filename):
  cmd = fs_cmd % '-cp %s %s' % (filename, path_or_filename)
  logging.debug('copying [%s] to [%s]: %s', filename, path_or_filename, cmd)
  call_cmd(cmd)


def mkdir(path):
  cmd = fs_cmd % '-mkdir %s' % path
  logging.debug('creating directory: %s', cmd)
  call_cmd(cmd)


def ensure_dir(path):
  if not dir_exists(path):
    mkdir(path)


def count_file(path):
  if not path:
    return 0
  cmd = fs_cmd % '-count %s' % path
  logging.debug('counting files of input folder: %s', cmd)
  status, output = call_cmd(cmd)
  #output = strip_first_line(output)
  if status:
    logging.error('failed to run command: %s', cmd)
    return 0
  file_count = [x for x in output.split(' ') if x][1]
  logging.debug('file count of directory [%s] is [%s]', path, file_count)
  return int(file_count)


def file_size(path):
  if not path:
    return 0
  cmd = fs_cmd % '-count %s' % path
  logging.debug('calculating file size: %s', cmd)
  status, output = call_cmd(cmd)
  #output = strip_first_line(output)
  if status:
    logging.error('failed to run command: %s', cmd)
    return 0
  file_size = [x for x in output.split(' ') if x][2]
  logging.debug('file size of directory [%s] is [%s]', path, file_size)
  return int(file_size)


def cp_or_mv_with_timestamp(src_dir, dst_dir, action='cp'):
  dst_dir = '/' + dst_dir.strip('/') + '/'
  timeflag = time.strftime('%Y%m%d%H%M%S')
  index = 0
  for f in list_files(src_dir):
    (mv if action == 'mv' else cp)(f, dst_dir + timeflag + ('_%s' % index if index else ''))
    now = time.strftime('%Y%m%d%H%M%S')
    if now == timeflag:
      index += 1
    else:
      timeflag = now
      index = 0

