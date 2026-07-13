"""Alex's thin wrapper around the labbrain slice for the flu cytokine panels.

Reads the configured panels for a paper and prints a verified value per panel.
(Demo artifact for the example vault — shows a mentee building on the shared package,
not reinventing it. See framework/figures-and-findings.md: restyle/reuse, don't reinvent.)
"""
from __future__ import annotations

import argparse

from labbrain.slice import run_slice


def main() -> int:
    ap = argparse.ArgumentParser(description="Read the flu cytokine panels via the labbrain slice.")
    ap.add_argument("--paper", default="gui2017")
    ap.add_argument("--provider", default="fixture", help="fixture | anthropic | hostllm")
    ap.add_argument("--vault", default="demo_vault")
    args = ap.parse_args()

    records = run_slice(
        paper_key=args.paper,
        provider_name=args.provider,
        vault_dir=args.vault,
        report_path=f"{args.vault}/figure_report.html",
    )
    for r in records:
        v = r.verification
        print(f"{r.provenance.figure_id}{r.provenance.panel_id}: "
              f"peak={r.extraction.peak_value} -> {v.tier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
