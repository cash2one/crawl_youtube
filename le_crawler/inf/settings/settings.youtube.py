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
    'le_crawler.common.page_writer_pipeline.PageWriterPipeline' : 999,
     }

DOWNLOADER_MIDDLEWARES = {
 'le_crawler.common.bindaddressmiddleware.BindaddressMiddleWare': 500,
 'le_crawler.common.site_crawled_stats.DomainExceptionStats': 999,
}


SCHEDULER = "le_crawler.core.scheduler.SchedulerYoutube"
CRAWLDOC_SCHEDULER_HOST = '65.255.32.210'
#CRAWLDOC_SCHEDULER_HOST = '107.155.52.89'
SCHEDULER_REQUEST_POOL_SIZE = 50
SCHEDULER_IDLE_BEFORE_CLOSE = 4
CRAWLDOC_SCHEDULER_PORT = 8088
URL_FILTER_PORT = 8089

DEBUG_MODE = False
#DEBUG_MODE = True
#DEBUG_HOST = '107.155.52.89'

DOWNLOAD_DELAY = 0.1
RANDOMIZE_DOWNLOAD_DELAY = True

COMPRESSION_ENABLED = True

CONCURRENT_ITEMS = 64

CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 3
CONCURRENT_REQUESTS_PER_IP = 0

#SCHEDULER_ORDER = 'BFO'

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DEPTH_LIMIT = 0
DEPTH_STATS = True
DEPTH_PRIORITY = 0

DOWNLOAD_TIMEOUT = 10

LOG_ENABLED = False
#LOG_ENCODING = 'utf-8'
#LOG_FORMATTER = 'scrapy.logformatter.LogFormatter'
#LOG_STDOUT = False
#LOG_LEVEL = 'DEBUG'
#LOG_FILE = '../log/crawler.log'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153'
#USER_AGENT = 'Mozilla/5.0 (X11; U; Linux x86_64; rv:2.0) Gecko/20110307 LetvCrawler/20140604 Firefox/4.0'
#USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'

BINDIP_LOCAL = True
BIND_ADDRESS_IP = '123.125.91.85'
BIND_ADDRESS_PORT = 10012


EXTENSIONS = {
    'le_crawler.common.site_crawled_stats.SiteCrawledStats': 0,
    }
# site download statistic flag
SITE_DOWNLOADER_STATS = True
# stop ROBOTSTXT_OBEY for toutiao video crawler
ROBOTSTXT_OBEY = False
JOBDIR = '../data/'
STATS_CLASS = 'le_crawler.common.site_crawled_stats.DiskableStateCollector'
STATS_DUMP_INTERVAL = 1380 # 23min
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False

CRAWL_DOC_WRITERS = """
le_crawler.common.crawl_doc_writer.CrawlDocWriter
"""
#le_crawler.common.youtube_writer.YoutubeWriter
#le_crawler.common.txt_file_writer.CrawlDocWriter
#le_crawler.common.lejian_writer.LejianWriter
#le_crawler.common.sequence_file_writer.CrawlDocWriter,
#le_crawler.common.realtime_video_writer.RealtimeVideoWriter
