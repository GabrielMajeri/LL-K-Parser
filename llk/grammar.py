from __future__ import annotations
import re
from typing import Dict, List, Set

from . import Symbol, Terminal, Nonterminal, SententialForm, Word, LAMBDA

class Production:
    """Production rule describing how a nonterminal can be rewritten"""

    __slots__ = ['start', 'end']

    def __init__(self, start: Nonterminal, end: SententialForm) -> None:
        self.start = start
        self.end = end

    def __contains__(self, symbol: Symbol) -> bool:
        """Checks if a symbol is produced by this rule."""
        return symbol in self.end

    def after_symbol(self, symbol: Symbol) -> SententialForm:
        """Determine the part of the production which follows the symbol."""
        if symbol not in self:
            return LAMBDA
        idx = self.end.index(symbol)
        return self.end[(idx + 1):]

    def __repr__(self) -> str:
        rhs = ''.join(map(str, self.end)) if self.end else 'λ'
        return f"{self.start} -> {rhs}"

PRODUCTION_REGEX = re.compile(r'(?P<start>[A-Z])\W*->\W*(?P<end>[A-z]*)')

class Grammar:
    vocabulary: Set[Symbol]
    nonterms: Set[Nonterminal]
    terms: Set[Terminal]
    sentence_symbol: Nonterminal
    prods: Set[Production]
    prod_by_nonterminal: Dict[Nonterminal, List[Production]]

    """Context-free grammar consisting of a 4-tuple (nonterminals, terminals,
    sentence symbol and productions).

    Also has a dictionary for fast look-up of the productions of
    a given nonterminal symbol
    """

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

        self.sentence_symbol = Nonterminal('S')
        assert self.sentence_symbol in nonterminals

        # Group productions by the nonterminal which generates them
        self.prod_by_nonterminal = {
            nonterminal: [
                prod for prod in productions if prod.start == nonterminal
            ]
            for nonterminal in nonterminals
        }

    @staticmethod
    def read(path: str) -> Grammar:
        """Reads a grammar from a file"""

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

    def __repr__(self) -> str:
        return f"Gramar({repr(self.nonterms)}, {repr(self.terms)}, {repr(self.sentence_symbol)}, {repr(self.prods)})"

    def __str__(self) -> str:
        return ("Grammar:\n"
        f"- Nonterminals: {self.nonterms}\n"
        f"- Terminals: {self.terms}\n"
        f"- Productions: {self.prod_by_nonterminal}\n")
