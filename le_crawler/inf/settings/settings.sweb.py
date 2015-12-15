# this settings using for web crawler of letv search
BOT_NAME = 'letvcrawler'
SPIDER_MODULES = ['le_crawler.spiders']
NEWSPIDER_MODULE = 'le_crawler.spiders'

SCHEDULER = "le_crawler.core.scheduler_client.CrawlDocScheduler"
CRAWLDOC_SCHEDULER_HOST = '10.150.140.87'
CRAWLDOC_SCHEDULER_PORT = 7007

#DUPEFILTER_CLASS = 'le_crawler.core.dupefilter.RFPDupeFilter'
DUPEFILTER_CLASS = 'le_crawler.core.bloom_dupefilter.BloomDupeFilter'
BLOOM_DUPE_HOST = '10.150.140.86'
BLOOM_DUPE_PORT = 8099

SCHEDULER_PERSIST = True

ITEM_PIPELINES =  {
    'le_crawler.core.page_writer_pipeline.PageWriterPipeLine' : 999,
     }

DOWNLOADER_MIDDLEWARES = {
  'le_crawler.core.domain_filter_middleware.DomainFilterMiddleware':0,
  'le_crawler.common.bindaddressmiddleware.BindaddressMiddleWare': 10,
  'le_crawler.core.jsp_download_middleware.JSPDownloadMiddleWare' : 100,
  'le_crawler.common.site_crawled_stats.DomainExceptionStats': 999,
  'le_crawler.common.item_express_pipeline.ItemExpressPipeline' : 998,
}

DOWNLOAD_DELAY = 0.8

COMPRESSION_ENABLED = True

CONCURRENT_ITEMS = 256

CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 10
CONCURRENT_REQUESTS_PER_IP = 0

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DEPTH_LIMIT = 6
DEPTH_STATS = True
DEPTH_PRIORITY = 1


DOWNLOAD_TIMEOUT = 60   # 3mins

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FORMATTER = 'le_crawler.common.log_format.LetvLogFormatter'
LOG_STDOUT = False
LOG_LEVEL = 'INFO'
LOG_FILE = '../log/crawler.log'

USER_AGENT = 'Mozilla/5.0 (X11; U; Linux x86_64; rv:2.0) Gecko/20110307 LetvCrawler/20140604 Firefox/4.0'

# if BINDIP_LOCAL is true BIND_ADDRESS_IP configure is disable
BINDIP_LOCAL = True
BIND_ADDRESS_IP = '123.125.91.82'

EXTENSIONS = {
    'le_crawler.common.site_crawled_stats.SiteCrawledStats': 0,
    'le_crawler.common.timer.TimerDispatcher': 100,
    }

# disable recrawler
# site download statistic flag
SITE_DOWNLOADER_STATS = True
ROBOTSTXT_OBEY = True

JOBDIR = '../data/'
STATS_CLASS = 'le_crawler.common.site_crawled_stats.DiskableStateCollector'
STATS_DUMP_INTERVAL = 1380 # 23min

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False

DEBUG_MODEL = False
CRAWL_DOC_WRITERS = """
le_crawler.common.simple_mediav_extract_writer.RealtimeVideoWriter,
le_crawler.common.sequence_file_writer.CrawlDocWriter,
"""
ITEM_EXPRESS_KEYS = ['http_header', 'meta',]
#le_crawler.common.page_local_writer.PageLocalJsonWriter
