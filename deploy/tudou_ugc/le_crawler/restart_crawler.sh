#!/bin/bash

ps aux|grep 'scrapy'|grep -v grep|awk '{print $2}'|xargs kill -9

rm -rf ../log/*
rm nohup.out

nohup scrapy crawl lejian &

