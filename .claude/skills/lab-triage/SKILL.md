---
name: lab-triage
description: Prioritize what's worth deep-reading — rank the scan manifest by likely knowledge value using ONLY cheap signals (name, path, type, size) and assign each file a read-tier (FULL / SKIM / METADATA / SKIP). Lets a lab semantically index 10k files without paying to deep-read all of them. Use after /lab-scan, or when the user says "lab-triage", "what's worth reading", "prioritize the scan".
---

# /lab-triage — decide what's worth reading (cheap LLM, gated)

The stage between the cheap structural scan and the expensive semantic read. It keeps a big corpus
affordable by reading deeply only what's likely to carry knowledge.

## Do this
1. Read `registry/manifest.jsonl` (from `/lab-scan`) and the `read_tiers` block in `lab-profile.yaml`.
2. Rank each entry by **likely knowledge value** using ONLY cheap signals — filename, path, type,
   size (never the content). A signal-rich slide deck outranks a CV; a temp `.xlsx` outranks nothing.
3. Assign each file a **read-tier**:
   - `FULL` — deep semantic read (slides, key docs, notebooks, code)
   - `SKIM` — text + captions only (long PDFs, big sheets)
   - `METADATA` — index only (media, archives, raw CSVs)
   - `SKIP` — ignore (temp files, `~$*`, `.DS_Store`)
   Seed from the profile's `read_tiers` map, then adjust per-file on the cheap signals.
4. **Human-gated:** emit the plan for approval before any expensive crawl runs — no `/lab-index`
   until the tier plan is confirmed.

## Output
- `registry/read_plan.jsonl` (one row per file with its tier + a one-line reason)
- `TRIAGE_REPORT.md` — counts by tier; the estimated FULL-read budget vs the profile cap.

## Next
`/lab-index` reads each file at its assigned tier (the swarm). Idempotent — re-run after a `/lab-scan`.
