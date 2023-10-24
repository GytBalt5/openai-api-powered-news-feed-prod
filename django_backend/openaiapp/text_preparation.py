import re

from pandas import DataFrame

from openaiapp.tokenizers import tokenize_text


MIN_TOKENS = 10
MAX_TOKENS = 500


def split_text_into_chunks(text: str, max_tokens: int) -> list[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)  # split the text into sentences
    sentences_token_amounts = [(sentence, len(tokenize_text(sentence))) for sentence in sentences]

    chunks = []
    accumulative_chunk = ""
    accumulative_size = 0

    for idx, (sentence, size) in enumerate(sentences_token_amounts):
        assert size <= max_tokens, f"The sentence tokens amount is greater than the maximum tokens. Tokens amount {size} > max tokens {max_tokens}."
        
        _, next_size = sentences_token_amounts[idx + 1] if idx < len(sentences_token_amounts) - 1 else ("", -1)

        accumulative_chunk += f" {sentence}" if accumulative_chunk else sentence
        accumulative_size += size

        if next_size == -1:
            chunks.append(accumulative_chunk)
        elif (accumulative_size + next_size > max_tokens and 
            accumulative_size <= max_tokens):
            chunks.append(accumulative_chunk)
            accumulative_chunk = ""
            accumulative_size = 0

    return chunks


def shorten_texts_of_df(df: DataFrame, max_tokens: int) -> DataFrame:
    """Shorten the texts based on the maximum token limit."""
    
    _check_max_tokens_amount(max_tokens)
    shortened_texts = []
    
    # Loop through the DataFrame.
    for _, row in df.iterrows():
        
        text = row["text"]
        
        # Skip rows where the text is None.
        if text is None:
            continue
        
        # Split the text into chunks if it exceeds the maximum token count.
        if len(tokenize_text(text)) > max_tokens:
            shortened_texts.extend(split_text_into_chunks(text, max_tokens))
        else:
            shortened_texts.append(text)

    return DataFrame(data=shortened_texts, columns=["text"])


def generate_each_text_of_df_tokens_amount(df) -> DataFrame:
    df['n_tokens'] = df.text.apply(lambda x: len(tokenize_text(x)))
    return df


def _check_max_tokens_amount(max_tokens: int):
    if max_tokens < MIN_TOKENS:
        raise ValueError(f"Tokens amount must be greater or equal to 10. Passed {max_tokens} max_tokens.")
    elif max_tokens > MAX_TOKENS:
        raise ValueError(f"Tokens amount must be less or equal to 500. Passed {max_tokens} max_tokens.")
