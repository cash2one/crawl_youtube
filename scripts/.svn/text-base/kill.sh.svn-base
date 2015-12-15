#!/bin/bash

ps aux|grep $1|grep -v grep|grep -v 'kill.sh'
result=`ps aux|grep $1|grep -v grep|grep -v 'kill.sh'|wc -l`

#if [ "$result"x = "0"x ]
if [ $result -eq 0 ]
then
  echo 'no process found'
  exit 0
fi

read -p 'continue or not? y/n -> ' choice
if [ "$choice"x = "y"x ]
then
  echo 'killing...'
  ps aux|grep $1|grep -v grep|grep -v kill.sh|awk '{print $2}'|xargs kill -9
else
  echo "not kill, exit."
  exit 0
fi

