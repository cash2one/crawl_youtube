# coding: utf-8

from pymongo import MongoClient
import base64
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.Thrift import TType
import logging
from le_crawler.proto.crawl.ttypes import CrawlDocType, Request, Response, HistoryItem, CrawlHistory, PageType
from le_crawler.proto.crawl_doc.ttypes import CrawlDoc
from le_crawler.proto.video.ttypes import MediaVideo, State, OriginalUser
from le_crawler.common.utils import video_fields


def gen_user_fields():
  data = {}
  for x in OriginalUser.thrift_spec:
    if x:
      data[x[2]] = x[1]
  return data

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


doc = collection.find({})
idx = 0
for obj in doc:
  #print obj['url']
  #print obj
  #print str2crawldoc(base64.b64decode(obj['crawl_doc'])) 
  if obj.get('update_time', 0) > 1445419680 :
    idx += 1
    #print obj
    video = str2mediavideo(base64.b64decode(obj['video']))
    print obj['url']
    for key, type_id in video_fields.items():
      value = getattr(video, key, None)
      if key == 'user':
        print 'user: '
        for user_key, user_type_id in gen_user_fields().items():
          user_value = getattr(value, user_key, None)
          print '\t%s: %s' % (user_key, user_value)
        continue
      print '%s: %s' % (key, value)
    print ''
    print ''
    print ''
    print ''
    if idx > 10:
      break
print collection.count()
