#!/bin/bash
cmd1="scrapy crawl baiduhot -a workdir=$(pwd)"
# loop interval 10 min
LOGF="../log/scheduler.log"
interval=3600
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
