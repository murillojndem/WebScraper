BOT_NAME = "core"

SPIDER_MODULES = ["core.spiders"]
NEWSPIDER_MODULE = "core.spiders"

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 0.25
CONCURRENT_REQUESTS_PER_DOMAIN = 1

FEED_EXPORT_ENCODING = "utf-8"

ITEM_PIPELINES = {
    "core.pipelines.CleanItemPipeline": 300,
}

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

RETRY_ENABLED = True
RETRY_TIMES = 3
DOWNLOAD_TIMEOUT = 10

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOG_FILE = "scrapy.log"