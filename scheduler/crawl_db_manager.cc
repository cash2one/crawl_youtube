// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)

#include <algorithm>
#include <chrono>
#include <iterator>
#include <map>
#include <mutex>
#include <memory>
#include <string>
#include <thread>

#include "base/logging.h"
#include "base/string_util.h"
#include "search2/crawler_ver2/scheduler/random.h"
#include "search2/crawler_ver2/scheduler/crawl_db.h"
#include "search2/crawler_ver2/scheduler/crawl_db_manager.h"
#include "search2/crawler_ver2/le_crawler/proto/ScheduleService.h"

namespace search2 {
namespace crawler_ver2 {
namespace scheduler {

CrawlDBManager::CrawlDBManager(const std::string& db_dir): db_dir_(db_dir) {
  exit_flag_ = false;
  leveldb::Options options;
  options.create_if_missing = true;
  for (int domain_id = 0; domain_id < DOMAIN_NUM_MAX + 1; domain_id++) {
    std::shared_ptr<CrawlDB> db(new CrawlDB(db_dir_ + std::to_string(domain_id)));
    db_list_.push_back(db);
  }
  std::thread monitor(&CrawlDBManager::GatherStatus, this);
  monitor.detach();
}

CrawlDBManager::~CrawlDBManager() {
  exit_flag_ = true;
}

void CrawlDBManager::GatherStatus() {
  LOG(INFO) << "monitor started.";
  while (!exit_flag_) {
    int idx = 0;
    LOG(INFO) << "Scheduler details:";
    for (auto db: db_list_) {
      LOG(INFO) << StringPrintf("\t[%-2d]: %lld", idx, db->Size());
      idx++;
    }
    std::this_thread::sleep_for(std::chrono::seconds(60));
  }
  LOG(INFO) << "monitor exit.";
}

std::string CalPriority(const CrawlDocSlim& doc, const int key_len=6) {
  const std::string& priority = std::to_string(doc.priority);
  return std::string(key_len - priority.size(), '0').append(priority);
}

void CrawlDBManager::SetCrawlDocs(int domain_id, const std::vector<CrawlDocSlim>& docs) {
  LOG(INFO) << "Setting crawl docs, " << docs.size();
  if (domain_id < 1 || domain_id > DOMAIN_NUM_MAX) {
    LOG(INFO) << "invalid domain id.";
    return;
  }
  std::vector<std::pair<std::string, std::string>> pairs;
  for (const auto& doc: docs) {
    std::string key = CalPriority(doc);
    pairs.push_back(std::pair<std::string, std::string>(key, doc.crawl_doc));
  }
  db_list_[domain_id]->BatchPut(pairs);
  LOG(INFO) << "Finish set crawl docs, " << docs.size();
}

std::vector<std::vector<std::string>> CrawlDBManager::GetCrawlDocs(const int required_num) {
  std::vector<std::vector<std::string>> result;
  if (!required_num) {
    return result;
  }
  int average = (required_num + db_list_.size() - 1) / db_list_.size();
  int last_spare = 0, total_spare = required_num;
  auto iter = select_randomly(db_list_.begin(), db_list_.end());
  int index = std::distance(db_list_.begin(), iter);
  int initial_index = index;
  while (total_spare) {
    int batch_target = last_spare + average;
    batch_target = std::min(batch_target, total_spare);
    auto data = db_list_[index]->BatchPopValue(batch_target);
    last_spare = batch_target - data.size();
    if (!data.empty()) {
      result.push_back(data);
      total_spare -= data.size();
    }
    index = (index + 1) % db_list_.size();
    if (initial_index == index) {
       break;
    }
  }
  LOG(INFO) << "Got crawl docs actually, " << required_num - total_spare;
  return result;
}

} //namespace scheduler
} //namespace crawler_ver2
} //namespace search2

