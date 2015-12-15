// Copyright 2015 letv Inc. All Rights Reserved.
// Author: guoxiaohe@letv.com

#ifndef SEARCH2_CRAWLER_VER2_UTIL_CONNECTION_POOL_H_
#define SEARCH2_CRAWLER_VER2_UTIL_CONNECTION_POOL_H_

#include <vector>
#include <string>
#include <utility>

#include "base/basictypes.h"
#include "base/mutex.h"
#include "base/logging.h"
#include "base/time.h"
#include "base/thread.h"
#include "util/gtl/stl_util-inl.h"
#include "third_party/hiredis/hiredis.h"

namespace search2 {
namespace crawl {
namespace util {

enum NodeStatus { ACTIVE = 0, INVALID, BUSY};

struct NodeClient {
  NodeClient(NodeStatus sta, redisContext* client,
             const std::string& ip, int32 port) :
      status(sta), client(client), ip(ip), port(port) {}
  NodeStatus status;
  redisContext* client;
  std::string ip;
  int32 port;
};


class ReconnectThread : public base::Thread {
 public:
  ReconnectThread(std::vector<NodeClient*> clients,
                  base::Mutex* operator_mutex) : clients_(clients),
    operator_mutex_(operator_mutex), stop_flag_(false) {

  }

  void Stop() {
    stop_flag_ = true;
  }

 protected:
  virtual void Run() {
    while (!stop_flag_) {
      {
        base::MutexLock lock(operator_mutex_);
        for (std::vector<NodeClient*>::iterator it = clients_.begin();
             it != clients_.end(); it++) {
          if ((*it)->status == INVALID) {
            redisContext* rediscontext = redisConnect((*it)->ip.c_str(),
                                                      (*it)->port);
            redisFree((*it)->client);
            (*it)->client = rediscontext;
            VLOG(2) << "reconnect redis:" << (*it)->ip << " ," << (*it)->port;
            (*it)->status = ACTIVE;
          }
        }
      }
      base::MilliSleep(5000);
    }
    LOG(INFO) << "ReconnectThread is exit normal!";
  }
 private:
  std::vector<NodeClient*> clients_;
  base::Mutex* operator_mutex_;
  bool stop_flag_;
};

class SimpleRedisConnectionPool {
 public:
  SimpleRedisConnectionPool(const std::vector<std::pair<std::string, int32> >&iplist,
                            int32 retry) : retry_max_(retry) {
    for (std::vector<std::pair<std::string, int32> >::const_iterator it
         = iplist.begin(); it != iplist.end(); ++it) {
      clients_.push_back(NewConnectionClient(it->first, it->second));
    }
    LOG(INFO) << "connection pool size:" << clients_.size();
    reconnect_thread_.reset(new ReconnectThread(clients_, &mutex_));
    reconnect_thread_->Start();
  }

  NodeClient* NewConnectionClient(const std::string& ip, int32 port) {
    redisContext* rediscontext = redisConnect(ip.c_str(), port);
    redisEnableKeepAlive(rediscontext);
    if (!rediscontext) {
      return new NodeClient(INVALID, rediscontext, ip, port);
    } else {
      return new NodeClient(ACTIVE, rediscontext, ip, port);
    }
  }

  virtual ~SimpleRedisConnectionPool() {
    reconnect_thread_->Stop();
    for (std::vector<NodeClient*>::iterator it = clients_.begin();
         it != clients_.end(); ++it) {
      redisFree((*it)->client);
      delete *it;
    }
  }

  NodeClient* GetClientNode(int64 wait_time = 10) {
    base::MutexLock lock(&mutex_);
    int32 tryed = 0;
    while (tryed < retry_max_) {
      for (std::vector<NodeClient*>::const_iterator it
           = clients_.begin();
           it != clients_.end(); ++it) {
        if ((*it)->status == ACTIVE) {
          (*it)->status = BUSY;
          return (*it);
        }
      }
      LOG(WARNING) << "Try get active node for: " << tryed << " times";
      ++tryed;
      base::MilliSleep(wait_time);
    }
    LOG(ERROR) << "Failed found active node";
    return NULL;
  }

  inline void SetNodeFailed(NodeClient* node) {
    node->status = INVALID;
  }

  inline void SetNodeIdle(NodeClient* node) {
    node->status = ACTIVE;
  }

 private:

  std::vector<NodeClient*> clients_;
  base::Mutex mutex_;
  int32 retry_max_;
  scoped_ptr<ReconnectThread> reconnect_thread_;
  //
  DISALLOW_COPY_AND_ASSIGN(SimpleRedisConnectionPool);

};

}  // namespace util

}  // namespace crawler
}  // namespace search2

#endif  // SEARCH2_CRAWLER_VER2_UTIL_CONNECTION_POOL_H_
