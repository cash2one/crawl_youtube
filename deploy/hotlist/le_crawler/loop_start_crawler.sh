#!/bin/bash
cmd1="scrapy crawl toptv_spider"
# loop interval 10 min
LOGF="../log/scheduler.log"
interval=604800
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
