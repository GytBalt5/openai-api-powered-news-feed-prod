from abc import ABC, abstractmethod

from django.conf import settings

import openai
import numpy as np
from pandas import DataFrame


openai.api_key = settings.OPENAI_API_KEY


class AbstractEmbeddings(ABC):
    @abstractmethod
    def create_embedding(self, input: str):
        pass


class SimpleEmbeddings(AbstractEmbeddings):
    EMBEDDING_ENGINE = "text-embedding-ada-002"

    def create_embedding(self, input: str):
        """
        Create an embedding for the given input text using the OpenAI API.

        Args:
            input: The input text to create an embedding for.
        """
        return openai.Embedding.create(input=input, engine=self.EMBEDDING_ENGINE)[
            "data"
        ][0]["embedding"]


class DataFrameEmbeddings(SimpleEmbeddings):
    def __init__(self, df: DataFrame):
        super().__init__()
        self.df = df

    def create_embeddings(self) -> DataFrame:
        """
        Create embeddings for the text column of the given DataFrame using the OpenAI API.

        Returns:
            The DataFrame with an additional embeddings column containing the embeddings.
        """
        self.df["embeddings"] = self.df.text.apply(
            lambda x: self.create_embedding(input=x)
        )
        return self.df

    def flatten_embeddings(self) -> DataFrame:
        """
        Flatten the embeddings column of the given DataFrame.

        Returns:
            The DataFrame with the embeddings column flattened (numpy array).
        """
        self.df["embeddings"] = self.df["embeddings"].apply(np.array)
        return self.df


def get_embeddings_object(data_object=None) -> AbstractEmbeddings:
    """
    Get an embeddings object for the given data object.
    """
    if data_object is None:
        return SimpleEmbeddings()
    elif isinstance(data_object, DataFrame):
        return DataFrameEmbeddings(data_object)
    raise TypeError("The data object is not supported.")
