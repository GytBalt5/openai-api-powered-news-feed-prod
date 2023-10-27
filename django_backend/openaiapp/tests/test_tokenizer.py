from django.test import TestCase

from openaiapp.tokenizers import tokenizer


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

    def test_tokenize_text(self):
        """
        Test that the tokenizer breaks down the text into a list of tokens.
        """
        tokens = tokenizer.tokenize_text(self.sample_text)

        self.assertIsInstance(tokens, list)
        self.assertEqual(self.expected_tokens, tokens)

    def test_decode_tokens(self):
        """
        Test that the tokenizer decodes a list of tokens into the original text.
        """
        decoded_text = tokenizer.decode_tokens(tokens=self.expected_tokens)

        self.assertIsInstance(decoded_text, str)
        self.assertEqual(self.sample_text, decoded_text)
