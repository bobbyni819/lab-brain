"""Regression tests for bugs found in the adversarial review pass."""

from pathlib import Path


def test_unowned_questions_do_not_leak_to_unrelated_person(tmp_path: Path) -> None:
    """An un-owned questions.md must NOT be attributed to every roster member
    (regression: the owned_path check was dead code when no owner was declared)."""
    from labbrain.lab_standup import gather

    sub = tmp_path / "Sub-tracks" / "03_other"
    sub.mkdir(parents=True)
    (sub / "questions.md").write_text(
        "## Open\n- Can we get more GPU budget?\n", encoding="utf-8"
    )
    # Dana's storage does NOT include 03_other
    result = gather(
        {"name": "Dana Lee", "handle": "DL", "role": "mentor",
         "storage": ["Sub-tracks/99_dana"]},
        vault_root=tmp_path, repo_root=None, since="2020-01-01",
    )
    assert not any("GPU budget" in q for q in result["open_questions"])


def test_owned_questions_are_attributed(tmp_path: Path) -> None:
    """A questions.md under the person's own storage path IS attributed to them."""
    from labbrain.lab_standup import gather

    sub = tmp_path / "Sub-tracks" / "02_flu"
    sub.mkdir(parents=True)
    (sub / "questions.md").write_text(
        "## Open\n- Which cytokines make the main figure?\n", encoding="utf-8"
    )
    result = gather(
        {"name": "Alex Rivera", "handle": "AR", "role": "mentee",
         "storage": ["Sub-tracks/02_flu"]},
        vault_root=tmp_path, repo_root=None, since="2020-01-01",
    )
    assert any("cytokines" in q for q in result["open_questions"])


def test_auto_provider_degrades_when_anthropic_sdk_missing(monkeypatch) -> None:
    """get_provider('auto') must fall back to fixture (not crash) when a key is set
    but the anthropic SDK isn't importable."""
    from labbrain import providers

    monkeypatch.setattr(providers, "_host_llm_available", lambda: False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-not-real")

    def _boom(*_a, **_k):
        raise RuntimeError("The anthropic SDK is not installed")

    monkeypatch.setattr(providers, "AnthropicProvider", _boom)
    provider = providers.get_provider("auto", fixtures_dir="tests/fixtures")
    assert isinstance(provider, providers.FixtureProvider)
