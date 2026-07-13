"""PDF page rendering via pypdfium2."""

from __future__ import annotations

from pathlib import Path

import pypdfium2 as pdfium


def render_page(
    pdf_path: str | Path,
    page_index: int,
    out_path: str | Path,
    scale: float = 3.05,
) -> str:
    """Render one zero-based PDF page to a PNG at approximately 220 DPI."""
    if page_index < 0:
        raise ValueError("page_index must be zero or greater")
    if scale <= 0:
        raise ValueError("scale must be positive")

    source = Path(pdf_path)
    destination = Path(out_path)
    if not source.is_file():
        raise FileNotFoundError(f"PDF not found: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)

    document = pdfium.PdfDocument(str(source))
    try:
        if page_index >= len(document):
            raise IndexError(
                f"Page index {page_index} is outside PDF with {len(document)} pages."
            )
        page = document[page_index]
        bitmap = None
        try:
            bitmap = page.render(scale=scale)
            image = bitmap.to_pil()
            image.save(destination, format="PNG")
            image.close()
        finally:
            if bitmap is not None:
                bitmap.close()
            page.close()
    finally:
        document.close()
    return str(destination)

