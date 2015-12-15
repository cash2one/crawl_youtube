# Copyright 2015 Letv Inc. All Rights Reserved.
# Author: guoxiaohe@letv.com
#
# Description:

# cc_binary (
#     name = 'bloom_filter_server',
#     srcs = [
#         'bloom_filter_server_main.cc'
#     ],
#     deps = [
#         # '#pthread',
#         ':bloom_redis_filter',
#         '//third_party/boost:boost_program_options',
#         '//third_party/thrift:thriftnb',
#         #'//third_party/thrift-1.0.0-dev:thriftnb',
#         '//third_party/libevent-2.0.11-stable:event',
#         '//third_party/thrift:thrift',
#     ],
#     # optimize = ['O0', 'g', 'msse4.2'],
# )

cc_binary (
    name = 'bloom_redis_filter',
    srcs = [
        'bloom_redis_filter.cc',
    ],
    incs = [
        ':redis_client.h',
        ':object_pool.h'
    ],
    deps = [
      '//third_party/glog:glog',
      '//third_party/thrift:thriftnb',
      '//third_party/libevent-2.0.11-stable:event',
      '//search2/crawler_ver2/le_crawler/proto:bloom_redis_filter_thrift',
      '//third_party/hiredis:hiredis',
      '//search2/util:global_init',
    ],
    optimize = ['O0', 'g', 'msse4.2'],
)

cc_binary (
     name = 'pool_test',
    srcs = [
        'pool_test.cc',
    ],
    incs = [
        ':redis_client.h',
        ':object_pool.h'
    ],
    deps = [
        '//third_party/glog:glog',
        '//third_party/hiredis:hiredis',
    ],
    optimize = ['O0', 'g', 'msse4.2'],
)

# cc_library (
#     name = 'redis_pool',
#     srcs = [
#         'redis_pool.cc',
#     ],
#     deps = [
#       '//third_party/hiredis:hiredis',
#     ],
#     # optimize = ['O0', 'g', 'msse4.2'],
# )
