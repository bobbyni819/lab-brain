---
name: lab-standup
description: The check-in digest engine — for each roster member, a NEUTRAL dated update of their work since their last round (one agent per person, concurrent), then a synthesized team rollup. Additive; never overwrites anyone's log. Pairs with /lab-feedback for the mentor half. Use when the user says "lab-standup", "team digest", "what did everyone do", or names a person for their digest.
---

# /lab-standup — the neutral digest half of the check-in loop

The command that makes "a whole team contributes to one brain" real. It produces the **neutral
record** of each person's work; the mentor's evaluative feedback is a separate artifact
(`/lab-feedback`) so the two never contaminate each other. Full convention:
`framework/mentorship-and-collaboration.md`.

## Two forms
```
/lab-standup            → every member's neutral update + a team synthesis
/lab-standup <person>   → just that person's update (then run /lab-feedback <person> for the mentor half)
```

## Runnable gather (the deterministic half — no LLM)
Collect each person's raw activity with the runnable gather, then hand it to the agents to write the
neutral updates:
```
python -m labbrain.lab_standup --vault <kb> --profile lab-profile.yaml --repo <repo> [--person X] [--out registry]
```
It pulls, per member: git commits (by author since their last feedback date), files modified since
then, their `progress-<person>.md` excerpt, and their `questions.md` open items — into a
`standup-input.md`. (Git degrades gracefully to none if the vault isn't a repo.)

## Do this (scales agents to roster size)
1. Read the roster from `lab-profile.yaml` (or run the gather above). For each member, set the
   **diff window** = the date of their last `<date>_<person>-feedback.md` (fallback: project start).
2. **Spawn one Explore agent per member, concurrently.** Each reads only that person's recent work:
   git-tracked members via `git log --author=<name> --since=<window>`; vault-based members via
   files modified since the window (day-logs, deliverables).
3. Each agent writes a **NEUTRAL** `<date>_<person>-update.md` (idempotent — replaces same-date):
   `Headline → per-piece breakdown (paths + line counts + mechanism) → quality flags → 1–3 verbatim
   quotes worth preserving → files for the mentor to spot-check (the key section) → mapping to the
   last feedback round (executed / partial / not addressed)`. Neutral = what was **done**, never
   "the mentor should…" (that's `/lab-feedback`'s job). Template: `framework/templates/update-PERSON.md`.
4. **Reduce** — one synthesis agent combines the per-person updates into a team rollup (what moved,
   cross-lane dependencies, what's ready to hand off) → a dated `Sources/standup-<date>.md`.
5. **Refresh the nav hub** — update the "current check-in round" table in `START_HERE.md` (one row
   per person, status `🔴 not pulled · 🟡 needs feedback · 🟢 captured · ✅ closed`).
6. **Additive only** — never overwrite a person's lane log or a previous round.

Same swarm discipline as `/lab-index`: 3 people → 3 agents; 15 → 15, then one reduce. Report the count.

## Output
- `<track>/<date>_<person>-update.md` per member (neutral)
- `Sources/standup-<date>.md` (team synthesis)
- refreshed check-in-round table in `START_HERE.md`

Then run **`/lab-feedback <person>`** to capture the mentor's items into the paired, structured
`<date>_<person>-feedback.md`. This is the check-in loop the lab already runs, made two commands.
