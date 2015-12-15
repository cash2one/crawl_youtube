#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for connection module.

A detailed description of connection.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'


import redis

REDIS_SERVER_LIST = [('localhost', 6379)]

def from_settings(settings):
  servers = []
  conf_list = settings.get('REDIS_SERVER_LIST', REDIS_SERVER_LIST)
  for conf in conf_list:
    servers.append(redis.Redis(host=conf[0], port=conf[1]))
  return servers
