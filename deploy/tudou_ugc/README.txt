视频信息抽取
/letv/crawler_ver2/deploy/tudou_ugc下
1. cd /le_crawler
2. 运行 scrapy crawl tudouugc
备注：
1.视频meta信息输出文件夹为：
/letv/ugc_data
2.如需添加抓取源
按格式修改letv/crawler_ver2/deploy/tudou_ugc/tudou_ugc.cfg

视频下载
/letv/extractor/screenshot
运行 python stream_download.py 输入文件完整路径   视频输出目录
备注：
输入文件完成路径 ： 视频抽取信息生成的文件 eg（/letv/ugc_data/20151112_152853_15190_0111291.txt）
