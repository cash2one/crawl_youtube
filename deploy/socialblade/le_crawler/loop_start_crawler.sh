#!/bin/bash
cmd1="scrapy crawl socialblade -a workdir=$(pwd)"
# loop interval 10 min
LOGF="../log/scheduler.log"
DATA_DIR="../data/*"
interval=900
function start() {
while [ 1 ];
do
  datestr=$(date +"%Y%m%d %H:%M:%S")
  echo "$datestr begin running..."
  rm -rf $DATA_DIR
  nohup $cmd1 2>&1 1>>$LOGF
  sleep $interval
done
}

start > $LOGF 2>&1 &
