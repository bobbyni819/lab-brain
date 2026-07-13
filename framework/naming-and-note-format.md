# Naming & note format — so filename-sort = sense, and every note is linkable

Consistent names mean a plain directory listing is already meaningful, links are predictable, and
nobody wonders "is this the latest version?" These are lifted from a KB that drifted into three
competing date formats before the convention was fixed.

## File naming convention

| File type | Pattern | Example |
|---|---|---|
| Wiki concept / methodology page | `kebab-case.md`, **undated** | `mfc-normalization-method.md`, `panel-xlsx-guide.md` |
| Source article / paper | `AuthorLastName_Year_short-title.md` | `Smith_2024_intestinal-lipids.md` |
| Dated output (report / plan / draft / audit / order) | `kebab-name-YYYY-MM-DD.md` (**trailing ISO date**) | `panel-audit-2026-05-28.md` |
| Versioned doc | `kebab-name-vN.md` | `finalized-proposal-v1.md` |
| Per-person work log | `progress-<person>.md` | `progress-faye.md` |
| Mentor feedback | `feedback-<person>-YYYY-MM-DD.md` | `feedback-faye-2026-07-13.md` |

**Rules**
- Dated files use the **trailing `YYYY-MM-DD`** form — *not* `YYYYMMDD_` prefix, *not* a compact
  `-YYYYMMDD`. One consistent format so filename sort is chronological.
- Pick a **date suffix OR a `-vN` suffix — never both.**
- **Wiki pages stay undated** (they're living references); their `updated:` frontmatter tracks
  freshness instead.
- Many labs also carry an **incoming** convention on raw dumps (`YYYYMMDD_Topic_INITIALS`, e.g.
  `20260210_flu_ABM_BN.pptx`) — Lab Brain's scanner parses that automatically (date-prefix +
  initials → owner), so a messy incoming folder still yields clean provenance.

## Note format (every note starts here)
```markdown
---
title: Note Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [project, category, subcategory]
status: ACTIVE | COMPLETE | ARCHIVED | DRAFT
aliases: [alternate names for linking]
---

# Title

Brief description (1–2 sentences: what this note is and why it exists).

## Section 1
…

## Related
- [[Link to related concept]]
- [[Link to related note]]
```

**When writing any note**
1. Always include the YAML frontmatter (title, created, tags, status).
2. Connect with `[[wiki-links]]`; end with a `## Related` section.
3. For verified claims, include the **exact quote** + a section reference.
4. For data/statistics, cite the source file (CSV name, line/row).
5. Date entries — keep the audit trail.

The template lives at [`templates/note-template.md`](./templates/note-template.md); `bootstrap.py`
seeds it into the vault.
