# Roles & lanes — how guidance and ownership adapt to each person

Lab Brain reads the `roster` in `lab-profile.yaml` and adapts what the shared
brain surfaces to each person's **role**, and enforces **lane** discipline so
concurrent contributors stay additive.

## Roles (set per member in the roster)

| Role | Who | What the KB surfaces | How `/lab-standup` treats them |
|---|---|---|---|
| `pi` | PI / group lead | Cross-person synthesis + the gaps/risk audit (`/lab-gaps`); the whole-project rollup | Receives the team synthesis |
| `collaborator` | Peer, postdoc, staff scientist | Lane + registry + shared findings. Assumes context — light touch | Neutral digest of their lane since last standup |
| `trainee` | Undergrad / rotation / new student | **More**: a project backgrounder, "start-here: the 3 files to open first", explicit next-steps, and a mentor-feedback doc | Neutral digest **+** a structured mentor-feedback scaffold routed to their mentor |

Guidance intensity is the point: a rotation student and a senior postdoc pull
from the *same* brain but the student gets scaffolding the postdoc doesn't need.
This is how you onboard a whole lab, not just the people who already have context.

`trainee` members may name a `mentor:` in the roster; feedback digests route there.

## Lanes — the anti-collision discipline

A **lane** is one person working one workstream (a figure, an analysis, a module,
a paper survey). The rule:

1. **Claim before you work.** Add a row to `LANES.md` (and, if you'll edit a
   shared file, a line under `🔒 ACTIVE EDITS` in the handoff log).
2. **Work in your lane's own files.** Findings → `Sources/<topic>-<date>.md`;
   your worklog → `progress-<you>.md`. Never edit someone else's lane file or a
   shared log concurrently.
3. **Write back additively.** New file per finding/day, not an edit to a shared
   one. A rollup aggregates. Nothing to merge, nothing to clobber.
4. **Release when done.** Update the `LANES.md` status; delete your ACTIVE-EDITS
   line.

### Conventions that make lanes safe
- **Per-user paths, never hardcoded.** Each person's storage differs. Use a
  resolver (`lab_paths`): code calls `resolve("raw_data")`, and each person's
  `lab_paths.local.json` (filled once) points it at *their* copy. This is the #1
  multi-user friction, fixed once.
- **Archive, never delete.** Superseded work moves to `_archive/`, so history is
  never lost and no one's contribution silently disappears.
- **Branch per lane** (for code): `git checkout -b <person>/<workstream>`; a
  `Lane: <person>/<workstream>` commit trailer records which human drove the
  agent that made each commit. `git blame` stays meaningful even when agents write.

## Why this scores as *depth*, not decoration
Anyone can demo one person chatting with their files. A system where **peers and
undergrads contribute to one cited brain concurrently, with mentor scaffolding
built in and zero clobbering**, is a categorically harder problem — and it's the
exact thing a lab needs to actually adopt a tool past the demo. It works here
because it's lifted from a system a real lab already runs, not invented for a pitch.
