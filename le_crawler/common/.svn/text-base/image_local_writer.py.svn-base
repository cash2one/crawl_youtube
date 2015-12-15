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

from scrapy.contrib.pipeline.files import FSFilesStore
from scrapy.utils.project import get_project_settings

from le_crawler.core.items import ItemType
from le_crawler.core.page_writer import PageWriterWithBuff

class ImageLocalWriter(PageWriterWithBuff):
  def __init__(self, spider, bufsize = 10240, *kargs, **kwargs):
    super(ImageLocalWriter, self).__init__(spider, bufsize)
    self.set_name('ImageLocalStorePipeline')
    basepath = get_project_settings()['FILES_STORE']
    self.store = FSFilesStore(basepath)
    self.image_writer_num = 0

  def writer(self, item):
    if item.get('item_type', 0) == ItemType.IMAGE and item.get('page', None):
      fpath = self._file_path(item)
      image_buf = StringIO(item['page'])
      self.store.persist_file(fpath, image_buf, None)
      self.image_writer_num += 1

  def _file_path(self, item):
    import os
    ext = os.path.splitext(item['url'])[1]
    fpath = item.get('source_type', 'nocategory')
    guid = hashlib.sha1(item['url']).hexdigest()
    return '%s/%s%s' % (fpath, guid, ext)

  def status(self):
    return super(ImageLocalWriter, self).status() \
        + ', Image Total Write:%s' % self.image_writer_num
