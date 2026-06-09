BOT_NAME = "corby_scraper"

SPIDER_MODULES = ["corby_scraper.spiders"]
NEWSPIDER_MODULE = "corby_scraper.spiders"

# Ignore robots.txt so Google links work
ROBOTSTXT_OBEY = False

# Pretend to be a real browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"

# Allow redirects from Google search results
REDIRECT_ENABLED = True

# Slow down crawling slightly
DOWNLOAD_DELAY = 1

# Export encoding
FEED_EXPORT_ENCODING = "utf-8"

# Allow crawling ANY domain
# (Google search results point to many different sites)
# You can remove allowed_domains entirely in the spider
