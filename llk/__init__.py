"""LL(k) parser implementation.

This parser is able to take in any Context-Free Grammar and then attempt
to parse a word and build a derivation tree for it.

The main priority is correctness, not necessarily efficiency.
"""

from .symbol import Symbol, Terminal, Nonterminal, SententialForm, Word, LAMBDA, END
from .util import concat, format_words
from .grammar import Production, Grammar
from .parser import LLParser
