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

# item drop pipeline using for picture, no need for one request one response
ITEM_PIPELINES =  {
    'le_crawler.common.item_dupe_filter_pipeline.ItemDupFilterPipeline' : 2,
    'le_crawler.core.page_writer_pipeline.PageWriterPipeLine' : 999,
     }

DOWNLOADER_MIDDLEWARES = {
 'le_crawler.common.bindaddressmiddleware.BindaddressMiddleWare': 500,
 'le_crawler.common.site_crawled_stats.DomainExceptionStats': 999,
}


DOWNLOAD_DELAY = 8

COMPRESSION_ENABLED = True

CONCURRENT_ITEMS = 40

CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN = 4
CONCURRENT_REQUESTS_PER_IP = 0

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'image/*,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DEPTH_LIMIT = 20
DEPTH_STATS = True
DEPTH_PRIORITY = 1


DOWNLOAD_TIMEOUT = 60   # 3mins

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FORMATTER = 'scrapy.logformatter.LogFormatter'
LOG_STDOUT = False
LOG_LEVEL = 'INFO'
LOG_FILE = '../log/crawler.log'

#USER_AGENT = 'Version2.4 / LetvCrawler'
#USER_AGENT = 'Mozilla/5.0 (X11; U; Linux x86_64; rv:2.0) Gecko/20110307 LetvCrawler/20140604 Firefox/4.0'
USER_AGENT = 'Mozilla/5.0 (Linux; U; Android 4.3; zh-cn; vivo X520L Build/JLS36C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30'

BINDIP_LOCAL = True

EXTENSIONS = {
    'le_crawler.common.site_crawled_stats.SiteCrawledStats': 0,
    }

SITE_DOWNLOADER_STATS = True
ROBOTSTXT_OBEY = False
JOBDIR = '../data/'
STATS_CLASS = 'le_crawler.common.site_crawled_stats.DiskableStateCollector'
STATS_DUMP_INTERVAL = 1380 # 23min
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False
DEBUG_MODEL = False
CRAWL_DOC_WRITERS = """
le_crawler.core.page_writer.PageWriterBase,
le_crawler.common.image_local_writer.ImageLocalWriter
"""
# DOC LOCLWriter
# page local write configure
LOCAL_PAGE_WRITER_DATA_DIR ='/letv/crawler_delta_phone/'
LOCAL_PAGE_WRITER_DATA_FLUSH_LIMIT = 20000
LOCAL_PAGE_WRITER_DATA_TIME_LIMIT = 86400
# this failure will usefull,
HTTPERROR_ALLOWED_CODES =  [404]
FILES_STORE = 'file:///letv/crawler_delta_phone/wallpapers/'
