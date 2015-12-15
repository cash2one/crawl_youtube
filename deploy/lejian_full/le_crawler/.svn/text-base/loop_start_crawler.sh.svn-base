#!/bin/bash

cmd1="scrapy crawl lejian -a workdir=$(pwd)"
LOGF="../log/scheduler.log"
interval=10
function start() {
while [ 1 ];
do
  datestr=$(date +"%Y%m%d %H:%M:%S")
  echo "$datestr begin running..."
  nohup $cmd1 2>&1 1>>$LOGF
  sleep $interval
done
}

start > $LOGF 2>&1 &
