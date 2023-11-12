import re
from typing import List
from abc import ABC, abstractmethod

from pandas import DataFrame


class AbstractTextPreparatory(ABC):
    """
    Abstract base class for text preparation.
    Provides a structure for splitting text into manageable chunks.
    """

    @abstractmethod
    def split_text_into_chunks(self, text: str, max_tokens: int) -> List[str]:
        """
        Splits a text into chunks, each with a maximum token limit.
        """
        pass


class TextPreparatory(AbstractTextPreparatory):
    """
    Concrete implementation for text preparation.
    Splits text into chunks based on token limits.
    """

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def split_text_into_chunks(self, text: str, max_tokens: int) -> List[str]:
        """
        Splits text into chunks, each with at most `max_tokens` tokens.
        """
        sentences = re.split(r"(?<=[.!?])\s+", text)
        sentence_token_counts = [
            (sentence, len(self.tokenizer.tokenize_text(sentence)))
            for sentence in sentences
        ]

        chunks, current_chunk, current_chunk_size = [], "", 0

        for idx, (sentence, size) in enumerate(sentence_token_counts):
            assert (
                size <= max_tokens
            ), f"Sentence token count exceeds max tokens. Tokens: {size}, Max: {max_tokens}."

            next_size = (
                sentence_token_counts[idx + 1][1]
                if idx < len(sentence_token_counts) - 1
                else -1
            )
            current_chunk += (" " + sentence) if current_chunk else sentence
            current_chunk_size += size

            if next_size == -1 or current_chunk_size + next_size > max_tokens:
                chunks.append(current_chunk)
                current_chunk, current_chunk_size = "", 0

        return chunks


class DataFrameTextPreparatory(TextPreparatory):
    """
    Text preparation for DataFrame.
    Extends TextPreparatory to handle DataFrame-specific operations.
    """

    def __init__(self, df: DataFrame, tokenizer, min_tokens: int, max_tokens: int):
        super().__init__(tokenizer=tokenizer)
        self.df = df
        self._min_tokens = min_tokens
        self._max_tokens = max_tokens

    def shorten_texts(self, max_tokens: int = None) -> DataFrame:
        """
        Shortens texts in the DataFrame to a specified token limit.
        """
        max_tokens = self._max_tokens if max_tokens is None else max_tokens
        self._check_max_tokens_amount(max_tokens)

        shortened_texts = []
        for text in self.df["text"].dropna():
            token_count = len(self.tokenizer.tokenize_text(text))
            shortened_texts.extend(
                self.split_text_into_chunks(text, max_tokens)
                if token_count > max_tokens
                else [text]
            )

        return DataFrame(data=shortened_texts, columns=["text"])

    def generate_tokens_amount(self) -> DataFrame:
        """
        Generates token counts for each text in the DataFrame.
        """
        self.df["n_tokens"] = self.df["text"].apply(
            lambda x: len(self.tokenizer.tokenize_text(x)) if x else 0
        )
        return self.df

    def _check_max_tokens_amount(self, max_tokens: int):
        """
        Validates that the maximum token count is within the allowed range.
        """
        if max_tokens < self._min_tokens:
            raise ValueError(
                f"Max tokens must be ≥ {self._min_tokens}. Given: {max_tokens}."
            )
        elif max_tokens > self._max_tokens:
            raise ValueError(
                f"Max tokens must be ≤ {self._max_tokens}. Given: {max_tokens}."
            )

    @property
    def min_tokens(self):
        return self._min_tokens

    @property
    def max_tokens(self):
        return self._max_tokens
