#!/usr/bin/env python3

from abc import ABC
import re
from typing import Set, List

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


class Production:
    __slots__ = ['start', 'end']

    def __init__(self, start: Nonterminal, end: List[Symbol]) -> None:
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        rhs = ''.join(map(str, self.end)) if self.end else 'λ'
        return f"{self.start} -> {rhs}"


class Grammar:
    vocabulary: Set[Symbol]

    def __init__(
        self,
        nonterminals: Set[Nonterminal],
        terminals: Set[Terminal],
        productions: Set[Production],
    ) -> None:
        self.vocabulary = nonterminals | terminals
        self.nonterms = nonterminals
        self.terms = terminals
        self.prods = productions

        # Group productions by the nonterminal which generates them
        self.prod_by_nonterminal = {
            nonterminal: [
                prod for prod in productions if prod.start == nonterminal
            ]
            for nonterminal in nonterminals
        }

        print("Nonterminals:", nonterminals)
        print("Terminals:", terminals)
        print("Productions:", self.prod_by_nonterminal)


SententialForm = List[Symbol]
Word = List[Terminal]

def concat(a: Set[Word], b: Set[Word]) -> Set[Word]:
    """Performs concatenation of two languages."""
    return {u + v for u in a for v in b}

class LLParser:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar

    def first(self, k: int, w: SententialForm) -> Set[Word]:
        if k == 0:
            return set()
        else:
            first_symbol = w[0]
            if isinstance(first_symbol, Terminal):
                return concat({[first_symbol]}, self.first(k - 1, w[1:]))
            else:
                return NotImplemented


INPUT_FILE = 'simple1.txt'

nonterminals = set()
terminals = set()
productions = set()

production_regex = re.compile(r'(?P<start>[A-Z])\W*->\W*(?P<end>[A-z]*)')

with open(INPUT_FILE, 'r') as f:
    for line_number, line in enumerate(map(str.strip, f)):
        # Skip comments and blank lines
        if not line or line[0] == '#':
            continue

        match = production_regex.match(line)
        if not match:
            raise Exception(f"Wrong syntax for production at line {line_number}: '{line}'")

        start = Nonterminal(match.group('start'))
        nonterminals.add(start)

        end = []
        for ch in match.group('end'):
            symbol: Symbol
            if ch.isupper():
                symbol = Nonterminal(ch)
                nonterminals.add(symbol)
            else:
                symbol = Terminal(ch)
                terminals.add(symbol)
            end.append(symbol)

        productions.add(Production(start, end))

grammar = Grammar(nonterminals, terminals, productions)