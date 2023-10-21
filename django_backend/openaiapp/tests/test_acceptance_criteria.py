from django.test import TestCase

from scrapy.http import HtmlResponse

from openaiapp.spiders import NewsSpider
from openaiapp.utils import tokenize_text


class OpenAIGeneratedNewsFeedAcceptanceTestCase(TestCase):
    def test_should_crawl_website_and_return_all_text(self):
        """Should crawl the website and linked HTML documents within the same domain."""
        domain = "example.com"
        url = f"http://{domain}"
        link1 = f"http://{domain}/page1.html"
        link2 = f"http://{domain}/page2.html"
        link3 = "/page3.html"
        sharp_link = "#"
        mailto_link = "mailto:johnbrawo1231@gg123mail.com"
        js_link = f"/file.js"
        other_link = "http://www.other.com"

        spider = NewsSpider(domain=domain, start_urls=[url])

        # Define URLs and corresponding bodies.
        url_bodies = [
            (
                url,
                "<html><body><p>This is some sample text.</p></body></html>",
                {"Content-Type": "text/html"},
            ),
            (
                link1,
                "<html><body><p>This is some sample text.</p></body></html>",
                {"Content-Type": "text/html"},
            ),
            (
                link2,
                "<html><body><p>This is some sample text.</p></body></html>",
                {"Content-Type": "text/html"},
            ),
            (
                link3,
                "<html><body><p>This is some sample text.</p></body></html>",
                {"Content-Type": "text/html"},
            ),
            (
                sharp_link,
                "<html><body><p>[BAD-#]This is some sample text.</p></body></html>",
                {"Content-Type": "text/html"},
            ),
            (
                mailto_link,
                "<html><body><p>[BAD-mailto]This is some sample text.</p></body></html>",
                {"Content-Type": "text/html"},
            ),
            (js_link, "/*[BAD-js]*/", {"Content-Type": "file/js"}),
            (
                other_link,
                "<html><body><p>[BAD-other]This is some sample text.</p></body></html>",
                {"Content-Type": "text/html"},
            ),
        ]

        # Create mock HTTP responses with sample HTML content.
        responses = [
            HtmlResponse(
                url=url, body=body.encode("utf-8"), headers=headers, encoding="utf-8"
            )
            for url, body, headers in url_bodies
        ]

        # Call the spider's parse methods for mock responses.
        for response in responses:
            spider.parse(response)

        expected_articles = [
            {"url": url, "text": "This is some sample text."},
            {"url": link1, "text": "This is some sample text."},
            {"url": link2, "text": "This is some sample text."},
            {"url": link3, "text": "This is some sample text."},
        ]
        self.assertEqual(expected_articles, spider.articles)

    def test_should_text_be_tokenized(self):
        """Should break down the text into tokens (words or punctuation) and returns them as a list."""
        sample_text = (
            "Fact-based news, exclusive video footage, photos and updated maps."
        )
        tokens_list = tokenize_text(sample_text)
        expected_tokens_list = [
            "Fact",
            "-based",
            " news",
            ",",
            " exclusive",
            " video",
            " footage",
            ",",
            " photos",
            " and",
            " updated",
            " maps",
            ".",
        ]

        self.assertEqual(expected_tokens_list, tokens_list)

    # def test_should_from_tokens_create_embeddings(self):
    #     "Should create embeddings for a list of tokens."
    #     pass

    # def test_should_find_most_similar_context_for_question(self):
    #     """Should find the most similar context for question from vector database."""
    #     pass

    # def test_should_openai_generate_answer_for_question(self):
    #     """Should by the most similar context from the vector db and OpenAI's API generate a completion that answers a question."""
    #     pass
