"""Obsidian-compatible record and index writing with retained crop evidence."""

from __future__ import annotations

import os
import re
import shutil
import unicodedata
from pathlib import Path

import yaml

from .schema import PanelRecord


def _slug(value: str, limit: int = 64) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")
    return slug[:limit].rstrip("-") or "record"


def _format_number(value: float | None) -> str:
    return "unread" if value is None else f"{value:g}"


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _finding(record: PanelRecord) -> str:
    extraction = record.extraction
    if extraction.peak_value is None:
        return f"{extraction.series_label or 'Series'} peak could not be read reliably."
    location = f" at {extraction.peak_x}" if extraction.peak_x else ""
    unit = next((point.y_unit for point in extraction.points if point.y_unit), "")
    suffix = f" {unit}" if unit else ""
    return (
        f"{extraction.series_label or 'Series'} peaks at "
        f"{extraction.peak_value:g}{suffix}{location}."
    )


def _upsert_index(index_path: Path, record: PanelRecord, record_path: Path) -> None:
    header = (
        "# Figure-reading index\n\n"
        "| Paper | Panel | Peak value | Tier |\n"
        "|---|---|---:|---|\n"
    )
    existing = index_path.read_text(encoding="utf-8") if index_path.is_file() else header
    target = f"papers/{record_path.name}"
    rows = [line for line in existing.splitlines() if f"]({target})" not in line]
    while rows and not rows[-1].strip():
        rows.pop()

    panel = f"{record.provenance.figure_id}{record.provenance.panel_id}"
    peak = _format_number(record.extraction.peak_value)
    row = (
        f"| [{_markdown_cell(record.provenance.title)}]({target}) "
        f"| {_markdown_cell(panel)} | {peak} | {record.verification.tier} |"
    )
    index_path.write_text("\n".join([*rows, row, ""]), encoding="utf-8")


def write_record(record: PanelRecord, vault_dir: str | Path) -> Path:
    """Write or replace one record, copy its crop, and idempotently index it."""
    vault = Path(vault_dir)
    papers_dir = vault / "papers"
    crops_dir = papers_dir / "crops"
    crops_dir.mkdir(parents=True, exist_ok=True)

    paper_slug = _slug(record.provenance.title, limit=48)
    panel_slug = _slug(
        f"{record.provenance.figure_id}{record.provenance.panel_id}", limit=24
    )
    series_slug = _slug(record.extraction.series_label, limit=40)
    stem = f"{paper_slug}-{panel_slug}-{series_slug}"
    record_path = papers_dir / f"{stem}.md"

    source_crop = Path(record.provenance.crop_path)
    if not source_crop.is_file():
        raise FileNotFoundError(f"Panel crop not found: {source_crop}")
    crop_path = crops_dir / f"{stem}.png"
    if source_crop.resolve() != crop_path.resolve():
        temporary_crop = crop_path.with_suffix(".png.part")
        shutil.copyfile(source_crop, temporary_crop)
        os.replace(temporary_crop, crop_path)
    crop_relative = f"crops/{crop_path.name}"

    frontmatter = {
        "doi": record.provenance.doi,
        "license": record.provenance.license,
        "figure": record.provenance.figure_id,
        "panel": record.provenance.panel_id,
        "tier": record.verification.tier,
        "confidence": record.extraction.confidence,
        "source_url": record.provenance.source_url,
        "crop": crop_relative,
    }
    yaml_text = yaml.safe_dump(
        frontmatter, sort_keys=False, allow_unicode=True, default_flow_style=False
    ).strip()
    value_rows = [
        f"| {_markdown_cell(point.x)} | {point.y:g} | {_markdown_cell(point.y_unit)} |"
        for point in record.extraction.points
    ]
    if not value_rows:
        value_rows = ["| — | — | — |"]
    reasons = "\n".join(f"- {reason}" for reason in record.verification.reasons)
    contradiction = ""
    if record.verification.contradiction:
        contradiction = (
            "\n## Text vs figure\n\n"
            f"> **Needs review:** {record.verification.contradiction}\n"
        )

    markdown = (
        f"---\n{yaml_text}\n---\n\n"
        f"# {record.provenance.figure_id}{record.provenance.panel_id}: "
        f"{record.extraction.series_label or 'unlabeled series'}\n\n"
        f"{_finding(record)}\n\n"
        "## Extracted values\n\n"
        f"| {record.extraction.x_axis_label or 'x'} | "
        f"{record.extraction.y_axis_label or 'y'} | Unit |\n"
        "|---|---:|---|\n"
        + "\n".join(value_rows)
        + "\n\n## Verification\n\n"
        f"**{record.verification.tier.upper().replace('_', '-')}**\n\n"
        f"{reasons}\n"
        f"{contradiction}\n"
        "## Audit crop\n\n"
        f"![crop]({crop_relative})\n"
    )
    record_path.write_text(markdown, encoding="utf-8")
    _upsert_index(vault / "_Index.md", record, record_path)
    return record_path
