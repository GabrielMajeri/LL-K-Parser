from . import concat, Terminal, Nonterminal, Word, SententialForm, LAMBDA, END, Production, Grammar, format_words
from itertools import combinations
from typing import Dict, List, Set

class LLParser:
    grammar: Grammar
    k: int
    look_up: Dict[Nonterminal, Dict[Word, Production]]

    def __init__(self, grammar: Grammar) -> None:
        self.grammar = grammar
        self.k = self._find_k()
        self.look_up = {}
        for nonterm in self.grammar.nonterms:
            table = {}

            for prod in self.grammar.prod_by_nonterminal[nonterm]:
                look_ahead = self._look_ahead(self.k, prod)
                for w in look_ahead:
                    table[w] = prod

            self.look_up[nonterm] = table

    def parse(self, word: str) -> bool:
        w = tuple(map(lambda ch: Terminal(ch), word))

        padding = (END, ) * self.k
        w += padding

        stack = [*padding, self.grammar.sentence_symbol]

        i = 0

        while stack:
            top = stack.pop()

            if isinstance(top, Nonterminal):
                ahead = w[i:i + self.k]
                if (top not in self.look_up or ahead not in self.look_up[top]):
                    return False

                prod = self.look_up[top][ahead]
                expansion = prod.end

                stack += expansion[::-1]

            elif isinstance(top, Terminal):
                char = w[i]
                if char != top:
                    return False
                i += 1
            else:
                raise NotImplementedError

        return True

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

    def _first(self, k: int, w: SententialForm) -> Set[Word]:
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
                follows |= self._first(k, rhs + extra)

        return follows

    def _follow(self, k: int, nt: Nonterminal) -> Set[Word]:
        visited: Set[Nonterminal] = set()
        return self._follow_impl(k, nt, visited)

    def _look_ahead(self, k: int, p: Production) -> Set[Word]:
        follows = self._follow(k, p.start)

        look_aheads: Set[Word] = set()
        for follow in follows:
            look_aheads |= self._first(k, p.end + follow)
        return look_aheads

    def _find_k(self) -> int:
        if all(map(lambda prods: len(prods) == 1, self.grammar.prod_by_nonterminal.values())):
            return 0

        k = 1
        done = False

        while not done:
            done = True
            for nonterm in self.grammar.nonterms:
                for prod_a, prod_b in combinations(self.grammar.prod_by_nonterminal[nonterm], 2):
                    lah_a = self._look_ahead(k, prod_a)
                    lah_b = self._look_ahead(k, prod_b)
                    if lah_a & lah_b:
                        k += 1
                        done = False

        return k

    def print_firsts(self) -> None:
        print(f"First {self.k} generated terminals:")
        for nonterminal in self.grammar.nonterms:
            firsts = self._first(self.k, (nonterminal,))
            print(f"{nonterminal} => {format_words(firsts)}")

    def print_follows(self) -> None:
        print(f"First {self.k} terminals after nonterminal:")
        for nonterminal in self.grammar.nonterms:
            follows = self._follow(1, nonterminal)
            print(f"{nonterminal} => {format_words(follows)}")

    def print_look_ahead(self) -> None:
        print(f"{self.k} terminals we need to look-ahead:")
        for production in self.grammar.prods:
            look_aheads = self._look_ahead(k, production)
            print(f"({production}) => {format_words(look_aheads)}")
