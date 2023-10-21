from django.test import TestCase

from scrapy.http import HtmlResponse

from openaiapp.spiders import NewsSpider


class CrawlerTestCase(TestCase):
    def test_should_spider_extract_from_html_response_all_text(self):
        """Test whether the spider correctly extracts all text from an HTML response."""
        domain = "example.com"
        url = f"http://www.{domain}"
        body = "<html><body><p>This is some sample text.</p></body></html>"
        headers = {"Content-Type": "text/html"}

        # Creating a mock HTTP response with the sample HTML content.
        response = HtmlResponse(
            url=url, body=body.encode("utf-8"), headers=headers, encoding="utf-8"
        )
        spider = NewsSpider(domain=domain, start_urls=[url])

        spider.parse(response)

        expected_articles = [{"url": url, "text": "This is some sample text."}]
        self.assertEqual(expected_articles, spider.articles)
