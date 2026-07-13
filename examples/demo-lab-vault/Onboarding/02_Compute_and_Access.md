# 02 · Compute & access (how to actually run things)

What you need set up before the sub-track work.

## Repos & install
- Clone the `flu-analysis` repo (and Lab Brain: `python bootstrap.py` installs the skills).
- `pip install -e .` in the Lab Brain repo, then `python -m pytest tests -q` should be green.

## The two harnesses
- **Claude Code** (this repo, git, running the slice) — you already have it.
- **Claude Science** — needed for live figure reads (`--provider hostllm`). Access is pending for you;
  until then use `--provider fixture` (offline) or `--provider anthropic` if you have an API key.

## Data
- OA papers are fetched on demand (license-gated). The hero paper (Gui 2017, CC-BY) is cached in the repo.
- Never fetch non-open-access papers; the tool refuses them.

## The one rule when we both touch a repo
One harness owns a working-dir at a time — claim it on `_handoff-log.md` (🔒) first. See
`framework/harness-playbook.md`.
