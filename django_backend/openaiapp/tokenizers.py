import tiktoken


def tokenize_text(text: str) -> list[list]:
    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model.
    tokenizer = tiktoken.get_encoding("cl100k_base")
    return tokenizer.encode(text)