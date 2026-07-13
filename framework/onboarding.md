# Onboarding — get a new member productive, and extract the mentor's tacit knowledge

Generalized from a lab's real onboarding system (a 10-week program that puts undergraduates onto
real project tracks). Onboarding isn't a welcome packet — it's a **walkable sequence** plus a
**per-person scaffold** that makes someone productive in days and surfaces what the mentor knows but
never wrote down.

## Two parts: a program sequence + a per-person scaffold

### 1. The program sequence — `Onboarding/` (everyone reads it once, in order)
A fixed, numbered set so a newcomer always knows what to read next:
```
Onboarding/
├── 00_Checklist.md            ← access to grant + read-order; the one page they open first
├── 01_The_Project.md          ← the science + the goal, in plain language
├── 02_Compute_and_Access.md   ← how to actually run things: repos, compute/cluster, and
│                                 setting up their own Claude Code + Claude Science
└── 03_Where_to_Find_Things.md  ← the vault map (this framework, in one page)
```
Template: [`templates/onboarding-checklist.md`](./templates/onboarding-checklist.md). This is the
"more scaffolding a mentee gets that a peer doesn't" — a `maintainer` skips it; a `mentee` walks it.

### 2. The per-person scaffold — their sub-track folder
Each mentee owns a folder with a fixed scaffold, so they always know *what they own* and *what's
out of scope*:
```
Sub-tracks/<NN_track>/
├── 00_START_HERE.md           ← their single entry point (below)
├── 01_Your_Sub_Track.md       ← what this track is; the deliverable
├── 02_Existing_Work.md        ← what already exists to build on (don't reinvent)
├── 03_Multi_Week_Plan.md      ← the phased plan, with supervision gates
├── 04_Unknowns_Register.md    ← the known/unknown map (below) — the standout scaffold
├── Day1_log.md, Week1_log.md  ← their own quick logs (feed the check-in digest)
└── questions.md               ← async questions the mentor checks between meetings
```

## The per-person `00_START_HERE.md` (the entry point)
Template: [`templates/sub-track-START_HERE.md`](./templates/sub-track-START_HERE.md). It carries:
- **In 60 seconds** — orientation a newcomer can read cold.
- **What you own** — the deliverable, stated as an outcome.
- **Deferred — do not build** — an explicit list of things *out of scope* (prevents scope creep,
  the #1 way a mentee burns weeks).
- **Supervision gates** — the work is phased, and each phase ends in **a concrete artifact the
  mentor reviews async before the next phase.** The plan flags, per decision, *which are yours to
  make* vs *which need the mentor's judgment* — so a mentor can be hands-off by design yet step in
  anytime (see [mentorship-and-collaboration](./mentorship-and-collaboration.md)).
- **How to work (the method)** — the loop the mentee runs (e.g. sketch → build one piece → verify →
  log → surface at check-in).
- **Reading order** — the machine-readable "how to orient to this track" contract.

## The Unknowns Register (the distinctive scaffold)
Template: [`templates/unknowns-register.md`](./templates/unknowns-register.md). A living table a
mentee and mentor **both edit**, structured as the four quadrants:

| | known | unknown |
|---|---|---|
| **known** | *known knowns* — settled facts | *known unknowns* — questions we know to ask |
| **unknown** | *unknown knowns* — the mentor's tacit knowledge, not yet written | *unknown unknowns* — blind spots to go looking for |

Each row is tagged **`[for <mentee>]`** (theirs to resolve) or **mentor-owned**, plus two standing
sections: **"questions to extract the mentor's tacit knowledge"** (the mentee is told to ask these),
and **"deliberate blind-spot passes to run"** before each build. This is how a program turns a
mentor's head-knowledge into shared, written knowledge instead of losing it.

## Anti-scaffolding (for someone already weeks in)
Once a person is oriented, their feedback and docs get **no** welcome framing, **no** biography, **no**
domain backgrounder (that's what `Onboarding/` is for), and **no** `[DRAFT INCOMPLETE]` placeholders.
Respect their time; scaffold the newcomer, not the veteran.

## How onboarding connects to the rest of the framework
```
Onboarding/ sequence  →  sub-track scaffold (00_START_HERE + Unknowns Register)
   →  the mentee works, keeping Day/Week logs + questions.md
   →  /lab-standup digests their logs into a neutral -update  →  /lab-feedback captures the mentor's -feedback
   →  the Unknowns Register shrinks as tacit knowledge gets written down
```
`/lab-onboard <person>` generates the whole scaffold from the roster in `lab-profile.yaml`.
