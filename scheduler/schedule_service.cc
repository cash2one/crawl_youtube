// Copyright 2015 letv Inc. All Rights Reserved.
// Author: gaoqiang@letv.com(Qiang Gao)

#include <string>
#include "thrift/concurrency/PosixThreadFactory.h"
#include "thrift/concurrency/ThreadManager.h"
#include "thrift/protocol/TBinaryProtocol.h"
#include "thrift/server/TNonblockingServer.h"
#include "thrift/server/TThreadPoolServer.h"
#include "thrift/transport/TBufferTransports.h"
#include "thrift/transport/TServerSocket.h"

#include "base/flags.h"
#include "base/logging.h"
#include "schedule_service_handler.h"

using apache::thrift::TProcessor;
using apache::thrift::concurrency::PosixThreadFactory;
using apache::thrift::concurrency::ThreadManager;
using apache::thrift::protocol::TProtocolFactory;
using apache::thrift::protocol::TBinaryProtocolFactory;
using apache::thrift::transport::TServerTransport;
using apache::thrift::transport::TServerSocket;
using apache::thrift::transport::TTransportFactory;
using apache::thrift::transport::TBufferedTransportFactory;
using apache::thrift::server::TNonblockingServer;
using apache::thrift::server::TServer;
using apache::thrift::server::TThreadPoolServer;
using boost::shared_ptr;
using namespace ::search2::crawler_ver2::scheduler;

DEFINE_int32(server_port, 9090, "Server port");
DEFINE_int32(server_thread_num, 64, "Server thread number");
DEFINE_int32(io_thread_num, 8, "IO thread number");

int main(int argc, char **argv) {
  google::ParseCommandLineFlags(&argc, &argv, true);
  std::string db_path = "databases/";
  shared_ptr<ScheduleServiceHandler> handler(new ScheduleServiceHandler(db_path));
  shared_ptr<TProcessor> processor(new ScheduleServiceProcessor(handler));
  shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());
  shared_ptr<ThreadManager> threadManager = ThreadManager::newSimpleThreadManager(FLAGS_server_thread_num);
  shared_ptr<PosixThreadFactory> threadFactory = shared_ptr<PosixThreadFactory>(new PosixThreadFactory());
  threadManager->threadFactory(threadFactory);
  threadManager->start();
  TNonblockingServer server(processor, protocolFactory, FLAGS_server_port, threadManager);
  server.setNumIOThreads(FLAGS_io_thread_num);
  server.serve();
  return 0;
}

