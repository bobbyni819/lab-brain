"""Normalization boundary between vision providers and the fixed schema."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import asdict, is_dataclass
from typing import Any

from .schema import CHART_TYPES, CONFIDENCE, PanelExtraction, SeriesPoint

_MAX_POINTS = 500


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if is_dataclass(value):
        return asdict(value)
    if value is None:
        return {}
    names = (
        "chart_type",
        "x_axis_label",
        "y_axis_label",
        "y_min",
        "y_max",
        "series_label",
        "points",
        "peak_value",
        "peak_x",
        "confidence",
        "reader_notes",
        "flags",
    )
    return {name: getattr(value, name) for name in names if hasattr(value, name)}


def _text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def _number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if math.isfinite(number) else None


def _points(raw_points: Any) -> list[SeriesPoint]:
    if isinstance(raw_points, (str, bytes, bytearray)) or not isinstance(
        raw_points, Sequence
    ):
        return []
    points: list[SeriesPoint] = []
    for raw_point in raw_points[:_MAX_POINTS]:
        point = _mapping(raw_point)
        y_value = _number(point.get("y"))
        if y_value is None:
            continue
        points.append(
            SeriesPoint(
                x=_text(point.get("x")),
                y=y_value,
                y_unit=_text(point.get("y_unit")),
            )
        )
    return points


def _flags(raw_flags: Any) -> list[str]:
    if isinstance(raw_flags, str):
        values = [raw_flags]
    elif isinstance(raw_flags, Sequence):
        values = list(raw_flags)
    else:
        values = []
    flags: list[str] = []
    for value in values:
        normalized = _text(value).lower().replace("-", "_").replace(" ", "_")
        if normalized and normalized not in flags:
            flags.append(normalized)
    return flags


def _coerce_extraction(raw: Any) -> PanelExtraction:
    payload = _mapping(raw)
    chart_type = (
        _text(payload.get("chart_type"), "unknown")
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )
    if chart_type not in CHART_TYPES:
        chart_type = "unknown"

    confidence = _text(payload.get("confidence"), "medium").lower()
    if confidence not in CONFIDENCE:
        confidence = "medium"

    points = _points(payload.get("points", []))
    peak_value = _number(payload.get("peak_value"))
    peak_x_value = payload.get("peak_x")
    peak_x = _text(peak_x_value) if peak_x_value is not None else None
    if peak_value is None and points:
        peak_point = max(points, key=lambda point: point.y)
        peak_value = peak_point.y
        peak_x = peak_point.x

    return PanelExtraction(
        chart_type=chart_type,
        x_axis_label=_text(payload.get("x_axis_label")),
        y_axis_label=_text(payload.get("y_axis_label")),
        y_min=_number(payload.get("y_min")),
        y_max=_number(payload.get("y_max")),
        series_label=_text(payload.get("series_label")),
        points=points,
        peak_value=peak_value,
        peak_x=peak_x,
        confidence=confidence,
        reader_notes=_text(payload.get("reader_notes")),
        flags=_flags(payload.get("flags", [])),
    )


def extract_panel(image_path: str, context: dict, provider: Any) -> PanelExtraction:
    """Delegate the blind read, then safely coerce a slightly-off payload."""
    raw = provider.extract_panel(image_path, context)
    return _coerce_extraction(raw)
