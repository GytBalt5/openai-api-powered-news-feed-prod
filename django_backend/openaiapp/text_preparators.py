import re
from typing import List
from abc import ABC, abstractmethod

from pandas import DataFrame

from openaiapp.tokenizers import tokenizer


class AbstractTextPreparatory(ABC):
    """
    Abstract base class for text preparation.
    """

    @abstractmethod
    def split_text_into_chunks(self, text: str, max_tokens: int) -> List[str]:
        """
        Abstract method to split a text into chunks with a maximum token limit.
        """
        pass


class TextPreparatory(AbstractTextPreparatory):
    """
    Concrete class for text preparation.
    """

    def split_text_into_chunks(self, text: str, max_tokens: int) -> List[str]:
        """
        Split a text into chunks of at most `max_tokens` tokens.
        """
        # Split the text into sentences.
        sentences = re.split(r"(?<=[.!?])\s+", text)

        # Get the token count for each sentence.
        sentence_token_counts = [(sentence, len(tokenizer.tokenize_text(sentence))) for sentence in sentences]

        chunks, current_chunk, current_chunk_size = [], "", 0

        for idx, (sentence, size) in enumerate(sentence_token_counts):
            # Check that the sentence token count is within the maximum limit.
            assert (
                size <= max_tokens
            ), f"The sentence tokens amount is greater than the maximum tokens. Tokens amount {size} > max tokens {max_tokens}."

            # Get the token count for the next sentence.
            next_size = sentence_token_counts[idx + 1][1] if idx < len(sentence_token_counts) - 1 else -1
            current_chunk += (" " + sentence) if current_chunk else sentence
            current_chunk_size += size

            if next_size == -1 or current_chunk_size + next_size > max_tokens:
                chunks.append(current_chunk)
                current_chunk, current_chunk_size = "", 0

        return chunks


class DataFrameTextPreparatory(TextPreparatory):
    """
    Text preparation for DataFrame.
    """

    def __init__(self, df: DataFrame, min_tokens: int, max_tokens: int):
        super().__init__()
        self.df = df
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens

    def shorten_texts(self, max_tokens: int = None) -> DataFrame:
        """
        Shorten the texts in the DataFrame based on the maximum token limit.
        """
        max_tokens = max_tokens or self.max_tokens
        self._check_max_tokens_amount(max_tokens)

        shortened_texts = []
        for text in self.df["text"].dropna():
            token_count = len(tokenizer.tokenize_text(text))
            if token_count > max_tokens:
                shortened_texts.extend(self.split_text_into_chunks(text, max_tokens))
            else:
                shortened_texts.append(text)

        return DataFrame(data=shortened_texts, columns=["text"])

    def generate_tokens_amount(self) -> DataFrame:
        """
        Generate the token count for each text in the DataFrame.
        """
        self.df["n_tokens"] = self.df["text"].apply(lambda x: len(tokenizer.tokenize_text(x)) if x else 0)
        return self.df

    def _check_max_tokens_amount(self, max_tokens: int):
        """
        Check that the maximum token count is within the allowed range.
        """
        if max_tokens < self.min_tokens:
            raise ValueError(f"Max tokens must be ≥ {self.min_tokens}. Given: {max_tokens}.")
        elif max_tokens > self.max_tokens:
            raise ValueError(f"Max tokens must be ≤ {self.max_tokens}. Given: {max_tokens}.")
