// Copyright 2015 letv Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com


#include <signal.h>

#include "thrift/concurrency/PosixThreadFactory.h"
#include "thrift/concurrency/ThreadManager.h"
#include "thrift/protocol/TCompactProtocol.h"
#include "thrift/server/TThreadPoolServer.h"
#include "thrift/server/TNonblockingServer.h"
#include "thrift/transport/TBufferTransports.h"
#include "thrift/transport/TServerSocket.h"
#include "glog/logging.h"

// #include "base/flags.h"
// #include "base/logging.h"
#include "base/string_util.h"
#include "search2/util/global_init.h"
#include "search2/crawler_ver2/util/bloom_redis_filter.h"
//  if max_elements_number is set to 10000000000, positive_false iset to 0.0001
//  will cost 287551751321 bit numbers, redis bitmap limited to 523M 2 ^ 32;
//  that is to say will cost 287551751321 / 2 ^ 32 keys; every key  will cost 512M
//  so the total cost memery is 66 * 512M = 34G

DEFINE_uint64(max_elements_number, 100000000, "this max number of elements");
DEFINE_double(positive_false, 0.01, "this positive false expect");
DEFINE_string(redis_ipport, "10.150.140.84:6379", "redis ip, split by like ip1:port1;ip2:port2");
DEFINE_string(bloom_key, "short_video_dedup", "the key will be set");
DEFINE_int32(thread_num, 10, "redis connection num");
DEFINE_int32(io_thread_num, 4, "redis connection num");
DEFINE_int32(port, 8099, "the service port");
DEFINE_int32(connection_dupe_num, 20, "redis connection for per ip");

namespace search2 {
namespace crawl {
namespace util {
using apache::thrift::TProcessor;
using apache::thrift::concurrency::PosixThreadFactory;
using apache::thrift::concurrency::ThreadManager;
using apache::thrift::protocol::TProtocolFactory;
using apache::thrift::protocol::TCompactProtocolFactory;
using apache::thrift::transport::TServerTransport;
using apache::thrift::transport::TServerSocket;
using apache::thrift::transport::TTransportFactory;
using apache::thrift::transport::TBufferedTransportFactory;
using apache::thrift::server::TServer;
using apache::thrift::server::TNonblockingServer;
using apache::thrift::server::TThreadPoolServer;

using std::string;
using std::vector;
using std::pair;
using base::bloom::Bloom;
using base::bloom::FNV;
using base::bloom::FNVHash;

uint64 REDIS_BIT_MAX_LEN = 4294967296; // redis bit operation limit 2 ^ 32,
// bitmap cost 512M

BloomRedisFilter::BloomRedisFilter() {
  CHECK_GT(FLAGS_max_elements_number, 10001)
      << "Max elements must be set big than 10000";
  bloom_.reset(new Bloom<UserId, BType>(FLAGS_max_elements_number,
                                        FLAGS_positive_false,
                                        FNV<BType>::INIT,
                                        &FNVHash));
  p_hash_f = &FNVHash;
  // vector<pair<string, int32> > ipplst;
  // vector<pair<string, int32> > dest_list;
  // CHECK(ParseIpPort(FLAGS_redis_ipport, &ipplst)) << "Failed parse ip and port for redis";
  LOG(INFO) << "Create bloom redis service: "
      << "\nmax_elements_number:" << FLAGS_max_elements_number
      << "\npositive_false:" << FLAGS_positive_false
      << "\nredis_ip:" << FLAGS_redis_ipport
      << "\nbloom_key:" << FLAGS_bloom_key
      << "\n--------------------------"
      << "\nbit_nums:" << bloom_->getBitsNumber()
      << "\nbytes:" << bloom_->getBytesNumber()
      << "\nmin_hash_fnumber:" << bloom_->getMinHashFNumber();
  bit_size_number_ = bloom_->getBitsNumber();
  // MixConnectionNum(ipplst, FLAGS_connection_dupe_num, &dest_list);
  string ip = "10.150.140.84";
  redis_pool_.reset(new ObjectPool<RedisClient>(50, ip, 6379));
  LOG(INFO) << "Service begin listen:" << FLAGS_port;
}

void BloomRedisFilter::MixConnectionNum(const vector<pair<string, int32> >&src,
                                        int32 mix_num,
                                        vector<pair<string, int32> >* dest) {
  for (vector<pair<string, int32> >::const_iterator it = src.begin();
       it != src.end(); ++it) {
    for (int32 i = 0; i < mix_num; ++i) {
      dest->push_back(*it);
    }
  }
  LOG(INFO) << "connection num size:" << dest->size();
}

std::pair<string, uint64> BloomRedisFilter::CalKeyAndOffset(BType offset) {
  uint64 key_idx = offset / REDIS_BIT_MAX_LEN;
  uint64 uofset = offset % REDIS_BIT_MAX_LEN;
  VLOG(3) << "offset:" << offset << " key_idx:" << key_idx
      << " key_offset:" << uofset;
  return pair<string, uint64>(StringPrintf("%s_%lu",
                                           FLAGS_bloom_key.c_str(), key_idx),
                              uofset);
}

bool BloomRedisFilter::ParseIpPort(const string& flags,
                                   vector<pair<string, int32> >* ipps) {
  CHECK(!flags.empty()) << "redis ip and port is empty!";
  vector<string> tmpipp;
  SplitString(flags, ';', &tmpipp);
  CHECK(!tmpipp.empty()) << "parse  ip port failed!";
  for (vector<string>::const_iterator it = tmpipp.begin();
       it != tmpipp.end(); it++) {
    vector<string> tmppair;
    int32 port = 0;
    SplitString(*it, ':', &tmppair);
    if (tmppair.size() != 2 || !StringToInt(tmppair[1], &port)) {
      LOG(ERROR) << "Parse " << *it << " failed";
      continue;
    }
    ipps->push_back(pair<string, int32>(tmppair[0], port));
  }
  return !ipps->empty();
}

BloomRedisFilter::~BloomRedisFilter() {}

bool BloomRedisFilter::ping() {
  return true;
}

FilterStatus::type BloomRedisFilter::IsElementPresent(const UserId& key) {
  uint64 vi = FNV<BType>::INIT;
  uint64 offset_size = vi + bloom_->getMinHashFNumber();
  FilterStatus::type status = FilterStatus::BLOOM_EXIST;
  for (uint64 i = vi; i < offset_size; ++i) {
    BType hash = (*p_hash_f)(reinterpret_cast<const uint8*>(key.c_str()),
                             key.length(), i);
    BType boffset = hash % bit_size_number_;
    status = RedisBitOper(FLAGS_bloom_key, boffset, GETBIT);
    if (FilterStatus::BLOOM_NOT_EXIST == status ||
        FilterStatus::BLOOM_ERROR == status) {
      break;
    }
  }
  VLOG(2) << "get key:" << key << " , " << status;
  return status;
}

FilterStatus::type BloomRedisFilter::FillElement(const UserId& key) {
  uint64 vi = FNV<BType>::INIT;
  uint64 offset_size = vi + bloom_->getMinHashFNumber();
  FilterStatus::type status = FilterStatus::BLOOM_EXIST;
  for (uint64 i = vi; i < offset_size; ++i) {
    BType hash = (*p_hash_f)(reinterpret_cast<const uint8*>(key.c_str()), key.length(), i);
    BType boffset = hash % bit_size_number_;
    status = RedisBitOper(FLAGS_bloom_key, boffset, SETBIT);
    VLOG(3) << "setbit boffset return:" << status;
    if (FilterStatus::BLOOM_NOT_EXIST == status) {
      status = FilterStatus::BLOOM_NOT_EXIST;
    } else if (FilterStatus::BLOOM_ERROR == status) {
      LOG(ERROR) << "Failed redis bit operation:" << key << ", " << boffset;
      break;
    }
  }
  VLOG(2) << "set key:" << key << " , " << status;
  return status;
}

FilterStatus::type BloomRedisFilter::RedisBitOper(const UserId& key,
                                                  const BType offset,
                                                  const RedisOperType opert) {
  VLOG(4) << "redis operation:" << key << " ," << offset << " ," << opert;
  auto client = redis_pool_->Get();
  if (!client) {
    LOG(ERROR) << "Failed get redis client";
    return FilterStatus::BLOOM_ERROR;
  }
  redisReply* response = NULL;
  pair<string, uint64> redis_par = CalKeyAndOffset(offset);
  if (GETBIT == opert) {
    string cmd = StringPrintf("GETBIT %s %lu",
                              redis_par.first.c_str(),
                              redis_par.second);
    VLOG(4) << cmd;
    response = static_cast<redisReply*>(
        redisCommand(client->client, cmd.c_str()));
  } else if (SETBIT == opert) {
    string cmd = StringPrintf("SETBIT %s %lu 1",
                              redis_par.first.c_str(),
                              redis_par.second);
    VLOG(4) << cmd;
    response = static_cast<redisReply*>(
        redisCommand(client->client, cmd.c_str()));
  }
  FilterStatus::type ret = FilterStatus::BLOOM_NOT_EXIST;
  if (response == NULL)
    ret = FilterStatus::BLOOM_ERROR;
  else if (response->type == REDIS_REPLY_ERROR) {
    LOG(ERROR) << "GetBit error:" << response->str;
    ret = FilterStatus::BLOOM_ERROR;
  } else if (response->type == REDIS_REPLY_INTEGER) {
    VLOG(3) << "response:" << offset << " , " << response->integer;
    if (response->integer == 1)
      ret = FilterStatus::BLOOM_EXIST;
    else
      ret = FilterStatus::BLOOM_NOT_EXIST;
  } else {
    LOG(ERROR) << "response type un-catched:" << response->type;
  }
  // if (ret != FilterStatus::BLOOM_ERROR) {
  //   redis_pool_->SetNodeIdle(client);
  // } else {
  //   LOG(ERROR) << "redis node is failed:"
  //       << &client << " ip:" << client->ip
  //       << ", port:" << client->port;
  //   redis_pool_->SetNodeFailed(client);
  // }
  if (response) freeReplyObject(response);
  return ret;
}

class MyServer {
 public:
  MyServer() {}

  void Init() {
    boost::shared_ptr<BloomRedisFilter> handler(new BloomRedisFilter());
    boost::shared_ptr<TProcessor> processor(new BloomFilterRdServiceProcessor(handler));
    boost::shared_ptr<TProtocolFactory> protocolFactory(new TCompactProtocolFactory());
    boost::shared_ptr<ThreadManager> threadManager = ThreadManager::newSimpleThreadManager(FLAGS_thread_num);
    boost::shared_ptr<PosixThreadFactory> threadFactory = boost::shared_ptr<PosixThreadFactory>(new PosixThreadFactory());
    threadManager->threadFactory(threadFactory);
    threadManager->start();
    server_.reset(new TNonblockingServer(processor, protocolFactory, FLAGS_port, threadManager));
    server_->setNumIOThreads(FLAGS_io_thread_num);
  }

  void Run() {
    LOG(INFO) << "starting service...";
    server_->serve();
  }

  void Stop() {
    server_->stop();
  }

 private:
   scoped_ptr<TNonblockingServer> server_;
   // scoped_ptr<TThreadPoolServer> server_;
};

}  // namespace util
}  // namespace crawl
}  // namespace search2

search2::crawl::util::MyServer server;
void my_signal_handler(int sig) {
  LOG(INFO) << "recive service stop command";
  server.Stop();
  LOG(INFO) << "end stop receive";
}

int main(int argc, char** argv) {
  search2::util::GlobalInit init(&argc, &argv);
  struct sigaction act;
  act.sa_handler = my_signal_handler;
  sigemptyset(&act.sa_mask);
  act.sa_flags = 0;
  sigaction(SIGINT, &act, NULL);
  sigaction(SIGTERM, &act, NULL);
  signal(SIGPIPE, SIG_IGN);
  server.Init();
  server.Run();
  LOG(INFO) << "End of service";

  return 0;
}
