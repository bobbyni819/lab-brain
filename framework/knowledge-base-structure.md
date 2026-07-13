# Knowledge-base structure — where each file lives

The vault has **three layers**. Keeping them separate is what makes a lab's brain trustworthy: you
always know whether a file is raw evidence, synthesized understanding, or private strategy.

## The three layers
1. **`Sources/` — raw material (immutable).** Papers, transcripts, data dumps, order records,
   vendor docs. The agents *read* these but never modify them. If it came from outside your own
   synthesis, it lives here.
2. **`Wiki/` — synthesized understanding (LLM-owned).** Summaries, concept pages, methodology
   SOPs, cross-references. The agents create and maintain this layer; humans read it. Everything
   here is derived from `Sources/` and links back to it.
3. **`Output/` — strategy & deliverables (private).** Plans with checkboxes, drafts to a PI,
   grant text, session reports, filed-back query results. Not shared with collaborators.

Plus the root landing files that make the vault navigable (see
[documentation-and-handoffs](./documentation-and-handoffs.md)):
`START_HERE.md` · `_Index.md` · `_Catalog.md` · `_Log.md`.

## The standard vault layout
```
<project>/
├── START_HERE.md        ← the daily brief — the first file everyone opens
├── _Index.md            ← main entry point / map (auto-maintained)
├── _Catalog.md          ← source inventory (auto-maintained)
├── _Log.md              ← chronological activity log (append-only)
├── _handoff-log.md      ← the live coordination board (claims + handoffs + progress)
├── LANES.md             ← who is working what, right now
├── Sources/             ← RAW, immutable
│   ├── Articles/        ← paper summaries (AuthorLastName_Year_short-title.md)
│   ├── Papers/          ← full-text markdown (for exact-quote verification)
│   ├── Notes/           ← analysis / verification / planning notes (subfolder by theme)
│   └── Assets/          ← figures, images, charts referenced by notes
├── Wiki/                ← SYNTHESIZED, LLM-owned
│   ├── Concepts/        ← one concept per page (biology / analysis)
│   ├── Methodology/     ← one pipeline/SOP per page (technical how-to)
│   └── Summaries/       ← cross-concept synthesis
└── Output/              ← STRATEGY, private
    ├── Plans/           ← action plans with [ ]/[x] checkboxes
    ├── Drafts/          ← messages to PI, grant text
    ├── Reports/         ← session summaries, status
    └── Explorations/    ← valuable query results, filed back so they don't vanish
```
Domain extensions are fine (an equities KB adds `Companies/`; a modeling KB adds `Sims/`) — the
three-layer spine stays.

## The filing decision rule (the most common mistake, prevented)
The #1 mis-file is putting LLM-written synthesis into `Sources/` (which is supposed to be raw). One
question settles it:

```
Did an agent WRITE this as synthesis / how-to / SOP / reference?
   yes → Wiki/     (Wiki/Methodology for technical how-to + SOPs; Wiki/Concepts for analysis/biology)
   no  → it's raw material from elsewhere → Sources/
             (transcripts, grant excerpts, raw data, order records, paper PDFs, vendor docs)
```
When a `Sources/` note grows into a maintained how-to, **move it to `Wiki/Methodology`** and update
inbound links. Raw evidence stays in `Sources/`; understanding lives in `Wiki/`.

## Why the separation pays off
- **Trust:** you can always tell evidence from interpretation.
- **Safe agents:** an agent can freely rewrite `Wiki/` (it owns it) and is forbidden to touch
  `Sources/` (immutable) — so automation never corrupts your evidence.
- **Provenance:** every `Wiki/` claim links to the `Sources/` file it came from — the same
  verify-and-cite ethic the figure reader uses on panels.

## Profiles (adapt the spine to the project type)
A KB declares a **profile** so structure and agent-orientation fit its type — e.g. `research`
(lab/PhD, the default above), `mentoring` (adds per-student sub-tracks), `modeling` (adds sims +
parameter audits). A profile is data (a small JSON), not a code change; it also carries a
**reading order** — the machine-readable contract for how a new session should orient to that KB.
Lab Brain ships the `research` spine; a lab picks or edits a profile in `lab-profile.yaml`.
