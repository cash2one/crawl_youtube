// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)

#include <iostream>
#include <string>

#include "log4cplus/configurator.h"
#include "log4cplus/logger.h"
#include "log4cplus/loggingmacros.h"

#include "crawl_db.h"

using log4cplus::PropertyConfigurator;
using search2::crawler_ver2::scheduler::CrawlDB;

void PrintValues(int num, CrawlDB& db) {
  std::vector<std::string> values(db.BatchGetValue(num));
  for (auto& value: values) {
    std::cout << value << std::endl;
  }
}

int main() {
  PropertyConfigurator::doConfigure("log.conf");
  CrawlDB db("databases/test");
  std::vector<std::pair<std::string, std::string>> pairs;
  // for (int i = 0; i < 10; i++) {
  //   pairs.push_back(std::pair<std::string, std::string>(std::to_string(i), std::to_string(i)));
  // }
  db.BatchPut(pairs);
  PrintValues(4, db);
  std::cout << "=============" << std::endl;
  std::vector<std::string> values2(db.BatchPopValue(4));
  for (auto& value: values2) {
    std::cout << value << std::endl;
  }
  std::cout << "=============" << std::endl;
  PrintValues(10, db);
  std::cout << "=============" << std::endl;
  // std::vector<std::string> values3(db.BatchPopValue(20));
  // for (auto& value: values3) {
  //   std::cout << value << std::endl;
  // }
  return 0;
}

