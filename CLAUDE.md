# passlibs

<One sentence: what this is and who it is for.>

## Working here
- Simple over clever. Prefer the obvious solution; no abstractions for cases that do not exist yet.
- Small, focused changes. One concern per commit; leave unrelated code alone.
- Change behavior with a test. Reproduce a bug in a test before fixing it.
- No new dependencies without asking.
- Match the existing style. Run the formatter and linter before finishing.
- Explain non-obvious decisions in the commit message, not in comments.

## Workflow
Every change, fixes and docs included, follows this path. Nothing is pushed straight to `main`.
1. **Issue first.** Work starts as a GitHub issue with a "Done when" list (`gml issue create`). Pick it up by assigning yourself. An issue labelled `decision` (created with `gml issue create --brainstorm`) is a design question, not an implementation task: brainstorm with the owner and record the chosen direction in the issue, plus implementation issues, before writing any code.
2. **Branch in a worktree.** `gml issue start <n>`: branch `issue-<n>-<short-slug>` in a git worktree under `.worktrees/`, never on `main`.
3. **Commits reference the issue.** `#<n>` in the body; the final commit says `Closes #<n>`. One concern per PR; keep it small.
4. **Pull request for review.** When tests and lint pass, `gh pr create`: a summary, the evidence (test and lint output, anything checked by hand), and `Closes #<n>` if this PR finishes the issue, `Refs #<n>` if it does not (a plan for review, a first half). Never Closes, Fixes or Resolves in a PR that is not the last: GitHub acts on them anywhere in the body. Open the PR and stop.
5. **Review, then merge.** The maintainer reviews and merges, or says so; Claude merges only when told to. `gml issue merge <n>` merges the open PR if there is one and, once nothing is unmerged, removes the branch and worktree; it is also the command after a merge in the UI.

## Commands
- Setup: `uv sync`
- Test: `uv run pytest`
- Lint: `uv run ruff check .` and `uv run ruff format .`
- Types: `uv run pyright`
- Add a dependency: `uv add <package>` (or `uv add --group dev <tool>`); commit `uv.lock` with it
