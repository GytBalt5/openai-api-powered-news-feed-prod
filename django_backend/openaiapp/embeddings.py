from django.conf import settings

import numpy as np
import openai
from pandas import DataFrame


openai.api_key = settings.OPENAI_API_KEY


def create_embeddings_of_df_text(df: DataFrame):
    df['embeddings'] = df.text.apply(
        lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding']
    )
    return df


def flatten_embeddings_of_df(df: DataFrame):
    df['embeddings'] = df['embeddings'].apply(np.array)
    return df