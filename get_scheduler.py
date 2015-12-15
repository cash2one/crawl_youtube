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
collection = db.debug_schedule_info
#from pymongo import IndexModel, ASCENDING, DESCENDING
#collection.create_index('url', unique=True)


#doc = collection.find({'url': 'https://www.googleapis.com/youtube/v3/videos?part=contentDetails,player,recordingDetails,snippet,statistics,status,topicDetails&id=wXVhUZIpA2Y'})
doc = collection.find()
for obj in doc:
  #print obj['url']
  print obj
  #print str2crawldoc(base64.b64decode(obj['crawl_doc'])) 
  #print str2mediavideo(base64.b64decode(obj['video']))
  break
print collection.count()

