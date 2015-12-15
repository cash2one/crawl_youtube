#!/bin/env python
# encoding:utf8
# Copyright 2014 LeTV Inc. All Rights Reserved. 
__author__ = 'guoxiaohe@letv.cn'

# using for statistic all the crawler status
import sys
import time
import signal
from admin_utils import *
import cPickle as pickle
import threading
from logutil import Log
import json
from email.mime.text import MIMEText

class StatusCollector(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self._ips = [
        '10.150.140.82',
        '10.150.140.83',
        '10.150.140.84',
        '10.150.140.85',
        '10.150.140.86',
        '10.150.140.87',
        '10.180.155.135',
        '10.180.155.136',
        '10.180.155.137',
        '10.180.155.138',
        '10.180.155.139',
        '10.130.208.60',
        '10.130.208.64',
        '10.130.208.65',
        '10.130.208.66',
        '10.130.208.67',
        ]
    self._ports = [6080, 6081, 6082, 6083, 6084, 6085, 6086, 6087, 6088, 6089,
        6090, 6091, 6092]
    self.collector_ = CheckCrawlers(self._ips, self._ports)
    self.exit_ = False
    self.status_dir_ = '../data/'
    self.send_mail_hour_ = 8
    self.dump_t_ = threading.Thread(target = self.dump_thread, args = ())
    self.send_mail_starup_ = False
    self.vobers_ = False
  def set_send_mail_startup(self, send = True):
    self.send_mail_starup_ = send

  def exit(self, num, frame):
    loger.get_log().info('recv exit cmd')
    print 'recive exit command'
    self.exit_ = True

  def dump_thread(self):
    loger.get_log().info('dump thread is running...')
    #nows = int(time.time())
    #status = self.collector_.get_global_status()
    #filen = self._dump_satus_to_disk(nows, status)
    #loger.get_log().info('dump status to disk[%s]' % (filen))
    while not self.exit_:
      nows = int(time.time())
      # every hour dump
      if (nows % 3600) < 15:
        status = self.collector_.get_global_status()
        filen = self._dump_satus_to_disk(nows, status)
        loger.get_log().info('dump status to disk[%s]' % (filen))
        time.sleep(1)
      time.sleep(1)
    loger.get_log().info('dump thread exit')

  def status_collector_manager(self):
    loger.get_log().info('status collector is running...')
    if self.send_mail_starup_:
      nows = int(time.time())
      ctimr, cst = self.gen_the_day_status(nows - 86400, self.status_dir_)
      gtimr, gst = self.get_the_lastest_global_status(nows, self.status_dir_)
      #self._send_mail(st, nows - 86400, timr)
      #self._send_mail(gst, 0, timr)
      self._send_mail_all(cur_st = cst, glb_st = gst, cur_timr = ctimr, glb_timr =
        gtimr)
    last_send_day = 0
    while not self.exit_:
      nows = int(time.time())
      tms = time.localtime(nows)
      nowh =  tms.tm_hour
      nowd = tms.tm_mday
      if nowh == self.send_mail_hour_ and last_send_day != nowd:
        ctimr, cst = self.gen_the_day_status(nows - 86400, self.status_dir_)
        gtimr, gst = self.get_the_lastest_global_status(nows, self.status_dir_)
        #timr, st = self.gen_the_day_status(nows - 86400, self.status_dir_)
        #timr, gst = self.get_the_lastest_global_status(nows, self.status_dir_)
        #self._send_mail(cst, nows - 86400, ctimr)
        #self._send_mail(gst, 0, gtimr)
        self._send_mail_all(cur_st = cst, glb_st = gst, cur_timr = ctimr, glb_timr =
            gtimr)
        last_send_day = nowd
      time.sleep(1)

  def run(self):
    self.dump_t_.start()
    self.status_collector_manager()
    loger.get_log().error('status collector thread exit with exception')
    self.exit_ = True
    self.dump_t_.join()

  def __send_to_mysql(self, jsonstr):
    pass

  def _send_mail_all(self, cur_st, glb_st, cur_timr, glb_timr):
    if not cur_st or not glb_timr:
      loger.get_log().error('send mail stauts is null, quit! %s, %s' %
          (cur_timr, glb_timr))
      return False
    to_email = 'guoxiaohe@letv.com'
    cc_email = 'sanzhiyuan@letv.com xiezhi@letv.com yulizhu@letv.com search@letv.com'
    #cc_email = ''
    from_email = ''
    subjects = 'Crawler Status[%s]' %(time.strftime('%Y%m%d',
      time.localtime()))
    msg = []
    msg.append('Subject: %s' % (subjects))
    msg.append('From: %s' % (from_email))
    msg.append('To: %s' % (to_email))
    msg.append('Cc: %s' % (cc_email))
    msg.append('Content-Type: text/html')
    msg.append('MIME-Version: 1.0')
    msg.append('\n')
    strc_c, jsdc = self.__gen_mail_content(cur_st, glb_st, cur_timr.replace('.stats',
      ''), glb_timr.replace('.stats', ''))
    #strc_g, jsdg = self.__gen_mail_content(glb_st)
    msg.append(strc_c)
    import commands
    cmd = "echo \"%s\" | sendmail -t" % ('\n'.join(msg))
    status, res = commands.getstatusoutput(cmd)
    if status != 0:
      loger.get_log().error('Error send mail: %s\n%s' % cmd, res)
      return False
    self.__send_to_mysql(jsdc)
    loger.get_log().info('\n%s' % strc_c)

  def _send_mail(self, st, status_time, timr = None):
    subjects = None
    if not st:
      loger.get_log().error('send mail stauts is null, quit! %s' % (timr))
      return False
    if status_time != 0:
      subjects = 'Crawler Status[%s] [%s]' %(time.strftime('%Y%m%d',
        time.localtime(status_time)), timr.replace('.stats', ''))
    else:
      subjects = 'Current Global Status[%s]' % (time.strftime('%Y%m%d',
        time.localtime()))
    loger.get_log().info(subjects)
    loger.get_log().info('send mail...')
    strc, jsd = self.__gen_mail_content(st)
    #msg = MIMEText(strc)
    to_email = 'guoxiaohe@letv.com'
    from_email = ''
    cc_email = ''
    #msg['Subject'] = subjects
    #msg['From'] = 'guoxiaohe@letv.com'
    #msg['To'] = to_email
    msg = []
    msg.append('Subject: %s' % (subjects))
    msg.append('From: %s' % (from_email))
    msg.append('To: %s' % (to_email))
    msg.append('Cc: %s' % (cc_email))
    msg.append('Content-Type: text/html')
    msg.append('MIME-Version: 1.0')
    msg.append('\n')
    msg.append('%s' % (strc))
    try:
      # using sendmail to send email
      import commands
      cmd = "echo \"%s\" | sendmail -t" % ('\n'.join(msg))
      #cmd = "echo '%s' | mail -u guoxiaohe  -s '%s' -c guoxiaohe@letv.com %s" % (strc, subjects, to_email)
      status, res = commands.getstatusoutput(cmd)
      if status != 0:
        loger.get_log().error('Error send mail: %s\n%s' % cmd, res)
        return False
      #s = smtplib.SMTP()
      #s.connect('localhost')
      #s.login('crawler@localhost', 'passwd')
      #s.sendmail('crawler@localhost', to_email, msg.as_string())
      #s.close()

    except Exception, e:
      loger.get_log().info('Error try to send email: %s' % e.message)
      print e
      return False
    self.__send_to_mysql(jsd)
    loger.get_log().info('\n%s' % strc)
    return True

  def smtp_service(self):
    import asyncore
    from smtpd import SMTPServer
    s = SMTPServer(('', 25), None)
    try:
      asyncore.loop()
    except KeyboardInterrrupt:
      pass

  # return a (str, dict)
  def __gen_mail_content(self, st, gst, stimr, gtimr):
    if not st and not gst:
      return None, None
    rets = []
    all_res = {}
    mail_res = {}
    for (key, value) in st.items():
      all_res[key.split('/')[-1]] = value
      if key.startswith('[domain]') and key.endswith('(crawled)'):
        mail_res[key] = value
    tmprets = sorted(mail_res.items(), key=lambda d: d[1], reverse = True)
    for i in tmprets:
       #print i
       rets.append(
           '<tr><td><font size=4 color=\'blue\'  >%-40s</td><td>%-14s<td>%s</td></font></td></tr>'
               % (i[0].replace('[domain]', '').replace('(crawled)', ''), format(i[1], ','), format(gst[i[0]], ',')))
    tablestr = """
    <table border = "1">
    <tr>
    <th><font size=4>Type</font></th><th><font size=4>The
    Day[%s]</font></th><th><font size=4>Global[-%s]</font></th>
    </tr>
    <tr>
    <td><font color = 'red'>Total Crawled</font></td><td>%s</td><td>%s</td>
    </tr>
    <tr>
    <td><font color = 'red'>Discovery Links</font></td><td>%s</td><td>%s</td>
    </tr>
    %s
    </table>
    """ % ( stimr, gtimr,
        format(st['item_scraped_count'], ','),
        format(gst['item_scraped_count'], ','),
        format(st['scheduler/enqueued/redis'], ','),
        format(gst['scheduler/enqueued/redis'], ','),
        '\n'.join(rets))
    all_res['Total Crawled'] = st['item_scraped_count']
    all_res['Discovery Links'] = st['scheduler/enqueued/redis']
    #str1 += '\n\n-----------more details------------\n\n%s' % ('\n'.join(self.collector_.print_res(st)))
    return tablestr, json.dumps(all_res)

  def _dump_satus_to_disk(self, nows, status):
    filen = time.strftime('%Y%m%d_%H%M%S.stats', time.localtime(nows))
    fp = open(os.path.join(self.status_dir_, filen), 'wb')
    pickle.dump(status, fp, 2)
    fp.close()
    return filen

  def _load_status_from_disk(self, filen):
    fp = open(filen, 'rb')
    status = pickle.load(fp)
    return status

  # return status file list
  def __gen_the_day_status_files(self, times, data_dir):
    strprefix = time.strftime('%Y%m%d_', time.localtime(times))
    dayfs = filter(lambda f: f.startswith(strprefix) and f.endswith('stats'), os.listdir(data_dir))
    if not dayfs:
      loger.get_log().error('can not found any file startswith:[%s]' %
          (strprefix))
      return []
    dayfs.sort()
    return dayfs

  # return the time lastest status data
  def get_the_lastest_global_status(self, times, data_dir):
    dayfs = self.__gen_the_day_status_files(times, data_dir)
    if not dayfs:
      return None, None
    loger.get_log().info('using %s gen global status' % (dayfs[-1]))
    return '%s' % (dayfs[-1].split('_')[0]), self._load_status_from_disk(os.path.join(data_dir, dayfs[-1]))

  # return the time first and last diff status
  def gen_the_day_status(self, times, data_dir):
    bfs = self.__gen_the_day_status_files(times, data_dir)
    efs = self.__gen_the_day_status_files(times + 86400, data_dir)
    if not bfs:
      return None, None
    bgf = None
    edf = None
    bgf = bfs[0]
    if not efs and len(bfs) > 1:
      edf = bfs[-1]
    if efs:
      edf = efs[0]
    if bgf and not edf:
      return '%s' % (bgf), self._load_status_from_disk(os.path.join(data_dir,
        bgf))
    loger.get_log().info('using %s and %s to gen status' % (bgf, edf))
    return '%s-%s' % (bgf, edf), self.collector_.status_operater(
        self._load_status_from_disk(os.path.join(data_dir,edf)),
        self._load_status_from_disk(os.path.join(data_dir, bgf))
        )
    
  def print_res(self, status1):
    return self.collector_.print_res(status1)

  def print_global(self):
    status1 = self.collector_.get_global_status()
    strs = self.collector_.print_res(status1)
    return strs

  def print_spiders_status(self):
    status1 = self.collector_.get_spider_status()
    rests = []
    for s in status1:
      rests.append(self.collector_.print_res(s))
    return rests

sts_c = StatusCollector()
def test_exit(sig, fram):
    sts_c.exit()

loger = Log(logf = '../log/status.log')
signal.signal(signal.SIGINT, sts_c.exit)                                           
signal.signal(signal.SIGTERM, sts_c.exit)
if __name__ == '__main__':
  print 'can use sendmail option for send mail on startup service'
  if len(sys.argv) >= 2 and 'sendmail' in sys.argv:
    sts_c.set_send_mail_startup(True)
  #  print 'using [global|details|dump|sendmail] for args'
  #sts_c.print_global()
  sts_c.setDaemon(True)
  sts_c.start()
  while sts_c.isAlive():
    time.sleep(2)
  sts_c.exit(12, None)
  loger.get_log().info('service stoped')
