// Copyright 2015 LeTV Inc. All Rights Reserved.
// Author: gaoqiang@letv.com (Qiang Gao)

// this file using for crawler
namespace py le_crawler.proto.filter
namespace cpp search2.crawler_ver2.filter

service UrlFilterService {
  bool url_seen(1:string url);
}

