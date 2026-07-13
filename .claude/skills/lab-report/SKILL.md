---
name: lab-report
description: Render a self-contained, visual HTML report of a Lab Brain run — the swarm (how many agents ran, across which areas), what was read, the figure panels with extracted values + verification badges, and provenance chains. Use when the user says "lab-report", "show me the report", "generate the visual summary", or wants to see the system's work at a glance.
---

# /lab-report — the visual system report

Turn a run into something a human (or a judge, or a PI) can see at a glance. This is
the artifact that shows every feature: that it read semantically, how many agents ran,
whether they scaled to the corpus, and every figure value with its verification + crop.

## Do this
1. Gather the run's records (`registry/artifacts/*.json` and/or the figure records
   under `<vault>/papers/`) + run metadata (paper(s), provider, worker counts by area).
2. Build a **single self-contained HTML file** (inline CSS, images as base64 data URIs,
   no external assets — portable + theme-aware + responsive):
   - Header: what was processed, #files/#panels, #verified vs #needs-review, providers.
   - **Swarm panel:** the live agent count and its breakdown by content area — the
     "scales dynamically" story, on screen.
   - **Pipeline strip** (inline SVG): fetch → render → crop → extract → verify → vault.
   - **Per-panel cards:** the crop, chart type, values table, peak, a VERIFIED /
     NEEDS-REVIEW badge, confidence, provenance (DOI/license/figure/panel), and any
     text↔figure note.
   - **Provenance:** clicking a claim reveals the artifact (and panel crop) it came from.
3. For the per-run figure view, `labbrain.report.build_report(...)` already emits this;
   use it, or extend it for a project-level view.

## Output
`lab_brain_report.html` (or the run's report path) — open it, or attach it. Self-contained,
so it travels (email, submission, a walk-through video).
