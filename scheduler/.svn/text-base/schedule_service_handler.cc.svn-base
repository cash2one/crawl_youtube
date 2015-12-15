// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)
// Description: schedule service main

#include <memory>
#include <string>
#include "third_party/leveldb/include/leveldb/db.h"

#include "base/logging.h"
#include "crawl_db_manager.h"
#include "schedule_service_handler.h"

namespace search2 {
namespace crawler_ver2 {
namespace scheduler {

ScheduleServiceHandler::ScheduleServiceHandler(const std::string& db_dir) {
  db_manager_ = std::shared_ptr<CrawlDBManager>(new CrawlDBManager(db_dir));
}

void ScheduleServiceHandler::get_crawldocs(std::vector<std::vector<std::string>> & _return, const int32_t required_num) {
  LOG(INFO) << "Getting crawl docs, " << required_num;
  _return = db_manager_->GetCrawlDocs(required_num);
}

void ScheduleServiceHandler::set_crawldocs(const std::map<int, std::vector<CrawlDocSlim>> & docs) {
  for (const auto& doc_pair: docs) {
    db_manager_->SetCrawlDocs(doc_pair.first, doc_pair.second);
  }
}

} //namespace scheduler
} //namespace crawler_ver2
} //namespace search2

