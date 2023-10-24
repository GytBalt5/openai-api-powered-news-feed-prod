from django.test import TestCase

from pandas import DataFrame

from openaiapp.embeddings import create_embeddings_of_df_text, flatten_embeddings_of_df
from openaiapp.ai_question_answering import create_context


class AIQuestionAnswering(TestCase):
    def setUp(self):
        self.texts = [
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra Csharp.",
        ]
        self.df = DataFrame({"text": self.texts})

    def test_should_context_for_question_be_created(self):
        """Should a context for a question be created by finding the most similar context from the data frame."""
        question = "What Csharp programming language pron and cons?"
        
        df = create_embeddings_of_df_text(df=self.df)
        df = flatten_embeddings_of_df(df=df)
        
        context = create_context(question, df)

        self.assertIsInstance(context, str)
        self.assertEqual(context, self.texts[1])
