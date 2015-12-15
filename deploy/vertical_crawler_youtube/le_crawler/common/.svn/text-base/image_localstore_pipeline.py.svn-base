#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
"""
this pipeline process image to store local, 
inheritaned from  ImagesPipeline
"""
import hashlib
from cStringIO import StringIO

from scrapy.http import Request
from scrapy.utils.misc import md5sum
from scrapy.contrib.pipeline.files import FilesPipeline

from le_crawler.core.items import ItemType

class ImageLocalStorePipeline(FilesPipeline):

  def file_downloaded(self, response, request, info):
    path, image_buf = self.get_image(response, request, info)
    image_buf.seek(0)
    checksum = md5sum(image_buf)
    self.store.persist_file(path, image_buf, info)
    return checksum

  def get_image(self, response, request, info):
    if response.status != 200:
      raise Exception('crawled failed for %s [%s]'
          % (request.url, response.status))
    image_buf = StringIO(response.body)
    path = self.file_path(self, request, response, info)
    return path, image_buf


  def get_media_requests(self, item, info):
    if ItemType.IMAGE == item.get('item_type', None):
      return [Request(x,
        headers = {'category' : item.get('source_type', 'nocategory')})
        for x in item.get('content_imgs', [])]

  def item_completed(self, results, item, info):
    return item

  def file_path(self, request, response = None, info = None):
    fpath = request.headers.get('category', 'nocategory')
    guid = hashlib.sha1(request.url).hexdigest()
    return '%s/%s' % (fpath, guid)
