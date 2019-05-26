from typing import Set

from . import Word, LAMBDA

def concat(set_a: Set[Word], set_b: Set[Word]) -> Set[Word]:
    """Performs concatenation of two languages."""
    if not set_a:
        return set_b
    if not set_b:
        return set_a
    return {u + v for u in set_a for v in set_b}

def format_word(word: Word) -> str:
    if word == LAMBDA:
        return 'λ'
    return ''.join(map(str, word))

def format_words(words: Set[Word]) -> str:
    if not words:
        return '∅'
    return f'{{{", ".join(map(format_word, words))}}}'
