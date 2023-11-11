from abc import ABC, abstractmethod

import openai
import numpy as np
from pandas import DataFrame


class AbstractEmbeddings(ABC):
    """
    Abstract base class for creating embeddings.
    """

    @abstractmethod
    def create_embedding(self, input: str):
        """
        Abstract method to create an embedding for the given input.

        :param input: The input text to create an embedding for.
        """
        pass


class TextEmbeddings(AbstractEmbeddings):
    """
    Concrete class for creating text embeddings.
    """

    def __init__(self, embedding_engine: str):
        self.embedding_engine = embedding_engine

    def create_embedding(self, input: str):
        """
        Create an embedding for the given input text using the OpenAI API.

        :param input: The input text to create an embedding for.
        :return: The embedding as a list of floats.
        """
        try:
            response = openai.Embedding.create(input=input, engine=self.embedding_engine)
            return response["data"][0]["embedding"]
        except Exception as e:
            raise RuntimeError(f"Error in creating embedding: {e}.")


class DataFrameEmbeddings(AbstractEmbeddings):
    """
    Concrete class for creating embeddings for a DataFrame.
    """

    def __init__(self, df: DataFrame, embedding_engine: str):
        self.df = df
        self.embedding_engine = embedding_engine

    def create_embeddings(self) -> DataFrame:
        """
        Create embeddings for the text column of the given DataFrame using the OpenAI API.

        :return: The DataFrame with an additional 'embeddings' column containing the embeddings.
        """
        try:
            self.df["embeddings"] = self.df["text"].apply(
                lambda x: TextEmbeddings(self.embedding_engine).create_embedding(x) if x else None
            )
            return self.df
        except Exception as e:
            raise RuntimeError(f"Error in creating DataFrame embeddings: {e}.")

    def flatten_embeddings(self) -> DataFrame:
        """
        Flatten the embeddings column of the given DataFrame.

        :return: The DataFrame with the embeddings column flattened (numpy array).
        """
        self.df["embeddings"] = self.df["embeddings"].apply(np.array)
        return self.df
