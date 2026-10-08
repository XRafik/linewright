# Briefs

One brief per stage, read at startup from the `briefs` setting (default: these,
built into the binary). Each is a fork of a skill from
[`mattpocock/skills`](https://github.com/mattpocock/skills) (commit
`f3fc5632`), under its MIT license (`LICENSE`), made non-interactive for
Linewright:

- each decision the original puts to a person is made by the agent or handed
  back as an outcome;
- tracker access is replaced by the brief (the task Linewright appends) and
  the result (the JSON the session ends with);
- the review's sub-agents invoke no skills.

| brief | forked from | used by |
|---|---|---|
| `triage.md` | `triage` (with `AGENT-BRIEF.md`, `OUT-OF-SCOPE.md`) | triage |
| `to-tickets.md` | `to-tickets` | tickets |
| `implement.md` | `implement` | implementation, rework, CI fixes, conflicts |
| `tdd.md` | `tdd` (with `tests.md`, `mocking.md`) | appended to `implement.md` |
| `code-review.md` | `code-review` | appended to `implement.md` |
| `pr.md` | `pr` | appended to `implement.md` |

Linewright appends the task (the issue, pull request or spec diff) and the
result contract to each brief, so a brief says how to work, not what the
result looks like.
