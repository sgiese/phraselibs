"""The five word lists, one text file per part of speech, one word per line.

They're plain data so programs in other languages can read them too. Every word is common,
lowercase and easy to say; tests pin the sizes and rules.
"""

from functools import cache
from importlib.resources import files

PARTS: tuple[str, ...] = ("adjective", "subject", "adverb", "verb", "object")

_FILES = {
    "adjective": "adjectives.txt",
    "subject": "subjects.txt",
    "adverb": "adverbs.txt",
    "verb": "verbs_ing.txt",
    "object": "objects.txt",
}


@cache
def load(part: str) -> tuple[str, ...]:
    """The words for one part of speech. KeyError for a part that isn't in PARTS."""
    text = (files("phraselibs") / "words" / _FILES[part]).read_text(encoding="utf-8")
    return tuple(text.split())
