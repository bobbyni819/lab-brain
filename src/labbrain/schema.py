"""Core data contracts for the lab-brain first build slice.

These dataclasses are the STABLE interface every other module codes against
(fetch -> render -> crop -> extract -> verify -> vault -> report). Keep logic
OUT of this file: types + trivial (de)serialization only. If a field changes
here, it changes for everyone, so treat this as the API.

Design anchors:
- D3 figure scope: chart_type is restricted to bar/box/dose_response/
  kaplan_meier/kinetics (+ "unknown" escape hatch). Anything else is punted.
- D5 verification: every PanelRecord carries a Verification AND a crop_path in
  its Provenance -- the crop is ALWAYS retained so a human can audit the read.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Optional

# --- controlled vocabularies (kept as plain strings for json friendliness) ---
CHART_TYPES = ("bar", "box", "dose_response", "kaplan_meier", "kinetics", "unknown")
VERIFY_TIERS = ("verified", "needs_review")
CONFIDENCE = ("high", "medium", "low")


@dataclass
class Provenance:
    """Where a value came from -- the audit trail. crop_path is mandatory (D5)."""
    doi: str
    title: str
    source_url: str
    license: str            # e.g. "CC-BY-4.0"
    figure_id: str          # "Fig 5"
    panel_id: str           # "b"
    page_index: int         # 0-based PDF page the panel was rendered from
    crop_path: str          # repo-relative path to the panel crop PNG (ALWAYS set)
    pdf_sha256: str


@dataclass
class SeriesPoint:
    x: str                  # "day 2" / "10 uM" / "week 4"
    y: float
    y_unit: str = ""


@dataclass
class PanelExtraction:
    """The blind read of ONE cropped panel. No paper-body text was used."""
    chart_type: str                     # one of CHART_TYPES
    x_axis_label: str
    y_axis_label: str
    y_min: Optional[float]
    y_max: Optional[float]
    series_label: str                   # which bar-group / curve this describes
    points: list[SeriesPoint] = field(default_factory=list)
    peak_value: Optional[float] = None
    peak_x: Optional[str] = None
    confidence: str = "medium"          # one of CONFIDENCE
    reader_notes: str = ""              # honest caveats in prose
    flags: list[str] = field(default_factory=list)  # e.g. broken_axis, busy, log_scale


@dataclass
class Verification:
    """D5 two-tier gate result. tier is computed deterministically in verify.py,
    never taken from the model's self-report."""
    tier: str                           # one of VERIFY_TIERS
    reasons: list[str] = field(default_factory=list)
    axis_consistent: bool = True        # peak within [y_min, y_max]
    text_figure_agreement: Optional[bool] = None  # None => text says nothing comparable
    text_evidence: str = ""             # caption/body snippet compared against
    contradiction: str = ""             # populated only on a real text<->figure clash


@dataclass
class PanelRecord:
    """One panel, end to end: provenance + what was read + how it verified."""
    provenance: Provenance
    extraction: PanelExtraction
    verification: Verification

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @staticmethod
    def from_dict(d: dict) -> "PanelRecord":
        prov = Provenance(**d["provenance"])
        ex = d["extraction"]
        extraction = PanelExtraction(
            **{k: v for k, v in ex.items() if k != "points"},
            points=[SeriesPoint(**p) for p in ex.get("points", [])],
        )
        verification = Verification(**d["verification"])
        return PanelRecord(prov, extraction, verification)

    @staticmethod
    def from_json(s: str) -> "PanelRecord":
        return PanelRecord.from_dict(json.loads(s))
