---
name: lab-feedback
description: Capture a mentor's check-in feedback for one person into a structured, dated feedback doc (the mentor half of the check-in loop; pairs with /lab-standup's neutral update). Use when the user says "lab-feedback <person>", "write feedback for <person>", "capture my feedback", or gives verbal feedback items to record for a mentee.
---

# /lab-feedback <person> — capture the mentor's feedback (the evaluative half)

Turns the mentor's spoken check-in items into a dated, structured feedback doc — kept SEPARATE from
the neutral `/lab-standup` update so the record and the evaluation never blur. Full convention:
`framework/mentorship-and-collaboration.md`; template: `framework/templates/feedback-PERSON.md`.

## Do this
1. **Get the items from the mentor.** This is an *action-item doc derived from a check-in*, not an
   onboarding package. If the mentor hasn't given items, **ASK** — never fabricate feedback.
2. Read the paired `<date>_<person>-update.md` (what shipped) so the feedback can **reference** it
   rather than re-describe it.
3. Write `<track>/<date>_<person>-feedback.md` on the gold-standard skeleton:
   - front-matter → a pointer to the paired update → **`## In 30 seconds`** (mandatory, ~150–300
     words plain prose) → **`## TL;DR`** (2–3 imperative "big shifts" + a `The quality bar [Mentor]:`
     verbatim quote) → **`## Part N`** per shift (`Problem [Mentor]` / `Fix` / `Quality gate [Mentor]`
     / `Precedents & tools` table / `Concrete sequence`) → paper-grade quality bar → current state
     (honest gaps) → Related files → **Open questions for <person>**.
4. **`[Mentor]` tags mark VERBATIM quotes only** — never invent phrasing to sound on-voice. Prose
   over tables. Give a mentee the extra scaffolding (precedents table, concrete sequence, "push back
   if this doesn't make sense"); give a peer `maintainer` just the review.
5. **Dated, never overwritten** — supersede a prior round with a forward-pointer, not an edit. If the
   person works from a repo, optionally mirror to `<repo>/docs/onboarding/` (second repo gets a stub).
   **Never push to a remote without explicit go-ahead.**
6. Update the `START_HERE.md` check-in table (`🟢 captured` → `✅ closed`) and, weekly, condense the
   feedback into a jargon-stripped line in the shared team-meeting note for the PI.

## The source-of-truth chain this completes
`student's writeup → neutral <date>_<person>-update.md → this <date>_<person>-feedback.md → condensed team-meeting bullet`
