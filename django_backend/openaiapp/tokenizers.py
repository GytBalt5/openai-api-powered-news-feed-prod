import tiktoken


TOKENIZER = tiktoken.get_encoding("cl100k_base")


def tokenize_text(text: str) -> list[list]:
    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model.
    return TOKENIZER.encode(text)