# Mentorship & collaboration — how a team contributes, and how mentees report up

Generalized from a program a real lab runs: a **PI → lead-mentor → students** chain (a 10-week
undergraduate research program), coordinated in one shared vault. The engine is a **paired-by-date
check-in loop** that keeps a neutral record of each person's work separate from the mentor's
evaluative feedback — so both compound over time and neither contaminates the other.

## Roles (what actually differs is *review direction* and *guidance intensity*)
The load-bearing distinction is **peer-maintainer vs. contribution**, not a rigid title:

| Role | What it means | How their work is treated |
|---|---|---|
| **pi** | faculty / group lead | reads the condensed team-meeting rollup; sets direction |
| **mentor** | runs the check-in loop (a PM / lead mentor for students) | writes the feedback, condenses for the PI |
| **maintainer** | a peer who owns and maintains a workstream | their commits are peer contributions — reviewed as an equal, no scaffolding |
| **mentee** | a student contributing under supervision | their branches are **contributions to review/merge, not a peer maintainer's**; gets scaffolding + a digest + feedback each round |

Guidance intensity is **set per person by how well-defined their problem is**, and stated
explicitly in their feedback ("rely more on your own judgment here — the direction isn't clear-cut").
An autonomous mentee runs on a **supervision-gate model**: a concrete artifact the mentor reviews
async before the next phase, with the plan flagging *which decisions are the mentee's to make* vs.
*which need the mentor's judgment* — so a mentor can be hands-off by design yet step in anytime.

## The check-in loop (the engine) — two paired, dated artifacts per round
Each round produces **two files, same date, in the person's sub-track folder**, and they stay
separate on purpose:

### 1. `<date>_<person>-update.md` — the NEUTRAL digest (agent-written)
- **One Explore agent per person, spawned in parallel.** Each reads only that person's recent work.
- **Inputs by source:** git-tracked people via `git log --author=<name> --since=<last-round>`;
  vault-based people via files modified since the last round. The **diff window = the date of their
  last feedback doc** (fallback: program start).
- **Neutral — no "the mentor should…".** It captures *what was done*, not what should change:
  `Headline → per-piece breakdown (paths + line counts + mechanism) → quality flags (TODOs,
  hardcoded values, placeholders) → 1–3 verbatim quotes worth preserving → **files for the mentor to
  spot-check** (the most important section) → mapping to the last feedback round (executed / partial
  / not addressed)`.
- Idempotent (re-running replaces the same-date file). Template: [`templates/update-PERSON.md`](./templates/update-PERSON.md).

### 2. `<date>_<person>-feedback.md` — the STRUCTURED feedback (mentor's voice, captured)
An **action-item doc derived from a check-in — not an onboarding package.** Its gold-standard
skeleton (template: [`templates/feedback-PERSON.md`](./templates/feedback-PERSON.md)):
- Front-matter → a one-line pointer to the paired update → **`## In 30 seconds`** (mandatory ~150–300
  words plain prose, so the main points are summarized up top) → **`## TL;DR`** = 2–3 imperative
  "big shifts" + a **`The quality bar [Mentor]:`** verbatim quote → **`## Part N`** per shift, each =
  `### Problem [Mentor]` / `### Fix` / `### Quality gate [Mentor]` (verbatim) / `### Precedents & tools`
  (a "don't reinvent — this already exists" table) / `### Concrete sequence` (numbered) → a
  paper-grade **quality-bar** section → **current state** (honest about gaps) → **Related files** →
  **Open questions for <person>**.
- **`[Mentor]` tags mark verbatim quotes ONLY** — never invented to sound on-voice. **Prose over
  tables** for narrative; tables only for state checklists, true comparisons, and the precedents list.
- **References** the paired update (in Related files) rather than re-describing what shipped.
- **Dated, never overwritten** — supersede a prior round with a forward-pointer, not an in-place edit
  (the dated trail *is* the value). Optional repo mirror to `<repo>/docs/onboarding/` when the person
  works from a repo (a second repo gets a one-line stub pointing at the canonical copy). Never pushed
  to a remote without explicit go-ahead.

### The source-of-truth chain (report-up path)
```
student's own writeup  →  neutral <date>_<person>-update.md  →  mentor <date>_<person>-feedback.md
                       →  condensed bullet in the shared team-meeting note (PI-readable, jargon-stripped)
```
Each stage is a different audience and a different voice; nothing is lost, nothing is duplicated.

## How a mentee documents their own work + surfaces it
- **Day/week logs** in their sub-track folder (`Day1_log.md`, `Week1_log.md`): 3–5 bullets, under
  5 minutes — what they did, read, blockers, next. Fine to draft with an LLM. Purpose stated plainly:
  *the mentor may not read these directly; they give the agents (and future-you) progress context* —
  which is exactly what the digest agent consumes.
- **`questions.md`** in their folder — an async channel the mentor checks between meetings.
- **Git commits** (committer = the student) for code tracks; the digest mines them by author + date.
- **The nav hub:** the vault's `START_HERE.md` carries a "current check-in round" table, one row per
  person, with a status flag (`🔴 not pulled · 🟡 needs feedback · 🟢 captured · ✅ closed`) and
  wikilinks to the update + feedback + their own outputs. Refreshed after every round.

## Scaffolding a mentee gets that a peer does not
- **Program onboarding sequence:** `Onboarding/00_Checklist → 01_The_Project → 02_Compute_and_Access
  → 03_Where_to_Find_Things` (+ harness setup docs).
- **Per-track scaffold:** `01_Your_Sub_Track`, `02_Existing_Work`, `03_Multi_Week_Plan`; autonomous
  tracks add a single `00_START_HERE` (a 60-second orientation, "what you own," an explicit
  **deferred — do not build** list, the supervision-gate model, a "how to work" method, a reading
  order) and an **Unknowns Register**.
- **The Unknowns Register** — a living known/unknown quadrant table, rows tagged *for-the-mentee* vs.
  *mentor-owned*, a list of "questions to extract the mentor's tacit knowledge," and deliberate
  blind-spot passes to run before each build. Shared-editable by mentor and mentee.
- **Feedback carries explanatory scaffolding** a peer wouldn't need: the precedents-&-tools table, a
  concrete numbered sequence, honest current-state gaps, open questions, and a standing "push back on
  anything that doesn't make sense" invitation.
- **Anti-scaffolding (equally important):** feedback for someone weeks into the team gets **no**
  welcome framing, **no** biography, **no** domain backgrounder (that lives in Onboarding), and **no**
  `[DRAFT INCOMPLETE]` placeholders. Respect their time.

## The privacy boundary (shared vault ≠ private space)
Mentees can read everything in the **shared** vault; they cannot read the private/strategy space.
The test before writing anything to the shared vault: **"would I be comfortable if every mentee read
this exact text?"** Personal/medical/family context never goes in the shared vault — only
schedule-only facts (*"out Jun 12–23"*) **without the reason**.

## In Lab Brain
`/lab-standup` runs the **digest half** (one agent per person → neutral update + team rollup);
`/lab-feedback` captures the **feedback half** from the mentor's check-in items into the dated,
structured skeleton. The roster in `lab-profile.yaml` assigns each member a role, which selects the
scaffolding and the report-up path above.
