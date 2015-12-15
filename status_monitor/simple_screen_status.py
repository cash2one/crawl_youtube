#!python
#
# Copyright 2014 LeTV Inc. All Rights Reserved. 
__author__ = 'guoxiaohe@letv.cn'
from crawler_status_service import StatusCollector
from admin_utils import CheckCrawlers
import sys
if __name__ == '__main__':
  sc = StatusCollector()
  adm = CheckCrawlers()
  if len(sys.argv) == 2 and sys.argv[1] == '--help':
    print 'Usage [status_f[status_t]]'
    sys.exit(1)
  if len(sys.argv) == 3:
    print 'reduce'
    a = sc._load_status_from_disk(sys.argv[1])
    b = sc._load_status_from_disk(sys.argv[2])
    diff = adm.status_operater(b, a)
    #print diff
    print '\n'.join(sc.print_res(diff))
  elif len(sys.argv) == 2:
    print 'print %s' % (sys.argv[1])
    a = sc._load_status_from_disk(sys.argv[1])
    #print a
    print '\n'.join(sc.print_res(a))
  else:
    res = sc.print_global()
    print '\n'.join(res)
  #print 'get result:[%s]' % (len(res))
  #sc.print_spiders_status()


