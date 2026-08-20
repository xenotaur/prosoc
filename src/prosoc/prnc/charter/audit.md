---
family: charter
card: charter
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-19
---

# Audit: Prosocial Robot Navigation Charter

- **Card:** `src/prosoc/prnc/charter/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-19
- **Verdict:** Ready, no blocking or should-fix issues found

This audit reviews the `WI-CHARTER-FRONTIERS-SYNC` content edit that
implements `PROP-CHARTER-FRONTIERS-SYNC`'s reconciliation decisions
against the Frontiers paper "The Prosocial Robot Navigation Charter"
(Francis, submitted): P1's broadened Safety scope (other robots,
self-damage); P2/P3/P4/P7's merged wording; P5's restored "where
feasible" hedge; P6's modal-only change; P8's inlined six-context
taxonomy; P9's trimmed task/context/goals qualifier; and the
MUST-for-P0-and-P1/SHOULD-elsewhere modal convention applied across all
ten principles' normative statements and YAML `description` fields.

During this audit, P1's Explanation prose was found not to reflect its
newly broadened Normative Statement (it still narrated only "harms
people or damages shared environments," omitting the newly-added
other-robots and self-damage protection) — this was fixed directly as
part of implementation before finalizing this audit, not left as an
open finding, since it was squarely in scope for the edit that
introduced the gap.

## Findings

### 1. `principles.md`'s summary table uses stale pre-restructure paths — suggestion
- **Section/field:** N/A (external shared reference file, not the charter itself)
- **Issue:** `.claude/skills/_shared/principles.md`'s header cites
  `prosoc/charter/charter.md`/`prosoc/charter/charter.yml`; the actual
  path since PR #95's package restructure is
  `src/prosoc/prnc/charter/charter.md`/`charter.yml`. This is a path
  staleness issue, not a content disagreement — the table's principle
  descriptions themselves still accurately summarize the charter's
  content after this edit.
- **Recommended fix:** Update `principles.md`'s header paths in a
  separate, small edit (out of this WI's scope per its Non-Goals — this
  WI touches only `charter.md`/`charter.yml`/`audit.md`).

## Prose/YAML Consistency

`scripts/distill/charter --dry-run --show-diffs` reports no differences
— `charter.yml` is exactly in sync with `charter.md`'s fenced YAML
blocks, for all ten principles including the nine edited this session.

Each edited principle's Normative Statement and YAML `description` were
checked pairwise; all match in substance (P1, P2, P3, P7, P8, P9 are
verbatim-identical between prose and YAML; P4, P5, P6 carry the same
pre-existing pattern of the YAML `description` restating the normative
content with minor additional elaboration that predates this edit and
was already accepted in the 2026-08-06 audit — not re-litigated here
per this WI's Non-Goals).

## Schema Compliance

- `charter.yml` validates against `schema.json` (confirmed via
  `lrh validate`, 0 errors).
- Every `severity` value is unchanged from the pre-edit charter, per
  `PROP-CHARTER-FRONTIERS-SYNC`'s explicit decision not to re-level
  severity. P1 (Safety) remains `critical`.
- No principle's examples were changed by this edit; none read as
  interchangeable with another principle's.

## Collective Coherence

- The ten principles remain distinct; no new redundancy introduced by
  this edit's wording changes.
- P0 and P9 remain genuinely distinct from each other and from P1–P8 —
  P9's trimmed normative statement (no longer restating the
  task/context/goals qualifier) does not collapse it into P0 or P8,
  since the Explanation still explicitly cross-references both ("It
  should never be read as license to sacrifice the robot's own goals
  (P0) or to act inappropriately for the task or context (P8)").
- Coverage against `.claude/skills/_shared/principles.md`'s summary
  table: content-wise consistent (see Finding 1 for that file's own
  path-staleness-only issue, unrelated to this audit's own reference to
  it).

## Completeness

- All ten principles retain every required field (`id`, `name`,
  `description`, `severity`, `examples.positive`, `examples.negative`).
- `## Status`, `## 1. Purpose`, `## 2. Definition`, `## 3. Structure of
  the Principles`, `## 14. Use of This Charter`, `## Definitions and
  Glossary`, and `## References` sections are all present and
  unmodified by this edit (Section 2's definition was explicitly
  preserved unchanged, per `PROP-CHARTER-FRONTIERS-SYNC`'s decision that
  only P9's own statement — not the general definition — drops the
  qualifier).
