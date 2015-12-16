# coding: utf-8

from pymongo import MongoClient
import base64
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.Thrift import TType
import logging
from le_crawler.proto.crawl.ttypes import CrawlDocType, Request, Response, HistoryItem, CrawlHistory, PageType
from le_crawler.proto.crawl_doc.ttypes import CrawlDoc
from le_crawler.proto.video.ttypes import MediaVideo, State



client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')

db = client.admin
db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
collection = db.channel_info



fp = open('channel_statistics.txt', 'w')
fp.write('channel_id\tchannel_title\tvideo_num\tfans_num\tplay_num\tcountry\tcategory\tlanguage\tcategory_proportion\tlanguage_proportion\r\n')
country_set = set([])
print collection.count()
doc = collection.find({})
doc = collection.find({'channel_id': 'UCJ6iuOEsD8GiDQgjHSKPztQ'})
count = 0
for obj in doc:
  print obj
  channel_id = obj.get('channel_id', None)
  channel_title = obj.get('channel_title', None)
  video_num = obj.get('video_num', None)
  fans_num = obj.get('fans_num', None)
  play_num = obj.get('play_num', None)
  country = obj.get('country', None)
  #category = obj.get('category', None)
  category = None
  category_str = None
  category_li = obj.get('category_proportion_list', None)
  if category_li:
    category = category_li[0]['category']
    category_str = ';'.join(['%s|%s' % (item['category'], item['proportion']) for item in category_li])

  language = obj.get('language', None)
  language_str = None
  language_li = obj.get('language_proportion_list', None)
  if language_li:
    language_str = ';'.join(['%s|%s' % (item['language'], item['proportion']) for item in language_li])

  info = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\r\n' % (channel_id, channel_title, video_num, fans_num, play_num, country, category, language, category_str, language_str)
  fp.write(info.encode('utf-8'))
  count += 1
  # if count > 10:
  #   break
  #print info
  #if obj.get('country', None):
  #  print obj
  #  country_set.add(obj['country'])
    #break
  #break
fp.close()
#print collection.count()
#print country_set
#print 'len: ', len(country_set)
