---
name: lab-findings
description: Log what each figure SHOWS (not just that it exists) into FIGURE_FINDINGS.md, and write captions as claims. Extracts per-panel method/data/key-findings/cross-references and refreshes the cross-figure synthesis. Use when the user says "lab-findings", "log the findings", "what do these figures show", or after generating/updating figures.
---

# /lab-findings — capture what the figures show

Figures are only useful if what they *show* is written down. This maintains `FIGURE_FINDINGS.md`
(next to the figure scripts) and keeps captions honest. Convention:
`framework/figures-and-findings.md`; template: `framework/templates/FIGURE_FINDINGS.md`.

## Do this
1. **Query the data FIRST** — for each figure, compute the real numbers (means, top pos/neg,
   significance/null context) *before* writing anything. Never describe a figure from memory.
2. For each new/updated panel, append/update its block (update in place if the heading exists —
   never duplicate):
   ```
   ## Panel X: <claim-form title>
   **Method:** <analysis in one line>
   **Data:** <#regions / windows / samples>
   **Key findings:**
   - <finding with specific numbers>
   - <finding with interpretation>
   **Cross-reference:** <supports/contradicts which panels>
   ```
   Answer the four fixed questions: what it shows (1 sentence) · key quantitative results ·
   interpretation · cross-references.
3. **Refresh the Cross-Figure Synthesis** block at the bottom every session (convergence,
   contradictions, open questions, high-priority follow-ups).
4. **Write/refresh the caption as a CLAIM, not a label** — one message, the direction + the number.
   Body: what it shows → precise methods (n=, test, correction) → one sentence of result. No
   subjective words (use the ρ, the count). Keep a ~150–200-word on-image caption and a ~400–600-word
   detailed version. Mark unvalidated findings `(provisional)`.
5. **Citation integrity:** every number traceable to a data file/query; every citation a verified
   verbatim quote; zero unverified citations before submission.

## Output
- updated `FIGURE_FINDINGS.md` (+ its Cross-Figure Synthesis)
- captions (two levels) in the KB `Output/figure-captions.md`
