import memcache
import hashlib
import urllib


class UrlMd5Inserter:
  def __init__(self, logger = None):
    self._client = memcache.Client(['127.0.0.1:11211'])
    self._logger = logger
    self._miss_count = 0
    self._has_send_message = False


  def send_message(self):
    for tel in ['13426031534', '18515029185', '15330025605']:
      api = 'http://10.182.63.85:8799/warn_messages'
      params = {}
      params['m'] = 'insert md5 failed in lejian crawler.'
      params['p'] = tel
      params = urllib.urlencode(params)
      urllib.urlopen("%s?%s" % (api, params))


  def insert_urlmd5(self, url):
    if not url:
      return False
    if not isinstance(url, basestring):
      return False
    md5_str = hashlib.md5(url).hexdigest()
    if not self._client.get(md5_str):
      if self._client.set(md5_str, url):
        self._miss_count = 0
        if self._logger:
          self._logger.debug('insert %s %s' % (md5_str, url))
        return True
      else:
        self._miss_count += 1
        if not self._has_send_message and self._miss_count > 5:
          self.send_message()
          self._has_send_message = True
        if self._miss_count < 5 or self._miss_count & 1023 == 0:
          self._client = memcache.Client(['127.0.0.1:11211'])
          if self._client.set(md5_str, url):
            return True
        if self._logger:
          self._logger.error('insert url_md5 failed! %s' % url)
        return False
    else:
      # if self._logger:
      #   self._logger.info('md5 %s already has, url = %s' % (md5_str, url))
      return True


if __name__ == '__main__':
  c = UrlMd5Inserter()
  import sys
  if len(sys.argv) == 1:
    print 'need url param!'
  else:
    url = sys.argv[1]
    c.insert_urlmd5(url)
