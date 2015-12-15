from datetime import datetime

from pycrawler.core.bloom_dupefilter import BloomRedisClient

if __name__ == '__main__':
  client = BloomRedisClient('127.0.0.1', 8099)
  s = 'hw1'
  now = datetime.now()
  print 'fill', s, client.fill_element(s)
  print datetime.now() - now


  s = 'hello world'
  print s, client.is_element_present(s)
  print 'fill', s, client.fill_element(s)
  print s, client.is_element_present(s)
  s = 'key hello world'
  print s, client.is_element_present(s)
  print 'fill', s, client.fill_element(s)
  print s, client.is_element_present(s)
  s = 'hw'
  print s, client.is_element_present(s)
  print 'fill', s, client.fill_element(s)
  print s, client.is_element_present(s)
