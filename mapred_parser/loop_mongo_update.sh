#!/bin/bash

pc=`ps aux | grep update_mongo.py | grep -v grep | wc -l`

function main_loop() {
  while [ 1 ];
  do
    if [ $(ps aux | grep update_mongo.py | grep -v grep | wc -l) = "0" ] ; then
      #echo 'no update_mongo'
      #echo "$pc"
      nohup python update_mongo.py > update_mongo.log 2>&1  &
      #nohup python update_mongo.py $
    fi
    sleep 30
  done
}

#main_loop 2>&1 &
main_loop &
#main_loop 
