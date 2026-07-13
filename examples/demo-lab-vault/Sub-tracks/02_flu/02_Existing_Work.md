# 02 · Existing work (build on this — don't reinvent)

Before you write anything, know what already exists.

- **The `labbrain` slice** (`python -m labbrain.slice`) already does fetch → render → crop → extract →
  verify → vault → report. **Use it**; don't rebuild the pipeline. Your `scripts/read_panels.py` is a
  thin wrapper.
- **`papers.yaml`** holds the per-panel config (figure, panel, page, bbox, series). Add panels here,
  not in code.
- **The D5 verify gate** (`verify.py`) already decides `verified` vs `needs-review` — read it so you
  know why IL-6 flags.
- **The reference reads:** Fig 5b TNF-α = 29-fold (verified); IL-6 ≈ 500 vs text 5.6 (needs-review).
  Reproduce these first (phase 1 gate) before extending.

Restyle/reuse before reinventing; archive, don't delete.
