# Copyright 2015 Letv Inc. All Rights Reserved.
# Author: guoxiaohe@letv.com
#
# Description:
thrift_library(
  name = 'crawl_doc_thrift',
  srcs = ['crawl_doc.thrift',],
)

thrift_library(
  name = 'scheduler_service_thrift',
  srcs = ['scheduler_service.thrift',],
  deps = [':crawl_doc_thrift'],
)

thrift_library(
  name = 'sharedb_thrift',
  srcs = ['sharedb.thrift'],
)

thrift_library(
  name = 'bloom_redis_filter_thrift',
  srcs = ['bloom_redis_filter.thrift'],
)

thrift_library(
  name = 'video_media_thrift',
  srcs = ['video_media.thrift'],
  deps = [':crawl_doc_thrift']

)
