"""Deterministic verification gates for blind figure extractions."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from .schema import CHART_TYPES, PanelExtraction, Provenance, Verification

_D3_CHART_TYPES = frozenset(chart for chart in CHART_TYPES if chart != "unknown")
_HARD_FLAGS = frozenset({"broken_axis"})
_COMPARABLE_NUMBER = re.compile(
    r"(?<![\w.])(?P<value>\d+(?:\.\d+)?)\s*(?:-\s*)?"
    r"(?P<unit>%|percent(?:age)?|fold(?:[ -](?:change|increase|decrease))?)"
    r"(?=\s|[.,;:!?)\]]|$)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class _TextComparison:
    agreement: bool | None
    evidence: str = ""
    contradiction: str = ""
    reason: str = ""


def _panel_analyte(
    extraction: PanelExtraction, provenance: Provenance, caption_text: str
) -> str:
    """Infer the analyte named for this panel without reading body prose."""
    panel_id = provenance.panel_id.strip()
    if panel_id:
        marker = re.escape(panel_id)
        panel_pattern = re.compile(
            rf"\b([A-Za-zΑ-Ωα-ω][A-Za-z0-9Α-Ωα-ω]*(?:-[A-Za-z0-9Α-Ωα-ω]+)*"
            rf"(?:\s+gene)?)\s*\(\s*{marker}\s*\)",
            re.IGNORECASE,
        )
        match = panel_pattern.search(caption_text)
        if match:
            return match.group(1).strip()

    gene_match = re.search(
        r"\b([A-Za-z0-9-]+\s+gene)\b", caption_text, flags=re.IGNORECASE
    )
    if gene_match:
        return gene_match.group(1).strip()

    axis_match = re.search(
        r"\b([A-Za-z0-9-]+\s+gene)\b", extraction.y_axis_label, flags=re.IGNORECASE
    )
    if axis_match:
        return axis_match.group(1).strip()

    return extraction.series_label.strip()


def _sentences(text: str) -> list[str]:
    return [
        " ".join(part.split())
        for part in re.split(r"(?:\.{2,}|(?<!\d)[.!?](?!\d))\s*|[\r\n]+", text)
        if part.strip()
    ]


def _find_comparable_number(text: str, analyte: str) -> tuple[float, str] | None:
    if not text.strip() or not analyte.strip():
        return None

    analyte_pattern = re.compile(re.escape(analyte), re.IGNORECASE)
    candidates: list[tuple[int, float, str]] = []
    for sentence in _sentences(text):
        analyte_matches = list(analyte_pattern.finditer(sentence))
        if not analyte_matches:
            continue
        for number_match in _COMPARABLE_NUMBER.finditer(sentence):
            distance = min(
                abs(number_match.start() - analyte_match.start())
                for analyte_match in analyte_matches
            )
            candidates.append((distance, float(number_match.group("value")), sentence))

    if not candidates:
        return None
    _, value, evidence = min(candidates, key=lambda item: item[0])
    return value, evidence


def _compare_to_text(
    extraction: PanelExtraction,
    provenance: Provenance,
    caption_text: str,
    body_text: str,
) -> _TextComparison:
    analyte = _panel_analyte(extraction, provenance, caption_text)
    found = _find_comparable_number(f"{caption_text}\n{body_text}", analyte)
    if found is None:
        label = analyte or "this panel"
        return _TextComparison(
            agreement=None,
            reason=f"No comparable fold or percentage value was stated for {label}.",
        )

    text_value, evidence = found
    figure_value = extraction.peak_value
    if figure_value is None or not math.isfinite(figure_value):
        return _TextComparison(
            agreement=None,
            evidence=evidence,
            reason="Text states a comparable value, but the figure peak is unreadable.",
        )

    if math.isclose(figure_value, text_value, rel_tol=0.0, abs_tol=1e-12):
        ratio = 1.0
    elif figure_value == 0 or text_value == 0:
        ratio = math.inf
    else:
        ratio = max(abs(figure_value), abs(text_value)) / min(
            abs(figure_value), abs(text_value)
        )

    if ratio < 1.5:
        return _TextComparison(
            agreement=True,
            evidence=evidence,
            reason=(
                f"Figure peak {figure_value:g} agrees with the text value "
                f"{text_value:g} (ratio {ratio:.2f}x)."
            ),
        )

    contradiction = (
        f"Figure peak {figure_value:g} conflicts with text value {text_value:g}; "
        f"text evidence: {evidence}"
    )
    return _TextComparison(
        agreement=False,
        evidence=evidence,
        contradiction=contradiction,
        reason=(
            f"Figure peak {figure_value:g} and text value {text_value:g} differ "
            f"by {ratio:.2f}x."
        ),
    )


def verify(
    extraction: PanelExtraction,
    provenance: Provenance,
    caption_text: str = "",
    body_text: str = "",
) -> Verification:
    """Apply the D5 two-tier gate without accepting a model self-verdict."""
    reasons: list[str] = []

    if extraction.y_min is None or extraction.y_max is None:
        axis_consistent = False
        reasons.append("Axis bounds unread.")
    elif extraction.peak_value is None or not math.isfinite(extraction.peak_value):
        axis_consistent = False
        reasons.append("Peak value unread.")
    elif extraction.y_min > extraction.y_max:
        axis_consistent = False
        reasons.append("Axis minimum is greater than axis maximum.")
    else:
        span = extraction.y_max - extraction.y_min
        slack = 0.02 * span
        axis_consistent = (
            extraction.y_min - slack
            <= extraction.peak_value
            <= extraction.y_max + slack
        )
        if axis_consistent:
            reasons.append("Peak lies within the axis bounds (including 2% slack).")
        else:
            reasons.append("Peak falls outside the axis bounds, including 2% slack.")

    text_check = _compare_to_text(
        extraction, provenance, caption_text=caption_text, body_text=body_text
    )
    reasons.append(text_check.reason)

    chart_in_scope = extraction.chart_type in _D3_CHART_TYPES
    if not chart_in_scope:
        reasons.append(f"Chart type '{extraction.chart_type}' is outside D3 scope.")

    confidence_ok = extraction.confidence != "low"
    if not confidence_ok:
        reasons.append("Reader confidence is low.")

    normalized_flags = {
        flag.strip().lower().replace("-", "_") for flag in extraction.flags
    }
    hard_flags = sorted(normalized_flags & _HARD_FLAGS)
    if hard_flags:
        reasons.append(f"Hard review flag present: {', '.join(hard_flags)}.")

    tier = (
        "verified"
        if chart_in_scope
        and axis_consistent
        and confidence_ok
        and text_check.agreement is not False
        and not hard_flags
        else "needs_review"
    )
    if tier == "verified":
        reasons.append("All deterministic verification checks passed.")

    return Verification(
        tier=tier,
        reasons=reasons,
        axis_consistent=axis_consistent,
        text_figure_agreement=text_check.agreement,
        text_evidence=text_check.evidence,
        contradiction=text_check.contradiction,
    )
