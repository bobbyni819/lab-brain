# Figures & findings — make it once, verify by looking, log what it shows

Generalized from a lab's real, battle-tested figure system. Two ideas run through all of it:
**a figure is regenerable code, not a hand-edited picture**, and **you don't trust a figure until
you've looked at it**.

## The core operating rule: restyle, never reinvent; verify by looking
When a figure needs to change, do **not** invent a new one — restyle the real one:
1. **Locate the real generating script** (it lives with the figures; find it, don't guess).
2. **Confirm data fidelity:** the script reads its real result file and checks the headline number
   *before* plotting — **no hard-coded values** — and writes a `.manifest.json` sidecar recording
   its data source. Every figure must be **regenerable from its script** (no manual pixel edits).
3. **Apply the house conventions** (below).
4. **Render.**
5. **VERIFY IT YOURSELF** — downscale the PNG to ≤1600px and *look at it* (multimodal read-back).
   Iterate render → look until it's clean. This is non-negotiable; a figure is not done until a
   reader (you) has confirmed it says what it should.
6. **Archive, don't delete** — copy the old PNG to a timestamped `_archive/` before replacing.
7. **Update the trackers** (figure registry / findings / roadmap) and **commit on a branch** (no
   push unless asked).

## House visual rules (the defaults; a project can override the *guidance* ones, not the correctness ones)
- **One standalone plot per figure** — so a panel can be placed individually in a deck. Don't merge
  separate plots into one image.
- **No gridlines. No overlapping elements. No text baked onto the plot body** — panel letters (A/B/C)
  and titles are added as slide/text-box overlays, not rendered into the PNG. Export a
  labels-stripped "main" PNG (for the deck) **and** a composite (everything, for the doc).
- **Type & line:** fonts as large as possible without overlap (print spec ≤7pt final, nothing below
  5pt, a clean sans); thin lines (~0.5pt); no top/right spines.
- **Locked colour scheme:** grey by default; colour *only* encodes sign, a second axis, or tracking
  one entity across panels — **never decoration**. Signed heatmaps use a diverging map centred at 0
  (red = +, blue = −); cluster with dendrograms only when clustering is the point.
- **Same colour = same entity across every panel.**
- **Output set per figure:** vector PDF (submission master) + editable SVG (`svg.fonttype='none'`) +
  300-dpi PNG + a JSON provenance sidecar. Export **each subpanel as its own file** so panels can be
  grouped/placed late.
- **Routing:** figures + scripts live in the **repo** (`figures/`, `panels/`, `scripts/`); captions
  and tracking live in the **KB**. (Figures are code output; captions are knowledge.)

## The three tiers (how the work is structured — the adoptable architecture)
- **Inner — one plot, correct & legible.** Split the rules into **correctness** (bind always:
  reads real data, axis labels with units, no baked title, legible) vs **guidance** (overridable
  defaults: palette, spacing). Finish with a render-then-verify QA loop: a *geometric* bbox-collision
  check (deterministic code) **and** a *perceptual* crop-and-look at each panel.
- **Middle — compose one multi-panel figure.** Outline on a 12-column grid (panel *a* = hook /
  schematic full-width; *b* = the one panel that alone makes the claim true; the rest = evidence),
  fan out **one sub-agent per panel**, tile + stamp bold letters, then an **adversarial composite
  review** (outline-level revisions vs per-panel violations), regenerating **only** the affected
  panels — *don't regenerate clean panels; that invites regression.* ≤3 rounds.
- **Outer — the paper narrative** decides which figures exist at all (see
  [storyline-and-manuscript](./storyline-and-manuscript.md)).

## Self-review: the skeptical first-time reader
Beyond the per-figure read-back, run an adversarial audit before the PI sees it: read all the text,
**visually read EVERY figure** in ≤1600px batches, and write numbered, file-grounded catches
(cross-panel contradictions, over-claims vs. the actual effect size, label-on-data, illegibility,
duplication). Emit a **dated audit doc** with a per-item status (`🔴 open · ✅ fixed · 🟢 checked-fine`),
then iterate-fix. The mechanical guarantees (dpi, min font, no baked titles) are owned by a
deterministic QA gate; the judgment calls (the one message, the claim wording, the squint test) are
owned by the reviewer. **The gate is the floor; the reviewer is the ceiling.**

## `FIGURE_FINDINGS.md` — logging what each figure *shows* (not just that it exists)
A findings log, appended per work session, kept next to the figure scripts. One block per panel
(update in place if the heading exists — never duplicate):
```markdown
## Panel X: Title
**Method:** brief description of the analysis
**Data:** #regions / windows / samples used
**Key findings:**
- finding with specific numbers (rho, p, counts)
- finding with biological interpretation
**Cross-reference:** how this relates to other panels
```
For every new/updated figure, answer four fixed questions: *what does it show (1 sentence) · key
quantitative results · interpretation · cross-references (supports/contradicts which panels).* Always
refresh the **Cross-Figure Synthesis** block at the bottom (convergence, contradictions, open
questions, follow-ups) after updating individual panels. Template:
[`templates/FIGURE_FINDINGS.md`](./templates/FIGURE_FINDINGS.md).

## Captions are CLAIMS, not labels
The load-bearing caption rule: **every figure has ONE message; the legend states it.**
- Bad: *"Graph of infiltration over time."* Good: a sentence stating the **direction and the number**.
  A reader seeing only the title should know what the panel shows.
- Caption body: first sentence = what it shows; then precise methods (n=, test, correction,
  threshold); then one sentence of the key result. **No subjective words** — replace "strong" with the
  ρ, "many" with the count. Define abbreviations on first use; keep terminology consistent across
  captions; cross-reference related panels; **don't interpret beyond the data**; mark unvalidated
  findings `(provisional)`.
- Keep two levels: a ~150–200-word on-image caption and a ~400–600-word detailed version (adds
  methods, cross-panel links, likely reviewer questions).
- **Citation integrity gate:** every number traceable to a specific data file/query; every citation
  verified (a verbatim full-text quote for any quantitative claim); zero unverified citations before
  submission.

See [storyline-and-manuscript](./storyline-and-manuscript.md) for how figures assemble into the
paper's argument, and [documentation-and-handoffs](./documentation-and-handoffs.md) for the
figure ↔ storyline lane split that keeps two people (or two chats) from clobbering each other.
