from abc import ABC, abstractmethod
from typing import List, Union

from django.conf import settings

import openai
from pandas import DataFrame
from scrapy.spiders import CrawlSpider

from openaiapp.spiders import NewsSpider
from openaiapp.tokenizers import AbstractTokenizer, Tokenizer
from openaiapp.embeddings import AbstractEmbeddings, TextEmbeddings, DataFrameEmbeddings
from openaiapp.text_preparators import AbstractTextPreparatory, TextPreparatory, DataFrameTextPreparatory
from openaiapp.ai_question_answering import AbstractAIQuestionAnswering, AIQuestionAnsweringBasedOnContext


# Set the OpenAI API key from Django settings.
openai.api_key = settings.OPENAI_API_KEY


class Factory(ABC):
    """
    Abstract base class for factories creating various objects.
    """

    @abstractmethod
    def create_object(self, *args, **kwargs):
        """
        Abstract method to create an object.
        """
        pass


class SpiderFactory(Factory):
    """
    Factory for creating web spider objects.
    """

    def create_object(self, domain: str, start_urls: List[str]) -> CrawlSpider:
        """
        Create a NewsSpider object.

        :param domain: The domain for the spider.
        :param start_urls: A list of URLs where the spider starts crawling.
        :return: An instance of NewsSpider.
        """
        return NewsSpider(domain=domain, start_urls=start_urls)


class TokenizerFactory(Factory):
    """
    Factory for creating tokenizer objects.
    """
    TOKENIZER_ENCODING = "cl100k_base"

    def create_object(self, encoding: str = TOKENIZER_ENCODING) -> AbstractTokenizer:
        """
        Create a Tokenizer object.

        :param encoding: The encoding to be used by the tokenizer.
        :return: An instance of Tokenizer.
        """
        return Tokenizer(encoding=encoding)


class EmbeddingsFactory(Factory):
    """
    Factory for creating embeddings objects.
    """
    EMBEDDING_ENGINE = "text-embedding-ada-002"

    def create_object(self, input: Union[str, DataFrame], embedding_engine: str = EMBEDDING_ENGINE) -> AbstractEmbeddings:
        """
        Create an embeddings object based on the input type.

        :param input: A string or DataFrame for which embeddings are to be created.
        :param embedding_engine: The engine to use for creating embeddings.
        :return: An instance of AbstractEmbeddings.
        :raises TypeError: If the input type is not supported.
        """
        if isinstance(input, str):
            return TextEmbeddings(input=input, embedding_engine=embedding_engine)
        elif isinstance(input, DataFrame):
            return DataFrameEmbeddings(df=input, embedding_engine=embedding_engine)
        else:
            raise TypeError(f"Unsupported input type {type(input)}.")


class DataPreparatoryFactory(Factory):
    """
    Factory for creating data preparatory objects.
    """
    MIN_TOKENS = 8
    MAX_TOKENS = 512

    def create_object(self, df: DataFrame = None) -> AbstractTextPreparatory:
        """
        Create a text preparatory object.

        :param df: A DataFrame for text preparation, if any.
        :return: An instance of AbstractTextPreparatory.
        """
        if df is None:
            return TextPreparatory()
        else:
            return DataFrameTextPreparatory(df=df, min_tokens=self.MIN_TOKENS, max_tokens=self.MAX_TOKENS)


class AIQuestionAnsweringFactory(Factory):
    """
    Factory for creating AI question answering objects.
    """
    MODEL = "gpt-3.5-turbo-instruct"
    ANSWER_MAX_TOKENS = 256
    CONTEXT_MAX_LEN = 2048

    def create_object(self, df: DataFrame, stop_sequence: str = None, model: str = MODEL, answer_max_tokens: int = ANSWER_MAX_TOKENS, context_max_len: int = CONTEXT_MAX_LEN) -> AbstractAIQuestionAnswering:
        """
        Create an AIQuestionAnsweringBasedOnContext object.

        :param df: A DataFrame to use for context creation.
        :param stop_sequence: A sequence indicating where to stop the answer generation.
        :param model: The model to use for question answering.
        :param answer_max_tokens: The maximum number of tokens for the answer.
        :param context_max_len: The maximum length of the context.
        :return: An instance of AIQuestionAnsweringBasedOnContext.
        """
        return AIQuestionAnsweringBasedOnContext(
            df=df,
            model=model,
            max_tokens=answer_max_tokens, 
            context_max_len=context_max_len,
            stop_sequence=stop_sequence,
        )


class OpenAIAppObjectFactory(Factory):
    """
    An abstract factory for creating various OpenAI app-related objects.
    """

    def __init__(self, factory: Factory):
        """
        Initialize the OpenAIAppObjectFactory with a specific factory.

        :param factory: The specific factory to use for object creation.
        """
        self.factory = factory

    def create_object(self, *args, **kwargs):
        """
        Create an object using the specified factory.

        :return: An object created by the specified factory.
        """
        return self.factory.create_object(*args, **kwargs)
