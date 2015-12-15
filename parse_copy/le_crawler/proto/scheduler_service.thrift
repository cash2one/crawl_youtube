// Copyright 2015 LeTV Inc. All Rights Reserved.
// Author: gaoqiang@letv.com (Qiang Gao)

// this file using for crawler

include "crawl_doc.def"

namespace py le_crawler.proto.scheduler
namespace cpp search2.crawl


struct CrawlDocSlim {
  1:  optional string                    url;
  2:  optional string                    crawl_doc;
  3:  optional i32                       priority;
}


service ScheduleService {
  list<list<string>> get_crawldocs(1:i32 required_num);
  void set_crawldocs(1:map<string, list<CrawlDocSlim>> docs);
}

