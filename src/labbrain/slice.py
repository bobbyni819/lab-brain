"""End-to-end CLI for the first auditable figure-reading build slice."""

from __future__ import annotations

import argparse
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Sequence

from .crop import crop_panel
from .extract import extract_panel
from .fetch import PAPERS, FetchedPaper, fetch_oa_pdf
from .providers import VisionProvider, get_provider
from .render import render_page
from .report import build_report
from .schema import PanelRecord, Provenance
from .vault import write_record
from .verify import verify

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _slug(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _audit_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(_REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return str(resolved)


def _read_panel(
    panel: dict[str, Any],
    paper: dict[str, Any],
    fetched: FetchedPaper,
    rendered_pages: dict[int, Path],
    crop_dir: Path,
    provider: VisionProvider,
) -> PanelRecord:
    figure_id = str(panel.get("figure_id", ""))
    panel_id = str(panel.get("panel_id", ""))
    page_index = int(panel["page_index"])
    artifact_stem = f"{_slug(figure_id)}_{_slug(panel_id)}"
    crop_path = crop_dir / f"{artifact_stem}.png"
    crop_panel(rendered_pages[page_index], panel["bbox"], crop_path)

    caption = str(paper.get("captions", {}).get(figure_id, ""))
    context = {
        "caption": caption,
        "figure_id": figure_id,
        "panel_id": panel_id,
        "analyte": str(panel.get("analyte", "")),
        "series_hint": str(panel.get("series_hint", "")),
        "chart_type_hint": str(panel.get("chart_type_hint", "")),
        "y_axis_hint": str(panel.get("y_axis_hint", "")),
    }
    extraction = extract_panel(str(crop_path), context, provider)
    provenance = Provenance(
        doi=fetched.doi,
        title=fetched.title,
        source_url=fetched.source_url,
        license=fetched.license,
        figure_id=figure_id,
        panel_id=panel_id,
        page_index=page_index,
        crop_path=_audit_path(crop_path),
        pdf_sha256=fetched.pdf_sha256,
    )
    verification = verify(
        extraction,
        provenance,
        caption_text=caption,
        body_text=str(paper.get("body_text", "")),
    )
    return PanelRecord(provenance, extraction, verification)


def _print_summary(records: Sequence[PanelRecord]) -> None:
    headings = ("Panel", "Peak", "Tier")
    rows = [
        (
            f"{record.provenance.figure_id}{record.provenance.panel_id}",
            "unread"
            if record.extraction.peak_value is None
            else f"{record.extraction.peak_value:g}",
            record.verification.tier,
        )
        for record in records
    ]
    widths = [
        max(len(headings[index]), *(len(row[index]) for row in rows))
        for index in range(len(headings))
    ]
    print("  ".join(value.ljust(widths[index]) for index, value in enumerate(headings)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)))


def run_slice(
    paper_key: str = "gui2017",
    provider_name: str = "fixture",
    vault_dir: str | Path = "demo_vault",
    report_path: str | Path = "examples/gui2017/figure_report.html",
    fixtures_dir: str | Path | None = None,
) -> list[PanelRecord]:
    """Run the configured paper through fetch, read, verify, vault, and report."""
    if paper_key not in PAPERS:
        available = ", ".join(sorted(PAPERS)) or "none"
        raise KeyError(f"Unknown paper '{paper_key}'. Configured papers: {available}")
    paper = PAPERS[paper_key]
    panels = paper.get("panels", [])
    if not isinstance(panels, list) or not panels:
        raise RuntimeError(f"Paper '{paper_key}' has no configured panels.")

    vault = Path(vault_dir)
    artifacts = vault / "_labbrain"
    fetched = fetch_oa_pdf(paper_key, artifacts / "pdf")
    provider = get_provider(
        provider_name,
        fixtures_dir=fixtures_dir or (_REPO_ROOT / "tests" / "fixtures"),
    )

    rendered_pages: dict[int, Path] = {}
    for page_index in sorted({int(panel["page_index"]) for panel in panels}):
        page_path = artifacts / "pages" / f"page_{page_index:03d}.png"
        render_page(fetched.local_pdf_path, page_index, page_path)
        rendered_pages[page_index] = page_path

    worker_count = len(panels)
    print(f"spawned {worker_count} panel-readers")
    crop_dir = artifacts / "crops"
    with ThreadPoolExecutor(
        max_workers=worker_count, thread_name_prefix="panel-reader"
    ) as executor:
        futures = [
            executor.submit(
                _read_panel,
                panel,
                paper,
                fetched,
                rendered_pages,
                crop_dir,
                provider,
            )
            for panel in panels
        ]
        records = [future.result() for future in futures]

    for record in records:
        write_record(record, vault)

    build_report(
        records,
        {
            "title": fetched.title,
            "doi": fetched.doi,
            "license": fetched.license,
            "provider": provider.name,
            "worker_count": worker_count,
        },
        report_path,
    )
    _print_summary(records)
    return records


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="labbrain",
        description="Read configured scientific figure panels with retained provenance.",
    )
    parser.add_argument("--paper", default="gui2017", help="paper key in papers.yaml")
    parser.add_argument(
        "--provider",
        default="fixture",
        choices=("auto", "fixture", "hostllm", "anthropic"),
        help="vision provider (fixture is deterministic and offline)",
    )
    parser.add_argument("--vault", default="demo_vault", help="output vault directory")
    parser.add_argument(
        "--report",
        default="examples/gui2017/figure_report.html",
        help="self-contained HTML report path",
    )
    parser.add_argument(
        "--fixtures-dir",
        default=str(_REPO_ROOT / "tests" / "fixtures"),
        help=argparse.SUPPRESS,
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        run_slice(
            paper_key=args.paper,
            provider_name=args.provider,
            vault_dir=args.vault,
            report_path=args.report,
            fixtures_dir=args.fixtures_dir,
        )
    except Exception as exc:
        print(f"labbrain: error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
