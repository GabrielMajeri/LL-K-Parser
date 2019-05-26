from . import concat, Terminal, Nonterminal, Word, SententialForm, LAMBDA, END, Production, Grammar
from itertools import combinations
from typing import Set

class LLParser:
    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar

    def _first_impl(self, k: int, w: SententialForm, visited: Set[Nonterminal]) -> Set[Word]:
        if k == 0:
            return set()

        # We were given a lambda production
        if not w:
            return {LAMBDA}

        first_symbol = w[0]

        if isinstance(first_symbol, Terminal):
            return concat({(first_symbol,)}, self._first_impl(k - 1, w[1:], visited))

        if isinstance(first_symbol, Nonterminal):
            # Avoid infinite recursion
            if first_symbol in visited:
                return set()

            visited.add(first_symbol)

            productions = self.grammar.prod_by_nonterminal[first_symbol]
            firsts: Set[Word] = set()
            for production in productions:
                if production.end == LAMBDA:
                    firsts |= self._first_impl(k, w[1:], visited)
                else:
                    firsts |= self._first_impl(k, production.end, visited)
            return firsts

        return NotImplemented

    def first(self, k: int, w: SententialForm) -> Set[Word]:
        visited: Set[Nonterminal] = set()
        return self._first_impl(k, w, visited)

    def _follow_impl(self, k: int, nt: Nonterminal, visited: Set[Nonterminal]) -> Set[Word]:
        if nt == self.grammar.sentence_symbol:
            return {(END, ) * k}

        if nt in visited:
            return set()

        visited.add(nt)

        follows: Set[Word] = set()
        productions = self.grammar.prods
        for production in productions:
            # We only care about rules which produce this nonterminal
            rhs = production.after_symbol(nt)
            if rhs == LAMBDA:
                continue

            extras = self._follow_impl(k, production.start, visited)
            for extra in extras:
                follows |= self.first(k, rhs + extra)

        return follows

    def follow(self, k: int, nt: Nonterminal) -> Set[Word]:
        visited: Set[Nonterminal] = set()
        return self._follow_impl(k, nt, visited)

    def look_ahead(self, k: int, p: Production) -> Set[Word]:
        follows = self.follow(k, p.start)

        look_aheads: Set[Word] = set()
        for follow in follows:
            look_aheads |= self.first(k, p.end + follow)
        return look_aheads

    def find_k(self) -> int:
        if all(map(lambda prods: len(prods) == 1, self.grammar.prod_by_nonterminal.values())):
            return 0

        k = 1
        done = False

        while not done:
            done = True
            for nonterm in self.grammar.nonterms:
                for prod_a, prod_b in combinations(self.grammar.prod_by_nonterminal[nonterm], 2):
                    lah_a = self.look_ahead(k, prod_a)
                    lah_b = self.look_ahead(k, prod_b)
                    if lah_a & lah_b:
                        k += 1
                        done = False

        return k
