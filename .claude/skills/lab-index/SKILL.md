---
name: lab-index
description: The core semantic read — a dynamically-scaled SWARM of area-specialist agents reads each artifact IN FULL (one file at a time) and emits a structured record, with an independent quality gate that grades each read and re-reads shallow ones. Use after /lab-scan+/lab-triage, or when the user says "lab-index", "read everything", or "build the registry".
---

# /lab-index — semantic read per artifact (the swarm + quality gate)

The expensive core. Reads EVERYTHING semantically, one file at a time, and proves
it read deeply — not skimmed. This is where "scales agents to the corpus" happens.

## The swarm (scales to the work)
Read `registry/read_plan.jsonl` (tiers from /lab-triage). Then:
- For each **content area** present, spawn that area's **specialist reader**
  (data-profiler, code-reader, slide-reader+figure-extractor, doc-reader,
  grant-reader, comms-reader, lit-reader, media-reader).
- Within an area, spawn `W = clamp(ceil(files_at_tier / files_per_worker), 1, max_workers)`
  concurrent workers. Report the LIVE count: *"spawned 34 readers across 6 areas
  (code 9, slides 7, lit 6, docs 5, data 4, comms 3)."* That number is the swarm story.
- Concurrency is bounded three ways: triage tiers cap FULL reads; `max_full_reads`
  in the profile; host batch concurrency. It never runs away.

## The 4-layer deep-read (per file — how we prove it's not skimming)
1. **Transcribe** (no LLM): binary → complete intermediate (full text + tables +
   per-slide text&notes + rendered figure/page PNGs). Nothing dropped.
2. **Semantic read** (specialist + tool schema): structured record — title, purpose,
   summary, key_results, entities (datasets/methods/people/tools), numbers,
   open_questions, self-confidence. File-specific, not generic.
3. **Quality gate** (a SEPARATE grader agent): scores the record vs the transcript on
   coverage / specificity / faithfulness and lists what was missed. The verdict is
   computed **deterministically in code** from the scores, NOT taken from the model's
   self-report: `accept` iff coverage≥75 AND specificity≥70 AND faithfulness≥90;
   faithfulness<90 forces a re-read; else re-read-deeper.
4. **Re-read / escalate:** on re-read-deeper, re-read with a bigger window AND feed
   rendered figure images to a vision read (figures get actually understood). Re-gate.
   On escalate → flag in the registry for a human.

Every record carries `provenance` (source path + backend) and `confidence`.
Slides/PDFs get figure rendering so figure content is read, not just text (this is
where `/lab-read-figure` plugs in for panel-level values).

## Output
- `registry/artifacts/*.json` — one record per file. Resumable: only unread/changed
  files are (re)processed. Gate scores become a KB-quality dashboard.

## Next
`/lab-link` (assemble the vault + provenance graph).
