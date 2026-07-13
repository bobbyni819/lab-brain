# Contributing to Lab Brain

Lab Brain is both a codebase and a **framework of conventions** — and it's built the way the
framework prescribes. If you contribute, work the same way.

## Run it locally
```bash
git clone https://github.com/<you>/lab-brain && cd lab-brain
pip install -e .
python -m pytest tests -q          # 40 tests, hermetic (no network needed)
python -m labbrain.slice --paper gui2017 --provider fixture --vault demo_vault --report /tmp/r.html
python -m labbrain.lab_scan --root . --out /tmp/scan
```
CI ([`.github/workflows/ci.yml`](./.github/workflows/ci.yml)) runs the tests + both CLIs on every
push and PR. Keep it green.

> **On `--provider fixture`:** it runs the *full* pipeline on the real paper but *replays a saved
> read* for the one extraction step (so CI is deterministic and needs no API key). A live panel read
> is `--provider anthropic` (needs `ANTHROPIC_API_KEY`) or `--provider hostllm` under Claude Science.
> Everything else — render, crop, the D5 verify gate, provenance, report — is identical.

## How we work here (the conventions, applied to this repo)
- **One branch per lane** — `git checkout -b <you>/<workstream>`; open a PR for review. Never commit
  to `main` directly.
- **Restyle, don't reinvent; archive, don't delete** — improve the real thing; move superseded work
  to `_archive/`, don't remove history.
- **Verify by looking** — for any figure/HTML change, actually render it and look before you claim
  it's done (see [`framework/figures-and-findings.md`](./framework/figures-and-findings.md)).
- **Honesty over cleverness** — the verification layer must flag uncertainty (`needs_review`), never
  fake confidence. Every value stays traceable to its source (a panel crop, a data file).
- **Add a test** — new behavior comes with a test; the suite stays hermetic (no network, no `work/`).

## Where things go
This repo follows its own [documentation & handoffs](./framework/documentation-and-handoffs.md)
convention. New synthesis/how-to → `framework/` or `docs/`; a design decision → the relevant doc + a
note; raw assets → committed only when license-permitted (e.g. the CC-BY test PDF).

## License
By contributing you agree your contributions are licensed under the repository's [MIT license](./LICENSE).
Only add data/assets you have the rights to redistribute.
