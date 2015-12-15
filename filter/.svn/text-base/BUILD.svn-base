# Copyright 2015 Letv Inc. All Rights Reserved.
# Author: gaoqiang@letv.com

cc_binary (
    name = 'bf_test',
    srcs = [
        'bf_test.cc',
    ],
    incs = [
        '../../../third_party/libbf',
    ],
    deps = [
        '//third_party/libbf:bf'
    ]
)

cc_binary (
    name = 'filter_service',
    srcs = [
        'filter_service.cc',
        'filter_handler.cc',
    ],
    incs = [
        '../../../third_party/libbf',
    ],
    deps = [
        '//base:base',
        '//third_party/libbf:bf',
        '//third_party/thrift:thriftnb',
        '//third_party/libevent-2.0.11-stable:event',
        '//search2/crawler_ver2/le_crawler/proto:url_filter_service_thrift',
    ]
)

