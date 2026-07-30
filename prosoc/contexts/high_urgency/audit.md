---
family: contexts
card: high_urgency
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 0
audited: 2026-07-29
---

# Audit: Emergency High-Urgency Operation

- **Card:** `prosoc/contexts/high_urgency/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-07-29
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Common tension wording drift — should-fix
- **Section/field:** Relationship to Prosocial Navigation Principles vs.
  `principle_emphasis.common_tensions`
- **Issue:** Prose lists "urgency versus perceived rudeness" as a common
  tension, but the YAML list has "urgency versus politeness" in that slot —
  a paraphrase, not the same phrase, and "perceived rudeness" and
  "politeness" aren't quite the same axis (one is an outcome/perception,
  the other a norm).
- **Recommended fix:** Reconcile the wording — pick one phrasing and use it
  in both places (or note explicitly in prose if they are meant to describe
  slightly different things).

### 2. `related_contexts` prose/YAML mismatch — should-fix
- **Section/field:** Derived and Related Contexts vs. `related_contexts`
- **Issue:** Prose lists three related contexts (`service.routine_delivery`,
  `baseline.public_navigation`, `emergency.coordinated_response`), but the
  YAML `related_contexts` only has the first two. The third,
  `emergency.coordinated_response`, has no matching card under
  `prosoc/contexts/` — it's a prose-only forward reference to a context not
  yet drafted.
- **Recommended fix:** Either add `emergency.coordinated_response` to
  `related_contexts` once it exists as a card (not before, per the "resolve
  to a real card" convention `related_scenarios` enforces for scenarios), or
  note explicitly in prose that it is a planned/future context rather than
  presenting it as an existing peer of the other two.

## Prose/YAML Consistency

Context Summary, Context Description, Normative Significance, and all five
Context Axes Instantiated subsections align with `context_class`,
`primary_robot_role`, `applies_to_tasks`, and `axes.*`. Relationship to
Prosocial Navigation Principles correctly identifies P0/P1/P9 as emphasized
and P2/P3 as deprioritized, matching `principle_emphasis.{emphasized,
deprioritized}` exactly, with the deprioritized principles still actively
discussed in prose (annotated, not dropped, per Decision 6 of
`PROP-NORMATIVE-PACKET-ASSEMBLY`). Applicability and Limits matches
`limits.{includes,excludes}`. See Findings 1–2 for the two discrepancies
found.

## Schema and Charter Compliance

- `scripts/distill/contexts --dry-run --show-diffs` produced no diff and no
  schema validation error (whole-family dry-run; no other context in the
  corpus showed drift either).
- `principle_emphasis.emphasized` (P0, P1, P9) and `.deprioritized` (P2, P3)
  — all valid P0–P9 IDs, no overlap between the two lists.
- `axes.*` fields stay qualitative/descriptive throughout — no numeric
  weightings encoded, consistent with the template's explicit instruction.
- `related_contexts` entries (`service.routine_delivery`,
  `baseline.public_navigation`) both resolve to real context cards by their
  dotted `id` field (contexts key `related_contexts` by `id`, not directory
  name — verified against `routine_delivery/context.yml` and
  `public_navigation/context.yml`).

## Completeness

All Required sections present: Context Summary, Context Description,
Normative Significance, Context Axes Instantiated (all five subsections),
Relationship to Prosocial Navigation Principles, Applicability and Limits.
Both optional-but-recommended sections (Derived and Related Contexts, Example
Scenario Classes) are populated — see Finding 2 for the one content issue.
