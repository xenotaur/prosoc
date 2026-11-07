---
family: contexts
card: routine_delivery
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-11-07
---

# Audit: Routine Service Delivery

- **Card:** `src/prosoc/prnc/contexts/routine_delivery/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED, no blocking, should-fix, or suggestion
  findings.

This is a fresh audit written after `WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD`
demoted this card from a stale `APPROVED`: the new audit-currency guard
found that a 2026-10-27 formatting fix (`WI-CHARTER-SUPPLEMENT-SOURCE-FIXES`,
PR #112 — code-spanning `Context ID:`/`Applies To Tasks:` values, inserting
blank lines before bullet lists) postdated this card's last audit.md
(2026-08-01) and had never been given its own `EDITED:` bullet or re-audit.
The prior `audit.md` (2026-08-01) is not carried forward, since it predates
that formatting change and this review.

## Findings

### Resolved: "Common tensions" prose/YAML wording drift

Caught during this re-audit, independent of the audit-currency finding
above: the "Common tensions include" prose bullets ("direct delivery
routes versus human comfort," "service effectiveness versus willingness
to yield") were paraphrases, not exact matches, of
`principle_emphasis.common_tensions`'s existing wording ("delivery speed
versus human comfort," "task completion versus yielding"). Reworded the
prose to match the YAML exactly. Re-distilled
(`scripts/distill/contexts --dry-run --show-diffs` reports no diff for
this field, since only the Markdown prose changed) and schema-validated
clean.

## Prose/YAML Consistency

- **Context Summary vs. `context_class`/`primary_robot_role`/`applies_to_tasks`:**
  Consistent. `CONTEXT TYPE: CORE` matches `context_class: core`;
  `Primary Role of Robot: service provider` is a social role, not a task
  description; `Applies To Tasks: deliver.object` matches
  `applies_to_tasks: [deliver.object]` exactly.
- **Context Axes Instantiated vs. `axes.*`:** All five subsections
  (Cultural, Diversity, Environmental/Geometric, Environmental/Operational,
  Task, Interpersonal) map cleanly onto their matching `axes` keys —
  consistent in substance, no contradictions.
- **Relationship to Prosocial Navigation Principles vs.
  `principle_emphasis`:** Prose names P0, P1, P2, P3, P9 as emphasized;
  YAML `emphasized: [P0, P1, P2, P3, P9]`, `deprioritized: []` — exact
  match, no principle discussed as deprioritized while actually emphasized
  or vice versa. Common tensions now consistent (see the resolved finding
  above).
- **Applicability and Limits vs. `limits.{includes,excludes}`:** Prose's
  two Includes bullets and three Excludes bullets consolidate cleanly onto
  the YAML's two-item `includes`/two-item `excludes` lists — paraphrased,
  not contradicted (e.g. prose's "Guidance or escort roles" and "explicit
  priority over humans" both fold into YAML's "roles involving guidance or
  authority").
- **Derived and Related Contexts vs. `related_contexts`:** Prose names
  `emergency.high_urgency`, `workplace.formalized_service`,
  `baseline.public_navigation` (order differs from YAML, not a defect);
  YAML has the same three. `emergency.high_urgency` and
  `baseline.public_navigation` both resolve to real context cards.
  `workplace.formalized_service` does not yet exist as a card — already
  tracked in `project/design/backlog.md`'s "Missing forward-referenced
  cards" table (noted 2026-08-01), not a new finding.

## Schema and Charter Compliance

- `context.yml` validates against `schema.json`: no
  `additionalProperties` violations; `axes.environmental` has only
  `geometric`/`operational`; `principle_emphasis` has only
  `emphasized`/`deprioritized`/`common_tensions`; `limits` has only
  `includes`/`excludes`.
- `principle_emphasis.emphasized` entries (`P0, P1, P2, P3, P9`) are all
  valid P0–P9 IDs; `deprioritized` is empty — no principle appears in
  both lists.
- `axes.*` fields stay qualitative/descriptive throughout — no numeric
  weightings, consistent with `template.md`'s instruction.
- `scripts/distill/contexts --dry-run --show-diffs` (whole-family
  dry-run, run fresh for this audit with the correct `PYTHONPATH` for
  this checkout) reports no diff and no schema-validation error for this
  card.

## Completeness

All Required sections (per `template.md`) are present and filled: Context
Summary, Context Description, Normative Significance, Context Axes
Instantiated (all five subsections), Relationship to Prosocial Navigation
Principles, Applicability and Limits. Both optional-but-recommended
sections (Derived and Related Contexts, Example Scenario Classes) are
populated and consistent with the YAML.

`VALIDATED: —` is reasonably blank — this context has not yet been
supported by empirical evidence, and `VALIDATED` is an optional, later
lifecycle stage per `workflow.md`.
