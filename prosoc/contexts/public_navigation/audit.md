---
family: contexts
card: public_navigation
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-08-01
---

# Audit: Baseline Public Navigation

- **Card:** `prosoc/contexts/public_navigation/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-01
- **Verdict:** Ready, no issues found

## Findings

No findings. `context.yml` is in sync with `context.md` (confirmed via
`scripts/distill/contexts --dry-run --show-diffs`, no diff for this card).
All required schema fields are present and valid:

- `id: baseline.public_navigation` matches the dotted-id pattern.
- `context_class: core` matches the STATUS block's `CONTEXT TYPE: CORE`.
- `primary_robot_role: neutral navigator` is a social role, not a task
  description.
- `applies_to_tasks: ["*"]` uses the schema's documented general-applicability
  wildcard, consistent with this being the baseline/default context.
- All five `axes` subsections are present, non-empty, and stay
  qualitative/descriptive rather than numeric weightings.
- `principle_emphasis` has all three required keys; every entry
  (`P1`, `P2`, `P3` emphasized; `P0` deprioritized) matches `^P[0-9]+$` and
  no principle appears in both lists.
- `P0`'s deprioritization is properly treated as an annotation, not a
  removal — the prose explicitly discusses it ("P0 (Goal Achievement) is
  constrained by the above principles and rarely justifies aggressive
  behavior") rather than silently dropping it from the normative picture.
- `limits.includes`/`limits.excludes` both present and consistent with the
  prose's "Includes"/"Excludes" lists.
- `related_contexts` (`service.routine_delivery`, `environment.child_centric`,
  `environment.dense_crowd`) — the first resolves to a real context card;
  the latter two are forward references to contexts not yet drafted in the
  corpus. This mirrors the same pattern already accepted in
  `guidance_docent`'s audit (`guidance.accessibility_sensitive`), so it is
  not flagged here either — `related_contexts` appears to be an intentional
  scaffolding field, not a strict existence-checked reference.

Prose/YAML cross-checks (Context Summary, Context Axes Instantiated,
Relationship to Prosocial Navigation Principles, Applicability and Limits)
all agree with their corresponding YAML fields — no contradictions or drift.

## Completeness

All required sections (per `template.md`) are present and filled in:
Context Summary, Context Description, Normative Significance, Context Axes
Instantiated (all five subsections), Relationship to Prosocial Navigation
Principles, Applicability and Limits.

Optional-but-recommended sections are also filled in: Derived and Related
Contexts, Example Scenario Classes.
