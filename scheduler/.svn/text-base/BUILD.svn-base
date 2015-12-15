# Copyright 2015 Letv Inc. All Rights Reserved.
# Author: gaoqiang@letv.com

cc_library (
    name = 'crawl_db',
    srcs = [
        'crawl_db.cc',
    ],
    incs = [
        '../../../third_party/leveldb/include',
        '../../../third_party/log4cplus-1.1.3-rc1/include',
    ],
    deps = [
        '//third_party/leveldb:leveldb',
        '//third_party/log4cplus-1.1.3-rc1:log4cplus',
        '//base:base',
    ]
)

cc_library (
    name = 'crawl_db_manager',
    srcs = [
        'crawl_db_manager.cc',
    ],
    incs = [
        '../../../third_party/leveldb/include',
        '../../../third_party/log4cplus-1.1.3-rc1/include',
    ],
    deps = [
        '//search2/crawler_ver2/le_crawler/proto:schedule_service_thrift',
        '//base:base',
        '//third_party/leveldb:leveldb',
        '//third_party/log4cplus-1.1.3-rc1:log4cplus',
    ],
)

cc_binary (
    name = 'schedule_service',
    srcs = [
        'schedule_service.cc',
        'schedule_service_handler.cc',
    ],
    incs = [
        '../../../third_party/leveldb/include',
    ],
    deps = [
        ':crawl_db_manager',
        ':crawl_db',
        '//base:base',
        '//third_party/thrift:thriftnb',
        '//third_party/libevent-2.0.11-stable:event',
        '//search2/crawler_ver2/le_crawler/proto:schedule_service_thrift',
        '//third_party/leveldb:leveldb',
        '//third_party/log4cplus-1.1.3-rc1:log4cplus',
        '#rt',
        '#pthread',
    ]
)

cc_binary (
    name = 'crawl_db_test',
    srcs = [
        'crawl_db_test.cc',
    ],
    incs = [
        '../../../third_party/leveldb/include',
        '../../../third_party/log4cplus-1.1.3-rc1/include',
    ],
    deps = [
        ':crawl_db',
        # '//third_party/glog:glog',
        '#rt',
        '#pthread',
    ],
    optimize = ['O3', 'g', 'msse4.2'],
    dynamic_link = False,
)

