---
name: lab-figure
description: Make or restyle a publication figure the lab way — restyle the real generating script (never reinvent), enforce data fidelity (reads real data, no hard-coded numbers, writes a manifest), apply the house visual rules, then VERIFY IT YOURSELF by looking at the render. Use when the user says "lab-figure", "make/restyle this figure", "fix figure X", or points at a figure to iterate.
---

# /lab-figure — make it once, verify by looking

The lab's figure discipline: a figure is **regenerable code**, and you don't trust it until you've
**looked at it**. Full convention: `framework/figures-and-findings.md`.

## Do this
1. **Restyle, never reinvent.** Find the real generating **script** (it lives with the figures).
   Don't hand-draw a new one.
2. **Data-fidelity check:** the script must read its real result file and check the headline number
   *before* plotting — **no hard-coded values** — and write a `.manifest.json` recording its data
   source. The figure must be regenerable from the script alone.
3. **Apply the house rules:** one standalone plot per figure; no gridlines / no overlapping elements
   / no title or panel letter baked on the plot body (those are overlays); large legible type; thin
   lines; no top/right spines; grey by default, colour only encodes sign / 2nd axis / entity; same
   colour = same entity across panels. Export vector PDF + editable SVG + 300-dpi PNG + a JSON
   sidecar, and each subpanel as its own file.
4. **VERIFY IT YOURSELF** — downscale the PNG to ≤1600px and **Read it** (multimodal). Iterate
   render → look until it's clean. Run the QA checks: a geometric bbox-collision check and a
   per-panel crop-and-look.
5. **Archive, don't delete** — copy the old PNG to a timestamped `_archive/` before replacing.
6. **Log & commit:** add/update the panel's block in `FIGURE_FINDINGS.md` (via `/lab-findings`),
   refresh the figure registry, commit on a branch (no push unless asked). Figures + scripts live in
   the repo; captions/tracking live in the KB.

## When composing a MULTI-panel figure
Outline on a 12-column grid (a = hook, b = the panel that alone makes the claim, rest = evidence),
build one panel at a time, tile + stamp bold letters, then an adversarial composite review —
regenerate **only** the panels with issues (don't touch clean panels; that invites regression).

## Captions
Write the caption as a **CLAIM, not a label** — one message, the direction + the number. See
`/lab-findings` and `framework/figures-and-findings.md`.
