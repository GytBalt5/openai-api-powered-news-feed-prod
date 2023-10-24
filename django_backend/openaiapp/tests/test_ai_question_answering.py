from unittest.mock import patch, MagicMock
from django.test import TestCase

from pandas import DataFrame

from openaiapp.embeddings import create_embeddings_of_df_text, flatten_embeddings_of_df
from openaiapp.ai_question_answering import create_context, answer_question


# TODO. Need more testing (edge cases, etc.), use mocking.
class AIQuestionAnsweringTestCase(TestCase):
    def setUp(self):
        self.texts = [
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra Csharp.",
        ]
        df = DataFrame({"text": self.texts})
        df = create_embeddings_of_df_text(df=df)
        self.df = flatten_embeddings_of_df(df=df)

    def test_should_be_created_context_for_question(self):
        """Should a context for a question be created by finding the most similar context from the data frame."""

        question = "What Csharp programming language pron and cons?"
        context = create_context(question, self.df, max_len=30)

        self.assertIsInstance(context, str)
        self.assertEqual(context, self.texts[1])

    def test_should_answer_question(self):
        question = "What Matcha tea pron and cons?"
        answer = answer_question(question=question, df=self.df)

        self.assertIsInstance(answer, str)
        self.assertEqual(answer, "I don't know")

    def test_should_answer_question_mocking_example(self):
        with patch('openaiapp.ai_question_answering.create_context') as mock_create_context, \
             patch('openai.Completion.create') as mock_completion_create:
            mock_create_context.return_value = "context"
            mock_completion_create.return_value = {"choices": [{"text": "answer"}]}
            question = "What Matcha tea pron and cons?"
            answer = answer_question(question=question, df=self.df)

            self.assertIsInstance(answer, str)
            self.assertEqual(answer, "answer")
