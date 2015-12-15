#-*-coding:utf8-*-
#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.
# encoding = utf8
__author__ = 'guoxiaohe@letv.com'
"""
this pipeline using for fetch content from html
"""
from scrapy import log
from scrapy.selector import Selector

from le_crawler.base.extract_content import ContentExtractor
from le_crawler.base.timestr_parser import  TimestrParser

class ContentExtractorPipeline(object):
  def __init__(self):
    self.spider_ = None
    self.content_extractor = ContentExtractor()
    self.time_parser = TimestrParser()

  def initialize(self):
    pass

  def finalize(self):
    pass

  def open_spider(self, spider):
    self.spider_ = spider

  def close_spider(self, spider):
    pass

  #TODO(xiaohe):remove this ugly code for mtime
  def __extract_mtime_imgs(self, body_html):
    bodyjs = Selector(text = body_html, type = 'html')
    jscode = ''
    for j in bodyjs.xpath('//script[@type="text/javascript"]'):
      jscode += j.xpath('./text()').extract()[0] + ';'
    jslist = jscode.split(';')
    imgs = set()
    for i in jslist: 
      if 'var galleryImages' in i:
        isp = i.find('=', 0)
        if isp >= 0:
          tmpstr = i[isp + 1 :]
          try:
            import json
            jsd = json.loads(tmpstr)
            for im in jsd:
              if 'OriginalPicUrl' in im:
                imgs.update(im.get('OriginalPicUrl'))
              elif 'MiddlePicUrl' in im:
                imgs.update(im.get('MiddlePicUrl'))
              elif 'SmallPicUrl' in im:
                imgs.update(im.get('SmallPicUrl'))
          except Exception, e:
            import traceback
            print traceback.format_exc()
            print  e
            print i
            print tmpstr
            return set()
    return imgs

  def __extract_imgs(self, img_html):
    retimgs = []
    sel = Selector(text = img_html, type = 'html')
    iss = sel.xpath('//img/@src')
    for img_s in iss:
      if img_s:
        tmp = img_s.extract()
        if tmp:
          retimgs.append(tmp)
    return retimgs

  def __dupe_imgs(self, imgs):
    import os
    retimgs = []
    for i in imgs:
      # http://mat1.gtimg.com/ent/dc_ent/img_wm.jpg
      if 'img_wm.jpg' in i:
        continue
      if '/stn/' in i and '_stn.jpg' in i:
        continue
      if '/h180/' in i and '_h180.jpg' in i:
        continue

      ext = os.path.splitext(i)
      if not ext[1] or 'gif' in ext[1].lower():
        continue
      retimgs.append(i)
    return retimgs

  def process_item(self, item, spider):
    imgs = set()
    url = item.get('url', '')
    mtime_site = 'news.mtime.com' in url
    if not mtime_site and 'content_body' in item:
      imgs.update(self.__extract_imgs(item.get('content_body', '')))
    if item.has_key('page'):
      if mtime_site:
        imgs.update(self.__extract_mtime_imgs(item.get('page', ''))
            or self.__extract_imgs(item.get('content_body', '')))
      res = \
            self.content_extractor.extract_with_paragraph(item['page'],
                encode_type = 'utf8')
      if res[-1]:
        item['content_body'] = res[-1]
      if res[0]:
        imgs.update(set(self.__extract_imgs(''.join(res[0]))))
      if res[1]:
        item.setdefault('content_links', []).extend(res[1])
      if not item.has_key('title') and res[2]:
        item['title'] = res[2]
    if imgs:
      imgs = self.__dupe_imgs(imgs)
      item.setdefault('content_imgs', []).extend(imgs)
    self.spider_.log('Got Imgs %s for %s' % (len(imgs), item.get('url', None)), log.INFO)
    self.spider_.log('imgs:%s' % (imgs), log.INFO)
   #TODO(xiaohe): add time parser process
    if item.has_key('article_time_raw'):
      teststr = item['article_time_raw']
      teststr = teststr.replace(' ', ' ')
      nt = self.time_parser.time_stamp(teststr)
      if nt != -1:
        item['article_time'] = '%s' % nt
      else:
        self.spider_.log('Failed Convert TimeStr:%s' % (item['article_time_raw']),
            log.ERROR)
    return item
