# Lab Brain — submission summary

## 100–200 word written summary (draft for the submission form)

> **Lab Brain** turns a lab's messy storage *and its people* into one shared, cited knowledge
> base that a whole team builds together — across Claude Code and Claude Science.
>
> Most "chat with my files" tools onboard a single user. Lab Brain onboards a *lab*. One
> `bootstrap.py` wires every member's Claude with the lab's skills and conventions; a
> dynamically-scaled swarm of area-specialist agents reads the corpus semantically — one file at
> a time, with an independent quality gate that re-reads shallow passes; and a lane + handoff
> convention lets peers and undergraduates contribute concurrently to one vault — additive, no
> clobbering, with mentor scaffolding for trainees. Every claim traces back to its source.
>
> The showcased capability reads *figure panels*: on a real open-access paper it recovered
> TNF-α = 29-fold — a number that appears nowhere in the text — and honestly flagged an IL-6
> panel where the figure (~500-fold) contradicts the text ("5.6 fold"), keeping the crop as
> provenance.
>
> It isn't aspirational: the collaboration model is generalized from the system our lab already
> runs on a multi-person spatial-omics project. Open source (MIT).

*(~195 words. Trim the last sentence to land under 200 on any given form.)*

## The submission bundle (Builder track)
1. **3-min demo video** — a walk-through of `docs/showcase.html` (the interactive artifact):
   the problem → the swarm scaling live → the collaboration model (peers vs. trainees) → the
   figure-reading demo (TNF-α verified vs. IL-6 needs-review) → "already in the lab" → install.
2. **Open-source repo** — this repository (MIT).
3. **Written summary** — above.

## How it maps to the judging rubric
| Criterion | Weight | How Lab Brain earns it |
|---|---|---|
| **Demo** | 30% | A person goes zero → contributing; one jaw-drop moment (a figure-only number, verified live) |
| **Impact** | 25% | Named user (a PI onboarding a lab); the exact problem this hackathon exists to solve; already adopted in a real lab |
| **Claude Use** | 25% | Skill bundle + dynamically-scaled agent swarm + panel-level figure reading + a two-harness (Code + Science) collaboration layer — far beyond a chat app |
| **Depth** | 20% | Deterministic verification + provenance + an independent quality gate + a multi-user coordination model lifted from production |

## What's real vs. roadmap (honesty)
- **Real + verified here:** the Layer-0 structural scanner (`python -m labbrain.lab_scan`) and the
  figure-reading slice (`python -m labbrain.slice`) both run end-to-end offline on real inputs;
  **29 tests pass**; the installer, skill bundle, collaboration kit, and interactive artifact all
  work; the collaboration model is generalized from a system the lab already runs.
- **Claude-Science lane (roadmap):** advanced multi-panel auto-segmentation and
  supplementary-information reading — best developed on Claude Science's state-of-the-art figure
  harness, not re-implemented here.
