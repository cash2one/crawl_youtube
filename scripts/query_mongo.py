#!/usr/bin/python
# coding=utf-8
# Copyright 2015 LeTV Inc. All Rights Reserved.
# Author=gaoqiang@letv.com

import json
import sys
from datetime import datetime

from pymongo import MongoClient

def get_mongo():
  client = MongoClient('10.180.91.41:9224,10.180.91.115:9224,10.180.91.125:9224')
  client.admin.authenticate('admin', 'NjlmNTdkNGQ4OWY')
  return client

if __name__ == '__main__':
  client = get_mongo()
  print sys.argv[1]
  data = client.crawl.schedule_info.find({'url': sys.argv[1]}).next()
  data['update_time'] = '%s' % datetime.fromtimestamp(data['update_time'])
  del data['_id']
  print json.dumps(data, sort_keys=True, indent=4)

