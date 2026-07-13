"""Deterministic, offline data gathering for lab mentorship standups."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

import yaml

_DEFAULT_WINDOW_DAYS = 14
_MAX_MODIFIED_FILES = 50
_PROGRESS_LINES = 15
_EPOCH_DATE = date(1970, 1, 1)
_IGNORE_DIRS = frozenset(
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
_COMMIT_LINE = re.compile(
    r"^(?P<sha>[^|]+)\|(?P<date>\d{4}-\d{2}-\d{2})\|(?P<subject>.*)$"
)
_SHORTSTAT_FILES = re.compile(r"(?P<count>\d+)\s+files?\s+changed")
_FEEDBACK_FILE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})_(?P<owner>.+)-feedback\.md$",
    re.IGNORECASE,
)
_BULLET_LINE = re.compile(r"^\s*[-*+]\s+(?P<text>.+?)\s*$")


@dataclass(frozen=True)
class _VaultFile:
    """A successfully stated file below the vault root."""

    path: Path
    relative: str
    mtime: float
    modified: str


def _required_person_text(person: Mapping[str, Any], field: str) -> str:
    value = person.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"person must contain a non-empty {field!r}")
    return value.strip()


def _words(value: str) -> tuple[str, ...]:
    """Normalize punctuation and separators while retaining Unicode names."""
    return tuple(part.casefold() for part in re.findall(r"[^\W_]+", value))


def _person_aliases(name: str, handle: str) -> tuple[tuple[str, ...], ...]:
    candidates = (name, name.split()[0], handle)
    aliases: list[tuple[str, ...]] = []
    for candidate in candidates:
        normalized = _words(candidate)
        if normalized and normalized not in aliases:
            aliases.append(normalized)
    return tuple(aliases)


def _contains_alias(value: str, aliases: tuple[tuple[str, ...], ...]) -> bool:
    words = _words(value)
    return any(
        words[index : index + len(alias)] == alias
        for alias in aliases
        for index in range(len(words) - len(alias) + 1)
    )


def _owner_matches(value: str, aliases: tuple[tuple[str, ...], ...]) -> bool:
    return _words(value) in aliases


def _modified_date(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()


def _walk_vault(root: Path) -> list[_VaultFile]:
    records: list[_VaultFile] = []

    def ignore_walk_error(_error: OSError) -> None:
        return None

    for directory, dirnames, filenames in os.walk(
        root, topdown=True, onerror=ignore_walk_error, followlinks=False
    ):
        dirnames[:] = sorted(name for name in dirnames if name not in _IGNORE_DIRS)
        directory_path = Path(directory)
        for filename in sorted(filenames):
            path = directory_path / filename
            try:
                relative = path.relative_to(root).as_posix()
                mtime = path.stat().st_mtime
                modified = _modified_date(mtime)
            except (OSError, OverflowError, ValueError):
                continue
            records.append(_VaultFile(path, relative, mtime, modified))
    records.sort(key=lambda record: (record.relative.casefold(), record.relative))
    return records


def _since_date(value: str | None, files: Sequence[_VaultFile]) -> date:
    if value is not None:
        if not isinstance(value, str) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is None:
            raise ValueError("since must be an ISO date in YYYY-MM-DD format")
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("since must be an ISO date in YYYY-MM-DD format") from exc
    if not files:
        return _EPOCH_DATE
    newest = datetime.fromtimestamp(max(item.mtime for item in files), tz=timezone.utc)
    return (newest - timedelta(days=_DEFAULT_WINDOW_DAYS)).date()


def _storage_prefixes(person: Mapping[str, Any], vault_root: Path) -> tuple[str, ...]:
    storage = person.get("storage", [])
    if isinstance(storage, str):
        storage = [storage]
    if not isinstance(storage, (list, tuple, set)):
        return ()

    prefixes: set[str] = set()
    try:
        resolved_root = vault_root.resolve()
    except OSError:
        resolved_root = vault_root.absolute()

    for item in storage:
        if not isinstance(item, (str, os.PathLike)):
            continue
        raw = os.fspath(item).strip()
        if not raw:
            continue

        candidate = Path(raw).expanduser()
        if candidate.is_absolute():
            try:
                relative = candidate.resolve().relative_to(resolved_root).as_posix()
            except (OSError, ValueError):
                relative = ""
            if relative and relative != ".":
                prefixes.add(relative.casefold().rstrip("/"))
        else:
            normalized = PurePosixPath(raw.replace("\\", "/")).as_posix().lstrip("./")
            if normalized and normalized != ".":
                prefixes.add(normalized.casefold().rstrip("/"))

        normalized_raw = raw.replace("\\", "/")
        subtrack = re.search(r"(?:^|/)Sub-tracks/(.+)$", normalized_raw, re.IGNORECASE)
        if subtrack:
            prefixes.add(f"sub-tracks/{subtrack.group(1).strip('/')}".casefold())

    return tuple(sorted(prefixes))


def _under_prefix(relative: str, prefixes: Sequence[str]) -> bool:
    normalized = relative.casefold()
    return any(normalized == prefix or normalized.startswith(f"{prefix}/") for prefix in prefixes)


def _is_progress_file(
    record: _VaultFile, aliases: tuple[tuple[str, ...], ...]
) -> bool:
    if record.path.suffix.casefold() != ".md":
        return False
    stem = record.path.stem
    if not stem.casefold().startswith("progress-"):
        return False
    return _owner_matches(stem[len("progress-") :], aliases)


def _belongs_to_person(
    record: _VaultFile,
    aliases: tuple[tuple[str, ...], ...],
    storage_prefixes: Sequence[str],
) -> bool:
    return (
        _contains_alias(record.relative, aliases)
        or _is_progress_file(record, aliases)
        or _under_prefix(record.relative, storage_prefixes)
    )


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _progress_excerpt(
    files: Sequence[_VaultFile], aliases: tuple[tuple[str, ...], ...]
) -> str:
    candidates = [record for record in files if _is_progress_file(record, aliases)]
    candidates.sort(key=lambda record: (-record.mtime, record.relative.casefold()))
    for candidate in candidates:
        text = _read_text(candidate.path)
        if text:
            return "\n".join(text.splitlines()[:_PROGRESS_LINES]).strip()
    return ""


def _declared_question_owner(text: str) -> str | None:
    for line in text.splitlines()[:30]:
        metadata = re.match(r"^\s*(?:person|owner)\s*:\s*[\"']?(.+?)[\"']?\s*$", line, re.I)
        if metadata:
            return metadata.group(1).strip()
        if line.startswith("# "):
            heading = line[2:].strip()
            suffix = re.search(r"(?:—|–|\s-\s|:)\s*(.+?)\s*$", heading)
            if suffix:
                return suffix.group(1).strip()
    return None


def _bullet_questions(text: str) -> list[str]:
    lines = text.splitlines()
    open_heading = next(
        (
            index
            for index, line in enumerate(lines)
            if re.match(r"^##\s+Open\s*$", line, flags=re.IGNORECASE)
        ),
        None,
    )
    if open_heading is not None:
        selected: list[str] = []
        for line in lines[open_heading + 1 :]:
            if re.match(r"^#{1,2}\s+", line):
                break
            selected.append(line)
        lines = selected

    questions = {
        match.group("text").strip()
        for line in lines
        if (match := _BULLET_LINE.match(line))
        and "none yet" not in match.group("text").casefold()
    }
    return sorted(questions, key=lambda item: (item.casefold(), item))


def _open_questions(
    files: Sequence[_VaultFile],
    aliases: tuple[tuple[str, ...], ...],
    storage_prefixes: Sequence[str],
) -> list[str]:
    questions: set[str] = set()
    for record in files:
        if record.path.name.casefold() != "questions.md":
            continue
        text = _read_text(record.path)
        if not text:
            continue
        declared_owner = _declared_question_owner(text)
        owned_path = _under_prefix(record.relative, storage_prefixes) or _contains_alias(
            record.relative, aliases
        )
        if declared_owner is not None and not _owner_matches(declared_owner, aliases):
            continue
        if declared_owner is None or owned_path or _owner_matches(declared_owner, aliases):
            questions.update(_bullet_questions(text))
    return sorted(questions, key=lambda item: (item.casefold(), item))


def _last_feedback_date(
    files: Sequence[_VaultFile], aliases: tuple[tuple[str, ...], ...]
) -> str | None:
    dates: list[date] = []
    for record in files:
        match = _FEEDBACK_FILE.match(record.path.name)
        if match is None or not _owner_matches(match.group("owner"), aliases):
            continue
        try:
            dates.append(date.fromisoformat(match.group("date")))
        except ValueError:
            continue
    return max(dates).isoformat() if dates else None


def _parse_git_log(output: str) -> list[dict[str, Any]]:
    commits: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in output.splitlines():
        commit_match = _COMMIT_LINE.match(line)
        if commit_match:
            if current is not None:
                commits.append(current)
            current = {
                "sha": commit_match.group("sha"),
                "date": commit_match.group("date"),
                "subject": commit_match.group("subject"),
                "files": 0,
            }
            continue
        stat_match = _SHORTSTAT_FILES.search(line)
        if current is not None and stat_match:
            current["files"] = int(stat_match.group("count"))
    if current is not None:
        commits.append(current)

    commits.sort(
        key=lambda item: (
            -date.fromisoformat(str(item["date"])).toordinal(),
            str(item["sha"]),
            str(item["subject"]),
        )
    )
    return commits


def _git_commits(repo_root: object, name: str, since: str) -> list[dict[str, Any]]:
    if repo_root is None:
        return []
    repo = Path(repo_root).expanduser()
    command = [
        "git",
        "log",
        f"--author={name}",
        f"--since={since}",
        "--pretty=%h|%ad|%s",
        "--date=short",
        "--shortstat",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return _parse_git_log(completed.stdout)


def gather(
    person: dict,
    vault_root,
    repo_root=None,
    since: str | None = None,
) -> dict:
    """Collect one roster member's recent deterministic standup inputs."""
    if not isinstance(person, Mapping):
        raise TypeError("person must be a mapping")
    name = _required_person_text(person, "name")
    handle = _required_person_text(person, "handle")
    role = _required_person_text(person, "role")

    root = Path(vault_root).expanduser()
    if not root.exists():
        raise FileNotFoundError(f"Vault root does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Vault root is not a directory: {root}")

    files = _walk_vault(root)
    threshold = _since_date(since, files)
    threshold_iso = threshold.isoformat()
    aliases = _person_aliases(name, handle)
    storage_prefixes = _storage_prefixes(person, root)

    modified = [
        record
        for record in files
        if date.fromisoformat(record.modified) >= threshold
        and _belongs_to_person(record, aliases, storage_prefixes)
    ]
    modified.sort(
        key=lambda record: (-record.mtime, record.relative.casefold(), record.relative)
    )

    return {
        "person": name,
        "handle": handle,
        "role": role,
        "since": threshold_iso,
        "commits": _git_commits(repo_root, name, threshold_iso),
        "modified_files": [
            {"path": record.relative, "modified": record.modified}
            for record in modified[:_MAX_MODIFIED_FILES]
        ],
        "progress_excerpt": _progress_excerpt(files, aliases),
        "open_questions": _open_questions(files, aliases, storage_prefixes),
        "last_feedback_date": _last_feedback_date(files, aliases),
    }


def gather_all(
    roster: list[dict],
    vault_root,
    repo_root=None,
    since: str | None = None,
) -> list[dict]:
    """Gather records for every roster member, preserving roster order."""
    if not isinstance(roster, list):
        raise TypeError("roster must be a list")
    return [
        gather(person, vault_root=vault_root, repo_root=repo_root, since=since)
        for person in roster
    ]


def _markdown_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\r", " ").replace("\n", " ")


def write_standup_input(
    gathered: list[dict], out_path, as_json: bool = False
) -> str:
    """Write gathered records as readable Markdown or deterministic JSON."""
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if as_json:
        path.write_text(
            json.dumps(gathered, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return str(path)

    lines = ["# Standup Input", ""]
    for record in gathered:
        person = str(record.get("person", ""))
        handle = str(record.get("handle", ""))
        role = str(record.get("role", ""))
        since = str(record.get("since", ""))
        last_feedback = record.get("last_feedback_date") or "none"
        lines.extend(
            [
                f"## {person}",
                "",
                f"`{handle}` · {role} · since {since}",
                "",
                f"Last feedback date: **{last_feedback}**",
                "",
                "### Commits",
                "",
                "| Date | SHA | Subject | Files |",
                "| --- | --- | --- | ---: |",
            ]
        )
        commits = record.get("commits", [])
        if commits:
            lines.extend(
                "| {date} | `{sha}` | {subject} | {files} |".format(
                    date=_markdown_cell(commit.get("date", "")),
                    sha=_markdown_cell(commit.get("sha", "")),
                    subject=_markdown_cell(commit.get("subject", "")),
                    files=int(commit.get("files", 0)),
                )
                for commit in commits
            )
        else:
            lines.append("| — | — | No commits found | 0 |")

        lines.extend(
            [
                "",
                "### Modified files",
                "",
                "| Modified | Path |",
                "| --- | --- |",
            ]
        )
        modified_files = record.get("modified_files", [])
        if modified_files:
            lines.extend(
                f"| {_markdown_cell(item.get('modified', ''))} | "
                f"`{_markdown_cell(item.get('path', ''))}` |"
                for item in modified_files
            )
        else:
            lines.append("| — | No modified files found |")

        lines.extend(["", "### Progress excerpt", ""])
        progress = str(record.get("progress_excerpt", ""))
        if progress:
            lines.extend(">" if not line else f"> {line}" for line in progress.splitlines())
        else:
            lines.append("No progress file found.")

        lines.extend(["", "### Open questions", ""])
        questions = record.get("open_questions", [])
        if questions:
            lines.extend(f"- {question}" for question in questions)
        else:
            lines.append("- None found.")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def _load_roster(profile_path: str | None) -> list[dict]:
    if profile_path is None:
        raise ValueError("a profile with a non-empty roster is required")
    path = Path(profile_path).expanduser()
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, Mapping):
        raise ValueError(f"profile must be a YAML mapping: {path}")
    roster = loaded.get("roster")
    if not isinstance(roster, list) or not roster:
        raise ValueError(f"profile roster must be a non-empty list: {path}")
    if not all(isinstance(person, dict) for person in roster):
        raise ValueError(f"every profile roster entry must be a mapping: {path}")
    return roster


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m labbrain.lab_standup",
        description="Gather deterministic mentorship standup inputs.",
    )
    parser.add_argument("--vault", required=True, help="lab vault directory")
    parser.add_argument("--profile", help="lab profile YAML containing roster entries")
    parser.add_argument("--repo", help="optional git repository for commit activity")
    parser.add_argument("--person", help="limit gathering to one name or handle")
    parser.add_argument("--since", help="earliest activity date (YYYY-MM-DD)")
    parser.add_argument("--out", default=".", help="output directory")
    parser.add_argument("--json", action="store_true", help="write JSON instead of Markdown")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the deterministic standup gather CLI."""
    args = _parser().parse_args(argv)
    try:
        roster = _load_roster(args.profile)
        if args.person:
            target = args.person.casefold()
            roster = [
                person
                for person in roster
                if str(person.get("name", "")).casefold() == target
                or str(person.get("handle", "")).casefold() == target
            ]
            if not roster:
                raise ValueError(f"person not found in profile roster: {args.person}")

        gathered = gather_all(
            roster,
            vault_root=args.vault,
            repo_root=args.repo,
            since=args.since,
        )
        output = Path(args.out) / f"standup-input.{('json' if args.json else 'md')}"
        written = write_standup_input(gathered, output, as_json=args.json)
    except (OSError, TypeError, ValueError, yaml.YAMLError) as exc:
        print(f"labbrain.lab_standup: error: {exc}", file=sys.stderr)
        return 1

    commits = sum(len(record["commits"]) for record in gathered)
    modified = sum(len(record["modified_files"]) for record in gathered)
    print(
        f"Gathered {len(gathered)} people, {commits} commits, "
        f"{modified} modified files; wrote {written}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
