# messy-lab-dump — a tiny "before" for the ingestion demo

A small, deliberately messy lab folder — mixed file types, cryptic names, a stray duplicate, and a
non-project (admin) subfolder — so you can watch Lab Brain sort it. Run:

```bash
python -m labbrain.lab_scan --root examples/messy-lab-dump \
       --profile lab-profile.example.yaml --out examples/messy-lab-dump-scan
```

The result (see [`../messy-lab-dump-scan/SCAN_REPORT.md`](../messy-lab-dump-scan/SCAN_REPORT.md)):
**12 files → 8 content areas · 1 duplicate caught** (`raw_counts.csv` appears twice) **· the
`Admin/` folder excluded** (a domain rule for non-project material) **· the `~$…` temp file skipped.**

Notes: the office-type files (`.docx/.pptx/.xlsx`) are tiny text stubs — the *structural* scan
classifies by type and never opens them; the *semantic* swarm (an LLM step) is what reads their
contents and resolves the cryptic `1002732.pdf` (a copy of the CC-BY Gui 2017 paper) to its real
title. This folder shows the cheap Layer-0 sort; the interactive `docs/showcase.html` shows what each
file's specialist reader then extracts and where it lands in the KB.
