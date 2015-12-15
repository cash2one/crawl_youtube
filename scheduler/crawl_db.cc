// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)

#include "base/logging.h"
#include "leveldb/db.h"
#include "leveldb/write_batch.h"
#include "search2/crawler_ver2/scheduler/crawl_db.h"

namespace search2 {
namespace crawler_ver2 {
namespace scheduler {

CrawlDB::CrawlDB(const std::string& filename): db_name_(filename) {
  leveldb::Options options;
  options.create_if_missing = true;
  leveldb::Status status = leveldb::DB::Open(options, db_name_, &db_);
  if (!status.ok()) {
    LOG(ERROR) << "open/create leveldb failed";
  }
}

CrawlDB::~CrawlDB() {
  if (db_) {
    delete db_;
    db_ = nullptr;
  }
}

std::string CrawlDB::Get(const std::string& key) {
  std::string value;
  db_->Get(leveldb::ReadOptions(), key, &value);
  return value;
}

void CrawlDB::Put(const std::string& key, const std::string& value) {
  db_->Put(leveldb::WriteOptions(), key, value);
}

void CrawlDB::Del(const std::string& key) {
  db_->Delete(leveldb::WriteOptions(), key);
}

std::string CrawlDB::Pop(const std::string& key) {
  auto value = this->Get(key);
  this->Del(key);
  return value;
}

std::vector<std::pair<std::string, std::string>> CrawlDB::BatchGet(const int batch_num) {
  std::vector<std::pair<std::string, std::string>> pairs;
  leveldb::Iterator* it = db_->NewIterator(leveldb::ReadOptions());
  for (it->SeekToFirst(); it->Valid(); it->Next()) {
    pairs.push_back(std::pair<std::string, std::string>(it->key().ToString(),
                                                        it->value().ToString()));
  }
  delete it;
  return pairs;
}

std::vector<std::string> CrawlDB::BatchGetValue(const int batch_num) {
  std::vector<std::string> values;
  int spare_num = batch_num;
  leveldb::Iterator* it = db_->NewIterator(leveldb::ReadOptions());
  for (it->SeekToFirst(); it->Valid() && spare_num; it->Next()) {
    values.push_back(it->value().ToString());
    spare_num--;
  }
  delete it;
  return values;
}

long long CrawlDB::Size() {
  leveldb::Iterator* it = db_->NewIterator(leveldb::ReadOptions());
  long long size = 0;
  for (it->SeekToFirst(); it->Valid(); it->Next()) {
    size++;
  }
  return size;
}

void CrawlDB::BatchPut(const std::vector<std::pair<std::string, std::string>>& pairs) {
  leveldb::WriteBatch batch;
  for (const auto& pair: pairs) {
    batch.Put(pair.first, pair.second);
  }
  db_->Write(leveldb::WriteOptions(), &batch);
}

void CrawlDB::BatchDel(const std::vector<std::string>& keys) {
  leveldb::WriteBatch batch;
  for (const auto& key: keys) {
    batch.Delete(key);
  }
  db_->Write(leveldb::WriteOptions(), &batch);
}

std::vector<std::string> CrawlDB::BatchPopValue(const int batch_num) {
  std::vector<std::string> keys, values;
  int spare_num = batch_num;
  leveldb::Iterator* it = db_->NewIterator(leveldb::ReadOptions());
  for (it->SeekToFirst(); it->Valid() && spare_num; it->Next()) {
    keys.push_back(it->key().ToString());
    values.push_back(it->value().ToString());
    spare_num--;
  }
  delete it;
  this->BatchDel(keys);
  return values;
}

} //namespace scheduler
} //namespace crawler_ver2
} //namespace search2

