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
import urlparse


def get_url_map(f):
  fp = open(f, 'r')
  ret_list = []
  for line in fp.readlines():
    line = line.strip()
    data = line.split('\t')
    category = data[0]
    url = data[1]
    exmap =  {}
    urlparse_ret = urlparse.urlparse(url)
    path_list = urlparse_ret.path.strip('/').split('/')
    if not path_list:
      continue
    if 'user' == path_list[1]:
      kind = 'user'
      user = path_list[2].lower()
      exmap = {'kind': 'user', 'user': user}
    elif 'channel' == path_list[1]:
      source_type = 'channel'
      channel = path_list[2]
      exmap = {'kind': 'channel', 'channel': channel}
    if exmap:
      exmap['category'] = category
      exmap['source'] = 'socialblade'
      ret_list.append(exmap)
    else:
      print 'not exmap url:%s' % url
  fp.close()
  return ret_list

def get_data(collection, item):
  if item.get('channel', None):
    doc = collection.find({'channel': item['channel']})
    doc = [obj for obj in doc]
    if doc:
      print 'exist start url, item:[%s]' % item
      return doc[0]
    else:
      return []
  elif item.get('user', None):
    doc = collection.find({'user': item['user']})
    doc = [obj for obj in doc]
    if doc:
      print 'exist start url, item:[%s]' % item
      return doc[0]
    else:
      return []
  else:
    print 'not channel or user in item:[%s]' % item
    return None


if __name__ == '__main__':
  client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')

  db = client.admin
  db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
  collection = db.starturl_info
  from pymongo import IndexModel, ASCENDING, DESCENDING
  #collection.create_index('user', unique=True)
  #collection.create_index('channel', unique=True)
  #collection.drop_indexes()
  ret_list = get_url_map('sb_channel.cfg')
  for item in ret_list:
    print item
    if not get_data(collection, item):
      #print 'insert item:', item
      collection.insert(item, continue_on_error=True)

