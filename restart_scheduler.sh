#!/bin/bash
rm -rf database
rm -rf log/*

ps aux|grep 'url_filter_service'|grep -v grep|awk '{print $2}'|xargs kill -9
ps aux|grep 'scheduler_service.py'|grep -v grep|awk '{print $2}'|xargs kill -9

nohup python url_filter_service.py -H $1 > log/filter.log_ &
nohup python scheduler_service.py -H $1 > log/scheduler.log_ &
# nohup python url_filter_service.py -H 127.0.0.1 > log/local_filter.log_ &

