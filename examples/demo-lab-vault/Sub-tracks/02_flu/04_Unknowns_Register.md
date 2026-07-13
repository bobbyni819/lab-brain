---
title: "Unknowns Register — 02_flu (Alex)"
type: unknowns-register
status: "Living doc, edited by BOTH Alex and Sam. Turn tacit knowledge into written knowledge."
updated: 2026-07-13
---

# Unknowns Register — flu cytokine panel reading

## Known knowns
- Fig 5 uses 2^-ΔΔCt fold-change normalized to β-actin, calibrated to the infected control. `[mentor]`
- Bar-chart panels at ~220 DPI read reliably (proven on 5b). `[mentor]`

## Known unknowns
- [ ] Does the IL-6 figure/text discrepancy come from a different calibrator? `[for alex]`
- [ ] What's the right bbox for 5c (IL-2) — the legend overlaps the top-right. `[for alex]`

## Unknown knowns — the mentor's tacit knowledge, not yet written
<!-- Sam fills these as they come up in conversation; each moves to a Wiki page once written. -->
- "A broken y-axis (like Fig 4) always means read the upper segment with lower confidence — flag it." `[mentor]`
- "If the text only states one or two magnitudes, assume the rest are figure-only — that's the whole point." `[mentor]`

## Unknown unknowns — blind spots to go find
- Are any panels log-scaled? (would change how we read tick spacing) `[for alex]`

## Questions to extract the mentor's tacit knowledge (ask these)
- "What would you check first if a panel read looked off?"
- "When is a discrepancy worth chasing vs. just flagging?"

## Deliberate blind-spot passes to run before each build
- [ ] Confirm the y-axis is linear and un-broken before trusting a peak value.
- [ ] Confirm which series (infected vs treated vs uninfected) each bar colour is.
