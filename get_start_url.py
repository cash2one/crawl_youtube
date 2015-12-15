# coding: utf-8

from pymongo import MongoClient
import logging



client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')

db = client.admin
db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
collection = db.debug_starturl_info
#from pymongo import IndexModel, ASCENDING, DESCENDING
#collection.create_index('url', unique=True)


doc = collection.find({})
for obj in doc:
  print obj
  #break
print collection.count()
#collection.remove({})

