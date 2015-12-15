# encoding: utf8
# author: sanzhiyuan@letv.com
# description: utilities

import os
import re
import uuid
import gzip
import logging
import StringIO
import time
import urllib
import urllib2
import urlparse
import json
import smtplib
from datetime import datetime
from datetime import timedelta
from email.mime.text import MIMEText
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from lxml import etree
from decimal import Decimal

def _cmp(s1, s2):
  try:
    i1 = int(s1)
    i2 = int(s2)
    return i1 - i2
  except:
    if s1 > s2:
      return 1
    elif s1 < s2:
      return -1
    else:
      return 0

def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
      instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance

def enum(**enums):
  return type('Enum', (), enums)

def GetLargestKey(d):
  if len(d) == 0:
    return
  return sorted(d.keys(), cmp=_cmp)[-1]

def GetSmallestKey(d):
  if len(d) == 0:
    return
  return sorted(d.keys(), cmp=_cmp)[0]

def CanonicalizeDict(d):
  ret = {}
  if d is None:
    return ret
  for k, v in d.items():
    ret[k.replace("-", "")] = v
  return ret

def FromStrToDict(s, reversekv=False, valuelist=True, spliter=(';', '|')):
  result = {}
  if not s:
    return result
  for r in s.split(spliter[0]):
    kv = r.split(spliter[1])
    if len(kv) != 2:
      continue
    k, v = kv
    k, v = k.replace("-", "").strip(), v.strip()
    try:
      k = int(k)
    except:
      pass

    if not valuelist:
      if reversekv:
        result[v] = k
      else:
        result[k] = v
      continue

    if reversekv:
      if v not in result:
        result[v] = []
      result[v].append(k)
    else:
      if k not in result:
        result[k] = []
      result[k].append(v)
  return result

def FromDictToStr(d, reverse=False):
  ret = ""
  for k in sorted(d.keys(), cmp=_cmp, reverse=reverse):
    k = k.replace("|", "").replace(";", "") if isinstance(k, basestring) else k
    v = d[k]
    if isinstance(v, list):
      for _v in v:
        if isinstance(_v, basestring):
          _v = _v.replace("|", "").replace(";", "")
        ret += '%s|%s;' % (k, _v)
    else:
      v = v.replace("|", "").replace(";", "")
      ret += '%s|%s;' % (k, v)
  return ret

def Compress(content):
  buf = StringIO.StringIO()
  f = gzip.GzipFile(mode='wb', fileobj=buf)
  f.write(content)
  f.close()
  return buf.getvalue()

def Decompress(buf):
  f = gzip.GzipFile(fileobj=StringIO.StringIO(buf), mode='rb')
  html = f.read()
  f.close()
  return html

def GetCharset(html):
  charset = None
  rules = ["substring-after(/html/head/meta"
           "[contains(@content, 'charset')]/@content, 'charset=')",
           "/html/head/meta/@charset"]
  try:
    for rule in rules:
      datas = etree.HTML(html).xpath(rule)
      if isinstance(datas, str) and len(datas) > 0:
        charset = datas
      elif isinstance(datas, list) and len(datas) > 0 and len(datas[0]) > 0:
        charset = datas[0]
      else:
        continue
      break
  except Exception:
    logging.exception('failed to retrieve charset info')
    return None
  return charset

def formatToUtf8(html):
  charset = GetCharset(html)
  if charset is None:
    return html
  if charset == "utf8" or charset == "utf-8":
    return html
  else:
    return html.decode(charset, "ignore").encode('utf8')


def _fetch_html(url, timeout, check_charset=True, header={}, post_data=None, check_redirect=False):
  def get_charset(s):
    s = s.replace(" ", "").lower()
    index = s.find("charset=")
    if index != -1:
      s = s[index + len("charset="):]
      index = s.find(">")
      if index != -1:
        s = s[:index]
      s = s.strip("\",; /")
      return s
  try:
    req = urllib2.Request(url)
    ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153'
    req.add_header("User-Agent", ua)

    if isinstance(header, dict):
      req.headers.update(header)
    f = urllib2.urlopen(req, data=post_data, timeout=timeout)
    encoding = None
    if "content-encoding" in f.info().dict:
      encoding = f.info().dict["content-encoding"]
    if encoding and encoding != "gzip":
      logging.warning("invalid compress encoding [%s] for url [%s]" % (encoding, url))
      return (None, None) if check_redirect else None
    html = f.read()
    if encoding:
      html = Decompress(html)

    charset = None
    if "content-type" in f.info().dict:
      charset = get_charset(f.info().dict["content-type"])
    if charset is None and check_charset:
      charset = GetCharset(html)
    if charset not in [None, 'utf8', 'utf-8']:
      html = html.decode(charset, "ignore").encode('utf8')
    return (html, f.url) if check_redirect and html else html
  except:
    logging.debug("failed to get html, %s", url)
    return (None, None) if check_redirect else None
  else:
    f.close()

def FetchHTML(url, timeout=30, header={}, data=None, check_redirect=False):
  if not url:
    return (None, None) if check_redirect else None
  for i in range(2):
    ret = _fetch_html(url, timeout, True, header, data, check_redirect)
    if ret:
      return ret
    time.sleep(1)
  logging.debug('failed to get html of url, %s', url)
  return (None, None) if check_redirect else None

def FetchAPI(url, timeout=2, header={}):
  return FetchHTML(url, timeout, header)

def GetLocalIp(ifname):
  import socket, fcntl, struct

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))
  return socket.inet_ntoa(inet[20:24])

def PostImage(source_url, timeout=10):
  def SaveImage(url, timeout):
    try:
      req = urllib2.Request(url)
      f = urllib2.urlopen(req, timeout=timeout)
    except Exception, e:
      logging.error("failed to open url [%s], reason [%s]" % (url, e))
      return None
    import hashlib
    file_name = os.path.join('/tmp', '%s.jpg' % hashlib.md5(url).hexdigest())
    try:
      data = f.read()
      w = open(file_name, 'w')
      w.write(data)
      w.close()
    except Exception, e:
      logging.error("failed to save image, path [%s] reason[%s]" %
                    (file_name, e))
      return None
    return file_name

  def UploadImage(file_name):
    register_openers()
    post_dict = {'username': 'qiaolei',
                 'md5str': 'f4396d1131dc6ed315bfe6782d0a6ae9',
                 'channel': 'search',
                 'compress': '85',
                 'watermark': '0',
                 'single_upload_submit': 'ok',
                 'single_upload_file': open(image_file_name, 'rb')}
    datagen, headers = multipart_encode(post_dict)
    request = urllib2.Request(
      'http://upload2.lelecdn.com:8000/single_upload_tool.php', datagen, headers)
    try:
      resp = urllib2.urlopen(request, timeout=30).read()
    except Exception, e:
      logging.error("failed to upload image, path [%s] reason[%s]" %
                    (file_name, e))
      return None
    return resp

  if not source_url:
    return None

  image_file_name = SaveImage(source_url, timeout)
  if image_file_name is None:
    return None
  resp = UploadImage(image_file_name)
#  try:
#    os.remove(image_file_name)
#  except Exception, e:
#    logging.warning('fail to remove file[%s], reason[%s]' % (image_file_name, e))
  if resp is None:
    return None
  try:
    resp_obj = json.loads(resp)
  except Exception, e:
    logging.error("failed to extract json, string[%s] reason[%s]" %
                  (resp, e))
    return None
  error_code = resp_obj.get('state', -1)
  if error_code in (1, 2):
    return resp_obj.get('file', None)
  else:
    logging.error('failed to upload image, url[%s], error code[%d]' %
                  (source_url, error_code))
    return None

def SendMail(title, content, targets):
  try:
    import os, time

    s1 = "Subject: %s\nTo: %s\nContent-Type: text/html\n%s" % (title, targets, content)
    cmd = "echo '%s' | /usr/sbin/sendmail -t" % s1
    os.system(cmd)
  except Exception, e:
    logging.warning("failed to send mail, reason [%s]" % e)


def send_mail(from_address, to_address, subject, message, headers=None, **kw):
  msg = MIMEText(message)
  msg['Subject'] = subject
  msg['From'] = from_address
  msg['To'] = to_address
  try:
    server = smtplib.SMTP('mail.letv.com')
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()
    print 'send succeed.'
    return True
  except Exception, e:
    #logging.exception('failed to send mail, from: [%s], to: [%s], message: [%s]',
    #                  from_address, to_address, message)
    print 'send mail failed.', e
    return False


def load_object(path, package_len=1):
  path_list = path.split('.')
  try:
    module = '.'.join(path_list[:package_len])
    m = __import__(module)
  except ImportError:
    logging.exception("Error loading object '%s'", module)
    return None
  for name in path_list[1:]:
    try:
      m = getattr(m, name)
    except AttributeError:
      logging.error("Module '%s' doesn't define any object named '%s'",
                    str(m), name)
      return None
  return m


def canonicalize_url(url, keep_blank_values = True, keep_fragments = False):
  """Canonicalize the given url by applying the following procedures:

  - sort query arguments, first by key, then by value
  - percent encode paths and query arguments. non-ASCII characters are
    percent-encoded using UTF-8 (RFC-3986)
  - normalize all spaces (in query arguments) '+' (plus symbol)
  - normalize percent encodings case (%2f -> %2F)
  - remove query arguments with blank values (unless keep_blank_values is True)
  - remove fragments (unless keep_fragments is True)

  The url passed can be a str or unicode, while the url returned is always a
  str.
  """
  if type(url) is unicode:
    url = url.encode('utf8')
  scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
  keyvals = urlparse.parse_qsl(query, keep_blank_values)
  keyvals.sort()
  query = urllib.urlencode(keyvals)
  path = urllib.quote(urllib.unquote(path))
  fragment = '' if not keep_fragments else fragment
  return urlparse.urlunparse((scheme, netloc.lower(), path, params, query, fragment))

def safe_strptime(date_str, format_str):
  try:
    return datetime.strptime(date_str, format_str)
  except ValueError:
    logging.exception('Error occurred when formatting time.')
    return None

def safe_eval(input_str):
  if not input_str:
    return None
  try:
    return eval(input_str, {"__builtins__": None},
                {'false': False, 'true': True, 'null': None})
  except:
    logging.exception('failed to eval string, %s', input_str)
    return None

def safe_call(func, arg):
  if not func or not arg:
    return None
  try:
    return func(arg)
  except:
    logging.exception('failed to call %s, argument: %s', func, arg)
    return None


def strip_unicode_mb4(unicode_str):
  if not isinstance(unicode_str, unicode):
    return unicode_str
  try:
    highpoints = re.compile(u'[\U00010000-\U0010ffff]')
  except re.error:
    # UCS-2 build
    highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
  return highpoints.sub(u'', unicode_str)


def lists2dict(a, b):
  data = {}
  for k, v in zip(a, b):
    data[k] = v
  return data


def run_sql(conn, sql, params=None, need_commit=False, get_last_id=False, fields=None, auto_close=False, logger=None):
  # if fields is not None, return list<dict>
  # if get_last_id is True, return tuple(data/True, lastrowid)
  logger = logger if logger else logging
  succeed = True
  try:
    conn.ping(True, 5, 2)  # check connection first
    cursor = conn.cursor()
  except:
    logger.exception('failed to fetch cursor.')
    return None
  try:
    cursor.execute(sql, params)
    logger.debug('excuting sql: %s', cursor.statement)
    rows = [row for row in cursor]
    if fields:
      rows = map(lambda x: lists2dict(fields, x), rows)
    if cursor.with_rows:
      return rows if not get_last_id else (rows, None)
    elif cursor.rowcount > 0:
      return True if not get_last_id else (True, cursor.lastrowid)
    return True if not get_last_id else (True, None)
  except:
    succeed = False
    logger.exception("failed when executing sql [%s], values: %s", sql, params)
    conn.rollback()
    return None if not get_last_id else (None, None)
  finally:
    if need_commit and succeed:
      conn.commit()
    cursor.close()
    if auto_close:
      conn.close()


def off_shelve(record_id, logger=None):
  if not record_id:
    return False
  off_shelve_api = 'http://10.150.140.87:8088/api/album/disable_video.so?videoId=%s'
  try:
    data = json.loads(FetchHTML(off_shelve_api % record_id))
    if logger:
      logger.error('success off_shelve video, id:%s' % record_id)
    return data['code'] == 1
  except:
    logging.exception('failed to call off shelve api, record_id: %d', record_id)
    return False


def first_or_default(items, predicate=None, default=None):
  if not items:
    return default
  for k in items:
    if not predicate or predicate(k):
      if isinstance(items, dict):
        if not items[k]:
          continue
        return items[k]
      return k
  return default


def atoi(num_str):
  '''
  :param num_str: string like '1.2亿300万400.56', '一点二亿三百万四百点五六', etc
  :return: integer
  '''
  def to_dict(a, b):
    data = {}
    for k, v in zip(a, b):
      data[k] = str(v)
    return data

  if not num_str:
    return None
  if isinstance(num_str, (int, float, long)):
    return num_str
  if not isinstance(num_str, basestring):
    return None
  try:
    return int(num_str)
  except:
    pass

  try:
    num_str = num_str if isinstance(num_str, unicode) \
      else num_str.decode('utf-8', 'ignore')
    num_str = erase_all(num_str, [',', u'，', ' '])
    digit_list = [unicode(i) for i in range(0, 10)]
    digit_list.append(u'.')
    multiple = {u'亿': 100000000, u'万': 10000, u'千': 1000, u'百': 100, u'十': 10}
    digit_map = to_dict(list(u'零一二三四五六七八九'), range(0, 10))
    result = 0
    clip_num = ''
    clip_decimal = None
    skip_multiple = False
    num_len = len(num_str)
    for idx, char in enumerate(num_str):
      if char == u'.' or char == u'点':
        skip_multiple = False
        clip_decimal = ''
        if idx < num_len - 1:
          continue
      if char in digit_list or char in digit_map:
        skip_multiple = False
        char = digit_map[char] if char in digit_map else char
        if clip_decimal is None:
          clip_num += char
        else:
          clip_decimal += char
        if idx < num_len - 1:
          continue
      elif char not in multiple and char not in digit_list:
        return None
      if skip_multiple:
        continue
      factor = 1
      while(idx < num_len and num_str[idx] in multiple):
        factor *= multiple[num_str[idx]]
        idx += 1
        skip_multiple = True
      clip_num = '0' if not clip_num else clip_num
      clip_decimal = '0' if not clip_decimal else clip_decimal
      result += int(clip_num) * factor + \
                int(clip_decimal) * factor * 1.0 / (10 ** len(clip_decimal))
      clip_decimal = None
      clip_num = ''
      result_int = int(result)
    return result_int if result_int == result else result
  except:
    logging.exception('failed to parse string to int/float, %s', num_str)
    return None


def erase_all(string, erase_list, from_idx=0):
  clip = reduce(lambda x, y: x.replace(y, ''), erase_list, string)
  return clip if not from_idx else string[:from_idx] + clip


def replace_all(string, replace_map, from_idx=0):
  clip = reduce(lambda s, k: s.replace(k, replace_map[k]), replace_map, string[from_idx:])
  return clip if not from_idx else string[:from_idx] + clip


def longest_common_substring(s1, s2):
  max_len, start_idx, end_idx = 0, -1, -1
  len_dict = {}
  for i, x in enumerate(s1):
    for j, y in enumerate(s2):
      if x != y:
        len_dict[(i, j)] = 0
        continue
      if i and j:
        cur_len = len_dict[(i, j)] = len_dict[(i - 1, j - 1)] + 1
      else:
        cur_len = len_dict[(i, j)] = 1
      if cur_len > max_len:
        end_idx = i
        max_len = cur_len
  if not max_len:
    return ''
  return s1[end_idx - max_len + 1: end_idx + 1]


def cycle_run(func, seconds=60, times=-1, logger=None):
  # times = -1 -> infinite times
  assert seconds > 0 and times > -2
  if not times:
    return
  logger = logger if logger else logging
  while 1:
    stamp = time.time()
    func()
    used_time = time.time() - stamp

    logger.info('=' * 100)
    msg = 'Job lasts: %s' % timedelta(seconds=int(used_time))
    len_space = (96 - len(msg)) / 2
    logger.info('|*%s%s%s*|', ' ' * len_space, msg, ' ' * (96 - len(msg) - len_space))
    logger.info('=' * 100)

    spare = seconds - used_time
    if spare > 0:
      time.sleep(spare)
    if times == -1:
      continue
    times -= 1
    if not times:
      break


def get_uuid():
  return str(uuid.uuid1()).replace('-', '')


def bat_fetch_data(conn, sql, fields=None, cursor=0, delta=100, oneoff=False, logger=None):
  while 1:
    rows = run_sql(conn, sql % (cursor, delta), fields=fields, logger=logger)
    if not rows:
      raise StopIteration
    cursor += len(rows)
    if logger:
      logger.debug('sql cursor: %s', cursor)
    for row in rows:
      yield row
    if oneoff:
      break


if __name__ == "__main__":
  # print FetchHTML("http://www.fun.tv/vplay/m-105246.e-20130309")
  print canonicalize_url(
    'http://data.vod.itc.cn/?new=/168/249/DJsAvpohuJUDLnGv2l1pH4.mp4&vid=1001317871&plat=(^|&mkey=YTI8Y5HsXC4QFo91PYpEKtvbvvsYApze&ch=v')
  print canonicalize_url(
    'http://k.youku.com/player/getFlvPath/sid/04084020722161286fc4e_00/st/mp4/fileid/030020010050EA4DEF130D05AEBA217AB7789B-12B5-50D5-8EAE-1F8D280779AD?K=7327c1f1d39b6997261dda1c&ctype=12&ev=1&oip=3059483117&token=6042&ep=ciaUEk2NVM4H5yHejj8bbyq0J3NaXP4J9h%2BHgdJjALshSJ3OnUqksZyzTotCE4hsAFMEEeyA2dfgYklmYfFB220Q2k7cPProi4GW5awlzOQCbhkxdcSmwFSYQzTz')
