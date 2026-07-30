---
family: charter
card: charter
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 0
audited: 2026-07-29
---

# Audit: Prosocial Robot Navigation Charter

- **Card:** `prosoc/charter/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-07-29
- **Verdict:** Ready for AUDITED with fixes

## Findings

### 1. Six of ten principles lack a "### Explanation" subsection — should-fix
- **Section/field:** Principles P4–P9's structure vs. Section 3's stated
  requirement
- **Issue:** Section 3 ("Structure of the Principles") states every principle
  "includes: A normative statement, A human-readable explanation,
  Illustrative examples, A severity level." P0–P3 each have a `###
  Explanation` subsection between their Normative Statement and the fenced
  YAML block; **P4 (Politeness), P5 (Social Competency), P6 (Agent
  Understanding), P7 (Proactivity), P8 (Contextual Appropriateness), and P9
  (Prosocial Behavior) do not** — they go directly from Normative Statement
  to the YAML block.
- **Recommended fix:** Add a `### Explanation` subsection to each of P4–P9,
  matching the depth/purpose of P0–P3's (elaborating intent, scope, and
  motivation — see the Definitions and Glossary's own "Explanation" entry for
  what this section is supposed to do).

### 2. Some principles' YAML `description` states normative content that
   appears nowhere in the prose — should-fix
- **Section/field:** `description` vs. Normative Statement (and, where
  present, Explanation)
- **Issue:** P1's `description` adds "This includes maintaining a safe
  distance unless explicitly invited to approach" — a specific normative
  requirement not stated in either P1's Normative Statement or its
  Explanation subsection. P4's `description` adds "offering help when asked
  and avoiding dismissive or intrusive behaviors," and P5's adds "avoid
  inappropriate behaviors such as interrupting conversations or blocking
  passage" — in both cases more specific than the bare Normative Statement,
  and (per Finding 1) neither P4 nor P5 has an Explanation subsection to
  house it. Since `description` is the authoritative machine-readable text
  (Section 3), a reader of only the human-readable prose would miss these
  constraints entirely.
- **Recommended fix:** Either fold each addition into the principle's prose
  (Normative Statement or a new Explanation, per Finding 1), or, if the
  addition is intentionally YAML-only elaboration, note that explicitly
  rather than leaving it silently prose-invisible.

## Prose/YAML Consistency

For seven of ten principles (P0, P2, P3, P6, P7, P8, P9), the prose Normative
Statement and `description` match closely (P2's added detail is captured by
its Explanation subsection; P0/P3/P7 match verbatim; P6/P8/P9 are minor,
non-material paraphrases). See Findings 1–2 for the three principles (P1, P4,
P5) where `description` carries content absent from the prose entirely.

## Schema Compliance

- `scripts/distill/charter --dry-run --show-diffs` produced no differences —
  `charter.yml` is in sync with `charter.md`'s fenced YAML blocks and
  validates against `schema.json`.
- Exactly ten principles, `id` values `P0`–`P9`, no duplicates, no gaps.
- Every principle has `id`/`name`/`description`/`severity`/
  `examples.{positive,negative}`, all non-empty; every `severity` is a valid
  enum value (`critical`, `high`, `medium`, `optional`).
- `state: DRAFTED` is authored in the fenced YAML `## Status` block
  (fenced-YAML-authoritative), not inferred from the descriptive
  `**Status:** Draft (Normative)` top-matter line.
- P1 (Safety) is `severity: critical` — the only critical-severity
  principle, consistent with the charter's own framing ("Safety violations
  override all other considerations").

## Collective Coherence

The ten principles do not overlap to the point of redundancy — P4
(Politeness, interpersonal courtesy) and P5 (Social Competency, general norm
compliance) read as conceptually related but distinct, consistent with the
P&G paper's own eight-principle taxonomy that P1–P8 are drawn from. P0 (Goal
Achievement) and P9 (Prosocial Behavior) — this project's own extensions —
are clearly distinct from each other and from P1–P8. `.claude/skills/
_shared/principles.md`'s summary table matches the charter's own P0–P9
names and framing; no drift found there.

## Completeness

All structural sections are present: `## Status`, `## 1. Purpose of This
Charter`, `## 2. Definition`, `## 3. Structure of the Principles`, `## 14.
Use of This Charter`, `## Definitions and Glossary`, `## References`. All ten
principles have every schema-required field. See Finding 1 for the one
structural gap (missing Explanation subsections on six principles), which is
a completeness issue at the level of the charter's own stated structure, not
the schema.
