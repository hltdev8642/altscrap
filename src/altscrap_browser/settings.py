# Scrapy settings for altscrap_browser project

BOT_NAME = 'altscrap_browser'

SPIDER_MODULES = ['altscrap_browser.spiders']
NEWSPIDER_MODULE = 'altscrap_browser.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure pipelines
ITEM_PIPELINES = {
    'altscrap_browser.pipelines.AltscrapBrowserPipeline': 300,
}

# Set user agent to avoid blocking
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'

# Default request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://alternativeto.net/',
}

# Download delay
DOWNLOAD_DELAY = 1
