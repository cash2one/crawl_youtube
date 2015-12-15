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

rm -rf /letv/crawler_delta/*.txttmp
rm -rf crawler_0
svn export http://svn2.letv.cn/tp/search2/crawler_ver2/le_crawler --force "crawler_0/le_crawler"
svn export http://svn2.letv.cn/tp/search2/crawler_ver2/deploy/lejian_full/ --force "crawler_0/deploy/lejian_full"

cd crawler_0
svn export http://svn2.letv.cn/tp/search2/crawler_ver2/url_filter_service.py
mkdir ./log
nohup python url_filter_service.py -H 127.0.0.1 > log/local_filter.log_ &
cd -

cd crawler_0/deploy/lejian_full/le_crawler
echo $(pwd)
/bin/bash $(pwd)"/loop_start_crawler.sh"
cd -

for i in {1..15}
do
  dir="crawler_"$i
  echo $dir
  rm -rf "$dir"
  cp -r crawler_0 $dir
  cd $dir"/deploy/lejian_full/le_crawler"
  echo $(pwd)
  /bin/bash $(pwd)"/loop_start_crawler.sh"
  cd -
done

