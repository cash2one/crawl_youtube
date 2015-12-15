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
    'le_crawler.core.page_writer_pipeline.PageWriterPipeLine' : 999,
     }

DOWNLOADER_MIDDLEWARES = {
 'le_crawler.core.jsp_download_middleware.JSPDownloadMiddleWare' : 100,
 'le_crawler.common.bindaddressmiddleware.BindaddressMiddleWare': 500,
 'le_crawler.common.site_crawled_stats.DomainExceptionStats': 999,
}

URL_FILTER_LOCAL_HOST = '127.0.0.1'
URL_FILTER_LOCAL_PORT = 8089
URL_FILTER_HOST = '10.150.140.84'
URL_FILTER_PORT = 8089

DEBUG_MODE = True
DEBUG_HOST = '10.154.156.73'

DOWNLOAD_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = True

COMPRESSION_ENABLED = True

CONCURRENT_ITEMS = 200

CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 3
CONCURRENT_REQUESTS_PER_IP = 0


DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DEPTH_LIMIT = 0
DEPTH_STATS = True
DEPTH_PRIORITY = 0

DOWNLOAD_TIMEOUT = 10

LOG_ENABLED = False

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153'

BINDIP_LOCAL = True
BIND_ADDRESS_IP = '123.125.91.85'
BIND_ADDRESS_PORT = 10012


EXTENSIONS = {
    'le_crawler.common.site_crawled_stats.SiteCrawledStats': 0,
    }

SITE_DOWNLOADER_STATS = True  # site download statistic flag

ROBOTSTXT_OBEY = False  # stop ROBOTSTXT_OBEY for toutiao video crawler
JOBDIR = '../data/'
STATS_CLASS = 'le_crawler.common.site_crawled_stats.DiskableStateCollector'
STATS_DUMP_INTERVAL = 1380 # 23min
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False

CRAWL_DOC_WRITERS = """
le_crawler.common.ugc_file_writer.UgcItemWriter
"""
ENABLE_JS_DOWNLOAD = True

# 'D' stands for Default and 'N' for Not-using-js
# for video page, the value should always be exactly one string.
# for list page, if the value is a list, then it should be ['home_js', 'channel_js', 'list_js'], otherwise it is one string for all 3 parse methods
JS_DOWNLOADER_URL_PATTERT = {
    r'www\.tudou\.com\/(programs|albumplay|listplay)': 'D',
    r'.*?\.tudou.com$': 'D',
    r'gc\.tudou\.com': ['D', 'D', 'js_dep/tudou_gc_list_load.js'],
    r'tudou\.com.*item$': ['D', 'D', 'js_dep/tudou_user_item_load.js'],
    r'tudou\.com.*playlist$': 'D',}
