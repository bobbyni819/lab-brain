from pathlib import Path


def test_real_pdf_fixture_slice_writes_three_records_and_report(tmp_path: Path) -> None:
    from labbrain.slice import run_slice

    repo_root = Path(__file__).resolve().parents[1]
    assert (repo_root / "work" / "gui2017.pdf").exists()
    vault = tmp_path / "demo_vault"
    report = tmp_path / "examples" / "gui2017" / "figure_report.html"

    records = run_slice(
        paper_key="gui2017",
        provider_name="fixture",
        vault_dir=vault,
        report_path=report,
        fixtures_dir=repo_root / "tests" / "fixtures",
    )

    record_files = list((vault / "papers").glob("*.md"))
    html = report.read_text(encoding="utf-8")
    tnf = next(
        record
        for record in records
        if record.provenance.figure_id == "Fig5"
        and record.provenance.panel_id == "b"
    )
    il6 = next(
        record
        for record in records
        if record.provenance.figure_id == "Fig5"
        and record.provenance.panel_id == "a"
    )
    m_gene = next(record for record in records if record.provenance.figure_id == "Fig4")

    assert len(records) == 3
    assert len(record_files) == 3
    assert report.exists()
    assert "VERIFIED" in html
    assert "NEEDS-REVIEW" in html
    assert "data:image/png;base64," in html
    assert tnf.verification.tier == "verified"
    assert tnf.verification.text_figure_agreement is None
    assert il6.verification.tier == "needs_review"
    assert "5.6" in il6.verification.contradiction
    assert m_gene.verification.tier == "needs_review"
    assert "broken_axis" in m_gene.extraction.flags
