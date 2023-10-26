from django.test import TestCase

import numpy as np
from pandas import DataFrame

from openaiapp.embeddings import AbstractEmbeddings, get_embeddings_object


class EmbeddingsTestCase(TestCase):
    def setUp(self):
        self.texts = [
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
        ]
        df = DataFrame({"text": self.texts})
        self.embeddings_obj = get_embeddings_object(data_object=df)

    def test_should_embeddings_instance_inherits_abstract(self):
        """
        Test that the embeddings instance is also an instance of the AbstractEmbeddings class.
        """
        obj = get_embeddings_object(data_object=DataFrame({"text": ["test"]}))
        self.assertIsInstance(obj, AbstractEmbeddings)

    def test_should_raise_exception_with_unsupported_data_object(self):
        """ 
        Test that creating an embeddings object with an unsupported data object raises a TypeError.
        """
        with self.assertRaises(TypeError):
            get_embeddings_object(data_object=["a", "b"])

    def test_should_create_embedding_for_each_text_chunk(self):
        """
        Should create an embedding for each DataFrame text chunk.
        """
        df = self.embeddings_obj.create_embeddings()

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
        """
        Should transform embeddings into numpy array of 1D.
        """
        df = self.embeddings_obj.create_embeddings()
        df = self.embeddings_obj.flatten_embeddings()

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

    def test_should_save_flatten_embeddings_to_vector_db(self):
        """
        Should save flatten embeddings to the vector database.
        """ 
        raise NotImplementedError
