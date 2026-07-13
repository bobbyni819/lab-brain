# The Lab Brain collaboration model — a whole team, one brain

> This is the heart of Lab Brain. Everything else (onboarding commands, figure
> reading) produces knowledge; **this** is how a whole lab *contributes to it
> together without stepping on each other* — peers and undergrads alike, each
> driving their own Claude agent, picking up where the others left off.
>
> It is not aspirational. It is a generalization of the coordination system the
> Hickey Lab **already runs in production** on a multi-person spatial-omics
> project (CODEX spatial proteomics × MALDI-IMS lipidomics) and a Data+
> undergraduate team. We extracted the practice and made it installable.

## The problem this solves

A lab's knowledge is spread across people and tools. The moment two people (or
two AI harnesses) touch the same shared KB or repo at once, you get clobbered
files, stale views, and "who changed this?" A single-user "chat with my files"
tool cannot onboard a *team*. Lab Brain can, because it ships the **conventions**
that keep concurrent contributors additive instead of destructive.

## Three primitives

### 1. The KB is the shared source of truth; each person works in a lane
- **Read the KB first, always.** `START_HERE.md` is the curated current state;
  the handoff log is the live ping board. Nobody starts work without reading both.
- **A lane = one person × one workstream.** You claim a lane on `LANES.md` before
  you touch it, so two people never grab the same figure/analysis/module.
  Collisions are prevented by *convention*, not locks — the same way a lab shares
  a bench.
- **Write back additively.** Findings go to a dated `Sources/<topic>-<date>.md`.
  Your per-person worklog is `progress-<you>.md`. A rollup aggregates them. Nobody
  edits a shared log concurrently, so there is nothing to merge-conflict.

### 2. Two harnesses, one hard rule
Lab Brain is built for people who use **both** Claude Science (SOTA agentic
science harness + bundled bio skills) **and** Claude Code (repo/git/manuscript
mechanics, cheap hands-off loops). They do **not** share live context — the KB
files are the only thing they have in common. So:

> **One harness owns a repo/working-dir at a time.** Claim it on the handoff log
> before editing. Two harnesses in the same folder at once = corruption. If both
> are genuinely needed, give each its own clone and sync through git.

See `harness-playbook.md` for the full convention (which harness does what, the
handoff format, how each gets onboarded to the shared KB).

### 3. The roster drives everything (peers vs. trainees)
`lab-profile.yaml` carries a **roster**: each member + a role (`pi` /
`collaborator` / `trainee`). Two collaboration modes fall out automatically:

| | **Mode A — Peers** (collaborators) | **Mode B — Mentor/trainee** |
|---|---|---|
| Shape | Symmetric — everyone reads shared KB, works a lane, writes back | Asymmetric — a PI/mentor oversees students who need scaffolding |
| KB surfaces | Lane + registry + shared findings (assumes context) | + project backgrounder, "start-here 3 files", explicit next-steps, feedback docs |
| Sync | Claim a lane, additive write-back | Neutral **digest** of each student's recent work + structured dated **feedback** |
| From | Hickey-lab peer collaboration | `/dataplus-digest` + `/dataplus-feedback` |

The same shared brain serves a new postdoc (light touch) and a rotation
undergrad (hand-held) from one profile. That is the difference between onboarding
a *user* and onboarding a *lab*.

## The engine: `/lab-standup`
The command that makes "synthesize together, keep individual updates" real:

```
/lab-standup            → one digest agent PER roster member (concurrent) produces a
                          neutral summary of their work since the last standup, THEN a
                          reduce agent synthesizes a team rollup → dated Sources/ note.
                          Additive; never overwrites anyone's lane log.
/lab-standup <person>   → just that person's digest (+ a mentor-feedback scaffold if
                          their role is trainee).
```
It scales agents to roster size — the same swarm discipline the onboarding index
uses. A 3-person team gets 3 digest agents; a 15-person lab gets 15.

## What a new member's first hour looks like
1. Clone the lab's Lab Brain repo, run the one-line setup → their Claude Code (and
   Claude Science) now have the lab's skills + conventions preloaded.
2. `START_HERE.md` + the roster tell them what the lab knows and who owns what.
3. They claim a lane, point Lab Brain at a paper/topic or a corner of storage, and
   within minutes are **adding cited knowledge to the shared brain** — every claim
   traceable to its source (including values that live only inside a figure panel).
4. The next member opens the same vault and sees the contribution already there.

That loop — zero to contributing, without clobbering anyone — is the product.

## Files in this kit
- `harness-playbook.md` — the two-harness coordination doctrine (generalized).
- `roles-and-lanes.md` — roles, guidance intensity, the lane discipline.
- `templates/START_HERE.md` — curated current-state, the first file everyone reads.
- `templates/_handoff-log.md` — the append-only ping board (claim / handoff / progress).
- `templates/LANES.md` — the lanes board (person × workstream × status).
- `templates/progress-PERSON.md` — a per-person worklog (additive; rolled up).
