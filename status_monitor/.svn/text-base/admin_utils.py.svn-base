#!python

__author__ = 'guoxiaohe@letv.cn'

# using for statistic all the crawler status
import os

class CheckCrawlers(object):
  def __init__(self, ips = None, ports = None, debug = True):
    #assert ips and ports, 'ip and port enum must be given'
    self._ips = ips
    #self._ips = ['10.150.140.82',]
    self._ports = ports
    self._bin = 'scrapy-ws.py'
    self._debug = False

  def __gen_cmd(self, args, ip, port):
    cmd = 'python %s %s -H %s -P %s' %(self._bin, args, ip, port)
    #print cmd
    return cmd

  def __exe_cmd_internal(self, cmd):
    try:
      rets = os.popen(cmd).readlines()
      return rets
    except Exception, e:
      print 'Failed Exe %s ' % cmd
      #print e
      return []

  # return [[key, cmd],[key, cmd],]
  def __gen_batch_cmd(self, args):
    rets = []
    for ip in self._ips:
      for port in self._ports:
        rets.append(['%s:%s' %(ip, port), self.__gen_cmd(args, ip, port)])
    rets.sort()
    return rets

  # args: 
  def __exe_batch_internal(self, args):
    rets = []
    cmds = self.__gen_batch_cmd(args)
    ind = 0
    lens = len(cmds)
    for cmd in cmds:
      ind += 1
      print '%-3d/%d %s'% (ind, lens, cmd[0])
      if self._debug:
        print ' doing [%s]' %(cmd[1])
      sttmp  =  self.__exe_cmd_internal(cmd[1])
      if sttmp:
        rets.append(sttmp)
      else:
        print 'bad result:[%s]' % (cmd[0])
    rets.sort()
    return rets

  def _parse_line(self, line):
    tmp = line.split()
    if len(tmp) < 2:
      print 'can not parser line:%s' % line
      return None, None
    else:
      return tmp[0], ' '.join(tmp[1:])

  def __is_digital(self, value):
    try:
      int(value)
      return True
    except:
      return False

  # parser cmd result return dict
  def _parser_result(self, results):
    if not results:
      return None
    res_dict = {}
    for peer in results:
      for line in peer:
        key, value = self._parse_line(line)
        #print '%s, %s' %(key, value)
        if not key:
          continue
        if '(crawled)' in key:
          key = '[domain]%s' % key

        #print '%s, %s' %(key, value)
        if res_dict.has_key(key):
          #print '%s, %s' %(key, res_dict[key])
          if self.__is_digital(res_dict[key]):
            res_dict[key] += int(value)
          else:
            res_dict[key] = '%s' %(value)
        elif value.isdigit():
          res_dict[key] = int(value)
        else:
          res_dict[key] = value
    return res_dict

  # print format status
  def print_res(self, results):
    retstr = []
    if not results:
      return None
    res = sorted([(k, v) for k, v in results.items()])
    for (k,v) in res:
      retstr.append('%-60s\t%s' %(k, v))
    return retstr

# return stats_cur - stats_pre, oper can be add or reduce
  def status_operater(self, stats_cur, stats_pre, oper = "reduce"):
    if not stats_cur or not stats_pre:
      return stats_cur or stats_pre
    allkeys = stats_cur.keys() + stats_pre.keys()
    resd = {}
    for k in allkeys:
      if stats_cur.has_key(k) and stats_pre.has_key(k):
        vcur = stats_cur[k]
        vpre = stats_pre[k]
        if self.__is_digital(vcur) and self.__is_digital(vpre):
          if oper == 'reduce':
            resd[k] = int(vcur) - int(vpre)
            if int(resd[k]) < 0:
              resd[k] = 0
          else:
            resd[k] = int(vcur) + int(vpre)
        else:
          resd[k] = str('%s|%s' %(vcur, vpre))
    return resd

  # get global status , return dict
  def get_global_status(self):
    results = self.__exe_batch_internal('get-global-stats')
    print 'Got results[%d]' % (len(results))
    return self._parser_result(results)

  # return each spider status, format a list
  def get_spider_status(self):
    args = 'get-spider-stats video_crawler'
    cmds = self.__gen_batch_cmd(args)
    if not cmds:
      return None
    retsdict = []
    for cmd in cmds:
      print '[%s]:' % cmd[0]
      tmpresult = self.__exe_cmd_internal(cmd[1])
      retsdict.append(self.parser_result([tmpresult]))

