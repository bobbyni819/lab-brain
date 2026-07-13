"""License-gated resolution and download of configured open-access papers."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
import yaml

_REPO_ROOT = Path(__file__).resolve().parents[2]
_PAPERS_PATH = _REPO_ROOT / "papers.yaml"


def _load_papers(path: Path = _PAPERS_PATH) -> dict[str, dict[str, Any]]:
    if not path.is_file():
        raise RuntimeError(f"Paper registry not found: {path}")
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise RuntimeError(f"Paper registry must be a YAML mapping: {path}")
    return loaded


PAPERS = _load_papers()


@dataclass(frozen=True)
class FetchedPaper:
    """Resolved PDF plus immutable source and license provenance."""

    local_pdf_path: str
    doi: str
    title: str
    source_url: str
    license: str
    pdf_sha256: str


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _license_allowed(license_name: str) -> bool:
    normalized = re.sub(r"[^A-Z0-9]+", "-", license_name.upper()).strip("-")
    if normalized == "CC0" or normalized.startswith("CC0-"):
        return True
    if "-NC" in normalized or "-ND" in normalized:
        return False
    return normalized == "CC-BY" or normalized.startswith("CC-BY-")


def _fetched(path: Path, config: dict[str, Any], digest: str) -> FetchedPaper:
    return FetchedPaper(
        local_pdf_path=str(path),
        doi=str(config.get("doi", "")),
        title=str(config.get("title", "")),
        source_url=str(config.get("source_url", config.get("pdf_url", ""))),
        license=str(config.get("license", "")),
        pdf_sha256=digest,
    )


def fetch_oa_pdf(paper_key: str, dest_dir: str | Path) -> FetchedPaper:
    """Resolve an OA PDF, refusing unapproved licenses before any I/O download."""
    if paper_key not in PAPERS:
        available = ", ".join(sorted(PAPERS)) or "none"
        raise KeyError(f"Unknown paper '{paper_key}'. Configured papers: {available}")
    config = PAPERS[paper_key]
    license_name = str(config.get("license", ""))
    if not _license_allowed(license_name):
        raise PermissionError(
            f"Refusing to fetch '{paper_key}': license '{license_name or 'missing'}' "
            "is not in the OA allowlist (CC-BY, CC-BY-SA, or CC0)."
        )

    expected_hash = str(config.get("pdf_sha256", "")).strip().lower()
    destination = Path(dest_dir) / f"{paper_key}.pdf"
    if destination.is_file():
        existing_hash = _sha256(destination)
        if expected_hash and existing_hash == expected_hash:
            return _fetched(destination, config, existing_hash)

    # Prefer a locally-staged copy over the network: work/ (dev) or tests/fixtures/
    # (a committed, license-permitted copy that keeps clone -> run/test hermetic).
    staged_candidates = (
        _REPO_ROOT / "work" / f"{paper_key}.pdf",
        _REPO_ROOT / "tests" / "fixtures" / f"{paper_key}.pdf",
    )
    for staged_pdf in staged_candidates:
        if not staged_pdf.is_file():
            continue
        staged_hash = _sha256(staged_pdf)
        if expected_hash and staged_hash != expected_hash:
            # A stale copy in one candidate (e.g. a dev's work/) must not block a valid
            # committed fixture: skip this candidate and try the next (or the network).
            continue
        if destination.resolve() != staged_pdf.resolve():
            destination.parent.mkdir(parents=True, exist_ok=True)
            temporary = destination.with_suffix(".pdf.part")
            shutil.copyfile(staged_pdf, temporary)
            os.replace(temporary, destination)
            return _fetched(destination, config, staged_hash)
        return _fetched(staged_pdf, config, staged_hash)

    pdf_url = str(config.get("pdf_url", "")).strip()
    if not pdf_url:
        raise RuntimeError(f"No local PDF or pdf_url is configured for '{paper_key}'.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".pdf.part")
    try:
        with requests.get(
            pdf_url,
            stream=True,
            timeout=(10, 60),
            headers={"User-Agent": "lab-brain/0.1 OA figure reader"},
        ) as response:
            response.raise_for_status()
            with temporary.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
        downloaded_hash = _sha256(temporary)
        if expected_hash and downloaded_hash != expected_hash:
            temporary.unlink(missing_ok=True)
            raise RuntimeError(
                f"Downloaded PDF checksum mismatch for {paper_key}: expected "
                f"{expected_hash}, got {downloaded_hash}."
            )
        os.replace(temporary, destination)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return _fetched(destination, config, _sha256(destination))
