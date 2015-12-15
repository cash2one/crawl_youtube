#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'

import time
import MySQLdb 
import Queue
import threading
import json
import traceback
import gzip
import sys
import md5
import re
from sle_crawler.common.url_filter import UrlFilter

reload(sys)
sys.setdefaultencoding('utf8')

import StringIO
from scrapy import log
from url_filter import UrlFilter
from page_writer import PageWriterBase
from scrapy.selector import Selector

class PageMysqlWriter(PageWriterBase):
  def __init__(self, spider):
    PageWriterBase.__init__(self, spider)
    # local test
    self.mysql_host_ = '10.200.91.74'
    self.mysql_port_ = 3306
    self.mysql_passwd_ = 'search@letv'
    self.mysql_usr_ = 'search'
    self.mysql_db_ = 'crawler_tmp'

    #online writer
    #self.mysql_db_ = 'headline_video'
    #self.mysql_host_ = '10.181.153.81'
    #self.mysql_port_ = 3315
    #self.mysql_usr_ = 'so_hlv_w'
    #self.mysql_passwd_ = 'SRVMXRB3EFfTEYN15UZF'

    self.connect_ = None
    self.set_name('PageMysqlWriter')
    self.data_queue_ = Queue.LifoQueue(maxsize = 10240)
    self.thread_ = threading.Thread(target = self.writer_mysql, args = ())
    self.url_filter_ = UrlFilter()
    # {url:{'type':'value'}}
    self.extend_map_ = {}
    #
    self.__init_regdict()
    self.store_pages_ = 0
    self.exit_ = False
    self.process_exit_ = False

    self.start_urls_ = UrlFilter.load_domains('../conf/start_urls.cfg')
    print self.start_urls_

  def __init_regdict(self):
    self.regdict_ = {}
    self.regdict_['IqiyiMoviesWebDB'] = re.compile(r'(.*)?(/(sports/game/|v_|w_).*)\.(html|htm)', re.IGNORECASE)
    self.regdict_['NetEaseMoviesWebDB'] = re.compile(r'(.*)?(/(v9|wc).*)\.(html|htm)',
        re.IGNORECASE)
    self.regdict_['SinaMoviesWebDB'] = re.compile(r'.*/\d*\.(html|htm)', re.IGNORECASE)

  def _extend_map(self, url):
    return url in self.start_urls_

  def get_connect(self):
    while not self.exit_:
      try:
        if not self.connect_:
          self.connect_ = MySQLdb.connect(host = self.mysql_host_, user =
              self.mysql_usr_, passwd = self.mysql_passwd_, db = self.mysql_db_,
              charset = 'utf8', port = self.mysql_port_)
          self.spider_.log('Success connect to mysql!', log.INFO)
        return self.connect_
      except Exception, e:
        self.spider_.log('Error connect to mysqldb[%s]:[%s, %s, %s, %s]' % (e,
          self.mysql_host_, self.mysql_port_, self.mysql_db_,
          self.mysql_usr_), log.ERROR)
        self.release_connect()
        time.sleep(4)
        continue

  def release_connect(self):
    if self.connect_:
      self.connect_.cursor().close()
      self.connect_.close()
      self.connect_ = None

  def get_table_from_url(self, domain):
    if not domain:
      return None
    if 'letv.com' in domain:
      return 'LetvMoviesWebDB'
    elif 'sina.com.cn' in domain:
      return 'SinaMoviesWebDB'
    elif '163.com' in domain:
      return 'NetEaseMoviesWebDB'
    elif 'fun.tv' in domain:
      return 'FunMoviesWebDB'
    elif 'so.tv.souhu.com' in domain:
      return 'SohuMoviesWebDB'
    elif '2014.qq.com' in domain:
      return 'QQMoviesWebDB'
    elif 'iqiyi.com' in domain:
      return 'IqiyiMoviesWebDB'
    elif '2014.youku.com' in domain:
      return 'YoukuMoviesWebDB'
    else:
      self.spider_.log('Failed get mysql table from [%s, %s]' %(domain, domain),
          log.ERROR)
      return None

  def initialize(self):
    self.get_connect().ping(True)
    self.thread_.start()
    return True

  def finalize(self):
    self.exit_ = True
    while not self.process_exit_:
      self.spider_.log('wait for all exit ...', log.INFO)
      time.sleep(10)
    time.sleep(40)
    self.release_connect()

   #def threading fun for writer to mysql
  def process_item(self, item):
    if not item:
      self.spider_.log('item is null %s' % (item), log.INFO)
      return
    while not self.exit_:
      try:
        self.data_queue_.put(item, block = True, timeout = 5)
        return
      except Exception, e:
        self.spider_.log('mysql writer buffer is full %s, size %d' % (e,
          self.data_queue_.qsize()), log.ERROR)
        continue

  # return json object include {"cover": "http://kkkkkk", "title": "title""}
  def _gen_json_result(self, dicts):
    if not dicts:
      return None
    try:
      return json.dumps(dicts, ensure_ascii = False).encode('utf8')
    except Exception, e:
      self.spider_.log('Convert to json ERROR [%s]' % (e.message), log.ERROR)
      return None

  def _gen_store_result(self, encoding = 'gb2312', lurl = None, lpic = None, ltitle = None, ltime =
      None, ldown_count = None):
    if not lurl:
      return None
    try:
      dicttmp = {}
      if lpic:
        tmppic = UrlFilter.get_base_url(lpic[0])
        if tmppic:
          dicttmp['cover'] = lpic[0].encode('utf8')
      if ltitle:
        #self.spider_.log('decode title: %s with %s' % (ltitle[0], encoding), log.INFO)
        dicttmp['title'] = ltitle[0].encode('utf8')
        #print dict
      if ltime:
        dicttmp['length'] = ltime[0]
      if ldown_count:
        dicttmp['download_count'] = ldown_count[0]
      if not dict:
        return None
      return dicttmp
    except Exception, e:
      print e
      print traceback.format_exc()
      self.spider_.log('Convert to json ERROR [%s]' % (e.message), log.ERROR)
      return None

  def  _letv_extend_map(self, sle_html):
    self.spider_.log('not support for letv.com domain')
    return {}

  def _netease_exetend_map(self, sel, enc = 'gb2312'):
    # part wc-focus
    #redict = [(url, (type, content))]
    redict = []
    try:
      # all urls
      aurls = sel.xpath('//a')
      for urls in aurls:
        tmpurl = urls.xpath('.//@href').extract()
        if not tmpurl:
          continue
        storeurl = tmpurl[0].strip()
        if not self._is_intresting_url(storeurl):
          continue
        tmppic = urls.xpath('.//img/@src').extract()
        tmptitle = urls.xpath('.//img/@alt').extract() or urls.xpath('./text()').extract() or urls.xpath('.//div[@class="text"]/h3/text()').extract()
      #wc-focus = sle_html.xpath('//div[@class="wc-focus-scroll"]')
        extend_s = self._gen_store_result(encoding = enc, lurl = tmpurl, lpic =
            tmppic, ltitle = tmptitle)
        if extend_s:
          redict.append((storeurl, extend_s))
      self.spider_.log('found url extends links[%d]' % (len(redict)), log.INFO)
      return redict
    except Exception, e:
        # to do nothing
        self.spider_.log('error for %s' % (e.message))
        return redict 


  def _iqiyi_extend_map(self, sel, enc = 'utf-8'):
    if not sel:
      return []
    # topic flush
    retdicts = []
    try:
      all_urls = sel.xpath('//a')
      all_urls.sort()
      for urls in all_urls:
        tmpurl = urls.xpath('./@href').extract()
        if not tmpurl:
          continue
        storeurl = tmpurl[0]
        if not self._is_intresting_url(storeurl):
          continue
        tmppic = urls.xpath('./img/@src').extract()
        tmptitle = urls.xpath('./@title').extract() or urls.xpath('./@alt').extract() or urls.xpath('./img/@alt').extract() or urls.xpath('./img/@title').extract() or urls.xpath('./text()').extract()
        extend_s = self._gen_store_result(encoding = enc, lurl = tmpurl, lpic =
            tmppic, ltitle = tmptitle)
        if extend_s:
          retdicts.append((storeurl, extend_s))
      self.spider_.log('found url extends links[%d]' % (len(retdicts)), log.INFO)
      return retdicts
    except Exception, e:
      self.spider_.log('error for %s' % (e.message))
      return retdicts 

  def _sina_extend_map(self, sel, enc = 'utf8'):
    if not sel:
      return []
    # topic flush
    retdicts = []
    try:
      alls = sel.xpath('//a')
      alls.sort()
      for urls in alls:
        tmpurl = urls.xpath('./@href').extract()
        if not tmpurl:
          continue
        store_url = tmpurl[0]
        if not self._is_intresting_url(store_url):
          continue
        tmppic = urls.xpath('./img/@src').extract()
        tmptitle = urls.xpath('./img/@alt').extract() or urls.xpath('./@title').extract() or urls.xpath('./text()').extract()
        extend_s = self._gen_store_result(encoding = enc, lurl = tmpurl, lpic =
            tmppic, ltitle = tmptitle)
        if extend_s:
          retdicts.append((store_url, extend_s))
      self.spider_.log('found url extends links[%d]' % (len(retdicts)), log.INFO)
      return retdicts
    except Exception, e:
      self.spider_.log('error for %s' % (e.message))
      return retdicts

  def _qq_extend_map(self, sle_html):
    self.spider_.log('not support for letv.com domain')
    return {}

  # return dict of {url:extend_map_str}
  def _parse_extend_map(self, domain, item_html, encode = 'gbk'):
    if not domain:
      return {} 
    selectors_tmp = Selector(text = item_html, type = 'html')
    if domain == 'letv.com':
      return self._letv_extend_map(selectors_tmp)
    elif domain == 'v.2014.163.com':
      return self._netease_exetend_map(selectors_tmp)
    elif domain == 'iqiyi.com':
      return self._iqiyi_extend_map(selectors_tmp)
    elif domain == '2014.qq.com':
      return self._qq_extend_map(selectors_tmp)
    elif domain == '2014.sina.com.cn':
      return self._sina_extend_map(selectors_tmp)
    else:
      self.spider_.log('not support url[%s]' % (domain), log.ERROR)
    return None

  def _lookup_extend_map(self, url):
    tmpurl = UrlFilter.get_base_url(url)
    if not tmpurl:
      self.spider_.log('Failed Got Url From[%s]' % (url), log.ERROR)
      return None
    if self.extend_map_.has_key(url):
      return self._gen_json_result(self.extend_map_[tmpurl])
    else:
      self.spider_.log('Failed lookup extend map for [%s]'% (url), log.ERROR)
    return None

  # if is ok, return table name
  def _is_intresting_url(self, url):
    for (tbln, regi) in self.regdict_.items():
      if regi.match(url):
        return tbln
    return None


  def _get_store_key(self, url):
    return md5.new(url).hexdigest()

  # url_extrdict: {url, exted_dict}
  def _put_extend_map(self, url_extrdict):
    if not url_extrdict:
      return
    for (url, exs) in url_extrdict:
      tmpurl = UrlFilter.get_base_url(url)
      if not tmpurl or not self._is_intresting_url(tmpurl):
        self.spider_.log('droped Url[%s]' % (url), log.INFO)
        continue
      if self.extend_map_.has_key(tmpurl):
        tmpti = None
        if self.extend_map_[tmpurl].has_key('title'):
          tmpti = self.extend_map_[tmpurl]['title']
        self.extend_map_[tmpurl].update(exs)
        if tmpti and len(self.extend_map_[tmpurl]['title']) < len(tmpti):
          self.extend_map_[tmpurl]['title'] = tmpti
      else:
        self.extend_map_[tmpurl] = exs
        self.spider_.log('new extend:[%s] for [%s] [%d]' % (tmpurl, exs,
          len(exs)), log.DEBUG)
    #self.spider_.log('now extend_map_size: [%d]' % (len(self.extend_map_)), log.INFO)
  def __unzip(self, buf):
    f = gzip.GzipFile(fileobj = StringIO.StringIO(buf), mode = 'rb')
    html = f.read()
    f.close()
    return html

  def __gzip(self, content):
    buf = StringIO.StringIO()
    f = gzip.GzipFile(mode = 'wb', fileobj = buf)
    f.write(content)
    f.close()
    return buf.getvalue()


  def _write_mysql_internal(self, item):
    if not item:
      return
    try:
      sql_str = ''
      url = UrlFilter.get_base_url(item['url']).encode('utf8').strip()
      if not url:
        self.spider_.log('bad url:[%s]' % (url), log.ERROR)
        return
      domain = self.url_filter_.get_allowed_domain_from_url(url)
      if not domain:
        self.spider_.log('disallowed domain:[%s]' % (domain), log.INFO)
        return
      page = item['page'].decode(item['page_encoding']).encode('utf8')
      # parser extend map
      if self._extend_map(url):
        print 'beging parser extend map:[%s]' % (url)
        self.spider_.log('Parser extend map url:[%s]' % (url), log.INFO)
        url_exsdict = self._parse_extend_map(domain, page)
        if url_exsdict:
          self._put_extend_map(url_exsdict)
        print 'end parser extend map:[%s]' % (url)
      # end parser extend map
      if not self._is_intresting_url(url):
        self.spider_.log('Not intresting:[%s]' % (url), log.INFO)
        return
      # compress page content with gzip
      #import zlib
      #cpage = zlib.compress(page)
      #print zlib.decompress(cpage)
      cpage = self.__gzip(page)
      #print self.__unzip(cpage)
      # end compress

      tmp_ext = self._lookup_extend_map(url)
      if not tmp_ext:
        tmp_ext = '{}'
      tbl_n = self.get_table_from_url(domain)
      if not tbl_n:
        self.spider_.log('Failed Found Table name [%s]' % (domain), log.ERROR)
        return
      #self.spider_.log('Finished parser[%s]' % (url), log.INFO)
      conn = self.get_connect()
      conn.ping(True)
      cursor = conn.cursor()
      sql_str = 'insert into %s' % (tbl_n)
      sql_str += "(id, url, html, parse_state, category, fetch_time, extend_map) values (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')"
      idstr = self._get_store_key(url) 
      if cursor.execute("""select id from %s where id='%s'""" % (tbl_n, idstr)) > 0:
        self.spider_.log('dupe [%s]' % (url), log.INFO)
        return
#MySQLdb.Binary(cpage)
      cursor.execute("""insert into %s 
      (id, url, parse_state, category, fetch_time, extend_map, html) values
      (%%s, %%s, %%s, %%s, %%s, %%s, %%s)""" % (tbl_n), (idstr, url, 0, 'worldcup',
        int(time.time()), str(tmp_ext), cpage))
      #cursor.execute(sql_str % (idstr, url, MySQLdb.Binary(cpage) , 0,
      #  'worldcup', int(time.time()), MySQLdb.escape_string(tmp_ext)))
      conn.commit()
      #cursor.close()
      self.store_pages_ += 1
      self.spider_.log('Store [%d] pages [%s]' % (self.store_pages_, url), log.INFO)
    except Exception, e:
      #print e
      #print traceback.format_exc()
      self.spider_.log('store to mysql error [%s] [%s] with coding [%s]' %(sql_str,
        traceback.format_exc(), item['page_encoding']), log.ERROR)
      #self.release_connect()

  def writer_mysql(self):
    self.spider_.log('writer to mysql threading running...', log.INFO)
    while not self.exit_ or not self.data_queue_.empty():
      item = None
      try:
        item = self.data_queue_.get(block = True, timeout = 10)
        if not item:
          continue
        self._write_mysql_internal(item)
      except Exception, e:
        #self.spider_.log('I am starving[%d] with error[%s]'
        #    %((self.data_queue_.qsize()), e.message), log.INFO)
        continue

    self.process_exit_ = True
    self.spider_.log('Mysql writer thread exit normal', log.INFO)

