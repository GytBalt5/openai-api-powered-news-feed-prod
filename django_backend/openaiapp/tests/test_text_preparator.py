from django.test import TestCase

from pandas import DataFrame

from openaiapp.text_preparators import get_text_preparator_object


class SimpleTextPreparatorTestCase(TestCase):
    def setUp(self):
        self.sample_text = "Fact-based news, exclusive video footage, photos and updated maps. Fact-based news, exclusive video footage, photos and updated maps. Fact-based news, exclusive video footage, photos and updated maps."
        self.sample_text_2 = "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH."
        self.text_preparator = get_text_preparator_object()

    def test_should_split_text_into_chunks_one_sentence(self):
        """
        Test that the text is split into chunks, where each chunk is composed of one full sentence.
        """
        max_tokens = 14

        chunks = self.text_preparator.split_text_into_chunks(
            text=self.sample_text,
            max_tokens=max_tokens,
        )
        expected_chunks_1 = [
            "Fact-based news, exclusive video footage, photos and updated maps.",
            "Fact-based news, exclusive video footage, photos and updated maps.",
            "Fact-based news, exclusive video footage, photos and updated maps.",
        ]
        self.assertIsInstance(chunks, list)
        self.assertEqual(expected_chunks_1, chunks)

        chunks = self.text_preparator.split_text_into_chunks(
            text="Fact-based news, exclusive video footage, photos and updated maps.",
            max_tokens=max_tokens,
        )
        expected_chunks_2 = [
            "Fact-based news, exclusive video footage, photos and updated maps.",
        ]
        self.assertIsInstance(chunks, list)
        self.assertEqual(expected_chunks_2, chunks)

    def test_should_split_text_into_chunks_two_sentences(self):
        """
        Test that the text is split into chunks, where each chunk is composed of two full sentences.
        """
        max_tokens = 30
        chunks = self.text_preparator.split_text_into_chunks(
            text=self.sample_text_2,
            max_tokens=max_tokens,
        )
        expected_chunks = [
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
        ]

        self.assertIsInstance(chunks, list)
        self.assertEqual(expected_chunks, chunks)


class DataFrameTextPreparatorTestCase(TestCase):
    def setUp(self):
        self.sample_df = DataFrame(
            data=[
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH."
            ],
            columns=["text"],
        )
        self.text_preparator = get_text_preparator_object(self.sample_df)

    def test_should_correctly_generate_each_text_amount_of_tokens(self):
        """
        Test that the function generates the correct number of tokens for each text.
        """
        df = self.text_preparator.generate_tokens_amount()
        expected_df = DataFrame(
            data=[
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH."
            ],
            columns=["text"],
        )
        expected_df["n_tokens"] = 75

        self.assertIsInstance(df, DataFrame)
        self.assertEqual(expected_df.to_dict(), df.to_dict())

    def test_should_shorten_texts(self):
        """
        Test that the function shortens the texts to the specified maximum number of tokens.
        """
        max_tokens = 30
        shortened_df = self.text_preparator.shorten_texts(max_tokens=max_tokens)
        expected_df = DataFrame(
            data=[
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            ],
            columns=["text"],
        )

        self.assertIsInstance(shortened_df, DataFrame)
        self.assertEqual(expected_df.to_dict(), shortened_df.to_dict())

    def test_should_max_tokens_be_greater_or_equal(self):
        """
        Test that the function raises a ValueError if the maximum number of tokens is less than MIN_TOKENS.
        """
        min = self.text_preparator.MIN_TOKENS
        max_tokens = 0

        with self.assertRaises(ValueError) as context:
            self.text_preparator.shorten_texts(max_tokens=max_tokens)

        self.assertEqual(
            str(context.exception),
            f"Tokens amount must be greater or equal to {min}. Passed {max_tokens} max_tokens.",
        )

    def test_should_max_tokens_be_less_or_equal(self):
        """
        Test that the function raises a ValueError if the maximum number of tokens is greater than MAX_TOKENS.
        """
        max = self.text_preparator.MAX_TOKENS
        max_tokens = 1024

        with self.assertRaises(ValueError) as context:
            self.text_preparator.shorten_texts(max_tokens=max_tokens)

        self.assertEqual(
            str(context.exception),
            f"Tokens amount must be less or equal to {max}. Passed {max_tokens} max_tokens.",
        )
