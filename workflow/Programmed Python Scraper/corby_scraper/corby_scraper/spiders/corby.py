import scrapy
from urllib.parse import urljoin, urlencode, urlparse, parse_qs, unquote
import trafilatura

from corby_scraper.hate_terms import TERMS, TERM_MAP
from corby_scraper.proximity import near


def extract_real_url(duck_url):
    """
    Extract the real target URL from DuckDuckGo redirect links.
    Example:
        https://duckduckgo.com/l/?uddg=https%3A%2F%2Fwww.theage.com.au%2F...
    """
    parsed = urlparse(duck_url)
    qs = parse_qs(parsed.query)
    if "uddg" in qs:
        return unquote(qs["uddg"][0])
    return duck_url


class CorbySpider(scrapy.Spider):
    name = "corby"

    SEARCH_TERMS = [
        '"schapelle corby"',
        '"schapelle corby" conviction',
        '"schapelle corby" legal',
        '"schapelle corby" bribe',
        '"schapelle corby" news',
        '"schapelle corby" controversy',
    ]

    JS_HEAVY_DOMAINS = [
        "reddit.com",
        "twitter.com",
        "facebook.com",
        "instagram.com",
        "tiktok.com",
        "youtube.com",
    ]

    visited = set()

    def start_requests(self):
        base = "https://lite.duckduckgo.com/lite/?"
        for term in self.SEARCH_TERMS:
            params = urlencode({"q": term})
            url = base + params
            yield scrapy.Request(url, callback=self.parse_results, meta={"query": term})

    def parse_results(self, response):
        query = response.meta["query"]
        self.logger.info(f"[{query}] DuckDuckGo Lite: {response.url}")

        # UPDATED SELECTOR — DuckDuckGo Lite changed its HTML
        links = response.css("a.result__a::attr(href)").getall()

        # fallback if DDG changes again
        if not links:
            links = response.css("a[href*='uddg=']::attr(href)").getall()

        self.logger.info(f"[{query}] Found {len(links)} links")

        for link in links:
            absolute = urljoin(response.url, link)

            if absolute in self.visited:
                continue
            self.visited.add(absolute)

            if any(domain in absolute for domain in self.JS_HEAVY_DOMAINS):
                continue

            yield scrapy.Request(
                absolute,
                callback=self.parse_article,
                meta={"query": query}
            )

    def parse_article(self, response):
        query = response.meta["query"]

        # Extract the real URL before using Trafilatura
        real_url = extract_real_url(response.url)
        self.logger.info(f"[{query}] Real URL: {real_url}")

        downloaded = trafilatura.fetch_url(real_url)
        if not downloaded:
            self.logger.info(f"[{query}] Trafilatura failed to fetch")
            return

        text = trafilatura.extract(downloaded)
        if not text:
            self.logger.info(f"[{query}] Trafilatura extracted no text")
            return

        text_lower = text.lower()

        # Always yield the article (no hatescale filtering)
        found_terms = [t for t in TERMS if near(text_lower, t, window=5000)]

        yield {
            "query": query,
            "url": real_url,
            "hate_terms_found": found_terms,
            "categories": list({TERM_MAP[t] for t in found_terms}) if found_terms else [],
            "text_excerpt": text_lower[:500],
        }
