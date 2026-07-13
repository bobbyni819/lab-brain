---
name: lab-storyline
description: Build the manuscript's narrative the lab way — messages first, figures follow. Derives the paper arc + hook, writes the per-figure storyline doc (thesis in one breath → panel beats → what moved out → gaps), and keeps figure↔storyline↔prose in sync. Use when the user says "lab-storyline", "build the narrative", "what's figure N's story", "storyboard the paper".
---

# /lab-storyline — the narrative drives the figures

Start from the messages; let the figures follow. Convention:
`framework/storyline-and-manuscript.md`; template: `framework/templates/storyline-figure.md`.

## Do this
1. **Derive the paper arc** (problem → hypothesis/innovation → approach → results → impact) and a
   **paper brief** (pitch, audience, most-arresting asset, per-figure claim).
2. **Handling-editor pass:** ask "would Figure 1 make me send this out for review?" Return the arc,
   any **figure moves** (panels in the wrong figure), **missing panels** (analyses to run), a
   **kill list**, and the **boldest defensible Figure 1**. Iterate until the hook verdict is "yes".
3. **Write the storyline doc** per main figure — `storyline-figure-<N>-<date>.md`:
   `## 🟢 Thesis in one breath` → `## Canonical panel map` → `## ⭐ The panels` (each panel: plain
   description + embedded image + a `> 📖 Beat:` line justifying its place in the *argument* +
   status/gap flags) → `## What moved OUT` → `## Old-draft → canonical letter map` → `## Gaps to build`.
4. **Only robust findings** earn a place — findings graded WEAK/UNSUPPORTED don't enter the
   manuscript; NEEDS_VALIDATION enters only with an explicit caveat.
5. **Bridge to prose** with the figure-narrative skeleton (a `**MESSAGE:**` per figure + a bullet per
   subpanel + reference hooks), then flesh into `Output/manuscript-<section>.md`.
6. **Keep views in sync** — figure work and storyline work are separate lanes (see
   `framework/documentation-and-handoffs.md`); after any figure change, refresh every copy (vault
   embed, deck, PDF) — a stale same-named duplicate silently shadows the update.

## Output
- `storyline-figure-<N>-<date>.md` per main figure (the narrative + panel beats)
- a figure-narrative skeleton feeding `Output/manuscript-<section>.md`
