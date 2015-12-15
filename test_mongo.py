# coding: utf-8

from pymongo import MongoClient
import logging
try:
  import cPickle as pickle
except:
  import pickle



client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')

db = client.admin
db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
collection = db.test_info
#from pymongo import IndexModel, ASCENDING, DESCENDING
#collection.create_index('url', unique=True)


di = {'name': u'赵锦城'}
print di
p_tr = pickle.dumps(di)
#p_tr = p_tr.decode('utf-8')

collection.save({'ptr': p_tr})

doc = collection.find({})
for obj in doc:
  print obj
  print pickle.loads(obj['ptr'].encode('utf-8'))
  #break
print collection.count()
#collection.remove({})

