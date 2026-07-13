import json
import os
import subprocess
from pathlib import Path

import yaml
import pytest

from labbrain.lab_standup import gather, gather_all, main, write_standup_input


def _build_vault(root: Path) -> None:
    files = {
        "progress-alex.md": "# Progress — Alex Rivera\n\n- Finished the first read.\n",
        "Sub-tracks/02_flu/questions.md": (
            "# Questions for the mentor — Alex\n\n"
            "## Open\n"
            "- Should I keep the configured crop?\n"
            "- Is the axis normalized?\n\n"
            "## Answered\n"
            "- *(none yet)*\n"
        ),
        "Sub-tracks/02_flu/analysis.md": "Deterministic notes.\n",
        "Sub-tracks/02_flu/results.csv": "day,value\n1,29\n",
        "2026-07-01_alex-feedback.md": "# Feedback\n",
    }
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    modified = 1_782_950_400  # 2026-07-02T00:00:00Z
    for relative_path in files:
        os.utime(root / relative_path, (modified, modified))


def test_gather_collects_person_activity_without_a_git_repo(tmp_path: Path) -> None:
    _build_vault(tmp_path)

    record = gather(
        {"name": "Alex Rivera", "handle": "AR", "role": "mentee"},
        vault_root=tmp_path,
        repo_root=None,
        since="2026-06-01",
    )

    assert record["person"] == "Alex Rivera"
    assert record["handle"] == "AR"
    assert record["role"] == "mentee"
    assert record["since"] == "2026-06-01"
    assert record["commits"] == []
    assert record["progress_excerpt"]
    assert record["open_questions"] == [
        "Is the axis normalized?",
        "Should I keep the configured crop?",
    ]
    assert record["last_feedback_date"] == "2026-07-01"
    assert record["modified_files"]


def test_default_since_uses_newest_vault_mtime_not_wall_clock(tmp_path: Path) -> None:
    _build_vault(tmp_path)

    record = gather(
        {"name": "Alex Rivera", "handle": "AR", "role": "mentee"},
        vault_root=tmp_path,
    )

    assert record["since"] == "2026-06-18"


def test_since_requires_dashed_iso_date(tmp_path: Path) -> None:
    _build_vault(tmp_path)

    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        gather(
            {"name": "Alex Rivera", "handle": "AR", "role": "mentee"},
            vault_root=tmp_path,
            since="20260601",
        )


def test_gather_parses_git_log_and_missing_git_is_harmless(
    tmp_path: Path, monkeypatch
) -> None:
    _build_vault(tmp_path)
    person = {"name": "Alex Rivera", "handle": "AR", "role": "mentee"}

    def completed(command, **_kwargs):
        assert command[0] == "git"
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=(
                "a1b2c3|2026-07-03|Add deterministic gather\n"
                " 2 files changed, 8 insertions(+), 1 deletion(-)\n\n"
                "d4e5f6|2026-07-02|Document edge case\n"
            ),
            stderr="",
        )

    monkeypatch.setattr("labbrain.lab_standup.subprocess.run", completed)
    record = gather(person, tmp_path, repo_root=tmp_path, since="2026-06-01")
    assert record["commits"] == [
        {
            "sha": "a1b2c3",
            "date": "2026-07-03",
            "subject": "Add deterministic gather",
            "files": 2,
        },
        {
            "sha": "d4e5f6",
            "date": "2026-07-02",
            "subject": "Document edge case",
            "files": 0,
        },
    ]

    def missing_git(_command, **_kwargs):
        raise FileNotFoundError("git")

    monkeypatch.setattr("labbrain.lab_standup.subprocess.run", missing_git)
    assert gather(person, tmp_path, repo_root=tmp_path, since="2026-06-01")[
        "commits"
    ] == []


def test_gather_all_preserves_roster_order_and_question_ownership(tmp_path: Path) -> None:
    _build_vault(tmp_path)
    roster = [
        {"name": "Sam Ortiz", "handle": "SO", "role": "mentor"},
        {"name": "Alex Rivera", "handle": "AR", "role": "mentee"},
    ]

    records = gather_all(roster, tmp_path, since="2026-06-01")

    assert [record["person"] for record in records] == ["Sam Ortiz", "Alex Rivera"]
    assert records[0]["open_questions"] == []
    assert len(records[1]["open_questions"]) == 2


def test_write_standup_input_writes_markdown_and_json(tmp_path: Path) -> None:
    _build_vault(tmp_path)
    record = gather(
        {"name": "Alex Rivera", "handle": "AR", "role": "mentee"},
        tmp_path,
        since="2026-06-01",
    )

    markdown_path = tmp_path / "output" / "standup-input.md"
    assert write_standup_input([record], markdown_path) == str(markdown_path)
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Alex Rivera" in markdown
    assert "open questions" in markdown.lower()

    json_path = tmp_path / "output" / "standup-input.json"
    assert write_standup_input([record], json_path, as_json=True) == str(json_path)
    assert json.loads(json_path.read_text(encoding="utf-8")) == [record]


def test_main_filters_person_writes_output_and_reports_one_line(
    tmp_path: Path, capsys
) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    _build_vault(vault)
    profile = tmp_path / "lab-profile.yaml"
    profile.write_text(
        yaml.safe_dump(
            {
                "roster": [
                    {"name": "Sam Ortiz", "handle": "SO", "role": "mentor"},
                    {"name": "Alex Rivera", "handle": "AR", "role": "mentee"},
                ]
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "standup"

    result = main(
        [
            "--vault",
            str(vault),
            "--profile",
            str(profile),
            "--person",
            "AR",
            "--since",
            "2026-06-01",
            "--out",
            str(output),
        ]
    )

    assert result == 0
    assert (output / "standup-input.md").is_file()
    summary = capsys.readouterr()
    assert summary.err == ""
    assert len(summary.out.splitlines()) == 1
    assert "1 people" in summary.out
    assert "commits" in summary.out
    assert "modified files" in summary.out


def test_main_errors_clearly_without_a_profile_roster(tmp_path: Path, capsys) -> None:
    assert main(["--vault", str(tmp_path)]) == 1
    error = capsys.readouterr().err
    assert "error" in error.lower()
    assert "roster" in error.lower()
