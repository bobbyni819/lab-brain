"""Portable, self-contained HTML report for a figure-reading run."""

from __future__ import annotations

import base64
import html
from pathlib import Path
from typing import Any

from .schema import PanelRecord


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _number(value: float | None) -> str:
    return "unread" if value is None else f"{value:g}"


def _data_uri(path_value: str) -> str:
    path = Path(path_value)
    if not path.is_file():
        raise FileNotFoundError(f"Cannot embed missing crop: {path}")
    media_type = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{media_type};base64,{payload}"


def _pipeline_svg() -> str:
    stages = ("fetch", "render", "crop", "extract", "verify", "vault")
    stage_width = 104
    gap = 28
    boxes: list[str] = []
    arrows: list[str] = []
    for index, stage in enumerate(stages):
        x = 8 + index * (stage_width + gap)
        boxes.append(
            f'<g transform="translate({x},8)">'
            f'<rect width="{stage_width}" height="44" rx="10" class="pipe-box"/>'
            f'<text x="{stage_width / 2:g}" y="27" text-anchor="middle">'
            f"{stage}</text></g>"
        )
        if index < len(stages) - 1:
            start = x + stage_width + 5
            end = x + stage_width + gap - 5
            arrows.append(
                f'<path d="M {start} 30 H {end}" class="pipe-arrow" '
                f'marker-end="url(#arrow)"/>'
            )
    width = 16 + len(stages) * stage_width + (len(stages) - 1) * gap
    return (
        f'<svg class="pipeline" viewBox="0 0 {width} 60" role="img" '
        'aria-label="fetch, render, crop, extract, verify, vault">'
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" class="arrow-head"/></marker></defs>'
        + "".join(arrows)
        + "".join(boxes)
        + "</svg>"
    )


def _values_table(record: PanelRecord) -> str:
    rows = "".join(
        "<tr>"
        f"<td>{_escape(point.x)}</td>"
        f"<td class=\"numeric\">{_number(point.y)}</td>"
        f"<td>{_escape(point.y_unit)}</td>"
        "</tr>"
        for point in record.extraction.points
    )
    if not rows:
        rows = '<tr><td colspan="3" class="muted">No readable points</td></tr>'
    return (
        '<div class="table-wrap"><table><thead><tr>'
        f"<th>{_escape(record.extraction.x_axis_label or 'x')}</th>"
        f"<th>{_escape(record.extraction.y_axis_label or 'y')}</th>"
        "<th>Unit</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></div>"
    )


def _card(record: PanelRecord) -> str:
    extraction = record.extraction
    verification = record.verification
    status = verification.tier.upper().replace("_", "-")
    panel = f"{record.provenance.figure_id}{record.provenance.panel_id}"
    reasons = "".join(f"<li>{_escape(reason)}</li>" for reason in verification.reasons)
    flags = (
        ""
        if not extraction.flags
        else '<p class="flags"><strong>Flags:</strong> '
        + _escape(", ".join(extraction.flags))
        + "</p>"
    )
    contradiction = (
        ""
        if not verification.contradiction
        else '<aside class="contradiction"><strong>Text vs figure</strong><p>'
        + _escape(verification.contradiction)
        + "</p></aside>"
    )
    reader_notes = (
        ""
        if not extraction.reader_notes
        else f'<p class="reader-notes">{_escape(extraction.reader_notes)}</p>'
    )
    return f"""
      <article class="panel-card {verification.tier}">
        <div class="crop-column">
          <img class="crop" src="{_data_uri(record.provenance.crop_path)}"
               alt="Audit crop for {_escape(panel)}">
          <p class="provenance">Page {record.provenance.page_index + 1} ·
             <code>{_escape(record.provenance.crop_path)}</code></p>
        </div>
        <div class="reading-column">
          <div class="card-heading">
            <div><p class="eyebrow">{_escape(panel)} · {_escape(extraction.chart_type)}</p>
              <h2>{_escape(extraction.series_label or 'Unlabeled series')}</h2></div>
            <span class="badge {verification.tier}">{status}</span>
          </div>
          <div class="stats">
            <div><span>Peak</span><strong>{_number(extraction.peak_value)}</strong>
              <small>{_escape(extraction.peak_x or 'x unread')}</small></div>
            <div><span>Confidence</span><strong>{_escape(extraction.confidence)}</strong>
              <small>reader estimate</small></div>
            <div><span>Axis</span><strong>{_number(extraction.y_min)}–{_number(extraction.y_max)}</strong>
              <small>{_escape(extraction.y_axis_label or 'label unread')}</small></div>
          </div>
          {_values_table(record)}
          {reader_notes}{flags}{contradiction}
          <details><summary>Verification reasons</summary><ul>{reasons}</ul></details>
        </div>
      </article>
    """


def build_report(
    records: list[PanelRecord], run_meta: dict[str, Any], out_path: str | Path
) -> Path:
    """Build one responsive report with inline CSS, SVG, and base64 crops."""
    destination = Path(out_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    verified = sum(record.verification.tier == "verified" for record in records)
    needs_review = len(records) - verified
    title = run_meta.get("title") or (records[0].provenance.title if records else "Paper")
    doi = run_meta.get("doi") or (records[0].provenance.doi if records else "")
    license_name = run_meta.get("license") or (
        records[0].provenance.license if records else ""
    )
    provider = run_meta.get("provider", "unknown")
    worker_count = run_meta.get("worker_count", len(records))
    cards = "".join(_card(record) for record in records)

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Figure-reading report · {_escape(doi)}</title>
  <style>
    :root {{ color-scheme: light dark; --bg:#f4f1ea; --surface:#fffdf8;
      --surface-2:#ebe7dd; --ink:#17211e; --muted:#66716d; --line:#d6d1c7;
      --accent:#144f45; --verified:#237a57; --verified-bg:#dff3e7;
      --review:#a45d05; --review-bg:#fff0cf; --shadow:0 14px 40px rgba(26,40,35,.10); }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--ink); font-family:Inter,ui-sans-serif,
      system-ui,-apple-system,"Segoe UI",sans-serif; line-height:1.5; }}
    main {{ width:min(1180px,calc(100% - 32px)); margin:0 auto; padding:54px 0 72px; }}
    .hero {{ display:grid; grid-template-columns:minmax(0,1fr) auto; gap:32px;
      align-items:end; padding-bottom:30px; border-bottom:1px solid var(--line); }}
    .kicker,.eyebrow {{ margin:0 0 8px; color:var(--accent); font-size:.73rem; font-weight:800;
      letter-spacing:.12em; text-transform:uppercase; }}
    h1 {{ max-width:850px; margin:0; font-family:Georgia,"Times New Roman",serif;
      font-size:clamp(2rem,4.5vw,4rem); font-weight:500; line-height:1.04; letter-spacing:-.025em; }}
    .citation {{ margin:18px 0 0; color:var(--muted); }}
    .run-summary {{ display:grid; grid-template-columns:repeat(3,minmax(92px,1fr)); gap:9px; }}
    .metric {{ min-width:96px; padding:14px; border:1px solid var(--line); border-radius:14px;
      background:var(--surface); }}
    .metric strong {{ display:block; font-size:1.55rem; }} .metric span {{ color:var(--muted); font-size:.74rem; }}
    .run-meta {{ margin:22px 0 0; color:var(--muted); font-size:.88rem; }}
    .pipeline-wrap {{ margin:30px 0 38px; padding:18px 22px; overflow-x:auto;
      border:1px solid var(--line); border-radius:18px; background:var(--surface); }}
    .pipeline {{ display:block; min-width:760px; width:100%; height:auto; }}
    .pipe-box {{ fill:var(--surface-2); stroke:var(--line); }} .pipeline text {{ fill:var(--ink);
      font:700 14px Inter,system-ui,sans-serif; }} .pipe-arrow {{ stroke:var(--muted); stroke-width:1.5; }}
    .arrow-head {{ fill:var(--muted); }}
    .panels {{ display:grid; gap:24px; }}
    .panel-card {{ display:grid; grid-template-columns:minmax(280px,.85fr) minmax(0,1.15fr);
      overflow:hidden; border:1px solid var(--line); border-top:4px solid var(--review);
      border-radius:22px; background:var(--surface); box-shadow:var(--shadow); }}
    .panel-card.verified {{ border-top-color:var(--verified); }}
    .crop-column {{ padding:22px; background:var(--surface-2); }}
    .crop {{ display:block; width:100%; max-height:440px; object-fit:contain; border-radius:12px;
      background:#fff; box-shadow:0 3px 14px rgba(0,0,0,.14); }}
    .provenance {{ margin:13px 0 0; color:var(--muted); font-size:.72rem; overflow-wrap:anywhere; }}
    code {{ font-family:"SFMono-Regular",Consolas,monospace; }}
    .reading-column {{ padding:28px 30px 30px; }}
    .card-heading {{ display:flex; justify-content:space-between; gap:18px; align-items:flex-start; }}
    h2 {{ margin:0; font-family:Georgia,"Times New Roman",serif; font-size:clamp(1.55rem,2.5vw,2.25rem);
      font-weight:500; line-height:1.15; }}
    .badge {{ flex:none; padding:7px 11px; border-radius:999px; background:var(--review-bg);
      color:var(--review); font-size:.72rem; font-weight:900; letter-spacing:.065em; }}
    .badge.verified {{ background:var(--verified-bg); color:var(--verified); }}
    .stats {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:24px 0; }}
    .stats div {{ padding:13px 14px; border:1px solid var(--line); border-radius:12px; }}
    .stats span,.stats small {{ display:block; color:var(--muted); font-size:.7rem; }}
    .stats strong {{ display:block; margin:2px 0; font-size:1.05rem; }}
    .table-wrap {{ overflow-x:auto; }} table {{ width:100%; border-collapse:collapse; font-size:.86rem; }}
    th,td {{ padding:9px 10px; border-bottom:1px solid var(--line); text-align:left; }}
    th {{ color:var(--muted); font-size:.69rem; letter-spacing:.05em; text-transform:uppercase; }}
    .numeric {{ font-variant-numeric:tabular-nums; text-align:right; }} .muted {{ color:var(--muted); }}
    .reader-notes,.flags {{ color:var(--muted); font-size:.84rem; }}
    .contradiction {{ margin-top:18px; padding:14px 16px; border-left:4px solid var(--review);
      border-radius:8px; background:var(--review-bg); color:#5e3706; }}
    .contradiction p {{ margin:5px 0 0; }} details {{ margin-top:16px; font-size:.84rem; }}
    summary {{ cursor:pointer; font-weight:700; }} li+li {{ margin-top:5px; }}
    @media (max-width:820px) {{ .hero,.panel-card {{ grid-template-columns:1fr; }}
      .run-summary {{ grid-template-columns:repeat(3,1fr); }} .crop-column {{ max-height:none; }} }}
    @media (max-width:540px) {{ main {{ width:min(100% - 20px,1180px); padding-top:28px; }}
      .run-summary,.stats {{ grid-template-columns:1fr; }} .reading-column,.crop-column {{ padding:18px; }} }}
    @media (prefers-color-scheme:dark) {{ :root {{ --bg:#111816; --surface:#18211e;
      --surface-2:#202b27; --ink:#ecf1ee; --muted:#aab8b2; --line:#34423d; --accent:#79c9b4;
      --verified:#85d7ad; --verified-bg:#183d2e; --review:#ffc56d; --review-bg:#473218;
      --shadow:0 16px 45px rgba(0,0,0,.28); }} .contradiction {{ color:#ffe1ac; }} }}
  </style>
</head>
<body>
  <main>
    <header class="hero">
      <div><p class="kicker">Lab Brain · auditable figure reading</p>
        <h1>{_escape(title)}</h1>
        <p class="citation">DOI {_escape(doi)} · {_escape(license_name)}</p></div>
      <div class="run-summary">
        <div class="metric"><strong>{len(records)}</strong><span>panels</span></div>
        <div class="metric"><strong>{verified}</strong><span>verified</span></div>
        <div class="metric"><strong>{needs_review}</strong><span>needs review</span></div>
      </div>
    </header>
    <p class="run-meta">Provider: <strong>{_escape(provider)}</strong> ·
      Workers: <strong>{_escape(worker_count)}</strong></p>
    <section class="pipeline-wrap" aria-label="Pipeline">{_pipeline_svg()}</section>
    <section class="panels" aria-label="Panel reads">{cards}</section>
  </main>
</body>
</html>
"""
    destination.write_text(document, encoding="utf-8")
    return destination
