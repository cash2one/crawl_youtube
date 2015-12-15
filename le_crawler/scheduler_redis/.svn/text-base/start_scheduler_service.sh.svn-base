#!/bin/bash
usage='start|stop|restart'
if [ $# -lt 1 ];then
  echo $usage
  exit 1
fi

type=$1
pidf='dbservice.pid'
function start_service() {
if [ ! -s $pidf ];then
  pid=$(cat $pidf)
  if [ [ "$pid" != "-1" ] -o [ -d "/proc/$pid" ] ];then
    echo 'service is already running'
    exit 1
  fi
fi
cmd="nohup /letv/python27/bin/python2.7 requests_manager.py"
echo $cmd
$cmd &
}

function stop_service() {
if [ -f $pidf ];then
  pid=$(cat $pidf)
  if [ "$pid" == "-1" ] || [ ! -d "/proc/$pid" ];then
    echo 'service is already stoped'
    exit 1
  fi
  kill $pid
  echo "wait stop ... $pid"
  while [ -d /proc/$pid ];
  do
    sleep 1
  done
else
  echo "not found $pidf, service start or stop exception"
  exit 1
fi

}

if [ 'start' = $type ];then
  start_service
elif [ 'stop' = $type ];then
  stop_service
elif [ 'restart' = $type ];then
  stop_service
  sleep 4
  start_service
fi
#echo "...Done[$type]"
