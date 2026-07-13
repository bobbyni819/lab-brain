"""Configured fractional panel cropping for rendered page images."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Sequence

from PIL import Image


def crop_panel(
    page_png: str | Path,
    bbox_frac: Sequence[float],
    out_path: str | Path,
) -> str:
    """Crop a fractional (x0, y0, x1, y1) box and save a tight PNG."""
    if len(bbox_frac) != 4:
        raise ValueError("bbox_frac must contain exactly four values")
    try:
        x0, y0, x1, y1 = (float(value) for value in bbox_frac)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("bbox_frac values must be finite numbers") from exc
    if not all(math.isfinite(value) and 0 <= value <= 1 for value in (x0, y0, x1, y1)):
        raise ValueError("bbox_frac values must lie in [0, 1]")
    if x0 >= x1 or y0 >= y1:
        raise ValueError("bbox_frac must have x0 < x1 and y0 < y1")

    source = Path(page_png)
    destination = Path(out_path)
    if not source.is_file():
        raise FileNotFoundError(f"Rendered page not found: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as image:
        width, height = image.size
        left = max(0, min(width - 1, round(x0 * width)))
        upper = max(0, min(height - 1, round(y0 * height)))
        right = max(left + 1, min(width, round(x1 * width)))
        lower = max(upper + 1, min(height, round(y1 * height)))
        cropped = image.crop((left, upper, right, lower))
        try:
            cropped.save(destination, format="PNG")
        finally:
            cropped.close()
    return str(destination)
