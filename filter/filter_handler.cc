// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)

#include <memory>
#include <mutex>
#include <bf.h>
#include "filter_handler.h"

namespace search2 {
namespace crawler_ver2 {
namespace filter {

UrlFilterServiceHandler::UrlFilterServiceHandler() {
  filter_ = std::shared_ptr<bf::basic_bloom_filter>(new bf::basic_bloom_filter(0.9999, 1000000000));
}

bool UrlFilterServiceHandler::url_seen(const std::string& url) {
  std::lock_guard<std::mutex> lock(bf_lock_);
  if (filter_->lookup(url)) {
    return true;
  }
  filter_->lookup(url);
  return false;
}

} //namespace filter
} //namespace crawler_ver2
} //namespace search2

