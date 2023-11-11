from abc import ABC, abstractmethod
from typing import List

import tiktoken


class AbstractTokenizer(ABC):
    """
    Abstract base class for a tokenizer.
    """

    @abstractmethod
    def tokenize_text(self, text: str) -> List[List[int]]:
        """
        Abstract method to tokenize a given text.

        :param text: The text to be tokenized.
        :return: A list of lists of token IDs.
        """
        pass

    @abstractmethod
    def decode_tokens(self, tokens: List[int]) -> str:
        """
        Abstract method to decode a list of token IDs back to text.

        :param tokens: A list of token IDs.
        :return: The decoded text.
        """
        pass


class Tokenizer(AbstractTokenizer):
    """
    Concrete implementation of a tokenizer.
    """

    def __init__(self, encoding: str):
        """
        Initialize the tokenizer with a specific encoding.

        :param encoding: The encoding to be used by the tokenizer.
        """
        try:
            self.tokenizer = tiktoken.get_encoding(encoding)
        except Exception as e:
            raise ValueError(f"Failed to initialize tokenizer with encoding '{encoding}': {e}.")

    def tokenize_text(self, text: str) -> List[List[int]]:
        """
        Tokenize a given text.

        :param text: The text to be tokenized.
        :return: A list of lists of token IDs.
        """
        try:
            return self.tokenizer.encode(text)
        except Exception as e:
            raise RuntimeError(f"Error during tokenization: {e}.")

    def decode_tokens(self, tokens: List[int]) -> str:
        """
        Decode a list of token IDs back to text.

        :param tokens: A list of token IDs.
        :return: The decoded text.
        """
        try:
            return self.tokenizer.decode(tokens)
        except Exception as e:
            raise RuntimeError(f"Error during token decoding: {e}.")
