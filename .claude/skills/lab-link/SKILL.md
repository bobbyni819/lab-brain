---
name: lab-link
description: Assemble the per-artifact records into a browsable, cited KB vault — cluster artifacts into projects (even when folders lie), dedupe, resolve cryptic PDFs to titles/DOIs, and build the cross-links (figure→script→dataset, doc→dataset, person→artifacts). Emits an Obsidian-style markdown vault mirroring the lab's KB. Use after /lab-index or when the user says "lab-link", "build the vault", "assemble the registry".
---

# /lab-link — assemble registry + infer structure → the KB vault

Turn a pile of per-file records into a *brain*: a browsable vault with the graph
that makes knowledge findable.

## Do this
1. **Cluster** artifacts into projects using content + the profile's project rules —
   even when folder names lie. Dedupe by content hash.
2. **Resolve identity** — cryptic PDFs (`1002732.pdf`) → real titles/DOIs.
3. **Build the cross-links (the graph):**
   - `figure → generating script → source dataset` (the provenance chain)
   - `doc → dataset it describes`, `code → its inputs/outputs`, `person → artifacts`
   - `method → artifacts/papers`, `project → members`
4. **Emit the vault** (Obsidian markdown, mirroring the lab's KB so it's instantly
   browsable + shareable):
   - `registry/_Index.md` — the map
   - `projects/*.md` — one rollup per project: description, members, data locations,
     code paths, key outputs, timeline, status, entrypoints (how to actually run it),
     open gaps, and **start_here** (the 3 files a newcomer opens first)
   - `catalogs/*.md` — `people.md`, `datasets.md`, `methods.md`, `glossary.md`
     (lab jargon), `storage_map.md`, `domains.md`
5. **Attach per-person lanes:** for each roster member, seed/refresh `progress-<person>.md`
   and (mentees) a sub-track folder + onboarding scaffold. This is what makes the vault a *team* vault.

Every emitted fact links back to its source artifact (and, for figure values, the
panel crop). No un-cited claims.

## Output
The shared KB vault at the profile's `output.location` (+ a JSON index if `also_json`).

## Next
`/lab-gaps` (audit) · `/lab-ask` (query) · `/lab-standup` (team synthesis).
