from pathlib import Path

from PIL import Image

from labbrain.schema import (
    PanelExtraction,
    PanelRecord,
    Provenance,
    SeriesPoint,
    Verification,
)


def _record(crop_path: Path) -> PanelRecord:
    return PanelRecord(
        provenance=Provenance(
            doi="10.1186/s12985-017-0683-y",
            title="Example figure-reading paper",
            source_url="https://doi.org/10.1186/s12985-017-0683-y",
            license="CC-BY-4.0",
            figure_id="Fig5",
            panel_id="b",
            page_index=8,
            crop_path=str(crop_path),
            pdf_sha256="abc123",
        ),
        extraction=PanelExtraction(
            chart_type="bar",
            x_axis_label="Day",
            y_axis_label="Fold Change",
            y_min=0,
            y_max=35,
            series_label="Infected control",
            points=[SeriesPoint("day 2", 29, "fold")],
            peak_value=29,
            peak_x="day 2",
            confidence="high",
        ),
        verification=Verification(
            tier="verified",
            reasons=["All deterministic verification checks passed."],
            axis_consistent=True,
        ),
    )


def test_write_record_creates_auditable_markdown_crop_and_index(tmp_path: Path) -> None:
    from labbrain.vault import write_record

    crop = tmp_path / "source_crop.png"
    Image.new("RGB", (12, 8), "white").save(crop)
    vault = tmp_path / "vault"

    md_path = write_record(_record(crop), vault)
    first_index = (vault / "_Index.md").read_text(encoding="utf-8")
    write_record(_record(crop), vault)

    markdown = md_path.read_text(encoding="utf-8")
    index = (vault / "_Index.md").read_text(encoding="utf-8")
    copied_crops = list((vault / "papers" / "crops").glob("*.png"))

    assert md_path.exists()
    assert copied_crops and copied_crops[0].read_bytes() == crop.read_bytes()
    assert "10.1186/s12985-017-0683-y" in markdown
    assert "![crop](crops/" in markdown
    assert "verified" in markdown.lower()
    assert "Fig5b" in index
    assert index == first_index

