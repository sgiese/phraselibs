# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- README guidance on hashing phrases and pinning a release to its commit.

## [0.1.0] - 2026-11-10

### Added

- `generate(words=5)`: sentence-shaped passphrases of 2 to 5 words from five word lists
  (adjectives, subjects, adverbs, `-ing` verbs, objects), every choice from `secrets`.
- `entropy_bits(words=5)`: the strength against an attacker who has the lists: 18.5, 26.2, 34.8
  and 42.4 bits for 2 to 5 words.
- The `phraselibs` command, with `--words N` and `--bits`.

[Unreleased]: https://github.com/sgiese/phraselibs/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sgiese/phraselibs/releases/tag/v0.1.0
