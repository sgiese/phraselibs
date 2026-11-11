import math
import re
from collections.abc import Callable
from typing import Any

import pytest

from phraselibs import generator
from phraselibs.generator import SHAPES, entropy_bits, generate
from phraselibs.words import PARTS, load

LENGTHS = range(2, 6)
BOTH: list[Callable[..., Any]] = [generate, entropy_bits]


def test_default_is_five_words() -> None:
    assert len(generate().split(" ")) == 5


@pytest.mark.parametrize("n", LENGTHS)
def test_each_length_has_that_many_words(n: int) -> None:
    assert len(generate(words=n).split(" ")) == n


@pytest.mark.parametrize("n", LENGTHS)
def test_phrase_is_single_spaced_lowercase(n: int) -> None:
    for _ in range(200):
        phrase = generate(words=n)
        assert re.fullmatch("[a-z]+( [a-z]+)*", phrase), phrase


@pytest.mark.parametrize("n", LENGTHS)
def test_words_come_from_the_shape_lists(n: int) -> None:
    for _ in range(50):
        words = generate(words=n).split(" ")
        assert any(
            all(w in load(part) for w, part in zip(words, shape, strict=True))
            for shape in SHAPES[n]
        ), words


def _shape_of(phrase: str) -> tuple[str, ...]:
    """The lists are disjoint, so each word names the list it came from."""
    return tuple(next(p for p in PARTS if w in load(p)) for w in phrase.split(" "))


def test_shapes() -> None:
    a, s, d, v, o = "adjective", "subject", "adverb", "verb", "object"
    assert SHAPES == {
        2: ((a, s), (a, o), (v, o), (v, s)),
        3: ((s, v, o), (v, a, o), (d, v, o), (d, v, s)),
        4: ((a, s, v, o), (s, d, v, o), (s, v, a, o), (d, v, a, o), (d, v, a, s)),
        5: ((a, s, d, v, o), (s, d, v, a, o), (a, s, v, o, d), (s, v, a, o, d)),
    }


@pytest.mark.parametrize("n", LENGTHS)
def test_every_shape_appears(n: int) -> None:
    seen = {_shape_of(generate(words=n)) for _ in range(500)}
    assert seen == set(SHAPES[n])


@pytest.mark.parametrize("n", LENGTHS)
def test_shapes_of_one_length_are_distinct(n: int) -> None:
    assert len(set(SHAPES[n])) == len(SHAPES[n])


def test_every_shape_uses_each_list_at_most_once() -> None:
    for shapes in SHAPES.values():
        for shape in shapes:
            assert len(set(shape)) == len(shape)
            assert set(shape) <= set(PARTS)


@pytest.mark.parametrize("fn", BOTH)
@pytest.mark.parametrize("n", [0, 1, 6, -5])
def test_out_of_range_raises(fn: Callable[..., Any], n: int) -> None:
    with pytest.raises(ValueError):
        fn(words=n)


@pytest.mark.parametrize("fn", BOTH)
@pytest.mark.parametrize("bad", ["3", 3.0, True, None])
def test_non_int_raises(fn: Callable[..., Any], bad: object) -> None:
    with pytest.raises(TypeError):
        fn(words=bad)


def test_entropy_table() -> None:
    assert {n: round(entropy_bits(n), 1) for n in LENGTHS} == {
        2: 18.5,
        3: 26.2,
        4: 34.8,
        5: 42.4,
    }


def _phrases(shape: tuple[str, ...]) -> int:
    return math.prod(len(load(part)) for part in shape)


@pytest.mark.parametrize("n", LENGTHS)
def test_entropy_counts_every_phrase_of_every_shape(n: int) -> None:
    assert entropy_bits(n) == pytest.approx(math.log2(sum(map(_phrases, SHAPES[n]))))


def test_shape_is_picked_in_proportion_to_its_phrases(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every phrase of a length is equally likely, so no shape is an easier guess."""
    calls: list[int] = []
    first, second = SHAPES[2][0], SHAPES[2][1]

    def randbelow(n: int) -> int:
        calls.append(n)
        return _phrases(first) if len(calls) == 1 else 0

    monkeypatch.setattr(generator.secrets, "randbelow", randbelow)
    phrase = generate(words=2)
    assert calls[0] == sum(map(_phrases, SHAPES[2]))
    assert _shape_of(phrase) == second


def test_uses_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(generator.secrets, "randbelow", lambda n: 0)
    assert generate(words=2) == f"{load('adjective')[0]} {load('subject')[0]}"
