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


def test_both_five_word_shapes_appear() -> None:
    firsts = [generate().split(" ")[0] for _ in range(200)]
    assert any(w in load("adjective") for w in firsts)
    assert any(w in load("subject") for w in firsts)


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
        2: 16.7,
        3: 24.3,
        4: 32.9,
        5: 41.4,
    }


def test_uses_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(generator.secrets, "randbelow", lambda n: 0)
    assert generate(words=2) == f"{load('adjective')[0]} {load('subject')[0]}"
