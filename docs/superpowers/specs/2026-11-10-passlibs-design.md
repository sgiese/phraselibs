# passlibs: sentence-shaped passphrases

## Why

People are handed passphrases to read aloud or type from a text message. Random
characters are miserable for that; random words are better; a little sentence built
Mad Libs style, one word per part of speech, is easier still: "adventurous aardvark
gracefully juggling teapots".

The generator and its word lists started inside another project of the author's, where a
tool prints a passphrase for a new user. A second project now needs the same thing, so the
generator moves here, as a small public library both can depend on instead of two copies.

## Goals

- A public, MIT-licensed Python library and command that generate sentence-shaped
  passphrases from hand-curated word lists.
- **A length flag, 2 to 5 words.** 5 is the default.
- The 5-word output is exactly what the original generator produces today (same lists, same
  two sentence shapes), so moving it here changes nothing for the first user.
- A repo a stranger can pick up: clear README, license, security policy, contributing notes,
  CI, tagged releases with notes.

## Non-goals

- **No hashing, verifying, sessions or lockout.** Callers own how a phrase is stored and
  checked; passlibs only makes phrases.
- **No normalizing.** Phrases come out lowercase with single spaces. A caller that wants to
  accept "Lazy Otter" for "lazy otter" lowercases on its side.
- No other languages, no WordNet or other big dictionaries: the lists are small on purpose
  so every word is common, easy to say and easy to spell.
- No PyPI release for now; installs are from the GitHub repo by tag.

## Anti-goals

- A shorter phrase must never become the default. Two words are about 17 bits: fine behind a
  sign-in with lockout, weak against an offline attack on a leaked hash.
- No weak randomness anywhere: every choice uses `secrets`.

## How it works

### The word lists

Five lists: ADJECTIVES (376), SUBJECTS (280), ADVERBS (187), VERBS_ING (262, all transitive),
OBJECTS (284), carried over unchanged. They're plain data, one word per line, a text file per
list inside the package (for example `passlibs/words/adjectives.txt`), so a program in
another language can read them too. The package loads them with `importlib.resources`.

Rules, pinned by tests: every word is lowercase a–z only; no duplicates within a list;
ADJECTIVES and SUBJECTS are disjoint, which keeps the two 5-word shapes tell-apart-able and so
the extra template bit real.

### Shapes by length

Every shape uses each list at most once.

| Words | Shape(s) | Example | Bits (approx.) |
|---|---|---|---|
| 2 | adjective subject | lazy otter | 16.7 |
| 3 | subject verb object | otter juggling teapots | 24.3 |
| 4 | adjective subject verb object | lazy otter juggling teapots | 32.9 |
| 5 | adjective subject adverb verb object; subject adverb verb adjective object | adventurous aardvark gracefully juggling teapots | 41.4 |

Shorter shapes drop the adverb first, since it's the smallest list, and each still reads as
something a person would say.

Bits are `log2(number of shapes) + sum(log2(len(list)))` for that length: the strength
against an attacker who has these lists, which are public. The lists being public costs
nothing; the strength comes from the random choice.

### The library

    from passlibs import generate, entropy_bits
    generate()           # 5 words, one of the two 5-word shapes
    generate(words=3)    # 2..5; anything else raises ValueError
    entropy_bits(5)      # float, ~41.4

Standard library only. Python >= 3.11. Tests pin `entropy_bits(5)` to 41.4 (one decimal) so
a list change that would weaken the default can't slip through.

### The command

    passlibs                 # one 5-word phrase on stdout
    passlibs --words 3       # 2..5
    passlibs --bits          # also the bit count, on stderr

Only the phrase goes to stdout, with a newline, so scripts can capture it. argparse, no
dependencies.

## The public-repo basics

- README: what it is, an example, install (`uv add "passlibs @ git+https://github.com/sgiese/passlibs@v0.1.0"`,
  `uvx --from git+https://github.com/sgiese/passlibs@v0.1.0 passlibs`), the bits table, the
  security notes above, license.
- LICENSE (MIT), SECURITY.md (report privately through GitHub's private vulnerability
  reporting), CONTRIBUTING.md (short: issue first, tests and lint pass, what changes to the
  lists need), CHANGELOG.md (Keep a Changelog).
- CI on GitHub Actions: tests, ruff and pyright on Python 3.11 and the newest supported
  version, for pushes to main and pull requests. Dependabot keeps the Actions current.
- Issue and pull request templates.
- Repo settings: description and topics, `main` protected by a ruleset (changes through pull
  requests, CI must pass), squash merges, head branches deleted after merge, private
  vulnerability reporting on.
- Releases: semver tags, each with a GitHub Release whose notes come from the changelog.
  `v0.1.0` is the first.
- Commits use the author's GitHub no-reply address.

## Left to the builder

File layout inside the package, test layout, exact message wording, template wording.
