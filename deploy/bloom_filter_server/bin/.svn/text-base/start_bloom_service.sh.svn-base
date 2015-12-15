#!/bin/bash
# guoxiaohe@letv.com 2015

USAGE="Usage [start|stop|restart]"
if [ $# -lt 1 ]; then
  echo $USAGE
  exit 1
fi
cmd_type=$1

ulimit -c unlimited
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# don't modify unless you know what are you doing
MAX_ELE_NUM=7500000000
POSITIVE_FALSE=0.000058
THREAD_NUM=40
IO_THREAD_NUM=10
PORT=8099
REDIS_IP_PORT=10.150.140.83:6379
BLOOM_KEY=websearch_url_dupe
# above setting will cost 30G memery
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

CURRDIR=$(pwd)
BIN=bloom_redis_filter
FLAGS=" --max_elements_number=$MAX_ELE_NUM --positive_false=$POSITIVE_FALSE 
    --port=$PORT --redis_ipport=$REDIS_IP_PORT --bloom_key=$BLOOM_KEY
    --daemon=true --v 2"
CMD="$CURRDIR/$BIN $FLAGS $@"
function start() {
  echo $CMD
  exec $CMD
}

function stop() {
  if [ -e "${BIN}.pid" ];then
    pid=$(cat "${BIN}.pid")
    kill $pid
    while [ -e "/proc/exec/$pid" ];do
      echo "wait for $pid"
      sleep 1
    done
  else
    echo "Not found pid file!"
    exit 1
  fi  
  echo "stoped!"
}

if [ "start" = $cmd_type ];then
  start
elif [ "stop" = $cmd_type ];then
  stop
elif [ "restart" = $cmd_type ];then
  stop
  start
else
  echo  $USAGE
fi
  
