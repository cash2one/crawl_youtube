#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

# this class inherited from singleton
from url_normalize import UrlNormalize
from url_normalize import get_abs_url

def test_access_url():
  assert ('http://ent.qq.com/a/n1234.html' ==
      get_abs_url('http://ent.qq.com/tv/', '/a/n1234.html'))
  assert( 'http://ent.qq.com/a/n1234.html'
      == get_abs_url('http://ent.qq.com/tv/index.html', '/a/n1234.html'))
  assert ('http://ent.qq.com/a/n1234.html' ==
      get_abs_url('http://ent.qq.com/tv/', '../a/n1234.html'))
  assert ('http://ent.qq.com/a/n1234.html' ==
      get_abs_url('http://ent.qq.com/', 'a/n1234.html'))
  assert ('http://ent.qq.com/a/n1234.html' ==
      get_abs_url('http://ent.qq.com/tv/', 'http://ent.qq.com/a/n1234.html'))
  print 'test access url [OK]'

un = UrlNormalize.get_instance('url_normalize_settings')
def test_url_normalize():
  assert ('http://google.com/test.html;12445' == 
      un.get_unique_url('http://google.com/test.html;12445#fadk?k1=v1&k2=v2'))
  assert ('http://google.com/test.html;12445#fadk?k1=v1&k2=v2' ==
      un.get_unique_url('http://google.com/test.html;12445#fadk?k1=v1&k2=v2', no_conf_no_oper = True))
  # qq
  assert ('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg' == 
      un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg'))
  assert ('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg' == 
      un.get_unique_url('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?vid=w0015xnrgrg&nonokey=nonvalue'))
  assert ('http://v.qq.com/cover/v/v0a5d3mvfs59t8q.html?id=w0015xnrgrg' == 
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
  assert ('http://info.3g.qq.com/g/s?aid=sports_ss&sid=1111&id=sports_20141214001978&icfa=sports_eng' ==
      un.get_unique_url('http://info.3g.qq.com/g/s?sid=1111&icfa=sports_eng&aid=sports_ss&id=sports_20141214001978&pos=eng_yctt&i_f=0'))

  print 'test url normalize [OK]'
test_access_url()
test_url_normalize()
