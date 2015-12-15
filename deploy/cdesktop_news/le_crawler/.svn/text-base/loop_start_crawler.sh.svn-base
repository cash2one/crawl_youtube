#!/bin/bash
if [ $# -lt 2 ];then
  echo 'Usage: (replace_spider) --dir=$(pwd) --interval(default 30min)'
  exit 1
fi
spider_name=$1
id_str=$2
cmd="scrapy crawl $spider_name -a $id_str"
# loop interval 30 min
interval=1800
log_file="../log/scheduler.log"
if [ $# -eq 3 ];then
  interval=$3
fi
echo "spider_name:$spider_name"
echo "id_str:$id_str"
echo "sleep_interval:$interval"
echo "cmd: $cmd"

function start_service() {
  while [ 1 ];
  do
    datestr=$(date +"%Y%m%d %H:%M:%S")
    echo "$datestr begin running..."
    nohup $cmd 2>&1 1>/dev/null
    echo "$datestr ...end loop"
    sleep $interval
  done
}

function main_loop() {
  start_service > $log_file 2>&1 &
}

main_loop

