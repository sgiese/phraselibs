# phraselibs

Passphrases shaped like little sentences, Mad Libs style:

    adventurous aardvark gracefully juggling teapots

Random characters are miserable to read aloud or type on a phone. Random words are better.
A tiny sentence, one word from each part of speech, is easier still: you can say it once,
picture it, and type it without looking back. The words come from small hand-picked lists of
common, easy-to-spell words.

## Install

phraselibs isn't on PyPI; install it from this repository by tag (the first release is
`v0.1.0`):

    uv add "phraselibs @ git+https://github.com/sgiese/phraselibs@v0.1.0"

Or run the command without installing anything:

    uvx --from git+https://github.com/sgiese/phraselibs@v0.1.0 phraselibs

Python 3.11 or newer; no dependencies.

## Use

```python
from phraselibs import generate, entropy_bits

generate()  # 'adventurous aardvark gracefully juggling teapots'
generate(words=3)  # 'otter juggling teapots'
entropy_bits(5)  # 42.4...
```

```console
$ phraselibs
rascally minstrel crocheting hoops
$ phraselibs --words 3 --bits
toad threading hammocks
26.2 bits
```

`--words` takes 2 to 5 (default 5). The phrase alone goes to stdout, so scripts can capture
it; `--bits` writes the strength to stderr.

## Lengths

| Words | Shapes | Example | Bits |
|---|---|---|---|
| 2 | adjective subject; adjective object; verb object; verb subject | lazy otter, juggling teapots | 18.5 |
| 3 | subject verb object; verb adjective object; adverb verb object; adverb verb subject | otter juggling teapots, gracefully juggling otter | 26.2 |
| 4 | adjective subject verb object; subject adverb verb object; subject verb adjective object; adverb verb adjective object; adverb verb adjective subject | lazy otter juggling teapots, gracefully juggling lazy otter | 34.8 |
| 5 | adjective subject adverb verb object; subject adverb verb adjective object; adjective subject verb object adverb; subject verb adjective object adverb | adventurous aardvark gracefully juggling teapots, otter juggling purple teapots gracefully | 42.4 |

A shape is picked in proportion to how many phrases it makes, so every phrase of a length is
equally likely. No word is in two lists, so no two shapes make the same phrase, and the bits
are log2 of how many phrases the length can make.

## Security notes

- **The word lists are public, and the bits assume an attacker has them.** The strength comes
  from choosing at random (Python's `secrets`), not from a secret dictionary.
- **Pick the length for where the phrase will be checked.** Behind a sign-in that locks out
  after a few wrong tries, even 2 or 3 words hold up. If a password hash could ever leak and
  be attacked offline, keep the default 5 words, and use a slow hash such as Argon2id.
- **phraselibs only makes phrases.** Hashing, storing and checking them is up to you.
  Phrases are lowercase with single spaces; if you want to accept "Lazy Otter" for
  "lazy otter", lowercase and collapse spaces before hashing and before comparing.

Found a security problem? Please report it privately through this repository's
**Security** tab, not in a public issue.

## License

MIT. See [LICENSE](LICENSE).
