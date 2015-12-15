#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# this class inherited from singleton

import re
import random
import threading
from urlparse import urlparse

from file_monitor import FileMonitorBlock


def get_host_from_url(url):
  # (TODO xiaohe): using urlparse cache instead
  return urlparse(url).hostname or ''


def get_match_domain_regex(domains):
  if not domains or len(domains) == 0:
    return re.compile('')
  regex = r'^(.*\.)?(%s)$' % '|'.join(re.escape(d) for d in domains)
  return re.compile(regex)


def get_match_domain_str(regs, url):
  host = get_host_from_url(url)
  if not host:
    return None
  matched = regs.search(host)
  if not matched:
    return None
  dicts = matched.groups()
  if not dicts:
    return None
  return dicts[-1]


class UrlFilter(object):
  _instance = None
  _instance_lock = threading.Lock()

  @staticmethod
  def get_instance(auto_update=False, allowed_domains_f='../conf/allowed_domains.cfg'):
    UrlFilter._instance_lock.acquire()
    if not UrlFilter._instance:
      UrlFilter._instance = UrlFilter(auto_update, allowed_domains_f)
    UrlFilter._instance_lock.release()
    return UrlFilter._instance

  # if using with auto_update True,
  # quit_update should be called
  def __init__(self, auto_update=False, allowed_domains_f='../conf/allowed_domains.cfg'):
    self.__auto_update = auto_update
    self.__allowed_domain_f = allowed_domains_f
    self.__lock = threading.Lock()
    if self.__auto_update:
      self._file_monitor = FileMonitorBlock()
      self._file_monitor.register_callback(self.__allowed_domain_f,
                                           self.reload_allowed_d)
      self._file_monitor.start_monitor()
    else:
      self.reload_allowed_d()

    self.allowed_host_regex_ = get_match_domain_regex(self.__allowed_domains)


  @staticmethod
  def load_lines(filepath):
    fp = open(filepath, 'r')
    lines = [line.strip().replace('\n', '') for line in fp.readlines()]
    lines = filter(lambda line: line and not line.startswith('#'), lines)
    fp.close()
    return lines

  @staticmethod
  def load_domains(filen, random_sort=False):
    if not random_sort:
      return UrlFilter.load_lines(filen)
    tmpurl = UrlFilter.load_lines(filen)
    random.shuffle(tmpurl)
    return tmpurl

  def reload_allowed_d(self):
    self.__lock.acquire()
    self.__allowed_domains = UrlFilter.load_lines(self.__allowed_domain_f)
    print 'reload allowed domains: %s' % (len(self.__allowed_domains))
    self.__allowed_domains.sort()
    self.__lock.release()

  def quit_update(self):
    if self.__auto_update:
      self._file_monitor.quit()

  def _is_allowed_host(self, host):
    return bool(self.allowed_host_regex_.search(host))

  def is_interesting_url(self, url):
    return self._is_allowed_host(get_host_from_url(url))

  def get_domain_from_url(self, url):
    return get_match_domain_str(self.allowed_host_regex_, url)

  def get_allowed_domain_from_url(self, url):
    return get_match_domain_str(self.allowed_host_regex_, url)

  def get_flag(self, url):
    if not url:
      return None
    domain = self.get_allowed_domain_from_url(url)
    if not domain:
      print 'failed get allowed domain from url:', url
    return domain

