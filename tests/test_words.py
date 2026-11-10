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


def test_adjectives_and_subjects_are_disjoint() -> None:
    """The two 5-word shapes differ only in whether they open with an adjective or a subject,
    so this is what makes the extra shape bit real."""
    assert set(load("adjective")).isdisjoint(load("subject"))


def test_unknown_part_raises() -> None:
    with pytest.raises(KeyError):
        load("noun")
