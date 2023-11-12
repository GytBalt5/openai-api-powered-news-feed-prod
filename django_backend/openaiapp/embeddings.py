from abc import ABC, abstractmethod
from typing import List, Union

import openai
import numpy as np
from pandas import DataFrame


class AbstractEmbeddings(ABC):
    """
    Abstract base class for creating embeddings.
    Defines a standard interface for embedding generation.
    """

    @abstractmethod
    def create_embeddings(self, input: Union[str, DataFrame]):
        """
        Abstract method to create embeddings from the given input.
        """
        pass


class TextEmbeddings(AbstractEmbeddings):
    """
    Concrete class for creating text embeddings using OpenAI API.
    """

    def __init__(self, embedding_engine: str):
        self.embedding_engine = embedding_engine

    def create_embeddings(self, input: str) -> List[float]:
        """
        Create an embedding for the given input text.

        :param input: The input text to create an embedding for.
        :return: The embedding as a list of floats.
        """
        try:
            response = openai.Embedding.create(
                input=input, engine=self.embedding_engine
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            raise RuntimeError(f"Error in creating text embedding: {e}.")


class DataFrameEmbeddings(AbstractEmbeddings):
    """
    Concrete class for creating embeddings for a DataFrame using OpenAI API.
    """

    def __init__(self, embedding_engine: str):
        self.embedding_engine = embedding_engine

    def create_embeddings(self, input: DataFrame) -> DataFrame:
        """
        Create embeddings for the 'text' column of the given DataFrame.

        :param input: DataFrame with a 'text' column.
        :return: DataFrame with an additional 'embeddings' column.
        """
        try:
            input["embeddings"] = input["text"].apply(
                lambda text: TextEmbeddings(self.embedding_engine).create_embeddings(
                    text
                )
                if text
                else None
            )
            return input
        except Exception as e:
            raise RuntimeError(f"Error in creating DataFrame embeddings: {e}.")

    def flatten_embeddings(self, input: DataFrame) -> DataFrame:
        """
        Flatten the 'embeddings' column of the DataFrame into a numpy array.

        :param input: DataFrame with an 'embeddings' column.
        :return: DataFrame with the 'embeddings' column flattened.
        """
        input["embeddings"] = input["embeddings"].apply(np.array)
        return input
