from abc import ABC, abstractmethod

from django.conf import settings

import openai
import numpy as np
from pandas import DataFrame


openai.api_key = settings.OPENAI_API_KEY
EMBEDDING_ENGINE = "text-embedding-ada-002"


class AbstractEmbeddings(ABC):
    @abstractmethod
    def create_embedding(self, input: str):
        pass


class DataFrameEmbeddings(AbstractEmbeddings):
    def __init__(self, df: DataFrame):
        self.df = df

    def create_embedding(self, input: str):
        """
        Create an embedding for the given input text using the OpenAI API.

        Args:
            input: The input text to create an embedding for.
        """
        return openai.Embedding.create(input=input, engine=EMBEDDING_ENGINE)["data"][0]["embedding"]

    def create_embeddings_for_df_texts(self) -> DataFrame:
        """
        Create embeddings for the text column of the given DataFrame using the OpenAI API.

        Returns:
            The DataFrame with an additional embeddings column containing the embeddings.
        """
        self.df["embeddings"] = self.df.text.apply(lambda x: self.create_embedding(input=x))
        return self.df

    def flatten_embeddings_of_df(self) -> DataFrame:
        """
        Flatten the embeddings column of the given DataFrame.

        Returns:
            The DataFrame with the embeddings column flattened (numpy array).
        """
        self.df["embeddings"] = self.df["embeddings"].apply(np.array)
        return self.df


def get_embeddings_object(data_object):
    """
    Get an embeddings object for the given data object.
    """
    if isinstance(data_object, DataFrame):
        return DataFrameEmbeddings(data_object)
    raise TypeError("The data object is not supported.")
