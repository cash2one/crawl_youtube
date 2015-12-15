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
 'le_crawler.core.jsp_download_middleware.JSPDownloadMiddleWare' : 100,
 'le_crawler.common.bindaddressmiddleware.BindaddressMiddleWare': 500,
 'le_crawler.common.site_crawled_stats.DomainExceptionStats': 999,
}

SCHEDULER = "le_crawler.core.scheduler.CrawlDocScheduler"
CRAWLDOC_SCHEDULER_HOST = '10.150.140.84'
SCHEDULER_IDLE_BEFORE_CLOSE = 4
CRAWLDOC_SCHEDULER_PORT = 8088
DEBUG_MODE = False
# DEBUG_MODE = True
DEBUG_HOST = '10.154.156.73'

DOWNLOAD_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = True

COMPRESSION_ENABLED = True

CONCURRENT_ITEMS = 200

CONCURRENT_REQUESTS = 100
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
HTTPERROR_ALLOWED_CODES = [404, 301, 302, 307]

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
le_crawler.common.fresh_doc_writer.FreshDocWriter,
le_crawler.common.crawl_doc_writer.CrawlDocWriter
"""

ENABLE_JS_DOWNLOAD = True
# ENABLE_JS_DOWNLOAD = False

# 'D' stands for Default and 'N' for Not-using-js
# for video page, the value should always be exactly one string.
# for list page, if the value is a list, then it should be ['home_js', 'channel_js', 'list_js'], otherwise it is one string for all 3 parse methods
JS_DOWNLOADER_URL_PATTERT = {
    r'(www\.hunantv\.com)\/(v)\/.*': 'js_dep/get_html_hunantv.js',
    r'www\.wasu\.cn\/Play.*': 'D',
    r'.*ifeng.com.*': 'D',
    r'.*people.com.cn.*': 'D',
    r'.*163.com\/hot.*': ['N', 'D', 'js_dep/163_load.js'],
    r'.*163.com\/(zixun|paike|yule)\/.*': 'js_dep/get_html_163.js',
    r'.*news.sina.com.cn.*': 'js_dep/sina_news_load.js',
    r'.*video.sina.com.cn.*': 'D',
    r'www\.iqiyi\.com.*': 'D',
    r'list.pptv.com': ['D', 'D', 'js_dep/pptv_load.js'],
    r'v.pptv.com': 'D',
    r'(v\.qq\.com)\/\w+\/?$': 'D',
    r'(v\.qq\.com)\/(boke|cover|page)\/.*(html|shtml|htm).*': 'js_dep/get_html_qq.js',
    r'www\.tudou\.com\/(programs|albumplay|listplay)': 'D',
    r'.*?\.tudou.com$': 'D',
    r'gc\.tudou\.com': ['D', 'D', 'js_dep/tudou_gc_list_load.js'],
    r'tudou\.com.*item$': ['D', 'D', 'js_dep/tudou_user_item_load.js'],
    r'tudou\.com.*playlist$': 'D',
    r'tv\.sohu\.com\/.*\.shtml': 'D',
    r'.*www\.v1\.cn\/.+': 'D',
    r'.*v1\.cn\/?$': ['D', 'D', 'js_dep/v1_list_load.js'],
    r'.*?www\.tudou\.com\/list\/.*': ['N', 'N', 'js_dep/tudou_list_load.js'],
    r'.*56\.com.*': 'D',
    r'tv\.hexun\.com.*': 'D'}

