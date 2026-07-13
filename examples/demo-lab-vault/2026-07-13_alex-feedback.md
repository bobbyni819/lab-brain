---
title: "Feedback — Alex, 2026-07-13"
author: "Sam Ortiz (verbal feedback, captured by the agent)"
date: 2026-07-13
audience: Alex Rivera
---

← paired update: [[2026-07-13_alex-update]]

## In 30 seconds
Strong first week — you stood up the pipeline and reproduced the TNF-α read exactly, which is the
right way to build trust in the method before scaling. Two things to shift: first, get the panel
bounding boxes out of the script and into a config so the reads are reproducible and reviewable;
second, when a figure value disagrees with the text (your IL-6 catch — nice), that's not a bug to
fix, it's a *finding* to log and flag `needs-review`, keeping the crop. That instinct is exactly
what we want. Next: finish 5c–d, then re-read 5e, and bring the panel-budget question to Thursday's
check-in — that decision is mine, not yours to guess.

## TL;DR — the big shifts
1. Move panel bboxes from code → a per-paper config.
2. Treat text↔figure disagreements as findings (log + flag), never silently "correct" them.
3. Verify every read by *looking* at the crop before trusting the number.

> **The quality bar [Mentor]:** "I want to be able to click any number in the figure findings and
> land on the exact panel crop it came from. If I can't, it's not done."

## Part 1 — Reproducibility: config, not hardcoding
### Problem [Mentor]
"A bbox baked into the script means the next person can't see or change what you read."
### Fix
Add a `papers.yaml` entry per panel (figure, panel, page, bbox, series) and read from it.
### Quality gate [Mentor]
"Someone else can re-run your read from the config without opening the script."
### Precedents & tools
| Thing | Where it already lives | Use it for |
|---|---|---|
| `papers.yaml` schema | `../../papers.yaml` | the exact per-panel config pattern |
| the slice | `python -m labbrain.slice` | fetch→render→crop→extract→verify→vault |

## Part 2 — Text↔figure disagreements are findings
### Problem [Mentor]
"You almost 'fixed' the IL-6 number to match the abstract. Don't — the disagreement IS the result."
### Fix
Log both values, flag `needs-review`, keep the crop, note the likely cause (normalization).
### Quality gate [Mentor]
"The finding names both numbers and where the text one came from."

## Working prototype / current state
Pipeline runs; 5a/5b done; 5c–e pending. Config refactor not started. Unknowns Register seeded.

## Related files
- [[2026-07-13_alex-update]] — what shipped this round
- [[FIGURE_FINDINGS]] · [[Sub-tracks/02_flu/00_START_HERE]]

## Open questions for Alex
- Do you want to try caption-driven panel auto-detection next, or keep configured bboxes for now?
- *(and: push back on anything here that doesn't make sense.)*
