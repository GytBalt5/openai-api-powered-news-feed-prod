import unittest

from django.test import TestCase
from django.test.runner import DiscoverRunner

from openaiapp.tests.unittest_crawler import CrawlerTestCase
from openaiapp.tests.unittest_tokenizer import TokenizerTestCase
from openaiapp.tests.unittest_text_preparator import (
    SimpleTextPreparatorTestCase,
    DataFrameTextPreparatorTestCase,
)
from openaiapp.tests.unittest_embeddings import EmbeddingsTestCase
from openaiapp.tests.unittest_ai_question_answering import AIQuestionAnsweringTestCase
from openaiapp.main import NewsFeedTextGenerator


class OpenAIGeneratorOfNewsFeedTextAcceptanceTestCase(TestCase):
    def run_tests_from_other_test_case(self, test_case_class):
        test_suite = unittest.TestLoader().loadTestsFromTestCase(test_case_class)
        test_runner = DiscoverRunner(verbosity=2)

        result = test_runner.run_suite(test_suite)

        # Check if any tests failed and print details.
        if result.failures or result.errors:
            return result, False
        return result, True

    def test_should_crawl_website_and_return_all_text(self):
        """
        1. Should crawl the website and link HTML documents within the same domain.
        """
        _, success = self.run_tests_from_other_test_case(CrawlerTestCase)
        self.assertTrue(success, f"Test failed.")

    def test_should_break_down_text_into_tokens(self):
        """
        2. Should break down the text into tokens.
        """
        _, success = self.run_tests_from_other_test_case(TokenizerTestCase)
        self.assertTrue(success, f"Test failed.")

    def test_should_preprocess_text(self):
        """
        3. Should text be preprocessed (chunked + shortened).
        """
        success = self.run_tests_from_other_test_case(SimpleTextPreparatorTestCase)
        self.assertTrue(success, "Test failed.")
        success = self.run_tests_from_other_test_case(DataFrameTextPreparatorTestCase)
        self.assertTrue(success, "Test failed.")

    def test_should_create_embeddings(self):
        """
        4. Should be flattened embeddings created.
        TODO 1.
        Not implemented yet.
        5. Should be flattened embeddings saved to the vector database.
        """
        _, success = self.run_tests_from_other_test_case(EmbeddingsTestCase)
        self.assertTrue(success, f"Test failed.")

    def test_should_find_context_and_answer_question(self):
        """
        TODO 2.
        In the future needs to be changed from DataFrame to vector database.
        Should find the most similar context for the question from the vector database.
        6. Should find the most similar context for a question.
        7. Should by using the most similar context generate a completion that answers a question.
        """
        _, success = self.run_tests_from_other_test_case(AIQuestionAnsweringTestCase)
        self.assertTrue(success, f"Test failed.")

    def test_should_generate_news_feed_text_10_key_points(self):
        """
        Should AI generate 10 key points about the selected topic
        (short-structured news feed).

        Testing the OpenAIApp all functionalities (1-7) general result.

        TODO 3.
        Need to use mocking for returning key points.
        Also add assertions for that.
        """
        key_points = NewsFeedTextGenerator().generate_news_feed_text_key_points(
            html_doc_url="https://www.bbc.com/news/world-europe-57978443",
            key_points_num=10,
        )

        self.assertIsInstance(key_points, list)
        self.assertEqual(len(key_points), 10)
