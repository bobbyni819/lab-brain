# Figure findings — flu-host-response

> What each panel SHOWS. Source: Gui et al. 2017, *Virology Journal* (CC-BY), Fig 5 (qPCR cytokine
> fold-changes in H9N2-infected mouse lung). See `framework/figures-and-findings.md`.

## Panel 5b: TNF-α spikes early, then returns to baseline
**Method:** qPCR relative quantification (2^-ΔΔCt), normalized to β-actin, calibrated to infected control.
**Data:** 3 groups (infected control, calcitriol-treated, uninfected) × days 2/4/6/8 post-infection.
**Key findings:**
- Infected-control TNF-α peaks at **29-fold at day 2**, then drops to ~0.5–2 fold by days 4–8.
- Calcitriol-treated ~16-fold at day 2 (lower early response).
- **VERIFIED** — value within axis (0–35), clean panel, no text contradiction.
**Cross-reference:** same day-2 spike pattern as IL-2 (5c) and IL-4 (5d); contrast with IFN-β (5e), which peaks day 4.

## Panel 5a: IL-6 — figure ≈ 500-fold vs text "5.6 fold"  ⚠️ NEEDS-REVIEW
**Method:** as above.
**Data:** as above; y-axis 0–600 fold.
**Key findings:**
- Calcitriol-treated IL-6 peaks near **500-fold at day 4**; infected-control ~205-fold at day 2.
- **NEEDS-REVIEW** — the paper's text states IL-6 "upregulated up to 5.6 fold"; the figure shows ~500.
  Almost certainly a normalization/baseline difference, but it's a genuine text↔figure discrepancy a
  skimming reader would miss. Crop retained.
**Cross-reference:** the discrepancy is the reason we log figure-only values (see Output/Explorations).

## Panel 5e: IFN-β — delayed peak (day 4)  [pending mentee read]
**Method:** as above.
**Data:** y-axis 0–70 fold; busiest panel.
**Key findings:**
- Infected-control IFN-β peaks ~55-fold at day 4 (later than the pro-inflammatory cytokines). *(provisional — @AR to confirm 5c–d then re-read 5e)*
**Cross-reference:** the delayed antiviral response vs early pro-inflammatory spike is the story's core contrast.

---

## Cross-Figure Synthesis
- **Convergence:** pro-inflammatory cytokines (TNF-α, IL-2, IL-4) peak day 2; the antiviral IFN-β peaks day 4 — a consistent early-vs-late split.
- **Contradictions:** IL-6 figure (~500) vs text (5.6) — flagged, unresolved (normalization?).
- **Open questions:** does calcitriol's blunting of the early spike explain the later worsened pathology?
- **High-priority follow-ups:** @AR reads 5c–d (IL-2, IL-4); confirm 5e; decide main-figure panel budget.
