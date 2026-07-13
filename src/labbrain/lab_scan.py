"""Deterministic, offline structural scanner for lab files."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

_HASH_READ_LIMIT = 65_536
_HUGE_SIZE = 50 * 1024 * 1024
_EPOCH_DATE = "1970-01-01"

_AREA_EXTENSIONS = {
    "code": {"py", "js", "ts", "java", "c", "cpp", "h", "go", "rs", "rb", "sh"},
    "notebook": {"ipynb"},
    "doc": {"md", "txt", "docx", "rtf", "odt", "pdf"},
    "slide": {"pptx", "key"},
    "sheet": {"xlsx", "xls", "csv", "tsv"},
    "figure": {"png", "jpg", "jpeg", "gif", "svg", "tif", "tiff"},
    "dataset": {"h5", "hdf5", "parquet", "fcs", "npy", "npz", "mat", "json"},
    "config": {"yaml", "yml", "toml", "ini", "cfg"},
    "archive": {"zip", "tar", "gz", "7z", "rar"},
    "media": {"mp4", "mov", "avi", "mp3", "wav"},
    "email": {"msg", "eml"},
}
_EXTENSION_AREAS = {
    extension: area
    for area, extensions in _AREA_EXTENSIONS.items()
    for extension in extensions
}

# Version-control, build, and cache directories are pruned from the walk by default
# (they are machine noise, not lab knowledge). Other dotfiles are still recorded and
# carry the ``hidden`` flag, so this is a targeted prune, not "skip everything hidden".
_DEFAULT_IGNORE_DIRS = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".ipynb_checkpoints",
        "node_modules",
        ".venv",
        "venv",
        ".tox",
    }
)


def _load_profile(profile: dict | str | None) -> dict[str, Any]:
    if profile is None:
        return {}
    if isinstance(profile, dict):
        return profile
    if not isinstance(profile, str):
        raise TypeError("profile must be a mapping, YAML path, or None")

    profile_path = Path(profile).expanduser()
    loaded = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ValueError(f"Profile must be a YAML mapping: {profile_path}")
    return loaded


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _patterns(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple, set)):
        return [str(pattern) for pattern in value]
    return []


def _is_excluded(relative_path: str, basename: str, profile: Mapping[str, Any]) -> bool:
    read_tiers = _mapping(profile.get("read_tiers"))
    if any(
        fnmatch.fnmatch(basename, pattern)
        for pattern in _patterns(read_tiers.get("SKIP"))
    ):
        return True

    privacy = _mapping(profile.get("privacy"))
    if any(
        fnmatch.fnmatch(relative_path, pattern)
        for pattern in _patterns(privacy.get("exclude_globs"))
    ):
        return True

    domains = profile.get("domains")
    if not isinstance(domains, list):
        return False
    for domain in domains:
        if not isinstance(domain, Mapping) or domain.get("action") != "exclude":
            continue
        pattern = domain.get("match")
        if not isinstance(pattern, str):
            continue
        try:
            if re.match(pattern, relative_path):
                return True
        except re.error:
            continue
    return False


def _modified_date(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()


def _content_hash(path: Path, size: int) -> tuple[str, bool]:
    digest = hashlib.sha1()
    digest.update(str(size).encode("ascii"))
    try:
        with path.open("rb") as handle:
            digest.update(handle.read(_HASH_READ_LIMIT))
    except OSError:
        return digest.hexdigest(), False
    return digest.hexdigest(), True


def _record(
    path: Path,
    relative_path: str,
    profile: Mapping[str, Any],
) -> dict[str, Any]:
    stat_readable = True
    try:
        file_stat = path.stat()
        size = int(file_stat.st_size)
        modified = _modified_date(file_stat.st_mtime)
    except (OSError, OverflowError, ValueError):
        stat_readable = False
        size = 0
        modified = _EPOCH_DATE

    content_hash, content_readable = _content_hash(path, size)
    basename = path.name
    extension = path.suffix.lower().removeprefix(".")
    parts = Path(relative_path).parts
    project = parts[0] if len(parts) > 1 else "(root)"
    aliases = _mapping(_mapping(profile.get("projects")).get("aliases"))
    project = str(aliases.get(project, project))

    flags: list[str] = []
    if size > _HUGE_SIZE:
        flags.append("huge")
    if any(part.startswith(".") for part in parts):
        flags.append("hidden")
    if basename.startswith("~$") or basename.endswith(".tmp") or basename.endswith("~"):
        flags.append("tmp")
    if stat_readable and size == 0:
        flags.append("empty")
    if not stat_readable or not content_readable:
        flags.append("unreadable")

    date_match = re.match(r"^(\d{8})_", basename)
    initials_match = re.search(r"_([A-Z]{2,4})(?=\.[^.]+$)", basename)
    return {
        "path": relative_path,
        "area": _EXTENSION_AREAS.get(extension, "other"),
        "format": extension,
        "size": size,
        "modified": modified,
        "date_prefix": date_match.group(1) if date_match else None,
        "initials": initials_match.group(1) if initials_match else None,
        "project": project,
        "content_hash": content_hash,
        "flags": flags,
    }


def scan(root: str, profile: dict | str | None = None) -> list[dict]:
    """Walk ``root`` and return one deterministic structural record per file."""
    root_path = Path(root).expanduser()
    if not root_path.exists():
        raise FileNotFoundError(f"Scan root does not exist: {root_path}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"Scan root is not a directory: {root_path}")

    loaded_profile = _load_profile(profile)
    records: list[dict[str, Any]] = []

    def ignore_walk_error(_error: OSError) -> None:
        return None

    for directory, dirnames, filenames in os.walk(
        root_path, topdown=True, onerror=ignore_walk_error, followlinks=False
    ):
        dirnames[:] = sorted(name for name in dirnames if name not in _DEFAULT_IGNORE_DIRS)
        filenames.sort()
        directory_path = Path(directory)
        for filename in filenames:
            path = directory_path / filename
            try:
                relative_path = path.relative_to(root_path).as_posix()
            except ValueError:
                continue
            if _is_excluded(relative_path, filename, loaded_profile):
                continue
            records.append(_record(path, relative_path, loaded_profile))

    records.sort(key=lambda record: record["path"])
    return records


def write_manifest(records, out_path) -> str:
    """Write scan records as deterministic JSON Lines and return the output path."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
    path.write_text("".join(f"{line}\n" for line in lines), encoding="utf-8")
    return str(path)


def _human_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    value = float(size)
    for unit in ("KB", "MB", "GB", "TB"):
        value /= 1024
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}"
    raise AssertionError("unreachable")


def _duplicate_groups(records: Iterable[Mapping[str, Any]]) -> list[tuple[str, list[str]]]:
    by_hash: dict[str, list[str]] = defaultdict(list)
    for record in records:
        by_hash[str(record.get("content_hash", ""))].append(str(record.get("path", "")))
    groups = [
        (content_hash, sorted(paths))
        for content_hash, paths in by_hash.items()
        if len(paths) > 1
    ]
    return sorted(groups, key=lambda group: (group[1][0], group[0]))


def _parse_date(value: object) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            return None


def _stale_count(records: Iterable[Mapping[str, Any]]) -> int:
    dates = [
        _parse_date(record.get("modified"))
        for record in records
        if "unreadable" not in record.get("flags", [])
    ]
    valid_dates = [modified for modified in dates if modified is not None]
    if not valid_dates:
        return 0
    newest = max(valid_dates)
    return sum((newest - modified).days > 180 for modified in valid_dates)


def _count_table(heading: str, counts: Mapping[str, int]) -> list[str]:
    lines = [f"| {heading} | Files |", "| --- | ---: |"]
    if counts:
        lines.extend(
            f"| {_markdown_cell(name)} | {counts[name]} |" for name in sorted(counts)
        )
    else:
        lines.append("| (none) | 0 |")
    return lines


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\r\n", "<br>").replace(
        "\n", "<br>"
    ).replace("\r", "<br>")


def write_report(records, out_path) -> str:
    """Write a human-readable deterministic Markdown scan report."""
    materialized = list(records)
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    total_size = sum(int(record.get("size", 0)) for record in materialized)
    area_counts = Counter(str(record.get("area", "other")) for record in materialized)
    project_counts = Counter(str(record.get("project", "(root)")) for record in materialized)
    duplicate_groups = _duplicate_groups(materialized)
    stale_count = _stale_count(materialized)
    flag_counts = Counter(
        str(flag)
        for record in materialized
        for flag in record.get("flags", [])
    )

    lines = [
        "# SCAN_REPORT",
        "",
        "## Summary",
        "",
        f"- Total files: **{len(materialized)}**",
        f"- Total size: **{_human_size(total_size)}** ({total_size} bytes)",
        "",
        "## Counts by area",
        "",
        *_count_table("Area", area_counts),
        "",
        "## Counts by project",
        "",
        *_count_table("Project", project_counts),
        "",
        "## Duplicates",
        "",
        f"Duplicate groups: **{len(duplicate_groups)}**",
        "",
    ]
    if duplicate_groups:
        for index, (content_hash, paths) in enumerate(duplicate_groups, start=1):
            lines.append(f"### Group {index} (`{content_hash}`)")
            lines.append("")
            lines.extend(f"- `{duplicate_path}`" for duplicate_path in paths)
            lines.append("")
    else:
        lines.extend(["No duplicate groups found.", ""])

    lines.extend(
        [
            "## Stale",
            "",
            f"Stale files: **{stale_count}**",
            "",
            "Files are stale when their modified date is more than 180 days older "
            "than the newest modified date in this scan.",
            "",
            "## Flags",
            "",
            *_count_table("Flag", flag_counts),
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m labbrain.lab_scan",
        description="Create a deterministic Layer-0 structural scan of lab files.",
    )
    parser.add_argument("--root", required=True, help="directory to scan recursively")
    parser.add_argument("--profile", help="optional lab profile YAML path")
    parser.add_argument("--out", default="registry", help="output directory")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the structural scanner CLI."""
    args = _parser().parse_args(argv)
    try:
        records = scan(args.root, args.profile)
        output = Path(args.out)
        write_manifest(records, output / "manifest.jsonl")
        write_report(records, output / "SCAN_REPORT.md")
    except (OSError, TypeError, ValueError, yaml.YAMLError) as exc:
        print(f"labbrain.lab_scan: error: {exc}", file=sys.stderr)
        return 1

    area_counts = Counter(str(record["area"]) for record in records)
    duplicates = _duplicate_groups(records)
    stale = _stale_count(records)
    total_size = sum(int(record["size"]) for record in records)
    print(f"Scanned {len(records)} files ({_human_size(total_size)}; {total_size} bytes)")
    print(
        "Areas: "
        + (", ".join(f"{area}={area_counts[area]}" for area in sorted(area_counts)) or "none")
    )
    print(f"Duplicates: {len(duplicates)} groups")
    print(f"Stale: {stale} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
