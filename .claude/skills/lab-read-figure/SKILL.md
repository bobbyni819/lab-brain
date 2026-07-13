---
name: lab-read-figure
description: Read a figure panel-by-panel and extract the quantitative values/trends — including the ones that live ONLY in the figure and never appear in the text — then verify each (two-tier, crop always shown) and write to the KB with provenance. Use when the user says "read this figure", "lab-read-figure", "extract the values from figure X", or points at an OA paper to mine its panels.
---

# /lab-read-figure — panel-level value extraction + verification

The showcased capability: pull a number/trend out of a figure panel that the paper's
text never states, and either **verify** it or honestly flag it **needs-review** —
with the panel crop always shown as provenance.

## Do this
1. Resolve the paper (DOI/URL) and confirm it is open-access with a fetchable license
   (CC-BY / CC0). Refuse otherwise — never fetch what we don't have rights to.
2. Run the pipeline (the `labbrain` package does this end to end):
   ```
   python -m labbrain.slice --paper <key> --provider <auto|hostllm|fixture> \
          --vault <kb-vault> --report <out.html>
   ```
   - `fetch` (license-gated) → `render` page (~220 DPI) → `crop` the panel →
     `extract` (blind panel read via the vision provider) → `verify` (D5) →
     `vault` (write record + copy crop) → `report` (per-run HTML).
   - **Provider seam:** under **Claude Science** use `hostllm` (its state-of-the-art
     figure reading); locally with an API key use `anthropic`; with neither use
     `fixture` (deterministic, for tests/demos). Advanced multi-panel auto-segmentation
     and supplementary-info reading are Claude-Science-lane roadmap items.
3. **Verification (D5, two-tier, deterministic — never trust a model self-verdict):**
   - `verified` = chart type in scope + value consistent with axis + no text
     contradiction + confidence not low + no hard flag (e.g. broken axis).
   - `needs_review` = anything else (out-of-axis, low confidence, broken/log axis,
     or a text↔figure disagreement). The crop is kept regardless.
4. **Scope (D3):** bar/box, dose-response, Kaplan-Meier, simple kinetics read
   confidently. Heatmaps and dense montages are flagged, never silently guessed.

## The payoff to show
On a real OA paper, the text may state only a couple of magnitudes while every other
value lives in the figures. `/lab-read-figure` recovers the figure-only numbers and
catches text↔figure disagreements a skimming reader misses.

## Output
- KB records under `<vault>/papers/*.md` (values table + verdict + embedded crop + DOI)
- a self-contained HTML report of the run (`/lab-report` renders the project-level view)
