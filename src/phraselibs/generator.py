"""Sentence-shaped passphrases: one word per part of speech, 2 to 5 words.

Each length has several shapes, and each shape uses a list at most once. No word is in two
lists, so a phrase shows which shape made it and every shape adds phrases no other shape
makes. A shape is picked in proportion to how many phrases it makes, so every phrase of a
length is equally likely and none is an easier guess than the rest.

The lists are public, so the strength is what's left for an attacker who has them: the bits
from `entropy_bits`. Every choice comes from `secrets`.
"""

import math
import secrets

from phraselibs.words import load

MIN_WORDS = 2
MAX_WORDS = 5
DEFAULT_WORDS = 5

_A, _S, _D, _V, _O = "adjective", "subject", "adverb", "verb", "object"

SHAPES: dict[int, tuple[tuple[str, ...], ...]] = {
    2: (
        (_A, _S),  # lazy otter
        (_A, _O),  # purple teapots
        (_V, _O),  # juggling teapots
        (_V, _S),  # juggling otter
    ),
    3: (
        (_S, _V, _O),  # otter juggling teapots
        (_V, _A, _O),  # juggling purple teapots
        (_D, _V, _O),  # gracefully juggling teapots
        (_D, _V, _S),  # gracefully juggling otter
    ),
    4: (
        (_A, _S, _V, _O),  # lazy otter juggling teapots
        (_S, _D, _V, _O),  # otter gracefully juggling teapots
        (_S, _V, _A, _O),  # otter juggling purple teapots
        (_D, _V, _A, _O),  # gracefully juggling purple teapots
        (_D, _V, _A, _S),  # gracefully juggling lazy otter
    ),
    5: (
        (_A, _S, _D, _V, _O),  # lazy otter gracefully juggling teapots
        (_S, _D, _V, _A, _O),  # otter gracefully juggling purple teapots
        (_A, _S, _V, _O, _D),  # lazy otter juggling teapots gracefully
        (_S, _V, _A, _O, _D),  # otter juggling purple teapots gracefully
    ),
}


def _check(words: object) -> int:
    if not isinstance(words, int) or isinstance(words, bool):
        raise TypeError(f"words must be an int, not {type(words).__name__}")
    if not MIN_WORDS <= words <= MAX_WORDS:
        raise ValueError(f"words must be {MIN_WORDS} to {MAX_WORDS}, not {words}")
    return words


def _phrases(shape: tuple[str, ...]) -> int:
    """How many different phrases one shape makes."""
    return math.prod(len(load(part)) for part in shape)


def _pick_shape(shapes: tuple[tuple[str, ...], ...]) -> tuple[str, ...]:
    """One shape, weighted by how many phrases it makes."""
    pick = secrets.randbelow(sum(map(_phrases, shapes)))
    for shape in shapes:
        if pick < _phrases(shape):
            return shape
        pick -= _phrases(shape)
    raise AssertionError("unreachable: pick is below the total")


def generate(words: int = DEFAULT_WORDS) -> str:
    """A random phrase of `words` words (2 to 5), lowercase, single spaces."""
    picked = []
    for part in _pick_shape(SHAPES[_check(words)]):
        pool = load(part)
        picked.append(pool[secrets.randbelow(len(pool))])
    return " ".join(picked)


def entropy_bits(words: int = DEFAULT_WORDS) -> float:
    """Bits of randomness in a `words`-word phrase, for an attacker who knows the lists.

    log2 of how many phrases that length can make, across all its shapes. That's exact
    because every phrase is equally likely and no two shapes make the same phrase.
    """
    return math.log2(sum(map(_phrases, SHAPES[_check(words)])))
