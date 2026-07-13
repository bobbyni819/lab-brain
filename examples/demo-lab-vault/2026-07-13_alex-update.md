---
title: "Update — Alex, 2026-07-13"
author: "agent (neutral digest)"
date: 2026-07-13
person: Alex Rivera
---

# Update — Alex, 2026-07-13

**Headline:** Alex set up the panel-reading pipeline and reproduced the TNF-α (5b) read; started on IL-2/IL-4.

## Per-piece breakdown
- **panel-read runner** — `Sub-tracks/02_flu/scripts/read_panels.py` (+82 lines) — wraps the labbrain slice; reads a configured bbox per panel and writes a record.
- **Fig 5b reproduction** — matched the reference: TNF-α infected-control = 29-fold @ day 2.
- **Day logs** — `Day1_log.md`, `Day2_log.md` present; questions.md has 2 open questions.

## Quality flags (neutral)
- bbox for 5c is hardcoded in the script (not yet in a config) — TODO left in the code.
- IFN-β (5e) not read yet; marked provisional in FIGURE_FINDINGS.

## Quotes worth preserving
> "the IL-6 panel doesn't match the abstract number — is that a normalization thing?" (questions.md)

## Files for the mentor to spot-check
- `Sub-tracks/02_flu/scripts/read_panels.py` — is the bbox approach OK, or should we auto-detect?
- `Sub-tracks/02_flu/04_Unknowns_Register.md` — Alex added 3 rows; two are `[for alex]`.

## Mapping to the last feedback round
- (first round — no prior feedback)
