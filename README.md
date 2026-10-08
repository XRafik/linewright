# Linewright

Linewright is a spec-driven software factory: you write the specification, and
coding agents turn it into working software.

It is a server that polls a GitHub repository. A merged pull request that
changes the spec (`docs/**/*.md` by default) is cut into tickets; an issue
labeled `needs-triage` is triaged; an issue labeled `ready-for-agent` is
implemented, reviewed by agents, and delivered as a pull request that is green
and ready for your review. You merge it, or comment and the factory reworks it.
What it does and why is in [`docs/specs/product.md`](docs/specs/product.md);
the decisions behind the code are in
[`docs/specs/architecture.md`](docs/specs/architecture.md).

## Running it

You need `git` and [Claude Code](https://code.claude.com) (`claude`) on the
path, your project's toolchain so agents can build and test it, and a GitHub
user for the factory with write access to the repository.

```sh
export GH_TOKEN=...            # the machine user's token (or GITHUB_TOKEN)
export ANTHROPIC_API_KEY=...   # or any login Claude Code already has
cargo install --path .
linewright --repo owner/name serve
```

- `linewright serve` polls until stopped; `once` runs one poll cycle and the
  runs it starts; `status` lists the work in flight.
- Every setting is a flag, a `LINEWRIGHT_<FLAG>` environment variable or a key
  in `linewright.toml`; `linewright --help` lists them with their defaults.
- The `Dockerfile` builds the base image: `linewright`, `git` and Claude Code.
  Build your own image from it with your project's toolchain added.

## Tuning the briefs

Each stage's agent works from a brief in [`briefs/`](briefs/). To try a change
against a real case:

```sh
linewright capture owner/name#123 case/      # a spec change or an issue
linewright --briefs briefs/ replay case/ --out run-1/
```

`run-1/` holds the issues and pull requests the run produced (`issues/`,
`pulls/`, as JSON, Markdown and diffs) and every session's brief, result and
trace (`sessions/`).

## Developing

```sh
cargo test
```

Tests sit where [`CODING_STANDARDS.md`](CODING_STANDARDS.md) puts them:
`tests/reconcile.rs` drives the decision function, and `tests/pipeline.rs`,
`tests/replay.rs` and `tests/config.rs` drive the system as a user would,
against a local store standing in for GitHub and a scripted agent runtime.
