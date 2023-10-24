from django.test import TestCase


class OpenAINewsFeedGeneratorAcceptanceTestCase(TestCase):
    def test_should_return_news_feed(self):
        """
        Should AI generate 10 key points about the selected topic
        (short-structured news feed).
        """
        
        # TODO.
        #test_should_crawl_website_and_return_all_text:
        # Should crawl the website and linked HTML documents within the same domain.
        
        # TODO.
        #test_should_text_be_tokenized:
        # Should break down the text into tokens (words or punctuation) and returns them as a list.

        # TODO.
        #test_should_text_be_preprocessed:
        # ...   

        # TODO.
        #test_should_form_text_chunks_create_embeddings:
        # ...

        # TODO.
        #test_should_save_flatten_embeddings_of_df_to_vector_db:
        # Should be saved flatten embeddings of df to the vector database.

        # TODO.
        #test_should_find_most_similar_context_for_question(self):
        # Should find the most similar context for question from vector database.

        # TODO.
        #test_should_openai_generate_answer_for_question(self):
        # Should by the most similar context from the vector db and OpenAI's API generate a completion that answers a question.

        raise NotImplementedError
