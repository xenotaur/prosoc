---
family: charter
card: charter
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-08-06
---

# Audit: Prosocial Robot Navigation Charter

- **Card:** `prosoc/charter/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-06
- **Verdict:** Ready, no issues found

This closes out the should-fix/suggestion findings tracked across the
2026-07-29 through 2026-08-06 audits. This session's two remaining fixes:

- **P9's Explanation** (Section 13, "## 13. Principle P9 — Prosocial
  Behavior") no longer names the cross-family scenario
  `movable_obstruction`; the trade-off it illustrated (P0/P8 bounding P9)
  is now made with a self-contained inline example ("a delivery robot
  noticing an obstruction it could clear should weigh that against how
  much delay clearing it would add to its own task and how urgent that
  task is"). The charter no longer depends on any other family's card
  content or lifecycle state to be understood on its own.
- **Section 3's principle list** ("## 3. Structure of the Principles") now
  reads "**P8** Contextual Appropriateness" instead of the abbreviated
  "Context," matching P8's actual heading, YAML `name`, and
  `.claude/skills/_shared/principles.md`'s summary table.

## Findings

None.

## Prose/YAML Consistency

`scripts/distill/charter --dry-run --show-diffs` reports no differences —
`charter.yml` is exactly in sync with `charter.md`'s fenced YAML blocks.
This specific pass's two edits (the P9 Explanation rewrite and the
Section 3 list-item rename, listed above) are themselves prose-only and
touch no fenced YAML block; this is narrower than a claim about the PR as
a whole; the PR's earlier commits *did* change `charter.yml` (P9's
`description`/`examples`, the `state` field, etc.) — each of those was
verified in sync via the same dry-run check at the time, per the charter's
own earlier `EDITED` history. `scripts/validate/status --family charter`
confirms `state: EDITED` is consistent between the fenced YAML and the
projected `STATE` bullet.

All ten principles' prose (Normative Statement + Explanation) now fully
covers their `description` fields, with no one-sided claims in either
direction, per the 2026-08-06 fixes to P1/P4/P5 and the addition of
Explanations to P4–P8 earlier this session.

## Schema Compliance

- `scripts/distill/charter --dry-run --show-diffs` produced no
  differences — `charter.yml` validates against `schema.json`.
- Exactly ten principles, `id` values `P0`–`P9`, no duplicates, no gaps.
- Every principle has `id`/`name`/`description`/`severity`/
  `examples.{positive,negative}`, all non-empty; every `severity` is a
  valid enum value. P1 (Safety) remains `severity: critical`.
- No principle's examples read as generic enough to double as another
  principle's.

## Collective Coherence

- The ten principles remain non-redundant. P1/P2's proximity-related
  overlap is explicitly disambiguated in P1's own Explanation (a
  safety-relevant vs. comfort-relevant distinction). P7/P9's
  proactivity-vs-prosociality distinction is stated in both principles'
  Explanations.
- P9's Explanation is now fully self-contained per the charter's own
  Interpretive Locality goal (no dependency on another family's card or
  its lifecycle state).
- `.claude/skills/_shared/principles.md`'s summary table matches the
  charter's current P0–P9 names and framing; no drift found.

## Completeness

All structural sections are present: `## Status`, `## 1. Purpose of This
Charter`, `## 2. Definition`, `## 3. Structure of the Principles`, `## 14.
Use of This Charter`, `## Definitions and Glossary`, `## References`. All
ten principles have every schema-required field and a `### Explanation`
subsection. Section 3's principle list now names every principle
consistently with its actual heading. `## References`'s entry for Francis
et al. (2025) cites the correct venue.
