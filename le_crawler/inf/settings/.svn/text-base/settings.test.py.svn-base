# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'letv_bot'
SPIDER_MODULES = ['le_crawler.spiders']
NEWSPIDER_MODULE = 'le_crawler.spiders'

ITEM_PIPELINES =  {
    'le_crawler.page_writer_pipeline.PageWriterPipeLine' : 999,
     }

DOWNLOADER_MIDDLEWARES = {
 #'le_crawler.common.middlewares.BindaddressMiddleWare': 500,
 'le_crawler.common.site_crawled_stats.DomainExceptionStats': 999,
}


DOWNLOAD_DELAY = 6


COMPRESSION_ENABLED = True

CONCURRENT_ITEMS = 64

CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 6
CONCURRENT_REQUESTS_PER_IP = 0

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DEPTH_LIMIT = 0
DEPTH_STATS = True
DEPTH_PRIORITY = 1


DOWNLOAD_TIMEOUT = 60   # 3mins

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FORMATTER = 'scrapy.logformatter.LogFormatter'
LOG_STDOUT = False
LOG_LEVEL = 'INFO'
LOG_FILE = '../log/crawler.log'

USER_AGENT = 'Version2.4 / LetvCrawler'

#BIND_ADDRESS_IP = '123.125.91.85'

#BIND_ADDRESS_PORT = 10012

EXTENSIONS = {
    'le_crawler.common.site_crawled_stats.SiteCrawledStats': 0,
    }

#INPUT_QUEUE_SHARD_DIST = [1]
#OUTPUT_QUEUE_SHARD_DIST = [1]
#DUPE_SHARD_DIST = [1]
# site download statistic flag
SITE_DOWNLOADER_STATS = True
# stop ROBOTSTXT_OBEY for toutiao video crawler
ROBOTSTXT_OBEY = False
JOBDIR = '../data/'
STATS_CLASS = 'le_crawler.common.site_crawled_stats.DiskableStateCollector'
STATS_DUMP_INTERVAL = 1380 # 23min
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False

DEBUG_MODEL = True
CRAWL_DOC_WRITERS = """
le_crawler.core.page_writer.PageWriterBase,
le_crawler.common.today_tv_writer.TodayTvWriter,
le_crawler.common.realtime_video_writer.RealtimeVideoWriter

"""
