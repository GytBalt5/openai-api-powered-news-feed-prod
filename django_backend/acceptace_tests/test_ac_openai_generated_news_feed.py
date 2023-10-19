from django.test import TestCase

from scrapy.http import HtmlResponse
from scrapy.utils.test import get_crawler

from openaiapp.spiders import NewsSpider


class OpenAIGeneratedNewsFeedAcceptanceTestCase(TestCase):

    def test_should_crawl_website_and_return_all_text(self):
        """Should also crawl that website linked HTML documents (the same domain)."""
        domain = "example.com"
        url = "http://www.example.com"

        link1 = "http://www.example.com/page1.html"
        link2 = "/page2.html"
        other_link = "http://www.other.com"

        spider = NewsSpider(domain=domain)
        spider.start_urls = [url]

        crawler = get_crawler(spidercls=type(spider))
        crawler.spider = spider

        # Create a mock HTTP response with some sample HTML content.
        body1 = "<html><body><p>This is some sample text.</p></body></html>"
        response1 = HtmlResponse(url=url, body=body1)
        body2 = "<html><body><p>This is some sample text.</p></body></html>"
        response2 = HtmlResponse(url=link1, body=body2)
        body3 = "<html><body><p>This is some sample text.</p></body></html>"
        response3 = HtmlResponse(url=link2, body=body3)
        other_link_body = "<html><body><p>This is some sample text.</p></body></html>"
        response_from_other = HtmlResponse(url=other_link, body=other_link_body)

        # Call the spider's parse method with the mock response.
        spider.parse(response1)
        spider.parse(response2)
        spider.parse(response3)
        spider.parse(response_from_other)  # from other domain

        self.assertEqual(len(spider.text), 23 * 3)

    # def test_should_text_be_tokenized(self):
    #     """Should break down the text into tokens (words or punctuation) and returns them as a list."""
    #     pass

    # def test_should_from_tokens_create_embeddings(self):
    #     "Should create embeddings for a list of tokens."
    #     pass

    # def test_should_find_most_similar_context_for_question(self):
    #     """Should find the most similar context for question from vector database."""
    #     pass

    # def test_should_openai_generate_answer_for_question(self):
    #     """Should by the most similar context from the vector db and OpenAI's API generate a completion that answers a question."""
    #     pass
