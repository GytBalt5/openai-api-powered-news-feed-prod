from abc import ABC, abstractmethod

import tiktoken


class Tokenizer(ABC):
    @abstractmethod
    def tokenize_text(self, text: str) -> list[list[int]]:
        pass

    @abstractmethod
    def decode_tokens(self, tokens: list[int]) -> str:
        pass


class CL100KBaseTokenizer(Tokenizer):
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def tokenize_text(self, text: str) -> list[list[int]]:
        return self.tokenizer.encode(text)

    def decode_tokens(self, tokens: list[int]) -> str:
        return self.tokenizer.decode(tokens)


tokenizer = CL100KBaseTokenizer()