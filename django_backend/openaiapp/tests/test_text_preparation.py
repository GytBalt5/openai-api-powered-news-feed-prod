from unittest import TestCase

from pandas import DataFrame

from openaiapp.text_preparation import (
    generate_each_text_of_df_tokens_amount,
    split_text_into_chunks,
    shorten_texts_of_df,
)


class TextIntoChunksSplitterTestCase(TestCase):
    def setUp(self):
        self.sample_text = "Fact-based news, exclusive video footage, photos and updated maps. Fact-based news, exclusive video footage, photos and updated maps. Fact-based news, exclusive video footage, photos and updated maps."
        self.sample_text_2 = "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH."

    def test_should_split_text_into_chunks_one_sentence(self):
        """
        Should split the text into chunks.
        The chunk should be composed of on full sentence.
        """

        max_tokens = 14

        chunks = split_text_into_chunks(
            text=self.sample_text,
            max_tokens=max_tokens,
        )
        expected_chunks_1 = [
            "Fact-based news, exclusive video footage, photos and updated maps.",
            "Fact-based news, exclusive video footage, photos and updated maps.",
            "Fact-based news, exclusive video footage, photos and updated maps.",
        ]
        self.assertEqual(type(chunks), list)
        self.assertEqual(expected_chunks_1, chunks)

        chunks = split_text_into_chunks(
            text="Fact-based news, exclusive video footage, photos and updated maps.",
            max_tokens=max_tokens,
        )
        expected_chunks_2 = [
            "Fact-based news, exclusive video footage, photos and updated maps.",
        ]
        self.assertEqual(type(chunks), list)
        self.assertEqual(expected_chunks_2, chunks)

    def test_should_split_text_into_chunks_two_sentences(self):
        """
        Should split the text into chunks.
        The chunk should be composed of two full sentences.
        """

        max_tokens = 30
        chunks = split_text_into_chunks(
            text=self.sample_text_2,
            max_tokens=max_tokens,
        )
        expected_chunks = [
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
        ]

        self.assertEqual(type(chunks), list)
        self.assertEqual(expected_chunks, chunks)


class DataFrameTextChunkierTestCase(TestCase):
    def setUp(self):
        self.sample_df = DataFrame(
            data=[
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH."
            ],
            columns=["text"],
        )

    def test_should_correctly_generate_each_text_amount_of_tokens(self):
        df = generate_each_text_of_df_tokens_amount(df=self.sample_df)
        expected_df = DataFrame(
            data=[
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH. Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH."
            ],
            columns=["text"],
        )
        expected_df["n_tokens"] = 75

        self.assertEqual(type(df), DataFrame)
        self.assertEqual(expected_df.to_dict(), df.to_dict())

    def test_should_shorten_texts_of_df(self):
        max_tokens = 30
        shortened_df = shorten_texts_of_df(
            df=self.sample_df,
            max_tokens=max_tokens,
        )
        expected_df = DataFrame(
            data=[
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
                "Fact-based news, exclusive video footage, photos and updated maps. Abra kadabra abra kadabra YEAH.",
            ],
            columns=["text"],
        )

        self.assertEqual(type(shortened_df), DataFrame)
        self.assertEqual(expected_df.to_dict(), shortened_df.to_dict())

    def test_should_max_tokens_be_greater_or_equal(self):
        max_tokens = 0
        with self.assertRaises(ValueError) as context:
            shorten_texts_of_df(
                df=DataFrame(data=[], columns=["text"]), max_tokens=max_tokens
            )

        self.assertEqual(
            str(context.exception),
            f"Tokens amount must be greater or equal to 10. Passed {max_tokens} max_tokens.",
        )

    def test_should_max_tokens_be_less_or_equal(self):
        max_tokens = 501
        with self.assertRaises(ValueError) as context:
            shorten_texts_of_df(
                df=DataFrame(data=[], columns=["text"]), max_tokens=max_tokens
            )

        self.assertEqual(
            str(context.exception),
            f"Tokens amount must be less or equal to 500. Passed {max_tokens} max_tokens.",
        )
