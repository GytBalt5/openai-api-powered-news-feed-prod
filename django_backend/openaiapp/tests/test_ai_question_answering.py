from unittest.mock import patch

from django.test import TestCase

from pandas import DataFrame

from openaiapp.embeddings import get_embeddings_object
from openaiapp.ai_question_answering import AbstractAIQuestionAnswering, get_ai_question_answering_object


class AIQuestionAnsweringTestCase(TestCase):
    def setUp(self):
        self.texts = [
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra Csharp.",
        ]
        df = DataFrame({"text": self.texts})
        embeddings_object = get_embeddings_object(data_object=df)
        df = embeddings_object.create_embeddings()
        self.df = embeddings_object.flatten_embeddings()
        self.ai_qa = get_ai_question_answering_object(data_object=self.df)

    def test_should_question_answering_instance_also_be_abstract(self):
        """
        Test that the AIQuestionAnswering instance is also an instance of the AbstractAIQuestionAnswering class.
        """
        self.assertIsInstance(self.ai_qa, AbstractAIQuestionAnswering)

    def test_should_be_created_context_for_question(self):
        """
        Test that a context for a question is created by finding the most similar context from the data frame.
        """
        question = "What Csharp programming language pron and con?"
        context = self.ai_qa.create_context(question=question, max_len=30)

        self.assertIsInstance(context, str)
        self.assertEqual(context, self.texts[1])

    def test_should_answer_question(self):
        """
        Test if can answer the question.
        """
        with patch(
            f"openaiapp.ai_question_answering.{type(self.ai_qa).__name__}.create_context"
        ) as mock_create_context, patch(
            "openai.Completion.create"
        ) as mock_completion_create:
            # Mock the create_context and Completion.create methods.
            mock_create_context.return_value = "context"
            mock_completion_create.return_value = {"choices": [{"text": "I don't know"}]}
            question = "What Matcha tea pron and con?"
            answer = self.ai_qa.answer_question(question=question)

            self.assertIsInstance(answer, str)
            self.assertEqual(answer, "I don't know")
