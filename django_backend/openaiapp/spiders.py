import scrapy
from bs4 import BeautifulSoup


class NewsSpider(scrapy.Spider):
    name = 'news_spider'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    def parse(self, response):
        # Extract the text from the response.
        soup = BeautifulSoup(response.text, 'html.parser')
        self.text = soup.get_text()

        # Get the hyperlinks from the response and follow them.
        for link in response.css('a::attr(href)').getall():
            if link.startswith('/') or link.startswith(self.start_urls[0]):
                yield scrapy.Request(response.urljoin(link), callback=self.parse)
