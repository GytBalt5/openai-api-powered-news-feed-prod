import tiktoken


# Load the cl100k_base tokenizer which is designed to work with the ada-002 model.
TOKENIZER = tiktoken.get_encoding("cl100k_base")


def tokenize_text(text: str) -> list[list]:
    return TOKENIZER.encode(text)


def decode_tokens(tokens: list[int]) -> str:
    """Decode the tokens into text."""
    return TOKENIZER.decode(tokens)
