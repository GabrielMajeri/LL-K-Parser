#!/usr/bin/env python3

import llk
from llk import *

grammar = Grammar.read('simple1.txt')
parser = LLParser(grammar)

for nonterminal in grammar.nonterms:
    firsts = parser.first(1, (nonterminal,))
    print(f"{nonterminal} => {firsts}")
