#!/bin/bash
# author: guoxiaohe@letv.com

usage="$0 [start|stop|restarat]"
if [ $# -lt 1 ]; then
  echo "$usage"
  exit 1
fi
cmd_type=$1
function start() {
  cmd="./redis-server ../config/redis.conf --loglevel verbose "
  echo $cmd
  eval $cmd
}

function stop() {
  echo "unsport "
  exit 1
}

function restart() {
 stop
 sleep 2
 start
}

if [ "start" = $cmd_type ];then
  start
elif [ "stop" = $cmd_type ];then
  stop
elif [ "restart" = $cmd_type ];then
  restart
else
  echo $usage
fi
