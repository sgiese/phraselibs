# phraselibs: sentence-shaped passphrases

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
- The 5-word output uses the original generator's lists and keeps its two sentence shapes,
  plus two more (owner's decision, 2026-11-10): still five words, still above the first
  user's 40-bit floor, and existing passphrases are unaffected.
- A repo a stranger can pick up: clear README, license, security policy, contributing notes,
  CI, tagged releases with notes.

## Non-goals

- **No hashing, verifying, sessions or lockout.** Callers own how a phrase is stored and
  checked; phraselibs only makes phrases.
- **No normalizing.** Phrases come out lowercase with single spaces. A caller that wants to
  accept "Lazy Otter" for "lazy otter" lowercases on its side.
- No other languages, no WordNet or other big dictionaries: the lists are small on purpose
  so every word is common, easy to say and easy to spell.
- No PyPI release for now; installs are from the GitHub repo by tag.

## Anti-goals

- A shorter phrase must never become the default. Two words are about 18 bits: fine behind a
  sign-in with lockout, weak against an offline attack on a leaked hash.
- No weak randomness anywhere: every choice uses `secrets`.

## How it works

### The word lists

Five lists: ADJECTIVES (376), SUBJECTS (280), ADVERBS (187), VERBS_ING (262, all transitive),
OBJECTS (284), carried over unchanged. They're plain data, one word per line, a text file per
list inside the package (for example `phraselibs/words/adjectives.txt`), so a program in
another language can read them too. The package loads them with `importlib.resources`.

Rules, pinned by tests: every word is lowercase a–z only; no duplicates within a list;
no word is in two lists, so a phrase shows which shape made it and every shape adds phrases
no other shape makes.

### Shapes by length

Every shape uses each list at most once.

| Words | Shapes | Example | Bits (approx.) |
|---|---|---|---|
| 2 | adjective subject; adjective object; verb object; verb subject | lazy otter, juggling teapots | 18.5 |
| 3 | subject verb object; verb adjective object; adverb verb object; adverb verb subject | otter juggling teapots, gracefully juggling otter | 26.2 |
| 4 | adjective subject verb object; subject adverb verb object; subject verb adjective object; adverb verb adjective object; adverb verb adjective subject | lazy otter juggling teapots, gracefully juggling lazy otter | 34.8 |
| 5 | adjective subject adverb verb object; subject adverb verb adjective object; adjective subject verb object adverb; subject verb adjective object adverb | adventurous aardvark gracefully juggling teapots, otter juggling purple teapots gracefully | 42.4 |

Each shape reads as something a person would say (owner's choice of shapes, 2026-11-10).
Shapes that end on a verb are left out, since every verb takes an object, and so are shapes
that use a list twice.

A shape is picked in proportion to how many phrases it makes, so every phrase of a length
is equally likely. Bits are `log2(sum over the shapes of the product of their list sizes)`
for that length: the strength
against an attacker who has these lists, which are public. The lists being public costs
nothing; the strength comes from the random choice.

### The library

    from phraselibs import generate, entropy_bits
    generate()           # 5 words, one of the four 5-word shapes
    generate(words=3)    # 2..5; anything else raises ValueError
    entropy_bits(5)      # float, ~42.4

Standard library only. Python >= 3.11. Tests pin `entropy_bits(5)` to 42.4 (one decimal) so
a list change that would weaken the default can't slip through.

### The command

    phraselibs                 # one 5-word phrase on stdout
    phraselibs --words 3       # 2..5
    phraselibs --bits          # also the bit count, on stderr

Only the phrase goes to stdout, with a newline, so scripts can capture it. argparse, no
dependencies.

## The public-repo basics

- README: what it is, an example, install (`uv add "phraselibs @ git+https://github.com/sgiese/phraselibs@v0.1.0"`,
  `uvx --from git+https://github.com/sgiese/phraselibs@v0.1.0 phraselibs`), the bits table, the
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
