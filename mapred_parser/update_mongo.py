from pymongo import MongoClient, InsertOne, UpdateOne
from pymongo import IndexModel, ASCENDING, DESCENDING
from le_crawler.common.utils import str2mediavideo, get_video_attr_state
from le_crawler.proto.crawl.ttypes import CrawlStatus
from pymongo.errors import PyMongoError, OperationFailure
import base64
import time
import subprocess
import time
import urllib
from python_library import utils
import logging
from logging.handlers import RotatingFileHandler
import urlparse
from le_crawler.common.domain_parser import query_domain_from_url


log_name = 'update_mongo.error'
handler = RotatingFileHandler(log_name, mode='w', maxBytes=100 * 1024 * 1024, backupCount=2)
formatter = logging.Formatter('[%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger = logging.getLogger(log_name)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

out_final_dir = '/user/search/short_video/out/video/'
fs_cmd = 'hadoop fs %s'
tmp_file = 'temp_unique'
BULK_WRITE_SIZE = 10000

def call_cmd(cmd):
  pro = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  logger.info('call cmd: %s', cmd)
  return pro.returncode, pro.stdout.read()


def get_url_param(url, key):
  if not url or not key:
    return None
  try:
    urlparse_ret = urlparse.urlparse(url)
    url_query = urlparse.parse_qs(urlparse_ret.query)
    value = url_query.get(key, [None])[0]
    return value
  except:
    return None

def gen_youtube_api(url):
  if not url:
    return None
  try:
    urlparse_ret = urlparse.urlparse(url)
    url_query = urlparse.parse_qs(urlparse_ret.query)
    video_id = url_query.get('v', [None])[0]
  except:
    video_id = None
  if not video_id:
    return None
  part = 'contentDetails,player,recordingDetails,snippet,statistics,status,topicDetails'
  api = 'https://www.googleapis.com/youtube/v3/videos?part=%s&id=%s' % (part, video_id)
  return api




def get_files(path, last_time):
  cmd = fs_cmd % '-ls ' + path
  cmd = cmd + ' | tail -500'
  logger.debug('listing files: %s', cmd)
  status, files = call_cmd(cmd)
  if status:
    logger.error('failed to run command [%s]', cmd)
    return []
  if not files:
    logger.info('hadoop input path is empty, [%s]', path)
    return []
  files = files.strip()
  files = [x.split()[-1] for x in files.split('\n')
           if not x.startswith('Found ') and not x.endswith(' items')]
  if path == out_final_dir and last_time:
    for i in range(len(files)-1, -1, -1):
      try:
        update_time = int(files[i].split('/')[-1])
      except:
        logger.info('get file failed, filename is %(filename)s' %{'filename':files[i]})
        continue
      if update_time <= last_time:
        files = files[i+1:]
        break
  logger.info('files in [%s]:\n\t%s', path, files)
  return files


def rm_file(file_path):
  cmd = 'rm ' + file_path
  call_cmd(cmd)


def history2dict(history):
  if not history:
    return None

  h_list = []
  if len(history.crawl_history) > 4:
    del history.crawl_history[3 : -1]
  for item in history.crawl_history:
    d = {}
    d['crawl_time'] = item.crawl_time
    d['crawl_interval'] = item.crawl_interval
    d['play_count'] = item.play_count
    h_list.append(d)
  h_dict = {}
  h_dict['crawl_history'] = h_list
  h_dict['update_time'] = history.update_time
  return h_dict 


def gen_next_schedule_time(crawl_time, content_timestamp, play_total):
  now = int(time.time())
  if not crawl_time:
  	return
  if not content_timestamp or (now - content_timestamp) > 604800:
  	return
  if not play_total:
    if crawl_time - content_timestamp > 0 and crawl_time - content_timestamp < 86400:
  	  return crawl_time + 10800
    else:
      return
  time_delta = crawl_time - content_timestamp
  if time_delta <= 0:
  	return
  next_delta = None
  now = int(time.time())
  if time_delta < 10800:
    next_delta = 3600
  elif time_delta < 86400:
  	next_delta = time_delta * 60 * 60 / play_total / 5
  	next_delta = max(next_delta, 3600)
  	next_delta = min(next_delta, 43200)
  elif time_delta < 604800:
  	next_delta = time_delta * 60 * 60 * 24 / play_total / 5
  	next_delta = max(next_delta, 43200)
  	next_delta = min(next_delta, 604800)
  if not next_delta:
  	return
  return crawl_time + next_delta


def bulk_write_request(requests, collection, ordered=False):
  try:
    result = collection.bulk_write(requests, ordered=ordered)
    logger.info('bulk_write result: upserted=%s matched=%s', result.upserted_count, result.matched_count)
  except OperationFailure, pme:
    logger.exception('update mongo bulk write error.')

def db_videos(file_path, db): 
  collection = db.schedule_info
  recrawl_collection = db.recrawl_page_info
  with open(file_path, 'r') as f:
    requests = []
    recrawl_requests = []
    result = None
    default_status = CrawlStatus._VALUES_TO_NAMES.get(CrawlStatus.EXTRACTED)
    missing_history_cnt = 0

    start_t = time.clock()
    for line in f:
      line = line.strip()
      line_data = line.split('\t')
      if len(line_data) not in [2, 3]:
        logger.error('schedule_info doc error: length of line incorrect.\n%s', line)
        continue
      url = line_data[0]
      base64str = line_data[-1]
      if not url:
        logger.error('schedule_info doc error: missing url.\n%s', line)
        continue
      try:
        thrift_str = base64.b64decode(base64str)
        video = str2mediavideo(thrift_str)
      except:
        logger.error('schedule_info doc error: b64decode or str2mediavideo error. %s', url)
        continue
      if not video:
        continue
      if query_domain_from_url(url) == 'youtube.com':
        url = gen_youtube_api(url)
      doc_id = video.id
      if not doc_id:
        logger.error('schedule_info doc error: missing doc_id. %s', url)
        continue
      if not video.crawl_history or not video.crawl_history.crawl_history:
        missing_history_cnt += 1
        continue
      crawl_history = history2dict(video.crawl_history)
      title = video.title
      content_timestamp = video.content_timestamp
      crawl_time = video.crawl_time
      play_total = video.play_total
      if play_total is None:
        logger.info('not play_total, url:%s, play_total:%s', url, play_total)
        

      update_time = int(time.time())
      attr_state = get_video_attr_state(video)
      time_now = int(time.time())
      # if content_timestamp and (time_now - content_timestamp) < 604800:
      rst_dict = {'doc_id':doc_id, 'url':url, 'crawl_history':crawl_history, 'update_time':update_time,
                  'title':title, 'content_timestamp':content_timestamp, 'status': default_status, 'attr_state': attr_state}
      requests.append(UpdateOne({'url':url}, {'$set':rst_dict}, upsert=True))
      next_schedule_time = gen_next_schedule_time(crawl_time, content_timestamp, play_total)
      if next_schedule_time:
        recrawl_dict = {'url': url, 
                        'crawl_time': crawl_time,
                        'content_timestamp': content_timestamp,
                        'crawl_history': crawl_history,
                        'play_total': play_total,
                        'next_schedule_time': next_schedule_time,
                        'update_time': update_time}
        recrawl_requests.append(UpdateOne({'url': url}, {'$set': recrawl_dict}, upsert=True))
      if len(requests) > BULK_WRITE_SIZE:
        bulk_write_request(requests, collection)
        requests = []
      if len(recrawl_requests) > BULK_WRITE_SIZE:
        bulk_write_request(recrawl_requests, recrawl_collection)
        recrawl_requests = []

    if requests:
      bulk_write_request(requests, collection)
    if recrawl_requests:
      bulk_write_request(recrawl_requests, recrawl_collection)
    logger.info('elapsed time: %s', time.clock() - start_t)
    logger.error('schedule_info doc error: missing crawl_history. count = %s. example below:', missing_history_cnt)


def process_files(collection = None):
  try:
    with open('mongo_last_update_time.txt', 'r') as f:
      line = f.read()
      line = line.strip()
      if line:
        last_time = int(line)
      else:
        last_time = None
  except:
    last_time = None

  try:
    db = None
    if last_time:
      files = get_files(out_final_dir, last_time)
    else:
      logger.info('not init last_time ...')
      return
    if files:
      client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')
      client.admin.authenticate('admin', 'NzU3ZmU4YmFhZDg')
      db = client.admin
      ensure_indexs(db)
    else:
      return

    last_file = None
    for file in files:
      cmd = fs_cmd % '-text ' + file + ' > ' + tmp_file
      logger.info('start processing %s ...' % file)
      status, result = call_cmd(cmd)
      if status:
        logger.info('failed to run command [%s]\n%s', cmd, result)
        continue
      db_videos(tmp_file, db)
      last_file = file
      if last_time and last_file:
        with open('mongo_last_update_time.txt', 'w') as f:
          last_time = last_file.split('/')[-1]
          f.write(last_time)
      logger.info('%s processed.' % file)
    rm_file(tmp_file)
    logger.info('=== job finished. ===')
  except:
    #send_message()
    logger.exception('mongodb exception.')
  finally:
    if db:
      db.logout()


def send_message():
  for tel in ['13426031534', '18515029185', '15330025605']:
    api = 'http://10.182.63.85:8799/warn_messages'
    params = {}
    params['m'] = 'update_mongo exception!'
    params['p'] = tel
    params = urllib.urlencode(params)
    urllib.urlopen("%s?%s" % (api, params))


def ensure_indexs(db):
  collection = db.schedule_info
  recrawl_collection = db.recrawl_page_info
  logger.info('creating indexes...')
  #collection.create_index('url', unique=True)
  #collection.create_index([('update_time', DESCENDING)])
  #collection.create_index([('next_schedule_time', DESCENDING)])
  #recrawl_collection.create_index('url', unique=True)
  #recrawl_collection.create_index([('update_time', DESCENDING)])
  #recrawl_collection.create_index([('next_schedule_time', DESCENDING)])
  logger.info('finish create indexes...')




if __name__ == '__main__':
  try:
    import pymongo
    logger.info('pymongo %s started.', pymongo.version)
    process_files()
  except Exception, e:
    logger.error('mongodb exception: %s', e)
    #utils.send_mail('wangziqing@letv.com', 'wangziqing@letv.com', 'update mongodb failed', str(e))
