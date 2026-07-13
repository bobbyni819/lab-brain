# The Lab Brain Framework — how a lab actually runs a shared brain

> This is the heart of Lab Brain. Not a figure reader — a **set of conventions** for how a whole
> lab documents, saves, hands off, makes figures, builds the storyline, and mentors, so that a team
> (and its AI agents) all contribute to **one knowledge base** without stepping on each other.
>
> It is not invented for a pitch. Every convention here is generalized from a system a real lab
> **already runs in production** — a spatial-omics project (CODEX proteomics × MALDI-IMS lipidomics)
> and a Data+ undergraduate team, coordinated across Claude Code and Claude Science. We lifted the
> practice out and made it adoptable.

## The one idea
A lab's knowledge doesn't get lost because people don't write things down. It gets lost because
**nobody agrees on WHERE things go** — so updates, decisions, handoffs, figures, and findings scatter
across chats, folders, and heads. Fix the *where* and the *how*, and a knowledge base maintains
itself as a side effect of doing the work.

## The five conventions (read in order)

| # | Convention | Answers |
|---|---|---|
| 1 | **[Knowledge-base structure](./knowledge-base-structure.md)** | Where does each *file* live? (the three-layer Sources / Wiki / Output vault + the filing rule) |
| 2 | **[Naming & note format](./naming-and-note-format.md)** | What do I *name* it, and what's the note template? |
| 3 | **[Documentation & handoffs](./documentation-and-handoffs.md)** | Where does each *update / decision / handoff / finding* go? (the routing map) |
| 4 | **[Figures & findings](./figures-and-findings.md)** | How are figures made, verified, saved, and their insights logged? |
| 5 | **[Storyline & manuscript](./storyline-and-manuscript.md)** | How is the narrative built and tracked as figures land? |
| 6 | **[Onboarding](./onboarding.md)** | How do you get a new member productive fast — and extract the mentor's tacit knowledge? |
| + | **[Mentorship & collaboration](./mentorship-and-collaboration.md)** | How do peers and mentees contribute, and how do mentees report up to mentors? |
| + | **[Harness playbook](./harness-playbook.md)** | How do Claude Science + Claude Code share one brain without corruption? |

## The routing map — "where does this go?" (the question the framework answers)

The single most valuable thing this framework gives a lab is a **default answer** for every kind of
thing you produce, so nothing lands in a chat log and evaporates:

| I just… | It goes to… | Why |
|---|---|---|
| finished something / hit a blocker (a today update) | `START_HERE.md` (dated, 🔴🟡🟢✅) | the rolling daily inbox everyone reads first |
| did an ingest / significant write | `_Log.md` (append-only, chronological) | the audit timeline |
| need to hand a task to a teammate or the other harness | `_handoff-log.md` (🤝 section) + claim under 🔒 ACTIVE EDITS | the live coordination board |
| made a decision worth remembering | the relevant Wiki page + a `_Log` line | decisions are reference material, not inbox items |
| wrote synthesis / a how-to / an SOP | `Wiki/Methodology` (technical) or `Wiki/Concepts` (analysis) | the LLM-owned synthesis layer |
| pulled in raw material (transcript, paper, data dump) | `Sources/` (immutable) | raw stays raw; never edited |
| produced a figure | the figure lane's folder + a line in `FIGURE_FINDINGS.md` | figure + its finding stay linked |
| discovered something worth the storyline | the storyline outline doc | figures feed the narrative deliberately |
| a mentee's weekly work | their `progress-<person>.md`; a mentor's notes → `feedback-<person>-<date>.md` | neutral log and evaluative feedback stay separate |
| a fact worth recalling across sessions | a `MEMORY.md` topic file (one-line index + a topic note) | survives context resets |

That table *is* the product: a lab that adopts it stops losing knowledge.

## How Lab Brain installs the framework
`python bootstrap.py` seeds a lab's vault with the templates in [`templates/`](./templates/) —
`START_HERE.md`, `_Log.md`, `_handoff-log.md`, `LANES.md`, a `progress-<person>.md` per member, a
note template, a `FIGURE_FINDINGS.md`, a storyline outline, and mentor-feedback scaffolds — already
filled from the roster in `lab-profile.yaml`. The skills (`/lab-standup`, `/lab-scan`, …) then
maintain them as the team works.
