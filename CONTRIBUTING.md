# Contributing

Thanks for helping. phraselibs is small on purpose; please open an issue before a pull request
so we can agree on the change first.

## Making a change

1. Branch from `main`.
2. `uv sync`, then make the change with a test.
3. Before opening the pull request, all of these pass:

       uv run pytest
       uv run ruff check .
       uv run ruff format --check .
       uv run pyright

4. Open a pull request that says what changed, why, and how you checked it, and links the issue.

## Changing the word lists

The bit counts depend on the lists, so list changes get extra care:

- One word per line, lowercase `a`-`z` only, common and easy to say and spell.
- No word in two lists, and no duplicates.
- Verbs end in `-ing` and take an object ("juggling teapots").
- Removing words lowers the bits. The tests pin the list sizes and the bits table; update them,
  the README table and `CHANGELOG.md` in the same pull request, and say why.

## Releases

Maintainers tag `vX.Y.Z` on `main` and publish a GitHub Release with the notes from
`CHANGELOG.md`.
