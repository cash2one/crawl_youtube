// Copyright 2015 LeTV Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com (Xiaohe Guo)

// bloom filter base on redis's setmap, for big data

namespace cpp search2.crawl.util
namespace py le_crawler.proto.util

enum FilterStatus {
  BLOOM_EXIST = 1,
  BLOOM_NOT_EXIST = 2,
  BLOOM_ERROR = 10,
}

service BloomFilterRdService {
  bool ping();
  FilterStatus IsElementPresent(1:string key);
  FilterStatus FillElement(1: string key);
}
