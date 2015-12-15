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
collection = db.debug_recrawl_page_info



doc = collection.find({})
for obj in doc:
  print obj['url']
  print obj
  #break
print collection.count()
