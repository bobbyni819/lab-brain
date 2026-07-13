import fnmatch
import json
import os
from pathlib import Path

import yaml

from labbrain.lab_scan import main, scan, write_manifest, write_report


def _build_fixture(root: Path) -> None:
    files = {
        "slides/20260210_flu_ABM_SO.pptx": b"presentation",
        "code/foo.py": b"print('offline')\n",
        "alpha/duplicate.bin": b"same bytes",
        "beta/duplicate-copy.bin": b"same bytes",
        "drafts/~$draft.docx": b"temporary",
        "empty.txt": b"",
        "private/CV_notes.md": b"private",
        "Admin/budget.md": b"excluded domain",
    }
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    newest = 200 * 24 * 60 * 60
    for relative_path in files:
        os.utime(root / relative_path, (newest, newest))
    os.utime(root / "empty.txt", (0, 0))


def _profile() -> dict:
    return {
        "read_tiers": {"SKIP": ["~$*"]},
        "privacy": {"exclude_globs": ["private/*"]},
        "domains": [{"match": r"^Admin/", "action": "exclude"}],
    }


def test_scan_classifies_files_and_applies_profile(tmp_path: Path) -> None:
    root = tmp_path / "lab"
    _build_fixture(root)

    records = scan(str(root), _profile())
    by_path = {record["path"]: record for record in records}

    assert [record["path"] for record in records] == sorted(by_path)
    slide = by_path["slides/20260210_flu_ABM_SO.pptx"]
    assert slide["area"] == "slide"
    assert slide["date_prefix"] == "20260210"
    assert slide["initials"] == "SO"
    assert slide["project"] == "slides"

    code = by_path["code/foo.py"]
    assert code["area"] == "code"
    assert code["format"] == "py"
    assert code["project"] == "code"

    assert by_path["alpha/duplicate.bin"]["content_hash"] == by_path[
        "beta/duplicate-copy.bin"
    ]["content_hash"]
    assert "empty" in by_path["empty.txt"]["flags"]
    assert by_path["empty.txt"]["project"] == "(root)"

    assert "drafts/~$draft.docx" not in by_path
    assert "private/CV_notes.md" not in by_path
    assert "Admin/budget.md" not in by_path


def test_profile_can_be_loaded_from_yaml(tmp_path: Path) -> None:
    root = tmp_path / "lab"
    _build_fixture(root)
    profile_path = tmp_path / "lab-profile.yaml"
    profile = _profile()
    profile["projects"] = {"aliases": {"slides": "influenza"}}
    profile_path.write_text(yaml.safe_dump(profile), encoding="utf-8")

    records = scan(str(root), str(profile_path))

    assert not any(record["path"].endswith("~$draft.docx") for record in records)
    assert next(record for record in records if record["area"] == "slide")[
        "project"
    ] == "influenza"


def test_writers_emit_jsonl_duplicates_stale_and_flags(tmp_path: Path) -> None:
    root = tmp_path / "lab"
    _build_fixture(root)
    records = scan(str(root), _profile())

    manifest_path = tmp_path / "registry" / "manifest.jsonl"
    report_path = tmp_path / "registry" / "SCAN_REPORT.md"

    assert write_manifest(records, manifest_path) == str(manifest_path)
    parsed = [
        json.loads(line)
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
    ]
    assert parsed == records

    assert write_report(records, report_path) == str(report_path)
    report = report_path.read_text(encoding="utf-8")
    assert "SCAN_REPORT" in report
    assert "## Duplicates" in report
    assert "alpha/duplicate.bin" in report
    assert "beta/duplicate-copy.bin" in report
    assert "## Stale" in report
    assert "Stale files: **1**" in report
    assert "empty" in report


def test_main_writes_outputs_and_prints_summary(tmp_path: Path, capsys) -> None:
    root = tmp_path / "lab"
    _build_fixture(root)
    profile_path = tmp_path / "lab-profile.yaml"
    profile_path.write_text(yaml.safe_dump(_profile()), encoding="utf-8")
    out = tmp_path / "registry"

    result = main(
        ["--root", str(root), "--profile", str(profile_path), "--out", str(out)]
    )

    assert result == 0
    assert (out / "manifest.jsonl").is_file()
    assert (out / "SCAN_REPORT.md").is_file()
    summary = capsys.readouterr().out
    assert "files" in summary
    assert "Areas:" in summary
    assert "Duplicates:" in summary
    assert "Stale:" in summary


def test_domain_regex_matches_only_at_start_of_relative_path(tmp_path: Path) -> None:
    root = tmp_path / "lab"
    (root / "nested").mkdir(parents=True)
    (root / "secret-root.txt").write_text("excluded", encoding="utf-8")
    (root / "nested/secret.txt").write_text("included", encoding="utf-8")
    profile = {"domains": [{"match": "secret", "action": "exclude"}]}

    paths = [record["path"] for record in scan(str(root), profile)]

    assert "secret-root.txt" not in paths
    assert "nested/secret.txt" in paths


def test_skip_globs_use_platform_fnmatch_semantics(tmp_path: Path) -> None:
    root = tmp_path / "lab"
    root.mkdir()
    filename = "DRAFT.DOCX"
    pattern = "draft.docx"
    (root / filename).write_bytes(b"draft")

    paths = [
        record["path"]
        for record in scan(str(root), {"read_tiers": {"SKIP": [pattern]}})
    ]

    assert (filename not in paths) is fnmatch.fnmatch(filename, pattern)


def test_stat_failure_is_unreadable_not_empty_or_stale(
    tmp_path: Path, monkeypatch
) -> None:
    root = tmp_path / "lab"
    root.mkdir()
    unreadable = root / "unreadable.dat"
    unreadable.write_bytes(b"content")
    (root / "newest.txt").write_bytes(b"newest")
    original_stat = Path.stat

    def fail_target_stat(path: Path, *args, **kwargs):
        if path == unreadable:
            raise PermissionError("fixture stat failure")
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", fail_target_stat)

    records = scan(str(root))
    record = next(item for item in records if item["path"] == "unreadable.dat")
    assert "unreadable" in record["flags"]
    assert "empty" not in record["flags"]

    report_path = tmp_path / "SCAN_REPORT.md"
    write_report(records, report_path)
    assert "Stale files: **0**" in report_path.read_text(encoding="utf-8")


def test_report_escapes_markdown_table_cells(tmp_path: Path) -> None:
    root = tmp_path / "lab"
    project = root / "project-pilot"
    project.mkdir(parents=True)
    (project / "notes.md").write_text("notes", encoding="utf-8")
    records = scan(str(root))
    records[0]["project"] = "project|pilot"

    report_path = tmp_path / "SCAN_REPORT.md"
    write_report(records, report_path)

    assert "project\\|pilot" in report_path.read_text(encoding="utf-8")
