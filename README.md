# 🧠 Lab Brain

**Onboard a whole lab — not just one user — onto Claude Code + Claude Science, and let
everyone contribute to one shared, cited knowledge base.**

> Built for **Built with Claude: Life Sciences** (Builder track). Lab Brain is a set of
> **accessory tools + conventions** that take a lab's messy existing storage and a lab's
> *people*, and turn them into a shared "brain" that the whole team reads from and writes
> to — each person driving their own Claude agent, every claim traceable to its source
> (including the numbers that live only inside a figure panel).

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
· Claude Code + Claude Science · Python 3.12

![Lab Brain — interactive showcase](./docs/assets/hero.png)

> The image above is a still from **[`docs/showcase.html`](./docs/showcase.html)** — a
> self-contained interactive walkthrough (open it in any browser: drag the swarm slider, toggle
> peers/trainee, click the figure panels).

---

## Why this exists

Every lab has the same two problems:

1. **The mess.** Years of data, code, decks, docs, grants, and papers scattered across
   Box/Drive/local, named `1002732.pdf` and `20260210_flu_ABM_BN.pptx`. A new member takes
   *months* to learn what the lab already knows.
2. **The team.** Knowledge lives in people's heads and separate folders. The moment two
   people (or two AI harnesses) touch the same shared notes at once, things get clobbered.
   "Chat with my files" tools onboard a *user*; they can't onboard a *lab*.

Lab Brain solves both — and it isn't aspirational. It's a generalization of the
coordination system the **Hickey Lab already runs in production** on a multi-person
spatial-omics project (CODEX spatial proteomics × MALDI-IMS lipidomics, human testis) and a
Data+ undergraduate team. We lifted the practice out and made it installable for any lab.

## The three moves

1. **Onboard fast.** One command wires a newcomer's Claude Code *and* Claude Science to the
   lab's shared KB, with the lab's conventions preloaded as skills.
2. **Contribute, don't just read.** Point Lab Brain at a corner of storage or a paper; a
   dynamically-scaled **swarm** of area-specialist agents reads everything semantically
   (one file at a time), verifies, and writes to the shared KB with provenance.
3. **A whole team, one brain.** Peers and undergrads contribute *concurrently* via lanes +
   a handoff convention — additive, no clobbering, with mentor scaffolding for trainees.
   This is the hero. See **[`collab/`](./collab/README.md)**.

## Quickstart — installs in minutes

```bash
git clone https://github.com/<you>/lab-brain && cd lab-brain
python bootstrap.py --members "Bobby:collaborator, Faye:trainee, John:pi"
```
That copies the lab's skills into your `.claude/`, writes a `lab-profile.yaml` to edit, and
seeds the shared collaboration structure (`START_HERE.md`, `_handoff-log.md`, `LANES.md`,
per-person progress logs). Then, in Claude Code:

```
/lab-init          # finish configuring this lab (storage, naming, ROSTER+roles, vocabulary)
/lab-scan          # structural inventory of the mess (no LLM, fast)
/lab-index         # the swarm: read everything semantically, with a quality gate
/lab-link          # assemble the browsable, cited KB vault + the provenance graph
/lab-ask "..."     # grounded, cited answers — the newcomer's day-one interface
/lab-standup       # per-person digests + a synthesized team rollup (the collab engine)
/lab-read-figure   # pull verified values out of figure panels (the showcased wow)
/lab-report        # a self-contained visual report of the run
```

> Two steps ship as **runnable, tested code** you can try immediately, no LLM required:
> `python -m labbrain.lab_scan --root <dir>` (a deterministic structural manifest + `SCAN_REPORT.md`
> of any messy folder) and `python -m labbrain.slice --paper gui2017 --provider fixture` (the figure
> read). The rest of the pipeline orchestrates agents via the skills above.

## The showcased capability: reading what the text never says

Papers hide their real quantities in figures. Lab Brain reads panels blind and verifies
each value — honestly. On a real open-access paper
([Gui et al. 2017, *Virology Journal*](https://doi.org/10.1186/s12985-017-0683-y), CC-BY):

![Figure-reading with honest verification](./docs/assets/figure-demo.png)


| Panel | Extracted (blind) | In the paper text? | Verdict |
|---|---|---|---|
| Fig 5b TNF-α | **29-fold @ day 2** | ❌ never stated | ✅ **VERIFIED** |
| Fig 5a IL-6 | ~500-fold @ day 4 | text says *"5.6 fold"* | ⚠️ **NEEDS-REVIEW** (text↔figure clash) |
| Fig 4 M-gene | grouped bars, broken axis | — | ⚠️ **NEEDS-REVIEW** (broken-axis flag) |

The verified numbers **exist only in the figures** — reading the text does not give them to
you. And the tool never fakes confidence: a busy panel, a broken axis, or a text↔figure
disagreement is flagged `needs-review` with the panel crop always kept as provenance
([D5 verification](./collab/README.md)). Run it yourself:

```bash
pip install -e .
python -m labbrain.slice --paper gui2017 --provider fixture \
       --vault demo_vault --report examples/gui2017/figure_report.html
```
`--provider fixture` runs fully offline. Under **Claude Science** use `--provider hostllm`
(its state-of-the-art figure reading); with an API key, `--provider anthropic`. Advanced
multi-panel auto-segmentation + supplementary-info reading are Claude-Science-lane roadmap.

## How it scores against the mess (design principle)

Genericity lives in **one file** — `lab-profile.yaml`. The skills and code ship with
grounded defaults and never change per-lab; another lab just edits the profile (its storage,
naming regexes, **roster + roles**, vocabulary, privacy rules). No abstract templates.

## Repo layout

```
lab-brain/
├── bootstrap.py              # the one-line installer (clone → setup)
├── lab-profile.example.yaml  # the ENTIRE per-lab customization layer (+ roster/roles)
├── .claude/skills/           # the skill bundle: /lab-init, /lab-scan, /lab-index, ...
├── collab/                   # ⭐ the multi-user collaboration kit (the hero)
│   ├── README.md             #   the collaboration model (peers + trainees, one brain)
│   ├── harness-playbook.md   #   Claude Science + Claude Code on one shared KB
│   ├── roles-and-lanes.md    #   roles, guidance intensity, anti-collision lanes
│   └── templates/            #   START_HERE / _handoff-log / LANES / progress-<person>
├── src/labbrain/             # the figure-reading capability (fetch→render→crop→extract→verify→vault→report)
├── examples/gui2017/         # the verified hero-paper run
├── demo_vault/               # a stripped demo KB that fills as you run
└── tests/                    # offline pytest (verification, vault, schema, end-to-end)
```

## Design docs
- **[`collab/README.md`](./collab/README.md)** — the collaboration model (start here for the hero).
- **[`collab/harness-playbook.md`](./collab/harness-playbook.md)** — two harnesses, one brain.
- **[`docs/`](./docs/)** — architecture, verification ethic, the swarm.

## License
MIT — see [LICENSE](./LICENSE). Uses only open-access, appropriately-licensed paper data.
