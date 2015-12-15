#!/usr/bin/env python
#-*-coding:utf-8-*-
#
#Copyright 2014 LeTV Inc. All Right Reserved.
#__auther__='zhaoguozhu@letv.com'

"""
  Calculate timestamp
"""

import re
import sys
#from datetime import timedelta
import time
import string

reload(sys)
sys.setdefaultencoding('utf8')

re_pattn_uslesstail =\
                 re.compile(ur"(.*?)([^\d|年|月|日|小时|分|秒|年前|月前|周前|天前|小时前|分前|秒前]*)$")

re_pattn_onlytime =\
                 re.compile(ur"[^\d]*?((\d+)[小时\s\:　]+)?((\d+)[分\s\:　]*)?((\d+)[秒\s　]*)?$")
re_pattn_normal =\
                 re.compile(ur"[^\d]*?((\d+)[年\-\.\\\/\s　]+)?((\d+)[月\-\.\\\/\s　]+)?((\d+)[日\s　]*)?((\d+)[小时\s\:　]+)?((\d+)[分\s\:　]*)?((\d+)[秒\s　]*)?$")
re_pattn_engstyle =\
                   re.compile(ur"[^\d]*?(january|february|march|april|may|june|july|august|september|october|november|december)+[\s　]+(\d+)[\s　]*,[\s　]*(\d+)[\s　]*(\d+)[小时\-\s\:　]+(\d+)[分\-|\s\:　]+(\d+)[秒\-|\s\:　]*.*")
re_pattn_timeago =\
                  re.compile(ur"[^\d]*?(\d+)[\s　]*(年前|月前|周前|天前|小时前|分前|秒前|years|months|weeks|days|hours|minutes|seconds)+.*")

class TimestrParser(object):
  """
  this is the namespace wrapping the methon calculating time stamp
  """
  def __init__(self):
    self.engmonthlist = {u'january':'1',u'february':'2', u'march':'3', u'april':'4', u'may':'5', u'june':'6',
                         u'july':'7', u'august':'8', u'september':'9', u'october':'10', u'november':'11', u'december':'12',
                         u'jan':'1', u'feb':'2', u'mar':'3', u'apr':'4', u'may':'5', u'jun':'6', u'jul':'7',
                         u'aug':'8', u'sep':'9', u'oct':'10', u'nov':'11', u'dec':'12',}

    self.timedeltaunitlist = {u"年前":0,u"月前":0,u"周前":604800,u"天前":86400,u"小时前":3600,u"分前":60,u"秒前":1,
                              u"years ago":0,u"months ago":0,u"weeks ago":604800,u"days ago":86400,u"hours ago":3600,u"minutes ago":60,u"seconds ago":1}

  def __now_time(self):
    now_time = time.localtime(time.time())
    return now_time

  def __month_before_span(self, timearray, offset):
      if timearray[1] > offset:
        timearray[1] = timearray[1] - offset
      else:
        timearray[1] = timearray[1] + 12 - offset
        timearray[0] = timearray[0] - 1
      return timearray

  def __timestr_format(self, timestr):
    """using re to judge time string format
       and parse each time field for future processing"""
    time_array_parse = ()
    timestr = timestr.strip()
    if not timestr:
      return 0, time_array_parse
    time_array_rematch = re_pattn_engstyle.match(timestr)
    if time_array_rematch is not None:
      time_array_parse = time_array_rematch.groups()
      return 2, time_array_parse
    time_array_rematch = re_pattn_timeago.match(timestr)
    if time_array_rematch is not None:
      time_array_parse = time_array_rematch.groups()
      return 3, time_array_parse
    time_array_rematch = re_pattn_onlytime.match(timestr)
    if time_array_rematch is not None:
      time_array_parse = time_array_rematch.groups()
      return 4, time_array_parse
    time_array_rematch = re_pattn_normal.match(timestr)
    if time_array_rematch is not None:
      time_array_parse = time_array_rematch.groups()
      return 1, time_array_parse
    return 0, time_array_parse

  def __parse_normal_eng_style(self, time_type, time_array_parse):
    """parsing absolute time string, the example patters is as follows:
       "2014-5-19 10:10:10","2014年5月19日 10小时10分10秒","14年5月19日 10小时10分10秒",
       "5月19日 10小时10分10秒","5月19日 10小时10分","May 19,2014 10小时10分10秒",
       "2014年5月19日","14年5月19日","5月19日","10小时10分10秒",
    """
    now_time_struct = self.__now_time()
    now_time_array = [now_time_struct[0],now_time_struct[1],now_time_struct[2],\
                      now_time_struct[3],now_time_struct[4],now_time_struct[5],]
    time_array_list = list(time_array_parse)
    time_array = []
    if time_type == 1:
      if time_array_parse[1] is not None:
        time_array.append(time_array_parse[1])
      else:
        time_array.append('%d'%now_time_array[0])
      if time_array_parse[3] is not None:
        time_array.append(time_array_parse[3])
        time_array.append(time_array_parse[5])
      else:
        time_array.append('%d'%now_time_array[1])
        time_array.append('%d'%now_time_array[2])
      if time_array_parse[7] is not None:
        time_array.append(time_array_parse[7])
        time_array.append(time_array_parse[9])
      else:
        time_array.append('0')
        time_array.append('0')
      if time_array_parse[11] is not None:
        time_array.append(time_array_parse[11])
      else:
        time_array.append('0')
    elif time_type == 4:
      time_array.append('%d'%now_time_array[0])
      time_array.append('%d'%now_time_array[1])
      time_array.append('%d'%now_time_array[2])
      time_array.append(time_array_parse[1])
      time_array.append(time_array_parse[3])
      if time_array_parse[5] is not None:
        time_array.append(time_array_parse[5])
      else:
        time_array.append('0')
    elif time_type == 2:
      for i in self.engmonthlist.keys():
        if time_array_list[0] == i:
          time_array_list[0] = self.engmonthlist[i]
          break
      time_array = [time_array_list[2],] + time_array_list[0:2] +\
                   [time_array_list[3],time_array_list[4],time_array_list[5],]

    time_array_ext = time_array[:] + ['0', '0', '0',]
    time_array_int = []
    for i in time_array_ext:
      time_array_int.append(string.atoi(i))

    if time_array_int[0] < 100:
      if time_array_int[0] <= now_time_array[0]%100:
        time_array_int[0] = time_array_int[0] + 2000
      else:
        time_array_int[0] = time_array_int[0] + 1900
    s_timestamp = int(time.mktime(time_array_int))
    return s_timestamp

#  def __parse_timeago_style(* time_array_parse, * now_time_array, now_time_stamp):
  def __parse_timeago_style(self, now_time_stamp, refer_time_array, time_array_parse):
    """parsing relative time to the time the latenth value is memorized ,the pattern is as follows:
       "5月前","5 dates ago"
    """
    time_span = string.atoi(time_array_parse[0])
    if time_array_parse[1] == u"年前" or time_array_parse[1] == u"years ago":
      time_array = [(refer_time_array[0]-time_span),] +\
                   [refer_time_array[1],refer_time_array[2],refer_time_array[3],refer_time_array[4],refer_time_array[5]]
    elif time_array_parse[1] == u"月前" or time_array_parse[1] == u"montha ago":
      time_array = self.__month_before_span(refer_time_array,time_span)
    else:
      time_delta = time_array_parse[0] * self.timedeltaunitlist[time_array_parse[1]]
      time_before_span = now_time_stamp - time_delta
      return time_before_span

    time_array_ext = time_array[:] + [0,0,0,]
    print time_array_ext
    s_timestamp = int(time.mktime(time_array_ext))
    return s_timestamp

  def time_stamp(self, timestr, timestr_encode = "utf-8", refer_time = None):

    timestr = timestr.lower()
    timestr = timestr.decode(timestr_encode)

    timestr = timestr.strip()
    if not timestr:
      return -1
    uslesstail_rematch = re_pattn_uslesstail.match(timestr)
    if uslesstail_rematch is not None:
      timestr = uslesstail_rematch.groups()[0]
    else:
      return -1

    (time_type, time_array_parse) = self.__timestr_format(timestr)

    if time_type == 0:
      return -1
    elif time_type == 1 or time_type == 2 or time_type == 4:
      s_timestamp = self.__parse_normal_eng_style(time_type, time_array_parse)
    elif time_type == 3:
      if refer_time is not None:
        refer_time_parse = re_pattn_normal.match(refer_time).groups()
        refer_time_array = self.__parse_normal_eng_style(refer_time_parse)
        refer_time_stamp = int(time.mktime(refer_time_array))
      else:
        now_time_struct = self.__now_time()
        refer_time_array = [now_time_struct[0], now_time_struct[1], now_time_struct[2], now_time_struct[3], now_time_struct[4], now_time_struct[5],]
        refer_time_stamp = int(time.mktime(now_time_struct))
      s_timestamp = self.__parse_timeago_style(refer_time_stamp, refer_time_array, time_array_parse)
    return s_timestamp

if __name__ == "__main__":

  now_time_struct = time.localtime(time.time())
  now_time_array = [now_time_struct[0],now_time_struct[1],now_time_struct[2],\
                      now_time_struct[3],now_time_struct[4],now_time_struct[5],]

  time_array_10h_10m_10s = now_time_array[0:3] + [10,10,10] + [0,0,0,]
  time_array_10h_10m = now_time_array[0:3] + [10,10,0] + [0,0,0,]

  timestamp_10h_10m_10s = int(time.mktime(time_array_10h_10m_10s ))
  timestamp_10h_10m = int(time.mktime(time_array_10h_10m ))

  test_timestr = {
                  u"日期：2014-10-4 ":1412352000,
                  u"发表于：2014年5月19日 10小时10分10秒 于北京":1400465410,
                  u"发表于：2014年5月19日 10小时10分10秒":1400465410,
                  "":-1,
                  "hhhkkdsssg- bhkkk5 -bikkkh 19njj ddddjd":-1,
                  "2014 hhhkkdsssg- bhkkk5 -bikkkh 19njj 10:10:10":-1,
                  "2014  5  19 10 10 10":1400465410,
                  "2014 - 5 - 19 10:10:10":1400465410,
                  "2014 .5 . 19 10:10:10":1400465410,
                  "2014 \ 5 \ 19 10:10:10":1400465410,
                  "2014 / 5 / 19 10:10:10":1400465410,
                  "2014年5月19日 10小时10分10秒":1400465410,
                  "14年5月19日 10小时10分10秒":1400465410,
                  "5月19日 10小时10分10秒":1400465410,
                  "5月19日 10小时10分":1400465400,
                  "5月19日　10小时10分":1400465400,
                  " 发表于：May 19, 2014 10小时10分10秒":1400465410,
                  " May 19, 2014 10小时10分10秒":1400465410,
                  "10小时10分10秒":timestamp_10h_10m_10s,
                  "10小时10分":timestamp_10h_10m,
                  "2014年5月19日":1400428800,
                  "14年5月19日":1400428800,
                  "5月19日":1400428800,
                  }

  special_case = [
                  "发表于：5年前",
                  "5年前",
                  " 5 月前",
                  ]
  calc_ts_obj = TimestrParser()
  teststr = '11月03日 09:12'
  teststr = teststr.replace(' ', ' ')
  print calc_ts_obj.time_stamp(teststr)
  for i in test_timestr:
    timestamp = calc_ts_obj.time_stamp(i)
    print 'test:', i
    assert timestamp == test_timestr[i]
  for i in special_case:
    print 'Special:', i, calc_ts_obj.time_stamp(i)

