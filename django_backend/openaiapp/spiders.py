from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup


class NewsSpider(CrawlSpider):
    name = "news_spider"

    def __init__(self, domain=None, *args, **kwargs):
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
        # Check if the response URL's domain is in the allowed domains.
        if any(domain in response.url for domain in self.allowed_domains):
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract and clean the text from the response.
            text = " ".join(soup.stripped_strings)

            article = {
                "url": response.url,
                "text": text,
            }
            self.articles.append(article)
