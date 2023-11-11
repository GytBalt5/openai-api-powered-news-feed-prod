from abc import ABC, abstractmethod

import openai
from openai.embeddings_utils import distances_from_embeddings
from pandas import DataFrame

from openaiapp.text_preparators import get_text_preparator_object
from openaiapp.embeddings import get_embeddings_object


class AbstractAIQuestionAnswering(ABC):
    """
    Abstract base class for AI-based question answering systems.
    """

    @abstractmethod
    def create_context(self, question: str) -> str:
        """
        Create a context for a question by finding the most similar context from a data frame.

        :param question: The question for which to create a context.
        :return: A string representing the context for the question.
        """
        pass

    @abstractmethod
    def answer_question(self, question: str) -> str:
        """
        Answer a question based on a context derived from a data frame.

        :param question: The question to be answered.
        :return: A string representing the answer to the question.
        """
        pass

class AIQuestionAnsweringBasedOnContext(AbstractAIQuestionAnswering):
    """
    Implementation of AbstractAIQuestionAnswering that answers questions
    based on context derived from a data frame.
    """

    def __init__(self, df: DataFrame, model: str, max_tokens: int, context_max_len: int, stop_sequence: str):
        """
        Initialize the AIQuestionAnsweringBasedOnContext object.

        :param df: A pandas DataFrame containing texts for context creation.
        :param model: The OpenAI model to use for generating answers.
        :param max_tokens: The maximum number of tokens for the generated answer.
        :param context_max_len: The maximum length of the context in tokens.
        :param stop_sequence: A sequence of tokens indicating where the answer generation should stop.
        """
        self.df = df
        self.model = model
        self.max_tokens = max_tokens
        self.context_max_len = context_max_len
        self.stop_sequence = stop_sequence

    def create_context(self, question: str) -> str:
        """
        Create a context for a question by finding the most similar context from the data frame.

        :param question: The question for which to create a context.
        :return: A string representing the context for the question.
        """
        text_preparator = get_text_preparator_object(data_object=self.df)
        df_prepared = text_preparator.generate_tokens_amount()

        # Get embeddings for the question.
        embeddings_object = get_embeddings_object()
        q_embeddings = embeddings_object.create_embedding(input=question)

        # Calculate distances from the embeddings.
        df_prepared["distances"] = distances_from_embeddings(
            q_embeddings, df_prepared["embeddings"].values, distance_metric="cosine"
        )

        context_texts = []
        current_length = 0

         # Sort by distance and construct the context.
        for _, row in df_prepared.sort_values("distances", ascending=True).iterrows():
            current_length += row["n_tokens"]
            if current_length > self.context_max_len:
                break
            context_texts.append(row["text"])

        return "\n\n###\n\n".join(context_texts)

    def answer_question(self, question: str) -> str:
        """
        Answer a question based on the most similar context derived from the data frame.

        :param question: The question to be answered.
        :return: A string representing the answer to the question.
        """
        context = self.create_context(question)

        try:
            response = openai.Completion.create(
                prompt=f"Context: {context}\n\nQuestion: {question}\nAnswer:",
                temperature=0,
                max_tokens=self.max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=self.stop_sequence,
                model=self.model,
            )
            return response.choices[0].text.strip()
        except openai.error.OpenAIError as e:
            raise RuntimeError(f"Error in generating answer from OpenAI: {e}.")

        except Exception as e:
            raise RuntimeError(f"Unexpected error in answer generation: {e}.")
