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
    url = line.strip()
    exmap =  {}
    urlparse_ret = urlparse.urlparse(url)
    path_list = urlparse_ret.path.strip('/').split('/')
    if not path_list:
      continue
    if 'user' == path_list[0]:
      kind = 'user'
      user = path_list[1].lower()
      exmap = {'kind': 'user', 'user': user}
    elif 'channel' == path_list[0]:
      source_type = 'channel'
      channel = path_list[1]
      exmap = {'kind': 'channel', 'channel': channel}
    if exmap:
      exmap['source'] = 'youtube'
      ret_list.append(exmap)
    else:
      print 'not exmap url:%s' % url
  fp.close()
  return ret_list


if __name__ == '__main__':
  client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')

  db = client.admin
  db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
  collection = db.debug_starturl_info
  from pymongo import IndexModel, ASCENDING, DESCENDING
  #collection.create_index('user', unique=True)
  #collection.create_index('channel', unique=True)
  #collection.drop_indexes()
  ret_list = get_url_map('youtube_channel.cfg')
  for item in ret_list:
    print item
    collection.update({'channel': item['channel']}, {'$set': item}, upsert=True)

