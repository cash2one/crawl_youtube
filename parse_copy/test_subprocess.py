#!/usr/bin/python
#coding=utf-8

import subprocess

def cmd_call(cmd):
  p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  #p = subprocess.Popen(cmd, shell=True)
  print 'stderr:', p.stderr.read()
  return p.returncode, p.stdout.read()

if __name__ == '__main__':
  cmd = 'hadoop fs -ls /user/search/short_video/out/video | tail -100'
  print 'start call cmd: ', cmd
  retcode, result = cmd_call(cmd)
  print 'result:', result
  #cmd_call(cmd)
  print 'finish call cmd: ', cmd

