"""Sentence-shaped passphrases: one word per part of speech, 2 to 5 words.

Each length has one or more shapes, and each shape uses a list at most once. Shorter shapes
drop the adverb first, since it's the smallest list. The two 5-word shapes differ in which
noun the adjective describes; they're told apart by whether the phrase opens with an
adjective or a subject, which is why those two lists must stay disjoint.

The lists are public, so the strength is what's left for an attacker who has them: the bits
from `entropy_bits`. Every choice comes from `secrets`.
"""

import math
import secrets

from phraselibs.words import load

MIN_WORDS = 2
MAX_WORDS = 5
DEFAULT_WORDS = 5

SHAPES: dict[int, tuple[tuple[str, ...], ...]] = {
    2: (("adjective", "subject"),),
    3: (("subject", "verb", "object"),),
    4: (("adjective", "subject", "verb", "object"),),
    5: (
        ("adjective", "subject", "adverb", "verb", "object"),
        ("subject", "adverb", "verb", "adjective", "object"),
    ),
}


def _check(words: object) -> int:
    if not isinstance(words, int) or isinstance(words, bool):
        raise TypeError(f"words must be an int, not {type(words).__name__}")
    if not MIN_WORDS <= words <= MAX_WORDS:
        raise ValueError(f"words must be {MIN_WORDS} to {MAX_WORDS}, not {words}")
    return words


def generate(words: int = DEFAULT_WORDS) -> str:
    """A random phrase of `words` words (2 to 5), lowercase, single spaces."""
    shapes = SHAPES[_check(words)]
    shape = shapes[secrets.randbelow(len(shapes))]
    picked = []
    for part in shape:
        pool = load(part)
        picked.append(pool[secrets.randbelow(len(pool))])
    return " ".join(picked)


def entropy_bits(words: int = DEFAULT_WORDS) -> float:
    """Bits of randomness in a `words`-word phrase, for an attacker who knows the lists.

    Every shape of one length uses the same lists, so the first shape stands for all of them.
    """
    shapes = SHAPES[_check(words)]
    return math.log2(len(shapes)) + sum(math.log2(len(load(part))) for part in shapes[0])
