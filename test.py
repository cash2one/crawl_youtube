# coding: utf-8

import base64
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.Thrift import TType
import logging
from le_crawler.proto.crawl.ttypes import CrawlDocType, Request, Response, HistoryItem, CrawlHistory, PageType, LanguageType
from le_crawler.proto.crawl_doc.ttypes import CrawlDoc
from le_crawler.proto.video.ttypes import MediaVideo, State, OriginalUser

from pymongo import MongoClient

client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')

db = client.admin
db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
collection = db.channel_info


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

def str2user(thrift_str):
  if not thrift_str:
    return None
  try:
    trans = TTransport.TMemoryBuffer(thrift_str)
    prot = TBinaryProtocol.TBinaryProtocol(trans)
    thrift_ob = OriginalUser()
    thrift_ob.read(prot)
    thrift_ob.validate()
    return thrift_ob
  except:
    logging.exception('str2mediavideo failed: %s', thrift_str)
    return None

fp = open('user.txt', 'r')
for line in fp:
  data = line.split('\t')[-1]
  user =  str2user(base64.b64decode(data))
  di = {}
  di['channel_id'] = user.channel_id
  category_proportion_list = user.category_proportion_list
  if category_proportion_list:
    category_pro_li = []
    di['category'] = category_proportion_list[0].category
    for category_proportion in category_proportion_list:
      category_pro_li.append({'category': category_proportion.category, 'proportion': category_proportion.proportion})
    di['category_proportion_list'] = category_pro_li

  language_proportion_list = user.language_proportion_list
  if language_proportion_list:
    language_pro_li = []
    di['language'] = LanguageType._VALUES_TO_NAMES.get(language_proportion_list[0].language_type, None)
    for language_proportion in language_proportion_list:
      language_pro_li.append({'language': LanguageType._VALUES_TO_NAMES.get(language_proportion.language_type, None), 'proportion': language_proportion.proportion})
    di['language_proportion_list'] = language_pro_li

  print di
  collection.update({'channel_id': di['channel_id']}, {'$set': di})
  #break

