from unittest import TestCase

from openaiapp.tokenizers import tokenize_text, decode_tokens


class TokenizerTestCase(TestCase):
    def setUp(self):
        self.sample_text = (
            "Fact-based news, exclusive video footage, photos and updated maps."
        )
        self.expected_tokens = [
            17873,
            6108,
            3754,
            11,
            14079,
            2835,
            22609,
            11,
            7397,
            323,
            6177,
            14370,
            13,
        ]

    def test_should_text_be_tokenized(self):
        """Should break down the text into list of tokens."""

        tokens_list = tokenize_text(self.sample_text)

        self.assertEqual(type(tokens_list), list)
        self.assertEqual(self.expected_tokens, tokens_list)

    def test_should_tokens_be_decoded_to_text(self):
        decoded_text = decode_tokens(tokens=self.expected_tokens)

        self.assertEqual(type(decoded_text), str)
        self.assertEqual(self.sample_text, decoded_text)
