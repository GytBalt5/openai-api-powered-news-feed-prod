import re
from typing import List
from abc import ABC, abstractmethod

from pandas import DataFrame

from openaiapp.tokenizers import tokenizer


class AbstractTextPreparator(ABC):
    @abstractmethod
    def split_text_into_chunks(text: str, max_tokens: int) -> List[str]:
        pass

    @abstractmethod
    def check_max_tokens_amount(max_tokens: int, min_amount: int, max_amount: int):
        pass


class SimpleTextPreparator(AbstractTextPreparator):
    @staticmethod
    def split_text_into_chunks(text: str, max_tokens: int) -> List[str]:
        """
        Split a text into chunks of at most `max_tokens` tokens.
        """
        # Split the text into sentences.
        sentences = re.split(r"(?<=[.!?])\s+", text)

        # Get the token count for each sentence.
        sentence_token_counts = [
            (sentence, len(tokenizer.tokenize_text(sentence))) for sentence in sentences
        ]

        chunks = []
        current_chunk = ""
        current_chunk_size = 0

        for idx, (sentence, size) in enumerate(sentence_token_counts):
            # Check that the sentence token count is within the maximum limit.
            assert (
                size <= max_tokens
            ), f"The sentence tokens amount is greater than the maximum tokens. Tokens amount {size} > max tokens {max_tokens}."

            # Get the token count for the next sentence.
            _, next_size = (
                sentence_token_counts[idx + 1]
                if idx < len(sentence_token_counts) - 1
                else ("", -1)
            )

            current_chunk += f" {sentence}" if current_chunk else sentence
            current_chunk_size += size

            if next_size == -1:  # the last sentence
                chunks.append(current_chunk)
            elif current_chunk_size + next_size > max_tokens and current_chunk_size <= max_tokens:
                chunks.append(current_chunk)
                current_chunk = ""
                current_chunk_size = 0

        return chunks

    @staticmethod
    def check_max_tokens_amount(max_tokens: int, min_amount: int, max_amount: int):
        """
        Check that the maximum token count is within the allowed range.
        """
        if max_tokens < min_amount:
            raise ValueError(
                f"Tokens amount must be greater or equal to {min_amount}. Passed {max_tokens} max_tokens."
            )
        elif max_tokens > max_amount:
            raise ValueError(
                f"Tokens amount must be less or equal to {max_amount}. Passed {max_tokens} max_tokens."
            )


class DataFrameTextPreparator(SimpleTextPreparator):
    MIN_TOKENS = 8
    MAX_TOKENS = 512

    def __init__(self, df: DataFrame):
        self.df = df

    def shorten_texts(self, max_tokens: int = MAX_TOKENS) -> DataFrame:
        """
        Shorten the texts based on the maximum token limit.
        """
        DataFrameTextPreparator.check_max_tokens_amount(
            max_tokens, self.MIN_TOKENS, self.MAX_TOKENS
        )
        shortened_texts = []

        # Loop through the DataFrame.
        for _, row in self.df.iterrows():
            text = row["text"]

            # Skip rows where the text is None.
            if text is None:
                continue

            # Split the text into chunks if it exceeds the maximum token count.
            if len(tokenizer.tokenize_text(text)) > max_tokens:
                shortened_texts.extend(
                    DataFrameTextPreparator.split_text_into_chunks(text, max_tokens)
                )
            else:
                shortened_texts.append(text)

        return DataFrame(data=shortened_texts, columns=["text"])

    def generate_tokens_amount(self) -> DataFrame:
        """
        Generate the token count for each text in the DataFrame.
        """
        self.df["n_tokens"] = self.df.text.apply(lambda x: len(tokenizer.tokenize_text(x)))
        return self.df


def get_text_preparator_object(data_object=None) -> AbstractTextPreparator:
    """
    Get a text preparator object for the given data object.

    Args:
        data_object: The data object to prepare text for.

    Returns:
        An instance of a text preparator object.

    Raises:
        TypeError: If the data object is not supported.
    """
    if data_object is None:
        return SimpleTextPreparator()
    elif isinstance(data_object, DataFrame):
        return DataFrameTextPreparator(data_object)
    raise TypeError("The data object is not supported.")
