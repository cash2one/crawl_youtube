#!/usr/bin/python
#
# Copyright 2014 LeTV Inc. All Rights Reserved.


"""One-line documentation for signals module.

A detailed description of signals.
"""

__author__ = 'xiezhi@letv.com (Xie Zhi)'

from scrapy.utils.project import get_project_settings

settings = get_project_settings()

minutely_timeout = object()
hourly_timeout = object()
daily_timeout = object()

for name in settings.get("CUSTOM_TIMERS", {}).keys():
  vars()[name] = object()
