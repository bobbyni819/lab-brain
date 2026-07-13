---
name: lab-update
description: Incremental re-sync — re-scan, diff by hash/mtime, re-index only what changed, patch the cross-links, and record a changelog. Keeps the lab brain LIVE instead of a one-time snapshot. Run on a schedule. Use when the user says "lab-update", "re-sync", "refresh the brain", or after new files land.
---

# /lab-update — incremental re-sync (keeps the brain live)

What makes the lab brain outlast the week: it stays current cheaply.

## Do this
1. Re-run `/lab-scan` structurally; diff against the last `manifest.jsonl` by hash + mtime.
2. **Only** re-index new/changed artifacts (`/lab-index` on the delta — resumable).
3. Patch the cross-links and project rollups affected by the delta (`/lab-link` on the delta).
4. Refresh per-person lanes if their work changed (so `/lab-standup` stays accurate).
5. Write `CHANGELOG.md` (what was added/changed/removed since last update).

Cheap by construction — it never re-reads unchanged files. Schedule it (daily/weekly)
and the KB tracks the lab instead of drifting stale.

## Output
Updated registry + vault + `CHANGELOG.md`.
