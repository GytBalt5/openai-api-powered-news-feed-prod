from abc import ABC, abstractmethod

from django.conf import settings

import openai
from openai.embeddings_utils import distances_from_embeddings
from pandas import DataFrame

from openaiapp.text_preparation import generate_each_text_of_df_tokens_amount
from openaiapp.embeddings import create_embedding


openai.api_key = settings.OPENAI_API_KEY


class AbstractAIQuestionAnswering(ABC):
    """
    An abstract class for answering questions based on the context.
    """

    @abstractmethod
    def create_context(self, question: str, max_len: int) -> str:
        """
        Create a context for a question by finding the most similar context from the data frame.

        :param question: The question to create a context for.
        :param max_len: The maximum length of the context.
        :return: The context for the question.
        """
        pass

    @abstractmethod
    def answer_question(self, question: str, max_len: int) -> str:
        """
        Answer a question based on the most similar context from the data frame texts.

        :param question: The question to answer.
        :param max_len: The maximum length of the context.
        :return: The answer to the question.
        """
        pass


class AIQuestionAnsweringBasedOnContext(AbstractAIQuestionAnswering):
    """
    A class for answering questions based on the context.
    """

    MODEL = "gpt-3.5-turbo-instruct"
    CONTEXT_MAX_LEN = 2048
    MAX_TOKENS = 256

    def __init__(self, df: DataFrame, model: str = MODEL, 
                 max_tokens: int = MAX_TOKENS, stop_sequence: str = None):
        """
        Initialize the AIQuestionAnswering object.

        :param df: A pandas DataFrame containing the texts to use for answering questions.
        :param model: The OpenAI model to use for answering questions.
        :param max_tokens: The maximum number of tokens to use for generating the answer.
        :param stop_sequence: The sequence to use for stopping the answer generation.
        """
        self.df = df
        self.model = model
        self.max_tokens = max_tokens
        self.stop_sequence = stop_sequence

    def create_context(self, question: str, max_len: int = CONTEXT_MAX_LEN) -> str:
        """
        Create a context for a question by finding the most similar context from the data frame.

        :param question: The question to create a context for.
        :param max_len: The maximum length of the context.
        :return: The context for the question.
        """
        df = generate_each_text_of_df_tokens_amount(df=self.df)

        # Get the embeddings for the question.
        q_embeddings = create_embedding(input=question)

        # Get the distances from the embeddings.
        df["distances"] = distances_from_embeddings(
            q_embeddings, self.df["embeddings"].values, distance_metric="cosine"
        )

        returns = []
        cur_len = 0

        # Sort by distance and add the text to the context until the context is too long.
        for _, row in df.sort_values("distances", ascending=True).iterrows():
            # Add the length of the text to the current length.
            cur_len += row["n_tokens"]

            # If the context is too long, break.
            if cur_len > max_len:
                break

            # Else add it to the text that is being returned.
            returns.append(row["text"])

        # Return the context.
        return "\n\n###\n\n".join(returns)

    def answer_question(self, question: str, max_len: int = CONTEXT_MAX_LEN) -> str:
        """
        Answer a question based on the most similar context from the data frame texts.

        :param question: The question to answer.
        :param max_len: The maximum length of the context.
        :return: The answer to the question.
        """
        context = self.create_context(question, max_len=max_len)

        try:
            # Create a completions using the question and context.
            response = openai.Completion.create(
                prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
                temperature=0,
                max_tokens=self.max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=self.stop_sequence,
                model=self.model,
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            raise Exception(f"Error generating answer: {str(e)}")
