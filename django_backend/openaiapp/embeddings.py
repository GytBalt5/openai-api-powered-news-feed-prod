from django.conf import settings

import numpy as np
import openai
from pandas import DataFrame


openai.api_key = settings.OPENAI_API_KEY
EMBEDDING_ENGINE = 'text-embedding-ada-002'


def create_embedding(input: str):
    return openai.Embedding.create(input=input, engine=EMBEDDING_ENGINE)['data'][0]['embedding']


def create_embeddings_of_df_text(df: DataFrame):
    df['embeddings'] = df.text.apply(lambda x: create_embedding(input=x))
    return df


def flatten_embeddings_of_df(df: DataFrame):
    df['embeddings'] = df['embeddings'].apply(np.array)
    return df


# TODO. Should be saved flatten embeddings of df to the vector database in future.
