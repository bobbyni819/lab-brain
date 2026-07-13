---
name: lab-init
description: Configure Lab Brain for THIS lab — interview the user (or sample a subtree) and write lab-profile.yaml (storage roots, naming conventions, roster+roles, domain routing, vocabulary, privacy). Run this once before any crawl. Use when onboarding a new lab/project or when the user says "set up lab brain", "lab-init", or "configure the onboarding kit".
---

# /lab-init — configure & adapt Lab Brain to this lab

Goal: produce a correct `lab-profile.yaml` — the ENTIRE customization layer. The
skills and code never change per-lab; this file is the only thing that does.

## Do this
1. **Start from the template:** read `lab-profile.example.yaml`. It documents every
   field. Copy it to `lab-profile.yaml`.
2. **Interview OR infer.** Ask the user, or sample a representative subtree and infer:
   - Storage roots + backends (box / gdrive / local / s3) and each root's role.
   - Naming conventions: date-prefix regex, initials-suffix regex, `_processed/` dirs.
   - Project inference rule + aliases for messy folder names.
   - **The roster** — every member with `name`, `handle`, `role`
     (`pi` | `mentor` | `maintainer` | `mentee`), their storage, and (mentees) a `mentor`.
     This drives all multi-user behavior — do not skip it.
   - Domain routing (exclude non-project subtrees, e.g. admin/budget), read tiers, vocabulary
     (lab jargon so entities tag correctly), privacy globs/redactions.
   - Output KB location + format, and cost caps (`max_full_reads`).
3. **Write `PROFILE_REVIEW.md`** — a short human-readable summary of what you
   inferred, with anything low-confidence flagged. The human corrects the yaml
   before any expensive crawl runs. **Never crawl before the profile is approved.**
4. **Initialize the framework structure** in the KB output location: copy
   `framework/templates/START_HERE.md`, `_Log.md`, `_handoff-log.md`, `LANES.md`, and a
   `progress-<person>.md` per roster member (mentees also get a `day-log.md` + `questions.md`).
   Fill in the roster. (`bootstrap.py` does this automatically.)

## Output
- `lab-profile.yaml` (edited, lab-specific) + `PROFILE_REVIEW.md`
- Seeded collaboration files in the KB (`START_HERE.md`, `_handoff-log.md`, `LANES.md`,
  `progress-*.md`).

## Next
`/lab-scan` (structural inventory) → `/lab-triage` → `/lab-index`. All human-gated.
