// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)

#ifndef SEARCH2_CRAWLER_VER2_SCHEDULER_CRAWL_DB_MANAGER_H_
#define SEARCH2_CRAWLER_VER2_SCHEDULER_CRAWL_DB_MANAGER_H_

#include <atomic>
#include <memory>
#include <vector>
#include "third_party/leveldb/include/leveldb/db.h"
#include "crawl_db.h"
#include "search2/crawler_ver2/le_crawler/proto/ScheduleService.h"

namespace search2 {
namespace crawler_ver2 {
namespace scheduler {

class CrawlDBManager {
 public:
  explicit CrawlDBManager(const std::string& db_dir);
  virtual ~CrawlDBManager();
  void SetCrawlDocs(int domain_id, const std::vector<CrawlDocSlim>& docs);
  std::vector<std::vector<std::string>> GetCrawlDocs(const int required_num);
  void GatherStatus();

 private:
  const std::string db_dir_;
  const int DOMAIN_NUM_MAX = 28;
  std::atomic_bool exit_flag_;
  std::vector<std::shared_ptr<CrawlDB>> db_list_;
};

} //namespace scheduler
} //namespace crawler_ver2
} //namespace search2

#endif

