---
name: lab-ask
description: The newcomer's day-one interface — answer a natural-language question grounded in the lab's registry/vault, with citations back to the exact source artifact (and figure-panel crop for figure-only values). Use when the user asks a question about the lab's knowledge, or says "lab-ask", "what does the lab know about X", "which datasets does project Y use".
---

# /lab-ask "<question>" — grounded retrieval over the lab brain

The interface a new member uses on day one. Every answer is cited.

## Do this
1. Load the vault + `registry/` (records, catalogs, cross-link indices).
2. Retrieve the relevant artifacts for the question (use the graph: person→artifacts,
   dataset→artifacts, method→papers, project→everything).
3. **Answer grounded** — synthesize from the retrieved records only. For every claim,
   cite the source artifact (`path` / DOI). For a figure-only value (a number that
   lives in a panel, not the text), cite the paper **and show/link the panel crop**.
4. If the registry doesn't support an answer, say so and point to `/lab-gaps` — never
   fabricate. Honesty is the whole ethic.

## Example
```
/lab-ask "what datasets does the flu project use, and who owns them?"
→ answer lists each dataset, its storage location + provenance, the code that reads it,
  and the owner — each line linking to the artifact record it came from.
```

## Role-aware answers
`mentee` askers get more explanatory answers + "start-here" pointers; `maintainer`
/ `pi` get terser, denser answers. Role comes from the roster.

## Output
A cited answer in chat (and optionally appended to `Sources/qa-<date>.md` for the team).
