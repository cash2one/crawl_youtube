#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# this class inherited from singleton
from url_normalize import UrlNormalize
from url_filter import UrlFilter

def test_access_url():
  assert ('http://ent.qq.com/a/n1234.html' ==
      UrlFilter.get_accessable_url('http://ent.qq.com/tv/', '/a/n1234.html'))
  assert( 'http://ent.qq.com/a/n1234.html'
      == UrlFilter.get_accessable_url('http://ent.qq.com/tv/index.html', '/a/n1234.html'))
  assert ('http://ent.qq.com/a/n1234.html' ==
      UrlFilter.get_accessable_url('http://ent.qq.com/tv/', '../a/n1234.html'))
  assert ('http://ent.qq.com/a/n1234.html' ==
      UrlFilter.get_accessable_url('http://ent.qq.com/', 'a/n1234.html'))
  assert ('http://ent.qq.com/a/n1234.html' ==
      UrlFilter.get_accessable_url('http://ent.qq.com/tv/', 'http://ent.qq.com/a/n1234.html'))
  print 'test access url [OK]'

def test_url_normalize():
  un = UrlNormalize()
  assert ('http://google.com/test.html;12445#fadk' == 
      un.get_unique_url('http://google.com/test.html;12445#fadk?k1=v1&k2=v2'))
  assert ('http://google.com/test.html;12445#fadk?k1=v1&k2=v2' ==
      un.get_unique_url('http://google.com/test.html;12445#fadk?k1=v1&k2=v2', no_conf_no_oper = True))
  # qq
  assert ('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg' == 
      un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg'))
  assert ('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg' == 
      un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg&nonokey=nonvalue'))
  assert ('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html' == 
      un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?id=w0015xnrgrg&nonokey=nonvalue'))
  assert ('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg' ==
      un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?nonokey=nonvalue&vid=w0015xnrgrg'))
  assert ('http://v.qq.com/cover/e/ecd5qnvlatbzc1p/n0015uy132r.html' ==
      un.get_unique_url('http://v.qq.com/cover/e/ecd5qnvlatbzc1p/n0015uy132r.html'))
  # youku
  assert ('http://v.youku.com/v_show/id_XNzU1OTc5NzAw.html' ==
      un.get_unique_url('http://v.youku.com/v_show/id_XNzU1OTc5NzAw.html?f=22723877'))
  assert ('http://v.youku.com/v_show/id_XNzUzMDEzOTQ4.html' ==
      un.get_unique_url('http://v.youku.com/v_show/id_XNzUzMDEzOTQ4.html?from=y1.3-tech-index3-232-10183.89969-89963.9-1'))
  assert ('http://v.youku.com/v_show/id_XNzM1MTc4NTg0.html' ==
      un.get_unique_url('http://v.youku.com/v_show/id_XNzM1MTc4NTg0.html?f=22024516&from=y1.3-tech-index3-232-10183.89988-89983.5-1'))
 # baomihua
  assert ('http://video.baomihua.com/16576029/34474714' ==
      un.get_unique_url('http://video.baomihua.com/16576029/34474714'))

  print 'test url normalize [OK]'
test_access_url()
test_url_normalize()
