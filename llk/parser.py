from . import concat, Terminal, Nonterminal, Word, SententialForm, Grammar
from typing import Set

class LLParser:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar

    def _first_impl(self, k: int, w: SententialForm, visited: Set[Nonterminal]) -> Set[Word]:
        if k == 0:
            return set()
        else:
            # We were given a lambda production
            if len(w) == 0:
                return set()

            first_symbol = w[0]

            if isinstance(first_symbol, Terminal):
                return concat({(first_symbol,)}, self._first_impl(k - 1, w[1:], visited))
            elif isinstance(first_symbol, Nonterminal):
                # Avoid infinite recursion
                if first_symbol in visited:
                    return set()

                visited.add(first_symbol)

                productions = self.grammar.prod_by_nonterminal[first_symbol]
                firsts: Set[Word] = set()
                for production in productions:
                    firsts |= self._first_impl(k, production.end, visited)
                return firsts
            else:
                return NotImplemented

    def first(self, k: int, w: SententialForm) -> Set[Word]:
        visited: Set[Nonterminal] = set()
        return self._first_impl(k, w, visited)
