"""The phraselibs command: print one phrase on stdout, so scripts can capture it."""

import argparse
import sys

from phraselibs.generator import DEFAULT_WORDS, MAX_WORDS, MIN_WORDS, entropy_bits, generate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="phraselibs",
        description="Print a sentence-shaped passphrase, such as "
        "'adventurous aardvark gracefully juggling teapots'.",
    )
    parser.add_argument(
        "--words",
        type=int,
        choices=range(MIN_WORDS, MAX_WORDS + 1),
        default=DEFAULT_WORDS,
        metavar="N",
        help=f"words in the phrase, {MIN_WORDS} to {MAX_WORDS} (default {DEFAULT_WORDS})",
    )
    parser.add_argument(
        "--bits", action="store_true", help="also print the phrase's strength in bits, on stderr"
    )
    args = parser.parse_args(argv)
    print(generate(words=args.words))
    if args.bits:
        print(f"{entropy_bits(args.words):.1f} bits", file=sys.stderr)
    return 0
