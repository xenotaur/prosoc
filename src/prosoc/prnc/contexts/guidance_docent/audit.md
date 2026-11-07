---
family: contexts
card: guidance_docent
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-11-07
---

# Audit: Guidance and Docent Operation

- **Card:** `src/prosoc/prnc/contexts/guidance_docent/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED, no blocking, should-fix, or suggestion
  findings.

This is a fresh audit written after `WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD`
demoted this card from a stale `APPROVED`: the new audit-currency guard
found that a 2026-10-27 formatting fix (`WI-CHARTER-SUPPLEMENT-SOURCE-FIXES`,
PR #112 — code-spanning `Context ID:`/`Applies To Tasks:` values, inserting
blank lines before bullet lists) postdated this card's last audit.md
(2026-08-02) and had never been given its own `EDITED:` bullet or re-audit.
The prior `audit.md` (2026-08-02) is not carried forward, since it predates
that formatting change and this review.

## Findings

### Resolved: `primary_robot_role` prose/YAML mismatch

Caught during this re-audit, independent of the audit-currency finding
above: the Context Summary's `Primary Role of Robot: guide / escort` and
the YAML's `primary_robot_role: guide` disagreed — the YAML dropped
"escort" entirely, even though the card's own Context Description opens
with "a robot leads, escorts, or guides" and its title is "Guidance and
Docent Operation." Expanded `primary_robot_role` to `guide / escort`,
matching the prose exactly. Re-distilled
(`scripts/distill/contexts --dry-run --show-diffs` shows exactly this one
field changing, nothing else) and schema-validated clean.

## Prose/YAML Consistency

- **Context Summary vs. `context_class`/`primary_robot_role`/`applies_to_tasks`:**
  Now consistent (see the resolved finding above). `CONTEXT TYPE: CORE`
  matches `context_class: core`; `Applies To Tasks: navigate.lead_agent`
  matches `applies_to_tasks: [navigate.lead_agent]` exactly.
- **Context Axes Instantiated vs. `axes.*`:** All five subsections map
  cleanly onto their matching `axes` keys — consistent in substance.
- **Relationship to Prosocial Navigation Principles vs.
  `principle_emphasis`:** YAML `emphasized: [P2, P3, P9]`,
  `deprioritized: [P0]`. Prose explicitly discusses P3 as "strongly
  emphasized," P2 as "important," and P9 as "expressed through
  attentiveness" (all three named emphasized in YAML); P0 is discussed as
  "reframed as successful guidance rather than mere arrival" — not
  silently dropped, satisfying the checklist's requirement that a
  deprioritized principle remain discussed as present, per
  `PROP-NORMATIVE-PACKET-ASSEMBLY` Decision 6. Common tensions
  (`pace versus group cohesion`, `efficiency versus clarity`, `autonomy
  versus responsiveness`) are an exact match between prose and YAML.
- **Applicability and Limits vs. `limits.{includes,excludes}`:** Prose's
  two Includes bullets and three Excludes bullets consolidate cleanly onto
  the YAML's two-item `includes`/two-item `excludes` lists — paraphrased,
  not contradicted.
- **Derived and Related Contexts vs. `related_contexts`:** Prose names
  `baseline.public_navigation`, `service.routine_delivery`,
  `guidance.accessibility_sensitive`; YAML has the same three, same
  order. The first two resolve to real context cards.
  `guidance.accessibility_sensitive` does not yet exist as a card —
  already tracked in `project/design/backlog.md`'s "Missing
  forward-referenced cards" table (noted 2026-08-01), not a new finding.

## Schema and Charter Compliance

- `context.yml` validates against `schema.json`: no
  `additionalProperties` violations; `axes.environmental` has only
  `geometric`/`operational`; `principle_emphasis` has only
  `emphasized`/`deprioritized`/`common_tensions`; `limits` has only
  `includes`/`excludes`.
- `principle_emphasis.emphasized` (`P2, P3, P9`) and `.deprioritized`
  (`P0`) entries are all valid P0–P9 IDs; no principle appears in both
  lists.
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
