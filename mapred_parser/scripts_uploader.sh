#!/bin/bash

binary=mapred_parser.tar.gz
rm -f ${binary} && rm -rf ../parse_copy && \

echo "remove ../parse_copy/" && mkdir ../parse_copy && \
echo 'copy to ../parse_copy/' && cp -r ./* ../parse_copy && \

echo 'replace letvbase.so' && rm ../parse_copy/letvbase.so && cp ../cpython/letvbase.so ../parse_copy/letvbase.so && \

echo '========jump to ../parse_copy========' && cd ../parse_copy && \

echo 'replace le_crawler' && rm le_crawler && mkdir le_crawler && touch le_crawler/__init__.py && \
echo 'replace lxml' && \
rm -rf ../le_crawler/common/lxml && \
# find ../util/lxml/ -type d -name "*.svn" | xargs rm -rf && \
# find ../util/lxml/ -type f -name "*.pyc" | xargs rm -rf && \
cp -r ../util/lxml/ ../le_crawler/common/ && \
cp -r ../le_crawler/common le_crawler && cp -r ../le_crawler/proto le_crawler && \
cp -r ../le_crawler/extractors le_crawler && \
cp -r ../le_crawler/core le_crawler && \
echo 'remove *.pyc' && find ../parse_copy -type f -name "*.pyc" | xargs rm -f && \
echo 'remove .svn' && find ../parse_copy -type d -name "*.svn" | xargs rm -rf && \

echo 'compress into '${binary} && tar -zcf ${binary} * && \
echo 'move to ../mapred_parser' && mv ${binary} ../mapred_parser/ && \

echo '========back to mapred_parser========' && \
cd ../mapred_parser && \
echo 'backing up binary...' && hadoop fs -mv /user/search/short_video/bin/${binary} /user/search/short_video/bin/${binary}_$(date +%Y%m%d_%H%M%S)
echo 'uploading...' && hadoop fs -put ${binary} /user/search/short_video/bin && \
rm -f ${binary} && \
echo 'Completed.'
