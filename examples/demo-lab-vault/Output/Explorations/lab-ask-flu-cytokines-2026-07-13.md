---
title: "/lab-ask — what does the flu project know about cytokine timing?"
created: 2026-07-13
tags: [exploration, lab-ask, influenza, cytokines]
status: COMPLETE
---

# /lab-ask "what does the flu project know about cytokine timing, and where did the numbers come from?"

> A newcomer's day-one question, answered grounded in the vault with citations. Filed back so it
> compounds (see `framework/documentation-and-handoffs.md`).

## Answer (every claim cited)
H9N2 infection drives **two temporally distinct cytokine waves** in the lung:

- An **early pro-inflammatory spike at day 2** — TNF-α peaks at **29-fold**
  ([[FIGURE_FINDINGS#Panel 5b]]), alongside IL-2, IL-4, and IL-6. This is the "cytokine storm"
  character ([[Wiki/Concepts/h9n2-hyperinflammation]]).
- A **delayed antiviral response at day 4** — IFN-β peaks ~55-fold, later than the pro-inflammatory
  cytokines ([[Wiki/Concepts/h9n2-hyperinflammation]]).

**Where the numbers came from:** they are **figure-derived** — the paper's *text* states only IL-6
"up to 5.6 fold" and VDR "≈2.5-fold" ([[Sources/Articles/Gui_2017_calcitriol-h9n2-inflammation#Verified Claims]]);
every other magnitude exists only in Fig 5's panels ([[Output/Explorations/cytokine-figure-only-values]]).
One value is **flagged, not trusted**: IL-6 reads ~500-fold in the figure but 5.6-fold in the text —
a text↔figure discrepancy kept as `needs-review` with the crop ([[FIGURE_FINDINGS#Panel 5a]]).

## Provenance
Answer synthesized from: [[FIGURE_FINDINGS]] · [[Wiki/Concepts/h9n2-hyperinflammation]] ·
[[Sources/Articles/Gui_2017_calcitriol-h9n2-inflammation]] (Gui et al. 2017, Virology Journal, CC-BY).
Every figure value links to its panel crop under `_labbrain/crops/`.
