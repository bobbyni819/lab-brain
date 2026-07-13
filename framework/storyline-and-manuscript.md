# Storyline & manuscript — the narrative drives the figures, not the other way around

Generalized from a lab's real manuscript workflow. The discipline: **start from the messages, let
the figures follow**, and track the figure ↔ storyline ↔ prose linkage explicitly so nothing drifts.

## Story-first selection discipline
- **Key messages first → figures follow.** The narrative arc is
  **problem → hypothesis / innovation → approach → results → impact**. Filter *every* candidate panel
  against that arc; if it doesn't advance the argument, it moves to the supplement.
- Sketch on paper/whiteboard **before** software. Revise a figure like prose.
- Two editorial reflexes on every claim: the **innovation formula** — *"Currently X / the limitation
  is Y / we overcome it by Z"* — and a **"So what?" pass**. Lead each section with the
  **known-vs-unknown gap**; one reference per statement; state limitations explicitly; active voice.

## The paper-narrative pass (run before composing figures)
Derive a **paper brief** (pitch, vision, audience, most-arresting asset, per-figure claims), then run
a **handling-editor review** that returns:
- a **hook verdict** — *"would Figure 1 make me send this out for review?"*
- the **arc** (hook → mechanism → evidence → application),
- **figure moves** (panels sitting in the wrong figure), **missing panels** (analyses still to run),
  a **kill list**, and the **boldest defensible Figure 1**.

Iterate — hand each figure's claim to the figure composer and re-run — until the hook verdict is
"yes" and there are no outstanding moves or missing panels. **Figure 1 renders the paper's
one-sentence pitch as data;** the later figures cover mechanism, evidence, robustness, application.

## The storyline doc (one per main figure, dated)
`storyline-figure-<N>-YYYY-MM-DD.md` with a fixed skeleton (template:
[`templates/storyline-figure.md`](./templates/storyline-figure.md)):
```markdown
## 🟢 Thesis in one breath          ← 1–3 dead-simple sentences: the figure's whole point
## Canonical panel map               ← a table of what the real figure currently is
## ⭐ The N panels
### **NA — <claim-form panel title>** *(¶n)*
  <plain description> + ![[panel.png|width]]
  > 📖 **Beat:** why this panel earns its place in the argument (+ which supplements back it)
  ⚠️ Status/Gap · 🔧 Method note
## What moved OUT of the canonical figure   ← demotions to supplement, with reasons
## Old-draft → canonical letter map          ← cross-ref table as panels get relettered
## Gaps / to-build before the figure is complete
```
The **Beat** line is the load-bearing part: every panel must justify its place in the *argument*,
not just exist.

## The figure-narrative skeleton (the bridge to prose)
Between the storyline and the written Results, keep a compact skeleton:
```markdown
## Paper arc (one breath)
### Figure N
**MESSAGE:** one claim-sentence for the whole figure
**Subpanels:**
- a — …
- b — …
**Reference hooks (verify):** …
```
"A message per figure, a bullet per subpanel." This is what gets fleshed into
`Output/manuscript-<section>.md` files (YAML frontmatter tracks `findings_used`,
`citations_verified`, `status: DRAFT`).

## Only robust findings earn a place
Findings that feed the storyline are graded first by a multi-agent reasoning pass
(Data Analyst → Domain Expert → Methods Critic → Synthesizer) into
`ROBUST / NEEDS_VALIDATION / WEAK / UNSUPPORTED`. The Synthesizer proposes the narrative arc (lead /
supporting / independent findings + a one-sentence thesis). **Only ROBUST findings (or explicitly
caveated NEEDS_VALIDATION) are allowed into the manuscript** — the storyline can't be built on sand.

## Keeping figure ↔ storyline ↔ prose in sync
Track the linkage with a few small registries (names are illustrative): a per-panel **build
manifest**, a **figure → storyline map** (with images embedded), a **figure registry** (owner +
source per figure), and a **figure-locations index** (path per figure). Main-vs-supplement split:
keep a main figure to a sane subpanel budget, keep a "probably cut, but show the PI" bucket, and
**the author owns the final split** — the tools propose with rationale.

## The two-lane split that makes this clobber-proof
Figure work and storyline work run as **separate lanes** (often separate chats or people) so they
never write the same file at once:
- **Figures lane** owns the repo (scripts, generated figures), the figure registry, per-figure
  write-ups, and `_Log.md`.
- **Storyline lane** owns the narrative docs (`storyline-figure-*`), the layout/deck, and the
  storyline visualization.
- **The author** owns the decisions (panel budget, cuts).
- A shared **coordination board** carries a **🔒 ACTIVE EDITS** check-out (claim a shared file before
  editing; 30-min stale-lock takeover) and a **🤝 OPEN HANDOFFS** section; each lane keeps its own
  **single-writer** `progress-<lane>.md` (one writes, the other only reads) — *zero shared-write =
  clobber-proof.* Full convention: [documentation-and-handoffs](./documentation-and-handoffs.md).

**Standing rule across both lanes:** *archive, don't delete; keep all views in sync.* After you fix a
figure, refresh **every** copy (vault embed, deck, exported PDF) — a stale same-named duplicate
silently shadows the update — and commit only once the views match the source.
