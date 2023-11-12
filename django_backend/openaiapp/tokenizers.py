from abc import ABC, abstractmethod
from typing import List

import tiktoken


class AbstractTokenizer(ABC):
    """
    Abstract base class for tokenizers.
    Defines the structure for tokenizing and decoding text.
    """

    @abstractmethod
    def tokenize_text(self, text: str) -> List[List[int]]:
        """
        Tokenize the given text.

        :param text: Text to be tokenized.
        :return: A list of lists containing token IDs.
        """
        pass

    @abstractmethod
    def decode_tokens(self, tokens: List[int]) -> str:
        """
        Decode a list of token IDs back into text.

        :param tokens: List of token IDs.
        :return: Decoded text.
        """
        pass


class Tokenizer(AbstractTokenizer):
    """
    A concrete implementation of the AbstractTokenizer.
    Utilizes the 'tiktoken' library for tokenization and decoding.
    """

    def __init__(self, encoding: str):
        """
        Initialize the tokenizer with the specified encoding.

        :param encoding: Encoding to use for the tokenizer.
        :raises ValueError: If the specified encoding is not supported.
        """
        try:
            self.tokenizer = tiktoken.get_encoding(encoding)
        except Exception as e:
            raise ValueError(f"Initialization error with encoding '{encoding}': {e}")

    def tokenize_text(self, text: str) -> List[List[int]]:
        """
        Tokenize the provided text.

        :param text: Text to tokenize.
        :return: A list of lists of token IDs.
        :raises RuntimeError: If tokenization fails.
        """
        try:
            return self.tokenizer.encode(text)
        except Exception as e:
            raise RuntimeError(f"Tokenization error: {e}")

    def decode_tokens(self, tokens: List[int]) -> str:
        """
        Decode the provided list of token IDs back to text.

        :param tokens: List of token IDs.
        :return: Decoded text.
        :raises RuntimeError: If decoding fails.
        """
        try:
            return self.tokenizer.decode(tokens)
        except Exception as e:
            raise RuntimeError(f"Decoding error: {e}")
