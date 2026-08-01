---
family: constitutions
card: asimov_four_laws
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-08-01
---

# Audit: Asimov's Four Laws of Robotics

- **Card:** `prosoc/constitutions/asimov_four_laws/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-01
- **Verdict:** Ready, no issues found

## Findings

No findings. This is a re-audit after two should-fix findings from the
2026-08-01 initial pass were addressed:

1. The `## Discussion` section's malformed list (a doubled bullet marker
   and a missing top-level bullet that buried "Assumptions about
   environment:" as unmarked continuation text) has been restructured into
   three parallel top-level bullets (Known ambiguities / Assumptions about
   environment / Ethical tradeoffs), matching `template.md`'s pattern. The
   orphaned "Arguably leads to robots taking over human civilization" line
   was moved under Ethical tradeoffs, where it fits as a stated risk rather
   than an ambiguity.
2. `rules[3]` (`L3`)'s `text` was reworded from "A robot **must** protect
   its own existence..." to "A robot **should** protect its own
   existence...", now matching `type: should`, `priority: low`, and the
   `rationale`'s "is allowed" framing.

Both fixes are prose/wording-only — no rule's `id`, `type`, `priority`,
`rationale`, `examples`, `evaluation_tags`, `scope`, or
`conflict_resolution` changed. `constitution.yml` is in sync with
`constitution.md` (confirmed via
`scripts/distill/constitutions --dry-run --show-diffs`, no diff for this
card after regenerating).

All required schema fields remain present and valid: fenced YAML is
correctly root-wrapped under `constitution:`; `id`/`name`/`state`/`rules`
present; every `rules[].type` is `must`/`must_not`/`should` and every
`priority` is `high`/`medium`/`low`, now with `L3`'s phrasing consistent
with its typing; no two rules directly contradict; `conflict_resolution`
explicitly orders both `high`-priority rules (`L0` overrides `L1`).

## Completeness

All required fenced-YAML fields present: `id`, `name`, `state`, `rules`
(4 rules, each with `id`/`text`/`type`/`priority`). STATUS block present
with `STATE` as the first bullet.

Optional-but-recommended content is filled in throughout: `scope`, every
rule's `rationale`/`examples`/`evaluation_tags`, `conflict_resolution`,
and `## Discussion` (now correctly structured).
