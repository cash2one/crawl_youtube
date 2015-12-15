# coding: utf-8

from pymongo import MongoClient
import logging
import json



client = MongoClient('10.120.1.61:9220,10.120.1.62:9220,10.120.1.63:9220')

db = client.admin
db.authenticate('admin', 'NzU3ZmU4YmFhZDg')
collection = db.starturl_info
#from pymongo import IndexModel, ASCENDING, DESCENDING
#collection.create_index('url', unique=True)


fp = open('channel.txt', 'w')
fp.write('source\tcategory\tuser\tchannel\tchannel_title\r\n')
doc = collection.find({})
for obj in doc:
  item = '%s\t%s\t%s\t%s\t%s' % (obj.get('source', None), obj.get('category', None),
      obj.get('user', None), obj.get('channel', None), obj.get('channel_title', None))
  #item = obj
  #item.pop('_id')
  #print item
  fp.write(item.encode('utf-8'))
  fp.write('\r\n')
fp.close()
print collection.count()
#collection.remove({})

