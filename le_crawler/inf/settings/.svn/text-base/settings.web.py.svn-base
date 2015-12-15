# this settings using for web crawler of letv search
BOT_NAME = 'letvcrawler'
SPIDER_MODULES = ['le_crawler.spiders']
NEWSPIDER_MODULE = 'le_crawler.spiders'

SCHEDULER = "le_crawler.core.scheduler_client.CrawlDocScheduler"

#SCHEDULER = "le_crawler.core.scheduler.Scheduler"
#SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#SCHEDULER = "le_crawler.primary_scheduler.PrimaryScheduler"

SCHEDULER_PERSIST = True
INPUT_QUEUE_KEY = '%(spider)s:input_requests'
OUTPUT_QUEUE_KEY = '%(spider)s:output_requests'
INPUT_QUEUE_CLASS = "le_crawler.core.queue.SpiderPriorityQueue"
OUTPUT_QUEUE_CLASS = "le_crawler.core.queue.SpiderQueue"


ITEM_PIPELINES =  {
    'le_crawler.core.page_writer_pipeline.PageWriterPipeLine' : 999,
     }

DOWNLOADER_MIDDLEWARES = {
  'le_crawler.core.domain_filter_middleware.DomainFilterMiddleware':0,
  'le_crawler.common.bindaddressmiddleware.BindaddressMiddleWare': 10,
  'le_crawler.common.site_crawled_stats.DomainExceptionStats': 999,
}

#REDIS_SERVER_LIST = [('10.150.140.82', 6379),]
REDIS_SERVER_LIST = [('10.150.140.82', 6379),
                     ('10.150.140.83', 6379),
                     ('10.150.140.84', 6379),
                     ('10.150.140.85', 6379),
                     ('10.150.140.86', 6379),
                     ('10.150.140.87', 6379),
                     ('10.180.155.135', 6379),
                     ('10.180.155.136', 6379),
                     ('10.180.155.137', 6379),
                     ('10.180.155.138', 6379),
                     ('10.180.155.139', 6379),
                     ('10.130.208.60', 6379),
                     ('10.130.208.64', 6379),
                     ('10.130.208.65', 6379),
                     ('10.130.208.66', 6379),
                     ('10.130.208.67', 6379),
                     ]

DOWNLOAD_DELAY = 2

DUPEFILTER_CLASS = 'le_crawler.core.dupefilter.RFPDupeFilter'

COMPRESSION_ENABLED = True

CONCURRENT_ITEMS = 256

CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 10
CONCURRENT_REQUESTS_PER_IP = 0

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DEPTH_LIMIT = 20
DEPTH_STATS = True
DEPTH_PRIORITY = 1


DOWNLOAD_TIMEOUT = 60

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FORMATTER = 'le_crawler.common.log_format.LetvLogFormatter'
LOG_STDOUT = False
LOG_LEVEL = 'INFO'
LOG_FILE = '../log/crawler.log'

USER_AGENT = 'Mozilla/5.0 (X11; U; Linux x86_64; rv:2.0) Gecko/20110307 LetvCrawler/20140604 Firefox/4.0'

# if BINDIP_LOCAL is true BIND_ADDRESS_IP configure is disable
BINDIP_LOCAL = True

EXTENSIONS = {
    'le_crawler.common.site_crawled_stats.SiteCrawledStats': 0,
    'le_crawler.common.timer.TimerDispatcher': 100,
    }

# disable recrawler
#'le_crawler.recrawl.Recrawl': 50,
INPUT_QUEUE_SHARD_DIST = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
OUTPUT_QUEUE_SHARD_DIST = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
DUPE_SHARD_DIST = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1 , 1, 1, 1, 1, 1, 1]
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
le_crawler.core.page_writer.PageWriterBase,
le_crawler.common.sequence_file_writer.CrawlDocWriter
"""
#CRAWLDOC_SCHEDULER_HOST = '10.180.155.135'
#CRAWLDOC_SCHEDULER_PORT = 8088
