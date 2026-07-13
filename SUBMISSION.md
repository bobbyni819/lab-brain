# Lab Brain — submission summary

## 100–200 word written summary (draft for the submission form)

> **Lab Brain** packages a proven *framework* for how a whole lab runs a shared knowledge base —
> and installs it on Claude Code + Claude Science in minutes.
>
> Labs lose knowledge not because people don't write things down, but because nobody agrees on
> *where things go*. Lab Brain fixes that: one `bootstrap.py` seeds a lab's vault with a documented
> convention for every artifact — where each file lives, how it's named, where an update / handoff /
> decision goes, how figures are made and verified and their findings logged, how the manuscript
> storyline is built, and how mentees collaborate and report up to mentors through a paired
> neutral-update + structured-feedback loop. A dynamically-scaled swarm of agents then reads the
> lab's messy storage into that structure, cited and provenance-tracked.
>
> It's generalized from the coordination practices our lab runs day-to-day — on a multi-person
> spatial-omics project and a Data+ undergraduate team — which we're now adopting in this packaged
> form. The showcased capability reads *figure panels* and can recover a value that appears nowhere
> in a paper's text (a 29-fold peak) while honestly flagging a figure whose value contradicts the
> text. Open source (MIT).

*(~190 words.)*

## The submission bundle (Builder track)
1. **3-min demo video** — a walk-through of `docs/showcase.html` (the interactive artifact):
   the problem → **the framework** (the "where does this go?" routing map) → the mentee↔mentor
   check-in loop → the swarm reading storage → the figure-reading demo (TNF-α verified vs. IL-6
   needs-review) → "already in the lab" → install.
2. **Open-source repo** — this repository (MIT).
3. **Written summary** — above.

## How it maps to the judging rubric
| Criterion | Weight | How Lab Brain earns it |
|---|---|---|
| **Demo** | 30% | A person goes zero → contributing; one jaw-drop moment (a figure-only number, verified live) |
| **Impact** | 25% | Named user (a PI onboarding a lab + mentoring undergrads); the exact problem this hackathon exists to solve; **generalized from — and being adopted in — our own lab** |
| **Claude Use** | 25% | A convention framework + a 16-skill bundle + a dynamically-scaled agent swarm + panel-level figure reading + a two-harness (Code + Science) coordination layer — far beyond a chat app |
| **Depth** | 20% | Conventions lifted from production (KB structure, doc-routing, figure/storyline discipline, the paired-doc mentorship loop) + deterministic verification + provenance + an independent quality gate |

## What's real vs. roadmap (honesty)
- **Real + verified here:** the framework docs + templates are generalized from a lab's live system;
  the Layer-0 structural scanner (`python -m labbrain.lab_scan`) and the figure-reading slice
  (`python -m labbrain.slice`) both run end-to-end offline on real inputs; **40 tests pass**; the
  installer, the 16-skill bundle, and the interactive artifact all work.
- **Claude-Science lane (roadmap):** advanced multi-panel auto-segmentation and
  supplementary-information reading — best developed on Claude Science's state-of-the-art figure
  harness, not re-implemented here.
