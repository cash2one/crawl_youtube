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


def str2crawldoc(thrift_str):
  if thrift_str is None:
    return None
  try:
    trans = TTransport.TMemoryBuffer(thrift_str)
    prot = TBinaryProtocol.TBinaryProtocol(trans)
    thrift_ob = CrawlDoc()
    thrift_ob.read(prot)
    thrift_ob.validate()
    return thrift_ob
  except:
    logging.exception('str2thrift failed: %s', thrift_str)
  return None

def str2mediavideo(thrift_str):
  if not thrift_str:
    return None
  try:
    trans = TTransport.TMemoryBuffer(thrift_str)
    prot = TBinaryProtocol.TBinaryProtocol(trans)
    thrift_ob = MediaVideo()
    thrift_ob.read(prot)
    thrift_ob.validate()
    return thrift_ob
  except:
    logging.exception('str2mediavideo failed: %s', thrift_str)
    return None

client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')

db = client.admin
db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
collection = db.doc_info
from pymongo import IndexModel, ASCENDING, DESCENDING
collection.create_index('url', unique=True)

index_info = collection.index_information()
print index_info


doc = collection.find({})
for obj in doc:
  #print obj['url']
  #print obj
  #print str2crawldoc(base64.b64decode(obj['crawl_doc'])) 
  if obj.get('update_time', 0) > 1445419680:
    print obj
    video = str2mediavideo(base64.b64decode(obj['video']))
    print str2mediavideo(base64.b64decode(obj['video']))
    print video.player
    print '%s\t%s' % (obj['url'], obj.get('update_time', 0))
    break
#print collection.count({'update_time': {'$lt': 1445419680}})
#print collection.count({'update_time': {'$gt': 1445419680}})
print collection.count()
doc = collection.find({'url': 'https://www.youtube.com/watch?v=qZSWkX4n-jc'})
for obj in doc:
  print obj
  print str2crawldoc(base64.b64decode(obj['crawl_doc']))
  video = str2mediavideo(base64.b64decode(obj['video']))
  print str2mediavideo(base64.b64decode(obj['video']))
  print video.player
