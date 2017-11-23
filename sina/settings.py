
BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'
#===================================================================
CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 1

# COOKIES_ENABLED = False
#===================================================================
# LOG_FILE = "sina.log"
# LOG_LEVEL = "INFO"

DOWNLOADER_MIDDLEWARES = {
    'sina.middlewares.UserAgentMiddleware': 401,
    'sina.middlewares.CookiesMiddleware': 402,
}

ITEM_PIPELINES = {
    'sina.pipelines.MongoDBPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,
}
#====================================================================
# PYMONGO SETTINGS
MONGODB_SERVER = "localhost"   
MONGODB_PORT = 27017   
MONGODB_DB = "Sina"   
MONGODB_COLLECTION_INFOMATION = "Information"
MONGODB_COLLECTION_TWEETS = "Tweets"
MONGODB_COLLECTION_RELATIONSHIPS = "Relationships"

#=====================================================================
# SCRAPY_REDIS_EXTENT SETTINGS
# SCHEDULER = 'sina.scrapy_redis.scheduler.Scheduler'
# SCHEDULER_PERSIST = True
# SCHEDULER_QUEUE_CLASS = 'sina.scrapy_redis.queue.SpiderSimpleQueue'

# SEED URLS QUEUE 
# REDIE_URL = None
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379

# FILTER QUEUE
# FILTER_URL = None
# FILTER_HOST = 'localhost'
# FILTER_PORT = 6379
# FILTER_DB = 0
#======================================================================

# REDEFINE THREE MODULE BASED ON scrapy-redis
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
SCHEDULER_PERSIST = True


# SEED URLS QUEUE 
REDIE_URL = None
REDIS_HOST = '192.169.1.199'
REDIS_PORT = 6379

# FILTER QUEUE
# FILTER_URL = None
# FILTER_HOST = '192.168.1.199'
# FILTER_PORT = 6379
# FILTER_DB = 0


#======================================================================

# AVOID 302
REDIRECT_ENABLED = False
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60
