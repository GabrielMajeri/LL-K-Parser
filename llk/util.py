from typing import Set

from . import Word

def concat(a: Set[Word], b: Set[Word]) -> Set[Word]:
    """Performs concatenation of two languages."""
    if not a:
        return b
    if not b:
        return a
    return {u + v for u in a for v in b}
