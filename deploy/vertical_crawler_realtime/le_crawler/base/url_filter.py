#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# this class inherited from singleton

import re
import traceback
import threading

from urlparse import urlparse
from urlparse import urlunparse

from singleton import Singleton
from file_monitor import FileMonitorBlock


class UrlFilter(Singleton):
  '''
  this class is using for url filter
  '''

  @staticmethod
  def load_lines(filepath):
    fp = open(filepath, 'r')
    lines = [line.strip().replace('\n','') for line in fp.readlines()]
    lines = filter(lambda line:line != '' and not line.startswith('#'), lines)
    print 'Finished load %s' % filepath
    fp.close()
    return lines

  @staticmethod
  def load_domains(filen, random_sort = False):
    if not random_sort:
      return UrlFilter.load_lines(filen)
    import random
    tmpurl = UrlFilter.load_lines(filen)
    random.shuffle(tmpurl)
    return tmpurl

  def reload_base_d(self):
    self.__lock.acquire()
    self.__base_domains = UrlFilter.load_lines(self.__base_domain_f)
    self.__base_domains.sort()
    print 'reload base domains: %s' % (len(self.__base_domains))
    self.__lock.release()

  def reload_allowed_d(self):
    self.__lock.acquire()
    self.__allowed_domains = UrlFilter.load_lines(self.__allowed_domain_f)
    print 'reload allowed domains: %s' % (len(self.__allowed_domains))
    self.__allowed_domains.sort()
    self.__lock.release()

  def reload_denied_d(self):
    self.__lock.acquire()
    self.__denied_domains = UrlFilter.load_lines(self.__denied_domain_f)
    print 'reload denied domains: %s' % (len(self.__denied_domains))
    self.__denied_domains.sort()
    self.__lock.release()

  # if using with auto_update True, 
  # quit_update should be called
  def init_onece(self, auto_update = False,
      base_domains_f = '../conf/base_domains.cfg',
      allowed_domains_f = '../conf/allowed_domains.cfg',
      denied_domains_f = '../conf/denied_domains.cfg'):
    self.__auto_update = auto_update
    self.__base_domain_f = base_domains_f
    self.__allowed_domain_f = allowed_domains_f
    self.__denied_domain_f = denied_domains_f
    self.__lock = threading.Lock()
    if self.__auto_update:
      self._file_monitor = FileMonitorBlock()
      self._file_monitor.register_callback(self.__base_domain_f,
          self.reload_base_d)
      self._file_monitor.register_callback(self.__allowed_domain_f,
          self.reload_allowed_d)
      self._file_monitor.register_callback(self.__denied_domain_f,
          self.reload_denied_d)
      self._file_monitor.start_monitor()
    else:
      self.reload_base_d()
      self.reload_allowed_d()
      self.reload_denied_d()

    self.base_host_regex_ = self.get_match_domain_regex(self.__base_domains)
    self.allowed_host_regex_ = self.get_match_domain_regex(self.__allowed_domains)
    self.denied_host_regex_ = self.get_match_domain_regex(self.__denied_domains)

  def quit_update(self):
    if self.__auto_update:
      self._file_monitor.quit()

  def get_match_domain_regex(self, domains):
    if not domains or len(domains) == 0:
      return re.compile('')
    regex = r'^(.*\.)?(%s)$' % '|'.join(re.escape(d) for d in domains)
    return re.compile(regex)

  def get_host_from_url(slef, url):
    #(TODO xiaohe): using urlparse cache instead
    return urlparse(url).hostname or ''

  def _is_allowed_host(self, host):
    return bool(self.allowed_host_regex_.search(host))

  def _is_denied_host(self, host):
    if not self.__denied_domains or len(self.__denied_domains) == 0:
      return False
    return bool(self.denied_host_regex_.search(host))

  def is_interesting_url(self, url):
    host = self.get_host_from_url(url)
    if self._is_denied_host(host) or not self._is_allowed_host(host):
      return False
    return True

  def __get_match_domain_str(self, regs, url):
    host = self.get_host_from_url(url)
    if not host:
      return None
    matd = regs.search(host)
    if not matd:
      return None
    dicts = matd.groups()
    if not dicts or len(dicts) <= 0:
      return None
    return dicts[-1]

  def get_domain_from_url(self, url):
    return self.__get_match_domain_str(self.base_host_regex_, url)
  # by now only return allowed domain info

  def get_allowed_domain_from_url(self, url):
    return self.__get_match_domain_str(self.allowed_host_regex_, url)

  # get url domain flag
  def get_flag(self, url):
      if not url:
        return None
      domain = self.get_allowed_domain_from_url(url)
      if not domain:
        domain = 'othres.site'
      return domain

  @staticmethod
  def is_valid_url(url):
    return bool(re.match(r'^https?:/{2}\w.+$', url))

  @staticmethod
  def get_accessable_url(base_url, test_url, canonicalize = False):
    """
      reture full accessable url, base root url
      # eg:
      # base_url : 'http://ent.qq.com/a/b/c'
      # test_url : 'http://ent.qq.com/a/b/c1.html'
      # test_url : '/a/b/c1.html'
      # test_url : '../c1.html''
      # all will return "http://ent.qq.com/a/b/c1.html"

      # url parse
      @staticmethod
      # input http://a.b/dc/htm.html;par?ksj&ddk
      # return http://a.b/dc/htm.html
    """
    if not test_url:
      return None
    test_url = test_url.strip()
    if UrlFilter.is_valid_url(test_url):
      return test_url
    purl = urlparse(base_url.strip())
    if not purl:
      return None
    nsc = purl.scheme
    nnetl = purl.netloc 
    npth = purl.path
    nurl = None
    if test_url.startswith('/'):
      nurl = urlunparse((nsc, nnetl, test_url, '', '', ''))
    else:
      import os
      nurl = urlunparse((nsc, nnetl,
        os.path.abspath(os.path.join(os.path.dirname(npth), test_url)),
        '',
        '',
        ''))
    if canonicalize:
      from scrapy.utils.url import canonicalize_url
      return canonicalize_url(nurl)
    return nurl

  @staticmethod
  def get_base_url(url, scheme = None, netloc = None):
    try:
      if not url:
        return None
      url = url.strip()
      purl = urlparse(url)
      if not purl:
        return None
      nscheme = purl.scheme or scheme
      nnetloc = purl.netloc or netloc
      if not nscheme or nscheme == '' or not nnetloc or nnetloc == '':
        return None
      return urlunparse((nscheme, nnetloc, purl.path,'', '',
        '')).strip()
    except Exception, e:
      print e
      print traceback.format_exc()
      return None
