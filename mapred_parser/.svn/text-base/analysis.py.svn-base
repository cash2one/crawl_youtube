#!/usr/bin/python
import sys

def none_status(line, infos, status):
  if line.startswith('Job:'):
    return 'Start'
  return 'None'

def start_status(line, infos, status):
  if line == 'page':
    return 'Page'
  return 'Start'

def page_status(line, infos, status):
  if line.startswith('File '):
    return 'PageEnd'

  (key, num) = line.split('=')
  (web, page_type) = key.split('-', 1)
  if page_type == 'list-url':
    infos.setdefault(web, {})['list-url']=int(num)
  elif page_type == 'video-url':
    infos.setdefault(web, {})['video-url']=int(num)

  return status

def pageend_status(line, infos, status):
  if line == ('parse'):
    return 'Parse'
  return status

def parse_status(line, infos, status):
  if line.startswith('Map-Reduce'):
    return 'ParseEnd'

  (key, num) = line.split('=')
  (web, page_type) = key.split('-', 1)
  if page_type == 'short-url':
    infos.setdefault(web, {})['short-url']=int(num)
  elif page_type == 'list-fail':
    infos.setdefault(web, {})['list-fail']=int(num)
  elif page_type == 'video-fail':
    infos.setdefault(web, {})['video-fail']=int(num)
  elif page_type == 'url-ok':#list-url-ok
    infos.setdefault(web, {})['url-ok']=int(num)

  return status

def list_info(key, info):
  list_url = info.get('list-url', 0)
  list_fail = info.get('list-fail', 0)
  if list_url != 0:
    print '%s list: %.2f [%d/%d]'%(key, list_fail*1.0/list_url, list_fail, list_url)

def video_info(key, info):
  video_url = info.get('video-url', 0)
  video_fail = info.get('video-fail', 0)
  short_url = info.get('short-url', 0)
  if video_url != 0:
    print '%s video: %.2f [%d/%d]'%(key, video_fail*1.0/video_url, video_fail, video_url) 
    print '%s short_video: %d'%(key,short_url)

def print_result(infos):
  for key, info in infos.items():
    list_info(key, info)
    video_info(key, info)

def parseend_status(line, infos, status):
  if len(infos) > 0:
    print_result(infos)
  infos = {}
  return 'None'
    
def main(argv):
  f = open('info.log')
  # status in ['None', 'Start','Page', 'PageEnd', 'Parse', 'ParseEnd']
  status = 'None'
  infos = {}
  for line in f:
    line = line.strip('\t\r\n ' )
    if status == 'None':
      status = none_status(line, infos, status)
      continue
    elif status == 'Start':
      status = start_status(line, infos, status)
      continue
    elif status == 'Page':
      status = page_status(line, infos, status)
    elif status == 'PageEnd':
      status = pageend_status(line, infos, status)
    elif status == 'Parse':
      status = parse_status(line, infos, status)
    elif status == 'ParseEnd':
      status = parseend_status(line, infos, status)

if __name__ == '__main__':
  main(sys.argv)
