from dataclasses import replace
from pathlib import Path

import pytest

from labbrain.schema import PanelExtraction, Provenance, SeriesPoint


CAPTION_FIG5 = (
    "Expression of pro-inflammatory and antiviral cytokines. "
    "IL-6 (a), TNF-a (b), IL-2 (c), IL-4 (d), IFN-b (e)."
)
BODY = (
    "The levels of IL-6 were upregulated up to 5.6 fold in "
    "calcitriol-treated infected mice at 4 days post-infection."
)


def _provenance(figure: str, panel: str) -> Provenance:
    return Provenance(
        doi="10.1186/s12985-017-0683-y",
        title="Gui et al. 2017",
        source_url="https://doi.org/10.1186/s12985-017-0683-y",
        license="CC-BY-4.0",
        figure_id=figure,
        panel_id=panel,
        page_index=8,
        crop_path="crop.png",
        pdf_sha256="hash",
    )


def _extraction(
    *,
    peak: float = 29.0,
    y_max: float = 35.0,
    confidence: str = "high",
    flags: list[str] | None = None,
    series: str = "Infected control",
) -> PanelExtraction:
    return PanelExtraction(
        chart_type="bar",
        x_axis_label="Days post infection",
        y_axis_label="Fold Change",
        y_min=0.0,
        y_max=y_max,
        series_label=series,
        points=[SeriesPoint("day 2", peak, "fold")],
        peak_value=peak,
        peak_x="day 2",
        confidence=confidence,
        flags=flags or [],
    )


def test_tnf_figure_only_peak_is_verified() -> None:
    from labbrain.verify import verify

    result = verify(_extraction(), _provenance("Fig5", "b"), CAPTION_FIG5, BODY)

    assert result.tier == "verified"
    assert result.axis_consistent is True
    assert result.text_figure_agreement is None
    assert result.contradiction == ""
    assert result.reasons


def test_il6_text_figure_contradiction_needs_review() -> None:
    from labbrain.verify import verify

    extraction = _extraction(
        peak=500.0,
        y_max=600.0,
        series="Calcitriol-treated infected",
    )
    result = verify(extraction, _provenance("Fig5", "a"), CAPTION_FIG5, BODY)

    assert result.tier == "needs_review"
    assert result.text_figure_agreement is False
    assert "500" in result.contradiction
    assert "5.6" in result.contradiction
    assert "IL-6" in result.text_evidence


def test_broken_axis_needs_review() -> None:
    from labbrain.verify import verify

    extraction = _extraction(peak=3900.0, y_max=5000.0, flags=["broken_axis"])
    result = verify(
        extraction,
        _provenance("Fig4", ""),
        "Expression of the H9N2 M gene. Note the broken y-axis.",
        BODY,
    )

    assert result.tier == "needs_review"
    assert any("broken_axis" in reason for reason in result.reasons)


def test_percentage_text_value_is_comparable() -> None:
    from labbrain.verify import verify

    extraction = _extraction(peak=50.0, y_max=100.0)
    result = verify(
        extraction,
        _provenance("Fig5", "a"),
        CAPTION_FIG5,
        "IL-6 increased by 50% after treatment.",
    )

    assert result.tier == "verified"
    assert result.text_figure_agreement is True
    assert "50%" in result.text_evidence


@pytest.mark.parametrize(
    ("extraction", "reason_fragment"),
    [
        (_extraction(peak=40.0, y_max=35.0), "outside"),
        (_extraction(confidence="low"), "low"),
        (replace(_extraction(), y_min=None), "axis bounds unread"),
    ],
)
def test_gate_rejects_unverifiable_reads(
    extraction: PanelExtraction, reason_fragment: str
) -> None:
    from labbrain.verify import verify

    result = verify(extraction, _provenance("Fig5", "b"), CAPTION_FIG5, BODY)

    assert result.tier == "needs_review"
    assert any(reason_fragment in reason.lower() for reason in result.reasons)


def test_fixture_provider_and_extractor_coerce_payload(tmp_path: Path) -> None:
    from labbrain.extract import extract_panel
    from labbrain.providers import FixtureProvider

    fixture = tmp_path / "fig1_a.json"
    fixture.write_text(
        '{"chart_type":"scatter","x_axis_label":1,"y_axis_label":"Y",'
        '"y_min":"0","y_max":"10","series_label":"S",'
        '"points":[{"x":2,"y":"7.5"}],"confidence":"certain",'
        '"flags":"busy"}',
        encoding="utf-8",
    )
    result = extract_panel(
        "unused.png",
        {"figure_id": "Fig1", "panel_id": "a"},
        FixtureProvider(tmp_path),
    )

    assert result.chart_type == "unknown"
    assert result.y_min == 0.0
    assert result.points[0].y == 7.5
    assert result.confidence == "medium"
    assert result.flags == ["busy"]


def test_auto_provider_falls_back_to_fixture_without_host_or_key(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from labbrain import providers

    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(providers, "_host_llm_available", lambda: False)

    selected = providers.get_provider("auto", fixtures_dir=tmp_path)

    assert isinstance(selected, providers.FixtureProvider)
