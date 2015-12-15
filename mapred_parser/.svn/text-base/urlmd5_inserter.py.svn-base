import memcache
import hashlib


class UrlMd5Inserter:
  def __init__(self, logger = None):
    self._client = memcache.Client(['127.0.0.1:11213'])
    self._logger = logger


  def insert_urlmd5(self, url):
    if not url:
      return False
    if not isinstance(url, basestring):
      return False
    md5_str = hashlib.md5(url).hexdigest()
    if not self._client.get(md5_str):
      if self._client.set(md5_str, url):
        if self._logger:
          self._logger.info('insert %s %s' % (md5_str, url))
        return True
      else:
        if self._logger:
          self._logger('insert url_md5 failed! %s' % url)
        return False
    else:
      #if self._logger:
        #self._logger('md5 %s already has, url = %s' % (md5_str, url))
      return True
      

if __name__ == '__main__':
  c = UrlMd5Inserter()
  import sys
  if len(sys.argv) == 1:
    print 'need url param!'
  else:
    url = sys.argv[1]
    c.insert_urlmd5(url)
