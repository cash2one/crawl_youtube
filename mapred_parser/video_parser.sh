#!/bin/bash

stream=/letv/search/hadoop-1.1.2/contrib/streaming/hadoop-streaming-1.1.2.jar
archives=hdfs://webdm-cluster/user/search/zhangrenzhong/parse.tar.gz#parse
reduce_task=100
mapper=./parse/mapper.py
reducer=./parse/reducer.py
outputformat=com.custom.MultipleTextOutputFormatByKey
#outputformat=com.custom.MultipleSequenceFileOutputFormatByKey
jar=custom.jar

while read line
do
	dir=${line##*/}
    input="-input crawler_upload/crawler_delta/$dir"
	output=crawler_upload/index_data/$dir
	hadoop fs -rmr $output
	echo "hadoop jar $stream -libjars $jar -archives $archives -D mapred.job.name=$dir -D mapred.reduce.tasks=$reduce_task  $input -output $output -mapper $mapper -reducer $reducer -inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat -outputformat $outputformat" >>log
	ret=`hadoop jar $stream -libjars $jar -archives $archives -D mapred.job.name=$dir -D mapred.reduce.tasks=$reduce_task  $input -output $output -mapper $mapper -reducer $reducer -inputformat org.apache.hadoop.mapred.SequenceFileAsTextInputFormat -outputformat $outputformat 2>&1`
	echo "ret: $ret" >>log 2>&1
	jobid=`echo "$ret"|grep "Job complete"|awk '{print $7}'`
	if [ "x$jobid" != "x" ]; then
	    echo "hadoop job -status $jobid" >>log
	    hadoop job -status $jobid >>info.log
		hadoop fs -rmr $output/_logs $output/_SUCCESS
	else
		echo "error $dir" >>error.log
	fi
done < dirs
