from abc import ABC
from typing import Tuple

class Symbol(ABC):
    """Represents a token from the grammar's vocabulary.

    Currently, only single-letter tokens are supported.
    """

    __slots__ = ['symbol']

    def __init__(self, symbol: str) -> None:
        assert len(symbol) == 1, '(Non)terminals should be a single letter'
        self.symbol = symbol

    def __repr__(self) -> str:
        return self.symbol

    def __eq__(self, rhs: object) -> bool:
        if not isinstance(rhs, Symbol):
            return NotImplemented
        return self.symbol == rhs.symbol

    def __hash__(self) -> int:
        return hash(self.symbol)

class Nonterminal(Symbol):
    def __init__(self, symbol: str) -> None:
        assert symbol.isupper(), 'Nonterminals should be uppercase'
        super().__init__(symbol)


class Terminal(Symbol):
    def __init__(self, symbol: str) -> None:
        assert symbol.islower(), 'Terminals should be lowercase'
        super().__init__(symbol)

SententialForm = Tuple[Symbol, ...]
Word = Tuple[Terminal, ...]
