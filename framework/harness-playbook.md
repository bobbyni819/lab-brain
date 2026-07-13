# Harness playbook — Claude Science + Claude Code on one shared brain

> Generalized from a production coordination system. If your team uses **both**
> Claude Science (CS) and Claude Code (CC), read this first. It says (1) which
> harness does what, (2) the ONE rule that keeps them from corrupting each
> other, and (3) the standard way every session logs progress and hands off so a
> teammate — or you tomorrow, or the other harness — can pick up cleanly.

## The two harnesses

| | **Claude Science (CS)** | **Claude Code (CC)** |
|---|---|---|
| Strength | SOTA agentic harness + bundled bio skills (single-cell, structural bio, literature) + bio-data connectors | repo conventions, git/PR/manuscript mechanics, cheap hands-off loops (optionally via a second executor model) |
| Best for | open-ended scientific analysis, omics, structural bio, literature synthesis, **figure & panel reading** | writing code, running sims, git, decks/manuscripts, long autonomous loops |
| Reads context from | its own memory + files you point it at | the repo instructions + the KB automatically |

**They do NOT share live context.** The only thing they have in common is the
**KB files** (this playbook, each project's `START_HERE.md`, and the project
**handoff log**). If it isn't written into those files, the other harness cannot
see it. So: **log everything load-bearing into the KB.**

## Per-project lane split (rule of thumb)
- **Omics / structural / literature analysis** → CS.
- **Code, sims, git, manuscripts, decks, long loops** → CC.
- **Figure/panel deep-reading, multi-panel, supplementary-info** → CS (it is
  already state-of-the-art at reading graphics; the CC figure slice is a bounded
  showcase, not the frontier).

> CS = "reason like a scientist with specialized tools."
> CC = "write code, run it, do git/manuscripts, drive long loops."

## ⛔ The one hard rule: one harness per repo/working-dir at a time
Two harnesses editing the same working directory at once → corruption + stale
views. So:
1. **A repo/working-dir is owned by ONE harness at a time.** Claim it on the
   project's handoff log under `🔒 ACTIVE EDITS` before touching it. Release by
   deleting your line when done.
2. If a project genuinely needs both at once, **give each its own clone** (they
   sync through git), **or serialize.**
3. **Always refresh before you reason about state** (`git fetch`, re-open the
   file) — never trust a working tree you didn't just refresh.

## The standard handoff / progress-logging convention
Every project has a **handoff log** — an append-only ping board both harnesses
(and all teammates) read and write: `<project>/_handoff-log.md`, next to
`START_HERE.md`.

**On START (every session, every harness, every person):**
1. Read `START_HERE.md` (curated current state) + `_handoff-log.md` (recent
   entries + open handoffs) + any project resume protocol.
2. If you'll edit a SHARED file (the log, a registry, a shared doc, the repo),
   **claim it** under `🔒 ACTIVE EDITS`:
   `- 🔒 [HH:MM] @CS|@CC <person/lane> — <file/area> — <what>`.
3. Give a one-paragraph **status** (below) so everyone knows where you picked up.

**While WORKING:** do it in your own lane's files. Append a **one-line, stamped**
entry to the `📝 PROGRESS` section (newest at top):
`[YYYY-MM-DD HH:MM] @CS|@CC <person/lane>: <what changed, verified>`.
Cross-asks → the `🤝 HANDOFFS` section, tagged `→ @CS` / `→ @CC` / `→ @<person>`.

**Keep the log SHORT** — if it's on a no-merge cloud drive, long rewrites clobber.
Detail lives in your owned lane docs; the log is the lightweight board. Re-read
before you append.

**Verify, don't trust:** never log "done" from a transcript claim — re-open the
artifact (file, table, figure, deck, `git status`) and confirm before marking it
done.

### Standard status output (paste when you resume)
```text
Harness: CS | CC        Person/Lane: <name> / <STORYLINE|FIGURES|ANALYSIS|CODE|AUDIT>
Read: START_HERE, _handoff-log, <resume protocol / transcript id>
Current: <one sentence>
Done (verified): <artifacts, not claims>
Open: <short actionable list>
Next: <what I'm doing now>
```

## How each harness gets onboarded to this doc
- **Claude Code:** auto-loads the repo instructions (which point here) + the KB
  `START_HERE.md`. Nothing to do — it finds this.
- **Claude Science:** does not auto-read the KB. Give it this once via its Memory,
  and/or start CS sessions with: *"Read `framework/harness-playbook.md` and this
  project's `START_HERE.md` + `_handoff-log.md`, then follow that handoff
  convention."*

That's the whole system. It is boring on purpose — boring is what lets ten agents
and five humans share one brain without a single merge conflict.
