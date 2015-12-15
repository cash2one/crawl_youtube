#!/bin/bash

stream=/letv/search/hadoop-1.1.2/contrib/streaming/hadoop-streaming-1.1.2.jar
archives=hdfs://webdm-cluster/user/search/zhangrenzhong/parse.tar.gz#parse
reduce_task=40
mapper=./parse/mapper.py
reducer=./parse/reducer.py
#outputformat=com.custom.MultipleTextOutputFormatByKey
outputformat=com.custom.MultipleSequenceFileOutputFormatByKey
jar=custom.jar
while read line
do
	dir=${line##*/}
    input=crawler_upload/crawler_delta/$dir
	output=crawler_upload/short_list/$dir
	video_dir=crawler_upload/short_video/$dir
    hadoop fs -rm -r $output
    hadoop fs -rm -r $video_dir #be a notice
    echo "hadoop jar $stream -libjars $jar -archives $archives -D mapred.job.name='parse' -D mapred.reduce.tasks=$reduce_task -D stream.num.reduce.output.key.fields=2 -D mapred.output.compress=true -D mapred.output.compression.type=BLOCK -input $input -output $output -mapper $mapper -reducer $reducer -inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat -outputformat $outputformat 2>&1"
    ret=`hadoop jar $stream -libjars $jar -archives $archives -D mapred.job.name=$dir -D mapred.reduce.tasks=$reduce_task -D stream.num.reduce.output.key.fields=2 -D mapred.output.compress=true -D mapred.output.compression.type=BLOCK -input $input -output $output -mapper $mapper -reducer $reducer -inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat -outputformat $outputformat 2>&1`
    echo "ret: $ret" >>log
    jobid=`echo "$ret"|grep "Job complete"|awk '{print $7}'`
	if [ "x$jobid" != "x" ]; then
        echo "hadoop job -status $jobid"
        hadoop job -status $jobid >>info.log
		hadoop fs -rm -r $output/_logs $output/_SUCCESS
		domains=`hadoop fs -ls $output|awk '{print $8}' |grep -v '^$'`
		for domain in $domains
		do
		    domain=${domain##*/}
			echo "hadoop fs -mkdir -p crawler_upload/short_video/$dir/$domain" >>log
			echo "hadoop fs -rm -r crawler_upload/short_video/$dir/$domain/*" >>log
			echo "hadoop fs -mv $output/$domain/video/* crawler_upload/short_video/$dir/$domain/" >>log
            hadoop fs -mkdir -p $video_dir/$domain/video
            hadoop fs -rm -r $video_dir/$domain/video/*
            hadoop fs -mv $output/$domain/video/* $video_dir/$domain/video/
            hadoop fs -mkdir -p $video_dir/$domain/video_tmp
            hadoop fs -rm -r $video_dir/$domain/video_tmp/*
            hadoop fs -mv $output/$domain/video_tmp/* $video_dir/$domain/video_tmp/
		done
	else
		echo "$dir" >>error.log
	fi
done < dirs
