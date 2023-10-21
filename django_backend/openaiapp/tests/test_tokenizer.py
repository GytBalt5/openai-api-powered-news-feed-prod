    
from unittest import TestCase

from openaiapp.tokenizers import tokenize_text


class TokenizerTestCase(TestCase):
    def test_should_text_be_tokenized(self):
        """Should break down the text into tokens (words or punctuation) and returns them as a list."""
        sample_text = (
            "Fact-based news, exclusive video footage, photos and updated maps."
        )
        tokens_list = tokenize_text(sample_text)
        expected_tokens_list = [
            "Fact",
            "-based",
            " news",
            ",",
            " exclusive",
            " video",
            " footage",
            ",",
            " photos",
            " and",
            " updated",
            " maps",
            ".",
        ]

        self.assertEqual(expected_tokens_list, tokens_list)