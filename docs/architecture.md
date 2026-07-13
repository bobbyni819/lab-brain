# Architecture

Lab Brain has three layers: an **onboarding pipeline** (skills), a **collaboration model**
(conventions), and a **figure-reading capability** (the `labbrain` Python package). All three
read from one place — `lab-profile.yaml` — so a new lab configures everything by editing one file.

```
                       lab-profile.yaml  (storage · naming · ROSTER+roles · vocabulary · privacy)
                                 │
        ┌────────────────────────┼────────────────────────┐
        ▼                        ▼                         ▼
  ONBOARDING PIPELINE      THE FRAMEWORK             FIGURE READING
  (.claude/skills)         (framework/)              (src/labbrain)
  /lab-init → scan →       KB structure · naming ·   fetch → render → crop →
  triage → index →         doc-routing · figures ·   extract(provider) →
  link → ask → standup     storyline · mentorship    verify(D5) → vault → report
```

## 1 · The onboarding pipeline (cheap-structural → expensive-semantic, human-gated)
Eight re-runnable, idempotent slash commands, staged by cost so an expensive crawl never runs
before a human approves the plan:

`/lab-init` (configure) → `/lab-scan` (structural manifest, no LLM) → `/lab-triage` (rank +
read-tier) → `/lab-index` (the swarm) → `/lab-link` (assemble the cited vault + graph) →
`/lab-ask` (grounded retrieval) → `/lab-standup` (team synthesis) → `/lab-update` (incremental
re-sync). See each skill's `SKILL.md`.

**Runnable today:** `/lab-scan` is backed by `src/labbrain/lab_scan.py` — a deterministic,
offline module (`python -m labbrain.lab_scan --root <dir>`) that emits `manifest.jsonl` +
`SCAN_REPORT.md` (areas, projects, duplicate groups, stale files) with no LLM. The figure-reading
capability below is likewise fully runnable. The remaining steps orchestrate agents through the
skills.

### The swarm (scales agents to the corpus)
`/lab-index` spawns one **specialist reader per content area** (code, slides, lit, docs, data,
comms, grants, media), and within an area `W = clamp(ceil(files_at_tier / files_per_worker), 1,
max_workers)` concurrent workers. Concurrency is bounded three ways — triage tiers, a per-run
`max_full_reads`, and host batch concurrency — so it never runs away. The live worker count is
reported and rendered in the report's swarm panel.

### The 4-layer deep read + quality gate (proof it isn't skimming)
Per file: **(0)** transcribe binary → complete text/tables/rendered-images (no LLM); **(1)**
semantic read → structured record; **(2)** an **independent grader** scores the record vs. the
transcript on coverage / specificity / faithfulness; **(3)** the verdict is computed
**deterministically in code** (`accept` iff coverage≥75 ∧ specificity≥70 ∧ faithfulness≥90),
and a sub-threshold read is re-read — for papers/slides by feeding the rendered figures to a
vision pass — then re-graded. The reader never grades itself.

## 2 · The framework — the conventions (the hero)
The heart of Lab Brain is `framework/` — a set of adoptable conventions generalized from a system a
real lab already runs. It answers, by default, *where does everything go*: files (three-layer
Sources / Wiki / Output + a filing rule), updates/handoffs/decisions (`START_HERE.md` daily-brief,
`_Log.md`, `_handoff-log.md`), figures (restyle-not-reinvent + verify-by-looking + `FIGURE_FINDINGS.md`),
the manuscript storyline (messages-first, per-panel "beats"), and mentorship (a paired-by-date
check-in loop: a neutral `-update.md` + a structured `-feedback.md`, with mentee scaffolding). Two
harnesses coordinate through the KB with one hard rule: **one harness owns a working-dir at a time.**
The roster's per-member role (`pi`/`mentor`/`maintainer`/`mentee`) selects scaffolding and the
report-up path. Full detail: [`../framework/README.md`](../framework/README.md).

## 3 · The figure-reading capability (`src/labbrain`)
A tight, offline-first pipeline, one module per stage:

| Module | Responsibility |
|---|---|
| `fetch.py` | resolve an OA paper (registry in `papers.yaml`) and download it — **license-gated** (CC-BY/CC0 only) |
| `render.py` | PDF page → PNG at ~220 DPI (pypdfium2) |
| `crop.py` | crop a panel by fractional bbox (v1 uses configured boxes; auto-segmentation is roadmap) |
| `providers.py` | the **vision seam**: `FixtureProvider` (offline/CI), `HostLLMProvider` (Claude Science), `AnthropicProvider` (API) behind one Protocol |
| `extract.py` | delegate to the provider; coerce/validate the payload |
| `verify.py` | the **D5 two-tier gate**, computed deterministically (never a model self-verdict) |
| `vault.py` | write an Obsidian record (values + verdict + embedded crop + DOI) and upsert the index |
| `report.py` | a self-contained HTML+SVG per-run report |
| `slice.py` | the end-to-end CLI |

### The provider seam
The one design decision that lets the same code run anywhere: every module talks to a
`VisionProvider` Protocol, so figure reading runs under Claude Science's `host.llm` (the demo
runtime), the Anthropic API, or a deterministic fixture (tests/offline) — nothing else changes.

### D5 verification (two-tier, crop always kept)
`verified` iff the chart type is in scope (bar/box/dose-response/KM/kinetics) **and** the peak is
within the axis (2% slack) **and** confidence isn't low **and** there is no text↔figure
contradiction **and** no hard flag (e.g. broken axis). Anything else is `needs_review`, with
explicit reasons. The panel crop is retained on every record, verified or not — provenance with
honesty beats false certainty.

## Grounding
The whole design is grounded in Bobby's own KB practice; see the project design notes
(`decisions-locked` D1–D5, `agent-orchestration`, `deep-reading-and-quality-gates`,
`paper-reading-design`, `multi-user-collaboration-design`) in the hackathon knowledge base.
