#!/usr/bin/env python3
"""
bootstrap.py — the one-line Lab Brain installer (the D4 "clone -> setup" surface).

Run once after cloning. It wires a project (yours, or a teammate's) up so that both
Claude Code and Claude Science have this lab's skills + conventions preloaded, and it
seeds the shared collaboration structure in your KB. No network, no build step.

    git clone <this-repo> && cd lab-brain && python bootstrap.py

Common flags (all optional; sensible defaults, non-interactive-friendly):
    --target DIR     where to install the .claude skills (default: current dir)
    --kb DIR         where to seed the shared KB collab files (default: ./labbrain_vault)
    --members "A:pi, B:collaborator, C:trainee"   seed the roster + per-person logs
    --no-skills      skip copying skills
    --force          overwrite existing files

What it does (idempotent — safe to re-run):
  1. Copies .claude/skills + .claude/commands into <target>/.claude/  (your agents get
     /lab-init, /lab-scan, /lab-index, /lab-link, /lab-ask, /lab-standup, /lab-read-figure, ...)
  2. Copies lab-profile.example.yaml -> <target>/lab-profile.yaml  (edit this one file)
  3. Seeds the shared KB with the collaboration templates (START_HERE, _handoff-log, LANES,
     and a progress-<person>.md per roster member).
  4. Prints the next steps.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent

# Only emit ANSI color when writing to a real terminal (clean logs/video otherwise).
_TTY = sys.stdout.isatty()


def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if _TTY else s


def info(msg: str) -> None:
    print(f"  {_c('36', '->')} {msg}")


def ok(msg: str) -> None:
    print(f"  {_c('32', 'OK')} {msg}")


def copy_tree(src: Path, dst: Path, force: bool) -> int:
    """Copy a directory tree, skipping existing files unless --force. Returns #files written."""
    n = 0
    for item in src.rglob("*"):
        if item.is_dir() or "__pycache__" in item.parts:
            continue
        rel = item.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            continue
        shutil.copy2(item, target)
        n += 1
    return n


def parse_members(spec: str) -> list[tuple[str, str]]:
    """'Bobby:collaborator, Faye:trainee' -> [('Bobby','collaborator'), ('Faye','trainee')]"""
    out: list[tuple[str, str]] = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            name, role = chunk.split(":", 1)
        else:
            name, role = chunk, "collaborator"
        out.append((name.strip(), role.strip() or "collaborator"))
    return out


def seed_collab(kb: Path, members: list[tuple[str, str]], force: bool) -> None:
    """Copy the collaboration templates into the KB and seed per-person progress logs."""
    templates = REPO / "collab" / "templates"
    kb.mkdir(parents=True, exist_ok=True)
    for name in ("START_HERE.md", "_handoff-log.md", "LANES.md"):
        target = kb / name
        if target.exists() and not force:
            info(f"kept existing {name}")
            continue
        shutil.copy2(templates / name, target)
        ok(f"seeded {name}")
    person_tpl = (templates / "progress-PERSON.md").read_text(encoding="utf-8")
    for name, role in members:
        target = kb / f"progress-{name.lower().replace(' ', '-')}.md"
        if target.exists() and not force:
            continue
        body = person_tpl.replace("<person>", name).replace("<pi|collaborator|trainee>", role)
        target.write_text(body, encoding="utf-8")
        ok(f"seeded progress-{name} ({role})")


def main() -> int:
    ap = argparse.ArgumentParser(description="Lab Brain one-line installer")
    ap.add_argument("--target", default=".", help="where to install .claude skills")
    ap.add_argument("--kb", default="./labbrain_vault", help="where to seed the shared KB")
    ap.add_argument("--members", default="", help='e.g. "Bobby:collaborator, Faye:trainee"')
    ap.add_argument("--no-skills", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    kb = Path(args.kb).resolve()
    members = parse_members(args.members)

    print("\n" + _c("1", "Lab Brain - bootstrap"))
    print(f"  repo:   {REPO}")
    print(f"  target: {target}")
    print(f"  kb:     {kb}\n")

    if not args.no_skills:
        info("installing Claude skills + commands ...")
        n = copy_tree(REPO / ".claude", target / ".claude", args.force)
        ok(f"installed {n} skill/command files into {target / '.claude'}")

    profile = target / "lab-profile.yaml"
    if not profile.exists() or args.force:
        shutil.copy2(REPO / "lab-profile.example.yaml", profile)
        ok(f"wrote {profile.name} (edit this one file to fit your lab)")
    else:
        info("kept existing lab-profile.yaml")

    info("seeding shared collaboration structure ...")
    seed_collab(kb, members, args.force)

    print("\n" + _c("1", "Next:"))
    print("  1. Edit lab-profile.yaml (storage roots, naming, ROSTER+roles, vocabulary).")
    print("  2. In Claude Code, run  /lab-init  to finish configuring + review the profile.")
    print("  3. Then  /lab-scan -> /lab-index -> /lab-link  to build the shared brain.")
    print("  4. Try  /lab-read-figure  on an OA paper, and  /lab-standup  for the team digest.")
    print("\n  Collaboration convention: collab/harness-playbook.md  (read before two people/harnesses work at once)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
