import pytest

from phraselibs.cli import main


def test_prints_five_words(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    out, err = capsys.readouterr()
    assert out.endswith("\n") and out.count("\n") == 1
    assert len(out.split()) == 5
    assert err == ""


@pytest.mark.parametrize("n", range(2, 6))
def test_words_flag(n: int, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--words", str(n)]) == 0
    assert len(capsys.readouterr().out.split()) == n


@pytest.mark.parametrize(("args", "bits"), [([], "42.4"), (["--words", "2"], "18.5")])
def test_bits_goes_to_stderr(
    args: list[str], bits: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([*args, "--bits"]) == 0
    out, err = capsys.readouterr()
    assert "bits" not in out
    assert err == f"{bits} bits\n"


@pytest.mark.parametrize("value", ["6", "1", "abc"])
def test_bad_words_value(value: str, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--words", value])
    assert exit_info.value.code == 2
    out, err = capsys.readouterr()
    assert out == ""
    assert "--words" in err
