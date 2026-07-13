# Documentation & handoffs — where every update, decision, and handoff goes

This is the convention people ask for most: *"I just did/decided/found something — where does it
go?"* A lab loses knowledge not from failing to write things down, but from writing them in a
chat that scrolls away. Every kind of item has **one home**. There are five, each with a job.

## The five surfaces (and the one job each does)

### 1. `START_HERE.md` — the rolling daily inbox (what's new, what's pending)
The single landing page a person opens to see what changed, what's waiting on them, and what's
ready to show the PI — without digging through folders. **Reverse-chronological by day, newest at
top.** Each day is keyed by status *from the human's perspective*:

```markdown
## 📅 YYYY-MM-DD (Weekday)
### 🟡 Ready to show <PI>
- 🟡 [[link]] — one-line description
### 🟢 In progress (working / waiting on external)
- 🟢 brief description + ETA or blocker
### 🔴 Open items — things you might still need to decide/do
- 🔴 short actionable item, with link
### ✅ Done today
- ✅ [[link]] — one-line description
```
| 🔴 | needs the human's attention/action | 🟡 | ready to review / show the PI |
|---|---|---|---|
| 🟢 | in progress (agent working, or waiting on external) | ✅ | done (moves to Done for that day) |

**Rules:** add today's section on first touch; log every new deliverable file here at the most-open
status; move items to ✅ on completion (auto-detect from a tool result when confident, and say so);
**never delete** — items stay in their day; keep a `## 🧭 Quick nav` block at the bottom linking the
active hubs. The newest day must **make sense cold**. START_HERE holds *links + one-liners only* —
never full detail (that lives in the actual file) and never deep history (that's `_Log.md`).

### 2. `_Log.md` — the append-only audit timeline (what happened, when)
Every ingest, significant write, or lint appends one entry. It's the chronological record a new
session greps to catch up.
```markdown
## [YYYY-MM-DD] <action> | Title
Brief description.
- Pages created/updated: [[page1]], [[page2]]
- Sources added: filename.md
```
Actions: `ingest · query · lint · compile · update · reorganize`. Don't log trivial reads — only
ingests, writes, and significant queries. (Greppable: `grep "^## \[" _Log.md | tail -10`.)

### 3. `_handoff-log.md` — the live coordination board (who's doing what, cross-asks)
The append-only ping board both harnesses and all teammates read on start. Three sections:
- **🔒 ACTIVE EDITS** — claim a shared file before editing it (delete your line when done). This is
  what prevents two people/harnesses from clobbering the same file.
- **🤝 OPEN HANDOFFS & DECISIONS** — cross-asks tagged `→ @CS` / `→ @CC` / `→ @<person>`.
- **📝 PROGRESS** — one stamped line per change, newest at top:
  `[YYYY-MM-DD HH:MM] @CS|@CC <person/lane>: <what changed, verified>`.

Keep entries **one line** (a no-merge cloud drive clobbers long rewrites); detail lives in your own
lane's files. Re-read before you append. Full convention: [harness-playbook](./harness-playbook.md).

### 4. `MEMORY.md` (+ topic notes) — facts worth surviving a context reset
A one-line index; each entry points to a topic note holding one durable, non-obvious fact (a
decision and its *why*, a gotcha, a pointer). Not a worklog — the durable spine that reorients any
future session.

### 5. The `Wiki/` page — where a *decision* or *understanding* actually lives
A decision worth remembering is reference material: record it on the relevant `Wiki/` page (+ a
one-line `_Log` entry pointing to it). START_HERE and the handoff log are *inboxes and boards* —
they point at the durable content, they are not the content.

## The routing map (memorize this, or let the skills apply it)

| I just… | Goes to |
|---|---|
| finished something / hit a blocker today | `START_HERE.md` (dated, status emoji) |
| did an ingest / significant write | `_Log.md` |
| need a teammate/harness to pick something up | `_handoff-log.md` 🤝 (+ claim 🔒 if editing a shared file) |
| am about to edit a shared file | claim it under `_handoff-log.md` 🔒 ACTIVE EDITS first |
| made a decision worth keeping | the relevant `Wiki/` page (+ a `_Log` line) |
| wrote a how-to / SOP / synthesis | `Wiki/Methodology` (technical) or `Wiki/Concepts` (analysis) |
| pulled in raw material | `Sources/` (immutable) |
| produced a valuable query answer | `Output/Explorations/` (file it back — don't let it vanish) |
| learned a durable, non-obvious fact | a `MEMORY.md` topic note |
| ended a work session | update `START_HERE`, append `_Log`, refresh the handoff/tracker |

## After every session (the closing ritual)
1. Update `START_HERE.md` (today's section; move finished items to ✅).
2. Append `_Log.md` for any ingests/writes/significant queries.
3. Update the `_handoff-log.md` (release your 🔒 claims; leave a 📝 progress line; raise any 🤝 handoff).
4. Mark completed plan items `[x]`; file back any valuable exploration.

Do this and the knowledge base stays current **as a byproduct of working** — nobody has to
"document" as a separate chore.
