#!/usr/bin/env python3

import llk
from llk import Grammar, LLParser

grammar = Grammar.read('simple1.txt')
parser = LLParser(grammar)

print(grammar)

print(f"Grammar is in LL({parser.k})")
print(f"Look-aheads: {parser.look_up}")

word = 'ab'

print(f"Word '{word}' is accepted: {parser.parse(word)}")
