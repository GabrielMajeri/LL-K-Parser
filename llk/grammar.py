from __future__ import annotations
import re
from typing import Set

from . import Symbol, Terminal, Nonterminal, SententialForm, Word

class Production:
    __slots__ = ['start', 'end']

    def __init__(self, start: Nonterminal, end: SententialForm) -> None:
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        rhs = ''.join(map(str, self.end)) if self.end else 'λ'
        return f"{self.start} -> {rhs}"

PRODUCTION_REGEX = re.compile(r'(?P<start>[A-Z])\W*->\W*(?P<end>[A-z]*)')

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

    @staticmethod
    def read(path: str) -> Grammar:
        nonterminals = set()
        terminals = set()
        productions = set()

        with open(path, 'r') as f:
            for line_number, line in enumerate(map(str.strip, f)):
                # Skip comments and blank lines
                if not line or line[0] == '#':
                    continue

                match = PRODUCTION_REGEX.match(line)
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

                productions.add(Production(start, tuple(end)))

        return Grammar(nonterminals, terminals, productions)
