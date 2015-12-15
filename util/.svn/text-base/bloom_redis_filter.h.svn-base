// Copyright 2015 letv Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com

#ifndef SEARCH2_CRAWLER_VER2_UTIL_BLOOM_REDIS_FILTER_H_
#define SEARCH2_CRAWLER_VER2_UTIL_BLOOM_REDIS_FILTER_H_

#include <string>
#include <utility>
#include <vector>

#include "base/bloom_filter.h"
#include "base/scoped_ptr.h"
#include "search2/crawler_ver2/le_crawler/proto/bloom_redis_filter_types.h"
#include "search2/crawler_ver2/le_crawler/proto/BloomFilterRdService.h"
#include "search2/crawler_ver2/util/object_pool.h"
#include "search2/crawler_ver2/util/redis_client.h"
#include "third_party/hiredis/hiredis.h"

// implements from "base/bloom_filter.h"

namespace search2 {
namespace crawl {
namespace util {

typedef std::string UserId;
typedef uint64 BType;
enum RedisOperType {
  SETBIT = 1,
  GETBIT = 2,
};

class BloomRedisFilter : virtual public BloomFilterRdServiceIf {
 public:
  explicit BloomRedisFilter();
  virtual ~BloomRedisFilter();
  bool ping();
  FilterStatus::type IsElementPresent(const UserId& key);
  FilterStatus::type FillElement(const UserId& key);

 private:
  void MixConnectionNum(const std::vector<std::pair<std::string, int32> >&src,
                        int32 mix_num,
                        std::vector<std::pair<std::string, int32> >* dest);
  bool ParseIpPort(const std::string& flags,
                   std::vector<std::pair<std::string, int32> >* ipps);
  FilterStatus::type RedisBitOper(const UserId& key,
                                  BType offset,
                                  RedisOperType opert);
  BType (*p_hash_f)(const uint8 *buf, size_t len, uint64 iv);

  std::pair<std::string, uint64> CalKeyAndOffset(BType offset);

  BType bit_size_number_;

  scoped_ptr<ObjectPool<RedisClient>> redis_pool_;
  scoped_ptr<base::bloom::Bloom<UserId, BType> > bloom_;
};
} // namespace util
} // namespace crawl
} // namespace search2
#endif  // SEARCH2_CRAWLER_VER2_UTIL_BLOOM_REDIS_FILTER_H_
