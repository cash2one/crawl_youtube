#!/bin/bash
usage="[start|stop|restart]"
if [ $# -lt 1 ];then
  echo $usage
  exit 1
fi
scrapy="/letv/python27/bin/scrapy"
cur_path=$(pwd)
replica_id=$(echo $cur_path | awk -F '/le_crawler|_' '{print $(NF-1)}')
base_cmd="video_crawler -a replica_id=$replica_id -a work_path=$cur_path"
cmd="nohup $scrapy crawl $base_cmd"
echo "workpath : $cur_path"
echo "replica_id : $replica_id"
echo $base_cmd

function start_crawler() {
  echo "starting crawler ..."
  pid=$(ps -elf | grep "$base_cmd" | grep -v grep | awk -F ' ' '{print $4}')
  if [ ! -z $pid ];then
    echo "$pid is already running, please stop it first"
    exit 1
  fi
  $cmd &
  echo "starting crawler succes!"
}

function stop_crawler() {
  pid=$(ps -elf | grep "$base_cmd" | grep -v grep | awk -F ' ' '{print $4}')
  if [ -z $pid ];then
    echo "$pid is not run!"
    exit 0
  fi
  kill $pid
  while [ -d /proc/$pid ]; do
    echo "wait exit...[$pid]"
    sleep 5
  done
  echo "crawler: $base_cmd exit"
}

if [ "start" == $1 ];then
  start_crawler
elif [ "stop" == $1 ];then
  stop_crawler
else
  echo "$usage"
fi
