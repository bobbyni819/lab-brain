import pytest


@pytest.mark.parametrize(
    ("license_name", "allowed"),
    [
        ("CC-BY", True),
        ("CC-BY-4.0", True),
        ("CC BY 4.0", True),
        ("CC-BY-SA-4.0", True),
        ("CC0-1.0", True),
        ("CC-BY-NC-4.0", False),
        ("CC-BY-ND-4.0", False),
        ("all rights reserved", False),
    ],
)
def test_oa_license_allowlist(license_name: str, allowed: bool) -> None:
    from labbrain.fetch import _license_allowed

    assert _license_allowed(license_name) is allowed


def test_fetch_uses_staged_pdf_without_network(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from labbrain import fetch

    def fail_on_network(*args, **kwargs):
        raise AssertionError("offline fixture fetch attempted network access")

    monkeypatch.setattr(fetch.requests, "get", fail_on_network)
    first = fetch.fetch_oa_pdf("gui2017", tmp_path)
    second = fetch.fetch_oa_pdf("gui2017", tmp_path)

    assert first == second
    assert first.pdf_sha256 == fetch.PAPERS["gui2017"]["pdf_sha256"]
