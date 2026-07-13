---
title: "Which cytokine values live ONLY in the figures?"
created: 2026-07-13
updated: 2026-07-13
tags: [exploration, influenza, cytokines, figure-reading]
status: COMPLETE
---

# Cytokine values that exist only in the figures

A query filed back so it doesn't vanish into chat. Question: of the fold-change magnitudes in Gui
2017, which are stated in the **text** vs recoverable only from the **figures**?

## Answer
The text states only **two** magnitudes: IL-6 "up to 5.6 fold" and VDR "≈2.5-fold". Everything
else — all of TNF-α, IL-2, IL-4, IFN-β, and the full day-2/4/6/8 time course — appears **only in the
figure panels**. A grep of the full text for `29`, `55`, `210`, `500` returns zero hits.

| Value | Source | Verdict |
|---|---|---|
| TNF-α = 29-fold @ day 2 | Fig 5b (figure-only) | verified |
| IFN-β ≈ 55-fold @ day 4 | Fig 5e (figure-only) | provisional |
| IL-6 ≈ 500-fold @ day 4 | Fig 5a | ⚠️ vs text "5.6 fold" |

## So what
Reading the paper's text gives you almost none of its quantitative content. Reading the *figures*
does. That's the whole reason the lab reads panels — and why every figure value is logged with its
crop as provenance.

## Related
- [[FIGURE_FINDINGS]] · [[Wiki/Concepts/h9n2-hyperinflammation]] · [[Sources/Articles/Gui_2017_calcitriol-h9n2-inflammation]]
