from unittest import TestCase

import numpy as np
from pandas import DataFrame

from openaiapp.embeddings import create_embeddings_of_df_text, flatten_embeddings_of_df


class EmbeddingsTestCase(TestCase):
    def setUp(self):
        self.texts = [
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
        ]
        self.df = DataFrame({"text": self.texts})

    def test_should_create_embedding_for_each_text_chunk(self):
        """Should create an embedding for each DataFrame text chunk."""

        df = create_embeddings_of_df_text(df=self.df)

        self.assertIsInstance(df, DataFrame)
        self.assertEqual(set(df.columns), set(["text", "embeddings"]))

        text_list = df["text"].tolist()
        embedding_list = df["embeddings"].tolist()

        # If pass than it creates embeddings for each text chunk.
        self.assertEqual(len(self.texts), len(embedding_list))

        # General checks.
        self.assertIsInstance(text_list, list)
        self.assertIsInstance(embedding_list, list)

        self.assertIsInstance(text_list[0], str)
        for embedding in embedding_list:
            self.assertIsInstance(embedding[0], float)
            self.assertIsInstance(embedding, list)
            self.assertGreater(len(embedding), 0)

        self.assertEqual(self.texts, text_list)

    def test_should_flatten_embeddings_to_1d(self):
        """Should transform embeddings into numpy array of 1D."""

        df = create_embeddings_of_df_text(df=self.df)
        df = flatten_embeddings_of_df(df=df)

        self.assertIsInstance(df, DataFrame)
        self.assertEqual(set(df.columns), set(["text", "embeddings"]))

        text_list = df["text"].tolist()
        embedding_list = df["embeddings"].tolist()

        # If pass than it flattens embeddings to 1D.
        for embedding in embedding_list:
            self.assertIsInstance(embedding, np.ndarray)
            self.assertEqual(embedding.ndim, 1)

        # General checks.
        self.assertIsInstance(text_list, list)
        self.assertIsInstance(embedding_list, list)

        self.assertIsInstance(text_list[0], str)
        for embedding in embedding_list:
            self.assertIsInstance(embedding[0], float)
            self.assertGreater(len(embedding), 0)

        self.assertEqual(self.texts, text_list)
