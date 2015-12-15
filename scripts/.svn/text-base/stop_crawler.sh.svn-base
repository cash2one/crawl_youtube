#!/bin/bash

ps aux |grep 'deploy/lejian_full/le_crawler/loop_start_crawler.sh' | grep -v grep | awk '{print $2}' | xargs kill -9
echo 'kill loop_start_crawler ......'

ps aux |grep 'scrapy crawl lejian' | grep -v grep | awk '{print $2}' | xargs kill -2
echo 'kill scrapy ......'

pc=`ps aux |grep 'scrapy crawl lejian' | grep -v grep | wc -l`
while [ "$pc" != "0" ];
do
  sleep 10
  pc=`ps aux |grep 'scrapy crawl lejian' | grep -v grep | wc -l`
  echo $pc' crawlers remain.'
done

ps aux|grep 'url_filter_service'|grep -v grep|awk '{print $2}'|xargs kill -9
echo 'kill url_filter_service'

