---
name: lab-onboard
description: Onboard a new member — generate their onboarding scaffold from the roster (the program sequence + a per-person sub-track folder with a supervision-gated START_HERE and an Unknowns Register), sized to their role. Use when the user says "lab-onboard <person>", "onboard <name>", "set up a new student/member", or adds someone to the roster.
---

# /lab-onboard <person> — get a new member productive fast

Generate the onboarding scaffold for a member from `lab-profile.yaml`, sized to their role. A
`mentee` gets the full scaffold; a `maintainer`/peer gets almost none (they self-onboard). Full
convention: `framework/onboarding.md`.

## Do this
1. Read the member's `role` + `mentor` from the roster. If `maintainer`/`pi`, stop after adding them
   to `LANES.md` and pointing them at `framework/README.md` — peers don't need scaffolding.
2. For a **mentee**, create/refresh:
   - The **program sequence** (once per lab): `Onboarding/00_Checklist` (from
     `framework/templates/onboarding-checklist.md`), `01_The_Project`, `02_Compute_and_Access`,
     `03_Where_to_Find_Things` — fill `01/02/03` from the lab's real project + compute + this
     framework. (Skip if they already exist.)
   - Their **sub-track folder** `Sub-tracks/<NN_track>/`: `00_START_HERE.md` (from
     `framework/templates/sub-track-START_HERE.md` — fill *In 60 seconds*, *What you own*,
     *Deferred/do-not-build*, the phased plan **with supervision gates**, the method, the reading
     order), `01_Your_Sub_Track`, `02_Existing_Work` (what already exists to build on — don't
     reinvent), `03_Multi_Week_Plan`, and `04_Unknowns_Register.md` (from
     `framework/templates/unknowns-register.md`).
   - Seed their `Day1_log.md` + `questions.md`, and add their row to `LANES.md` and the roster.
3. **Do NOT over-scaffold a veteran** — if the person has been active for weeks, skip the welcome
   material; onboard the newcomer, not the veteran.

## The point
This is what makes "onboard everyone to the project" real: a walkable sequence + a per-person
scaffold that also **extracts the mentor's tacit knowledge** (the Unknowns Register) instead of
losing it. From here the mentee's logs feed `/lab-standup` → `/lab-feedback` (the check-in loop).

## Output
- `Onboarding/*` (program sequence) + `Sub-tracks/<NN_track>/*` (per-person scaffold), filled from
  the roster; the member added to `LANES.md`.
