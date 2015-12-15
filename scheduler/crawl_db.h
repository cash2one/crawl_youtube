// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)

#ifndef SEARCH2_CRAWLER_VER2_SCHEDULER_CRAWL_DB_H_
#define SEARCH2_CRAWLER_VER2_SCHEDULER_CRAWL_DB_H_

#include <vector>
#include "third_party/leveldb/include/leveldb/db.h"

namespace search2 {
namespace crawler_ver2 {
namespace scheduler {

class CrawlDB {
 public:
  explicit CrawlDB(const std::string& filename);
  virtual ~CrawlDB();

  std::string Get(const std::string& key);
  void Put(const std::string& key, const std::string& value);
  void Del(const std::string& key);
  std::string Pop(const std::string& key);

  std::vector<std::pair<std::string, std::string>> BatchGet(const int batch_num);
  std::vector<std::string> BatchGetValue(const int batch_num);
  void BatchPut(const std::vector<std::pair<std::string, std::string>>& pairs);
  void BatchDel(const std::vector<std::string>& keys);
  std::vector<std::string> BatchPopValue(const int batch_num);

  long long Size();

 private:
  const std::string db_name_;
  leveldb::DB* db_;
};

} //namespace scheduler
} //namespace crawler_ver2
} //namespace search2

#endif

