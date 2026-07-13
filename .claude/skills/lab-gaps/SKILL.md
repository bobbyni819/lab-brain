---
name: lab-gaps
description: Audit the lab brain for risk — undocumented code, orphaned datasets, stale/duplicate docs, figures with no generating script, projects with no entrypoint, single-owner bus-factor risks, and text↔figure disagreements. The "what a new member should fix first" list. Use after /lab-link or when the user says "lab-gaps", "audit", "what's missing", "what's risky".
---

# /lab-gaps — audit & risk surface

The PI/newcomer's punch list. Reads the assembled registry and flags what's fragile.

## Flags
- **Undocumented code** — modules with no README / no docstring / no tests.
- **Orphaned datasets** — data no artifact references; **figures with no generating script.**
- **Stale / duplicate** docs (by mtime + content hash from /lab-scan).
- **No entrypoint** — projects where nothing says how to actually run them.
- **Bus-factor** — artifacts/projects with a single owner (knowledge concentration risk).
- **Text↔figure disagreements** — a stated number that contradicts a figure value
  (surfaced by `/lab-read-figure` verification).

## Output
`GAPS_REPORT.md` — ranked, each item linking to the artifact and (where relevant) the
person who owns it. This is the concrete "start here to reduce risk" list a new member
or PI acts on. Feeds the `pi`-role view and each project rollup's `open_gaps`.
