// Copyright 2014 LeTV Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com (Xiaohe Guo)
// for remote sharedb rpc

namespace py pycrawler.sharedb

service ShareDBService {
  bool ping();
  bool db_put(1:string key, 2:string value);
  string db_get(1:string key);
  bool batch_put(1:list<string> keys, 2:list<string> values);
  list<string> batch_get(1:list<string> keys);
  void db_delete(1:string key);
  }
