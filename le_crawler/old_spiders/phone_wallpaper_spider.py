 #!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
__author__ = 'guoxiaohe@letv.com'

"""
using for spider picture from some mobile site
for phone wall paper, project templore
by now support ilovebizhi, sogou bizhi
"""
import traceback

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy import log

from ..core.items import CrawlerItem, ItemType
from ..base.url_filter import UrlFilter
from le_crawler.common.phone_wallpaper_extractor import PhoneWallPaperExtractor
from le_crawler.base.start_url_loads import StartUrlsLoader
from le_crawler.base.url_normalize import UrlNormalize


#global var
class PhoneWallPaperSpider(Spider):
  name = 'phone_wallpaper_spider'
  allowed_domains = UrlFilter.load_domains('../conf/allowed_domains.cfg')
  start_url_loader = \
  StartUrlsLoader.get_instance('../start_urls/phone_wallpaper.cfg', random_sort
      = True)
  start_urls = start_url_loader.get_start_urls()

  def __init__(self, *a, **kw):
    super(PhoneWallPaperSpider, self).__init__(*a, **kw)
    self.finished_count = 0
    self.start_size = len(PhoneWallPaperSpider.start_urls)
    self.album_extractor = \
        PhoneWallPaperExtractor(self)
    # mock_start_urls = []
    self.mock_start_urls = set()
    self.image_counter = 0
    self.url_normalize = UrlNormalize.get_instance()

  def parse(self, response):
    try:
      url = response.url.strip()
      try:
        page = response.body.decode(response.encoding)
      except UnicodeDecodeError, e:
        page = response.body.decode('utf8')
        self.log('decode with %s error, try utf8 decode' %
            (response.encoding), log.ERROR)
      retre = self.album_extractor.parser_entery_info(url, page)
      if retre:
        self.finished_count += 1
        item_count = 0
        request_count = 0
        if 'items' in retre and retre.get('items', None):
          category_name = retre.get('category', 'nocategory')
          item_count = len(retre['items'])
          self.image_counter += item_count
          for i in retre['items']:
            yield Request(i.get('url'),
                headers = {'Referer':'%s' % (url), 'category': category_name},
                callback = self.image_parse)
          self.log('send image request size %s' % (item_count), log.INFO)
        if 'requests' in retre and retre.get('requests', None):
          request_count = len(retre['requests'])
          for r in retre['requests']:
            if not r or not r.strip():
              continue
            yield Request(r,
                headers={'Referer': '%s' % (url)},
                callback = self.parse)
        print 'Stage1:%s, item:%s, request:%s' % (url, item_count, request_count)
        self.log('Stage1:%s, item:%s, request:%s' % (url, item_count,
          request_count), log.INFO)
    except Exception, e:
      self.log('Exception in Spider:%s, %s' % (e.message,
        traceback.format_exc(), log.ERROR))
      print 'spidere error---------------->:', e
      print traceback.format_exc()
      return

  def image_parse(self, response):
    if response.status == 200:
      url = response.url
      category_name = response.request.headers.get('category', 'nocategory')
      item = CrawlerItem()
      item['url'] = self.url_normalize.get_unique_url(url)
      item['item_type'] = ItemType.IMAGE
      item['source_type'] = category_name
      item['page'] = response.body
      yield item
    else:
      self.log('Image Download Error:%s, %s' % (response.status, response.url),
          log.ERROR)

  def closed(self, reason):
    self.log('Spider image items: %s' %(self.image_counter), log.INFO)

