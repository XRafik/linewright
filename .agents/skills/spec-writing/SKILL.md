---
name: spec-writing
description: Write a project's decisions into its specs as you design. Use when deciding what the software should do, or writing or editing a spec.
---

# Spec Writing

Write the project's decisions into its specs as you design, the moment they crystallise. The specs are live documents: they say what the software should do and why, and the code follows them.

## File structure

Most repos have a single context:

```
/
├── docs/
│   └── specs/
│       ├── product.md
│       └── architecture.md
└── src/
```

If a `SPEC-MAP.md` exists at the root, the repo has multiple contexts, each with specs of its own. The map points to where each one lives:

```
/
├── SPEC-MAP.md
├── docs/
│   └── specs/                        ← system-wide specs
└── src/
    ├── ordering/
    │   └── docs/specs/               ← context-specific specs
    └── billing/
        └── docs/specs/
```

Create files lazily: only when you have something to write. If no `docs/specs/` exists, create it when the first spec is written.

## During the session

### Challenge against the specs

When the user says something that conflicts with a decision already in the specs, call it out immediately. "Your spec says a shipped Order can't be cancelled, but you just said it can. Which is it?"

### Update the specs inline

When a decision is resolved, write it into the spec it belongs to right there. Don't batch these up: capture them as they happen.

The specs say what the software should do and why. How the code does it belongs in the code and its comments, not the specs.

### Write architectural decisions sparingly

Only write an architectural decision into the specs when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, leave it out.
