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
entropy_bits(5)  # 41.4...
```

```console
$ phraselibs
rascally minstrel crocheting hoops
$ phraselibs --words 3 --bits
toad threading hammocks
24.3 bits
```

`--words` takes 2 to 5 (default 5). The phrase alone goes to stdout, so scripts can capture
it; `--bits` writes the strength to stderr.

## Lengths

| Words | Shape | Example | Bits |
|---|---|---|---|
| 2 | adjective subject | lazy otter | 16.7 |
| 3 | subject verb object | otter juggling teapots | 24.3 |
| 4 | adjective subject verb object | lazy otter juggling teapots | 32.9 |
| 5 | adjective subject adverb verb object, or subject adverb verb adjective object | adventurous aardvark gracefully juggling teapots | 41.4 |

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
