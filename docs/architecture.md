# Architecture

Linewright's architecturally significant decisions: the ones costly to change
later.

- **The store is an interface; GitHub is the production store.** Linewright
  persists nothing of its own; between polls it holds only the runs in
  flight. Each poll reconciles a snapshot of the store with those runs.
  Machine state is derived from the store's facts (assignee, linked PR,
  review and check state), never written as labels. A local store of plain
  files serves replay and tests.
- **Functional core, imperative shell.** The reconcile step is a pure
  function from a snapshot, the live runs and the clock to a list of actions.
  The store, git, the agent runtime and the clock sit behind interfaces with
  a real and a fake implementation.
- **Agents are headless Claude Code sessions, one per stage**, each in its
  own clone, without permission prompts, behind one runtime interface. The
  model is configuration.
- **Agents read through the brief and write through the result.** The
  manager puts what a session needs from the store (issue, comments, spec
  diff, PR comments) into its brief. The session works in its own clone
  under the work directory and commits there; its final message is JSON the
  manager parses and applies: the outcome, tickets, comments, the PR's title
  and body. The manager pushes the branch and opens the PR through the store.
  Only the manager writes to the store; prose for people goes to comments. A
  result that does not parse is sent back to the session with the error, a
  bounded number of times.
- **Briefs are files read at startup**, one per stage, forked from
  `mattpocock/skills` (`triage`, `to-tickets`, `implement`, `code-review`,
  `pr`, `tdd`) with their MIT notice, made non-interactive: each decision the
  originals put to a person is made by the agent or handed back as an
  outcome, tracker access is replaced by the brief and the result, and the
  review's sub-agents invoke no skills.
- **Every session's trace is kept**: the runtime's own transcript, copied
  beside the session's brief and result under the work directory.
- **Rust, with GitHub's REST and GraphQL APIs in-process.**
- **Spec changes are found by lookback**: pull requests merged within the
  window, minus those labeled processed.
- **Identity is a user account**: a token for a GitHub user dedicated to
  Linewright, whose assignments are its claims.
- **Runs on a host or in a container the operator builds.** A published base
  image (`linewright`, `git`, the agent runtime) is the starting point for
  the operator's image.
- **Configuration is layered**: flags, `LINEWRIGHT_*` environment variables,
  a TOML file, defaults, parsed once into one typed value. Credentials come
  from the environment only.
