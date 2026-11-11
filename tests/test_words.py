import itertools
import re

import pytest

from phraselibs.words import PARTS, load


def test_list_sizes() -> None:
    assert {p: len(load(p)) for p in PARTS} == {
        "adjective": 376,
        "subject": 280,
        "adverb": 187,
        "verb": 262,
        "object": 284,
    }


@pytest.mark.parametrize("part", PARTS)
def test_words_are_lowercase_letters_only(part: str) -> None:
    assert all(re.fullmatch("[a-z]+", w) for w in load(part))


@pytest.mark.parametrize("part", PARTS)
def test_no_duplicates_within_a_list(part: str) -> None:
    assert len(set(load(part))) == len(load(part))


def test_lists_are_disjoint() -> None:
    """No word is in two lists, so a phrase shows which shape made it and every shape adds
    phrases no other shape makes; entropy_bits counts on that."""
    for a, b in itertools.combinations(PARTS, 2):
        assert set(load(a)).isdisjoint(load(b)), (a, b)


def test_unknown_part_raises() -> None:
    with pytest.raises(KeyError):
        load("noun")
