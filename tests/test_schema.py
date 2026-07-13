from labbrain.schema import (
    PanelExtraction,
    PanelRecord,
    Provenance,
    SeriesPoint,
    Verification,
)


def test_panel_record_json_round_trip_is_lossless() -> None:
    record = PanelRecord(
        provenance=Provenance(
            doi="10.1234/example",
            title="Example paper",
            source_url="https://example.test/paper",
            license="CC-BY-4.0",
            figure_id="Fig5",
            panel_id="b",
            page_index=8,
            crop_path="artifacts/fig5_b.png",
            pdf_sha256="abc123",
        ),
        extraction=PanelExtraction(
            chart_type="bar",
            x_axis_label="Day",
            y_axis_label="Fold change",
            y_min=0.0,
            y_max=35.0,
            series_label="Infected control",
            points=[SeriesPoint("day 2", 29.0, "fold")],
            peak_value=29.0,
            peak_x="day 2",
            confidence="high",
            reader_notes="Clear panel.",
            flags=[],
        ),
        verification=Verification(
            tier="verified",
            reasons=["Peak lies within the reported axis bounds."],
            axis_consistent=True,
            text_figure_agreement=None,
        ),
    )

    assert PanelRecord.from_json(record.to_json()).to_dict() == record.to_dict()

