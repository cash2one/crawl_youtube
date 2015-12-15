#coding=utf-8

import time

def gen_next_schedule_time(crawl_time, content_timestamp, play_total):
  if not crawl_time:
  	return
  if not content_timestamp or content_timestamp > 604800:
  	return
  if not play_total:
  	return
  time_delta = crawl_time - content_timestamp
  if time_delta <= 0:
  	return
  next_delta = None
  now = int(time.time())
  if time_delta < 3600:
    next_delta = 3600
  elif time_delta < 86400:
  	next_delta = time_delta * 60 * 60 / play_total
  	next_delta = max(next_delta, 3600)
  	next_delta = min(next_delta, 43200)
  elif time_delta < 604800:
  	next_delta = time_delta * 60 * 60 * 24 / play_total
  	next_delta = max(next_delta, 86400)
  	next_delta = min(604800)
  if not next_delta:
  	return
  print next_delta
  return now + next_delta

if __name__ == '__main__':
  next_time = gen_next_schedule_time(3900, 1, 1000)
  print 'next_time: ', next_time

