# coding: utf-8

from pymongo import MongoClient

client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')

db = client.admin
db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
collection = db.channel_info



doc = collection.find({})
for obj in doc:
  print obj
  break
print collection.count()
