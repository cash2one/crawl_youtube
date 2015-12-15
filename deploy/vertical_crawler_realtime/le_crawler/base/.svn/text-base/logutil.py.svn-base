#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# not thread safe 
__author__ = 'guoxiaohe@letv.com'

import logging

class Log(object):
  def __init__(self, log_id, log_path):
    # log
    self.logger_ = logging.getLogger(log_id)
    fh = logging.FileHandler(log_path)  
    #fh.setLevel(logging.DEBUG) 
    self.logger_.setLevel(logging.INFO)
    #ch = logging.StreamHandler()  
    #ch.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s-%(filename)s:%(lineno)d[%(levelname)s]:%(message)s")
    #ch.setFormatter(formatter)  
    fh.setFormatter(formatter)  
    # add the handlers to logger  
    #self.logger_.addHandler(ch)  
    self.logger_.addHandler(fh)  
    # "application" code  

  def setdebuglevel(self):
    self.logger_.setLevel(logging.DEBUG)
  def setinfolevel(self):
    self.logger_.setLevel(logging.INFO)

  @property
  def log(self):
    return self.logger_

  def info(self, info):
    self.log.info(info)

  def error(self, info):
    self.log.error(info)

  def debug(self, info):
    self.log.debug(info)

  def warn(self, info):
    self.log.warn(info)



