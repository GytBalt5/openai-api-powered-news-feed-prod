"""
*
*** TODO. 
*** Need to execute created test cases from this global test file test case.
*
"""

from django.test import TestCase

from openaiapp.main import NewsFeedTextGenerator


class OpenAIGeneratorOfNewsFeedTextAcceptanceTestCase(TestCase):
    def test_should_crawl_website_and_return_all_text(self):
        """
        1. Should crawl the website and link HTML documents within the same domain.
        """
        raise NotImplementedError

    def test_should_break_down_text_into_tokens(self):
        """
        2. Should break down the text into tokens.
        """
        raise NotImplementedError

    def test_should_preprocess_text(self):
        """
        3. Should text be preprocessed (chunked + shortened).
        """
        raise NotImplementedError

    def test_should_create_flatten_embeddings(self):
        """
        4. Should be flattened embeddings created.
        """
        raise NotImplementedError

    def test_should_save_flatten_embeddings_to_vector_db(self):
        """
        TODO 1.
        Not implemented yet.
        5. Should be flattened embeddings saved to the vector database.
        """
        raise NotImplementedError

    def test_should_find_most_similar_context_for_question(self):
        """
        TODO 2.
        In the future needs to be changed from DataFrame to vector database.
        Should find the most similar context for the question from the vector database.
        6. Should find the most similar context for a question.
        """
        raise NotImplementedError

    def test_should_generate_completion_that_answers_question(self):
        """
        7. Should by using the most similar context generate a completion that answers a question.
        """
        raise NotImplementedError

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
