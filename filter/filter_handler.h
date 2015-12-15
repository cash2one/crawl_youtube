// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)

#include <mutex>
#include <bf.h>
#include "search2/crawler_ver2/le_crawler/proto/UrlFilterService.h"

using boost::shared_ptr;

using namespace  ::search2::crawler_ver2::filter;

namespace search2 {
namespace crawler_ver2 {
namespace filter {

class UrlFilterServiceHandler : virtual public UrlFilterServiceIf {
 public:
  UrlFilterServiceHandler();
  bool url_seen(const std::string& url);

 private:
  std::mutex bf_lock_;
  std::shared_ptr<bf::basic_bloom_filter> filter_;
};

} //namespace filter
} //namespace crawler_ver2
} //namespace search2

