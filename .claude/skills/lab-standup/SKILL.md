---
name: lab-standup
description: The multi-user synthesis engine — for each roster member, a neutral digest of their work since the last standup (one agent per person, concurrent), then a synthesized team rollup of what moved across the whole project. Additive; never overwrites anyone's log. Trainees also get a mentor-feedback scaffold. Use when the user says "lab-standup", "team digest", "what did everyone do", or names a person for their digest.
---

# /lab-standup — synthesize together, keep individual updates

The command that makes "a whole team contributes to one brain" real. It is how the
lab stays synchronized without anyone editing a shared log concurrently.

## Two forms
```
/lab-standup            → every member's neutral digest + a team synthesis
/lab-standup <person>   → just that person's digest (+ mentor-feedback scaffold if trainee)
```

## Do this (scales agents to roster size)
1. Read the roster from `lab-profile.yaml` and each member's `progress-<person>.md`
   (and their git branches / KB day-logs) since the last standup timestamp.
2. **Digest half** — spawn **one digest agent per member, concurrently**. Each writes a
   NEUTRAL summary of that person's work since last check-in (what landed, what's in
   progress, what's blocked). Neutral = factual, not evaluative.
3. **Feedback half (trainees only)** — for `role: trainee`, additionally emit a
   structured, dated `feedback-<person>-<date>.md` scaffold routed to their `mentor`,
   kept SEPARATE from the neutral digest (the mentor fills/edits it).
4. **Reduce** — one synthesis agent combines the per-person digests into a team rollup:
   what moved across the whole project, cross-lane dependencies, and what's ready to
   hand off. Write it to a dated `Sources/standup-<date>.md`.
5. **Additive only** — never overwrite a person's lane log or a previous standup.

Same swarm discipline as `/lab-index`: 3 people → 3 digest agents; 15 → 15, then one
reduce. Report the count.

## Output
- `Sources/standup-<date>.md` (team synthesis)
- per-person digests (in each person's lane or the standup note)
- `feedback-<trainee>-<date>.md` scaffolds for mentors

This is the mentor/peer collaboration loop the lab already runs, made one command.
