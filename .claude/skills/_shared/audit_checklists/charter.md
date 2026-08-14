# Prosoc Charter Audit Checklist

This is a verification rubric, companion to `src/prosoc/prnc/charter/schema.json`. Unlike
every other family, the charter is a **single document** (`src/prosoc/prnc/charter/charter.md`
-> `charter.yml`) holding ten principles, not a card-per-directory family — this
checklist audits the whole document collectively in one pass, not principle by
principle, and its output is one `src/prosoc/prnc/charter/audit.md`, not a per-principle file.

## Structural Shape (unique to this family)

- [ ] `charter.yml` is a top-level mapping with exactly `state` and `principles`
      (per `schema.json`'s `additionalProperties: false`) — not root-wrapped like
      constitutions
- [ ] `principles` contains exactly ten entries, `id` values `P0`–`P9`, no
      duplicates, no gaps
- [ ] `state` is authored in the fenced YAML `## Status` block (fenced-YAML-
      authoritative, per `src/prosoc/prnc/scenarios/workflow.md`'s foundation contract), not
      inferred from the descriptive `**Status:** Draft (Normative)` top-matter line

## Required Fields (schema.json, per principle)

| Field | Check |
|-------|-------|
| `id` | Matches `^P[0-9]+$`, unique across all ten |
| `name` | Matches the principle's `## N. Principle Px — <Name>` heading |
| `description` | The normative statement, non-empty |
| `severity` | One of `critical`, `high`, `medium`, `optional` |
| `examples.positive` / `.negative` | Both non-empty arrays |

## Prose/YAML Cross-Checks (per principle, but reported as one collective finding set)

| Prose subsection | Cross-check against fenced YAML field |
|---|---|
| Normative Statement | `description` |
| Explanation | (not directly machine-checked; should not contradict `description`) |
| Examples (positive/negative) | `examples.positive`, `examples.negative` |

Flag a **contradiction** when a principle's prose Normative Statement and its YAML
`description` diverge in substance (re-distill via
`python -m prosoc.prnc.charter.distill --dry-run --show-diffs` and treat any reported diff
as blocking — a tooling-freshness issue, not a prose/YAML content judgment call).

## Schema Compliance

- [ ] `charter.yml` validates against `schema.json`
- [ ] Every `severity` value matches the enum; check it against the P&G paper's
      framing of that principle's importance where traceable (P1 Safety at anything
      below `critical` would be a should-fix worth flagging explicitly)
- [ ] No principle's `examples` are generic enough to apply equally well to a
      different principle — a weak signal the principle's normative statement itself
      may be under-specified

## Collective Coherence (charter-specific — the ten principles as a system)

Unlike a per-card audit, the charter's primary risk is at the level of the whole
document:

- [ ] The ten principles do not overlap to the point of redundancy (two principles
      whose `description` and `examples` are effectively interchangeable)
- [ ] Coverage against `../principles.md`'s summary table — confirm this shared
      reference file has not drifted from the charter itself (the charter is the sole
      source of truth per that file's own header; flag `../principles.md` as stale if
      they disagree, but do not edit it as part of this audit)
- [ ] P0 (Goal Achievement) and P9 (Prosocial Behavior) — this project's own
      extensions beyond the P&G paper's eight — read as genuinely distinct from each
      other and from P1–P8, not restatements

## Completeness

- [ ] All ten principles have every required field (see above) — a charter missing
      examples for even one principle is incomplete, not merely a per-principle gap
- [ ] `## Status`, `## 1. Purpose`, `## 2. Definition`, `## 3. Structure of the
      Principles`, `## 14. Use of This Charter`, `## Definitions and Glossary`, and
      `## References` sections are present (structural sections, not per-principle
      content — their absence is a should-fix, not blocking, since the machine
      payload does not depend on them)
