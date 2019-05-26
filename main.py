#!/usr/bin/env python3

import llk
from llk import *

grammar = Grammar.read('simple3.txt')
parser = LLParser(grammar)

def print_firsts(k: int) -> None:
    print(f"First {k} generated terminals:")
    for nonterminal in grammar.nonterms:
        firsts = parser.first(k, (nonterminal,))
        print(f"{nonterminal} => {format_words(firsts)}")

def print_follows(k: int) -> None:
    print(f"First {k} terminals after nonterminal:")
    for nonterminal in grammar.nonterms:
        follows = parser.follow(1, nonterminal)
        print(f"{nonterminal} => {format_words(follows)}")

def print_look_ahead(k: int) -> None:
    print(f"{k} terminals we need to look-ahead:")
    for production in grammar.prods:
        look_aheads = parser.look_ahead(k, production)
        print(f"({production}) => {format_words(look_aheads)}")

print(grammar)

print(f"Grammar is in LL({parser.find_k()})")
