---
title: "START HERE — 02_flu (Alex)"
type: sub-track-entry
person: Alex Rivera
mentor: Sam Ortiz
updated: 2026-07-13
---

# START HERE — flu cytokine panel reading

## In 60 seconds
The H9N2 flu papers report cytokine dynamics, but the real fold-change numbers live in the figure
panels, not the text. Your track: reliably extract and **verify** those per-panel values (bar
charts, days 2–8) and log what each panel shows — so the lab can trust figure-derived numbers. "Done"
= every value traceable to its panel crop, verified or honestly flagged.

## What you own
- A reproducible pipeline that turns a figure panel into a verified, provenance-tracked value + a
  `FIGURE_FINDINGS` entry.

## Deferred — do not build  (out of scope on purpose)
- Multi-panel **auto-segmentation** — that's a Claude-Science-lane research item, not week 1.
- Any change to the shared `labbrain` package — you *use* it; you don't fork it.
- Fetching non-open-access papers.

## The plan & supervision gates
| Phase | You produce | Gate (mentor reviews) | Decisions that need the mentor |
|---|---|---|---|
| 1 · reproduce | TNF-α (5b) read matching the reference | the value + the crop | — |
| 2 · scale | 5a, 5c–e read from a **config**, not hardcoded | `papers.yaml` + FIGURE_FINDINGS | which cytokines make the main figure |
| 3 · verify | a `needs-review` flag on any text↔figure clash | the verification notes | how to resolve the IL-6 discrepancy |

Decisions **yours to make**: bbox values, code structure, which panels to read first.
Decisions that **need the mentor**: main-figure panel budget, how to report the IL-6 discrepancy.

## How to work (the method)
1. Read one panel; **look at the crop yourself** before trusting the number.
2. Log it in `Day<N>_log.md` (3–5 bullets); drop questions in `questions.md`.
3. Bring the gate artifact to Thursday's check-in. Restyle/reuse before reinventing; archive, don't delete.

## Reading order
1. `01_Your_Sub_Track.md` · 2. `02_Existing_Work.md` (the labbrain slice) · 3. `03_Multi_Week_Plan.md` ·
4. `04_Unknowns_Register.md` (add your questions) · 5. the project `START_HERE.md` + the framework.
