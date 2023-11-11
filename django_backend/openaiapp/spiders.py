from bs4 import BeautifulSoup

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class NewsSpider(CrawlSpider):
    name = "news_spider"

    def __init__(self, domain: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_domains = [domain] if domain else []
        self.start_urls = kwargs.get("start_urls", [])

        # Define the rules for link extraction and crawling.
        self.rules = (
            Rule(
                LinkExtractor(allow_domains=self.allowed_domains),
                callback=self.parse,
                follow=True,
            ),
        )

        self.articles = []

    def parse(self, response):
        # Ensure the response is of type HTML.
        if not response.headers.get("Content-Type").startswith(b"text/html"):
            return
        url = response.url
        # Check if the response URL's domain is in the allowed domains.
        if any(domain in url for domain in self.allowed_domains) or url.startswith("/"):
            # Extract and clean the text from the response.
            soup = BeautifulSoup(response.text, "html.parser")
            text = " ".join(soup.stripped_strings)

            article = {
                "url": url,
                "text": text,
            }
            self.articles.append(article)
