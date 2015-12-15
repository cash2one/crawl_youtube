// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)
// Description: schedule service main

#include <map>
#include <memory>
#include <vector>

#include "crawl_db_manager.h"
#include "search2/crawler_ver2/le_crawler/proto/ScheduleService.h"

namespace search2 {
namespace crawler_ver2 {
namespace scheduler {

class ScheduleServiceHandler : virtual public ScheduleServiceIf {
 public:
  explicit ScheduleServiceHandler(const std::string& db_dir);
  void get_crawldocs(std::vector<std::vector<std::string>>& _return, const int requiret_num);
  void set_crawldocs(const std::map<int, std::vector<CrawlDocSlim>>& docs);

 private:
  std::shared_ptr<CrawlDBManager> db_manager_;
};

} //namespace scheduler
} //namespace crawler_ver2
} //namespace search2
