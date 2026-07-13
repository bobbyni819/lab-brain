---
name: lab-scan
description: Structural inventory of a lab's storage — walk the roots and emit a manifest (one row per file: path, type, dates, initials, inferred project, dedupe hash, flags) with NO semantic reading. Fast, whole-corpus, deterministic. Use after /lab-init, or when the user says "scan the lab storage", "lab-scan", or "inventory the mess".
---

# /lab-scan — structural inventory (cheap, no LLM)

Map the mess before paying to read it. This is Layer 0: deterministic, no model calls.

## Do this
1. Read `lab-profile.yaml` for storage roots, naming regexes, domain routing, SKIP globs.
2. Walk every root. For each file emit a manifest row:
   - `path`, `backend`, `area` (code / notebook / doc / slide / sheet / figure /
     dataset / config / archive / media / email), `format`, `size`,
     `created` / `modified`, `owner` (fs metadata or git blame).
   - Parsed `date_prefix` and `initials` (from the naming regexes).
   - Inferred `project` (from the project rules) and `domain` (science vs excluded).
   - A cheap content-hash for dedupe.
   - Flags: `orphan`, `duplicate_hash`, `huge`, `binary_unreadable`, `stale_by_mtime`.
3. **No semantic reading yet** — just the map. Record structure as-found + flags.
4. On slow network mounts (Box), use a `--fast` mode that defers hashing.

## Runnable now (this step is real code, not just instructions)
Layer 0 ships as a deterministic module — no LLM, no network:
```
python -m labbrain.lab_scan --root <storage-root> [--profile lab-profile.yaml] [--out registry]
```
It walks the root, classifies every file by area, parses date-prefix / initials / project, computes
a cheap dedupe hash, honors the profile's SKIP / privacy / domain-exclude rules, and prunes VCS and
cache dirs. Emits `registry/manifest.jsonl` + `registry/SCAN_REPORT.md`. Use it directly, or let the
`/lab-index` swarm read the manifest it produces.

## Output
- `registry/manifest.jsonl` (one row per file)
- `SCAN_REPORT.md` — counts by area/project; duplicate groups; stale files (relative to the newest
  mtime in the set); a flags summary. "The pile, measured."

## Next
`/lab-triage` (rank what's worth deep-reading) → `/lab-index`. Idempotent — re-run anytime.
