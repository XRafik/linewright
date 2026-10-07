# Linewright

The vocabulary of a software factory that turns a repository's spec and
issues into software. The specs in `docs/` and the code use these terms as
defined here.

## Language

### Roles

**Operator**:
The person who runs Linewright.
_Avoid_: admin, user

**Maintainer**:
The person who owns the repository.
_Avoid_: owner, reviewer, human

**Reporter**:
Someone who files an issue, such as a customer.
_Avoid_: customer, author

**Agent**:
A coding-agent session Linewright runs.
_Avoid_: bot, model, worker

**Machine user**:
The GitHub user account Linewright acts as.
_Avoid_: bot account, service account
