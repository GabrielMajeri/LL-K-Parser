#!/usr/bin/env python3

import llk
from llk import *

grammar = Grammar.read('simple3.txt')
parser = LLParser(grammar)

print(grammar)

print(f"Grammar is in LL({parser.k})")
print(f"Look-aheads: {parser.look_up}")

word = 'abbbbb'

print(f"Word '{word}' is accepted: {parser.parse(word)}")
