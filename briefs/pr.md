<!-- Forked from mattpocock/skills, skills/engineering/pr (MIT, see LICENSE; its Summary visuals credit Dex Horthy's show-me skill). Made non-interactive for Linewright. -->

# Pull request body

The body of the pull request for your work, returned in your result. Use this
template:

```markdown
## Summary

<diagram, diff-sketch, or tree>

## Evidence

- **Before:** <output/failing test run>
  **After:** <output/passing test run>

## Merge Danger

**Door:** <one-way or two-way>

<optional: description>

**Blast Radius:** <one-word description>

<optional: potential ramifications of merge>
```

Skip preambles and keep prose brief. Use the domain language from
`GLOSSARY.md`. Leave out the closing reference to the ticket: Linewright adds
it.

## Summary

Pick the smallest view that makes the key point clear: pseudocode for logic,
a call tree for runtime control flow, a component tree for UI structure, a
shallow file tree for file responsibility or a broad refactor, Mermaid for
component interaction or data flow, or a `diff` of one of those when the point
is what changes and the surrounding shape already exists. Show the whole block
when most of it is new or when omitted context would hide ownership or order.
Place each visual next to the short text it supports, and keep only the calls,
files, states and boundaries needed to make the point; one or two visuals,
rarely more.

## Evidence

Concrete evidence that the change works, before and after. Execution-based
evidence is best here: test results and console output. Show the test that
failed before and passes now, using pseudocode.

## Merge Danger

Whether the change is a one-way or a two-way door: a change that is cheap to
roll back is a two-way door; destructive or hard-to-reverse changes are
one-way doors. The blast radius is the potential impact of the change:
breakages for consumers, data migrations, behavior others depend on.
