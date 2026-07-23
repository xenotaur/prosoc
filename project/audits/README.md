# Audits

This directory holds engineering/repo-level audit and review reports —
LRH's own convention, not a prosoc invention. `lrh request audit-docs`'s
`--audit-output` flag defaults to
`<control-root>/audits/YYYY-MM-DD-docs-audit.md`, and the same directory
name is used the same way in LRH's own repo and in LCATS
(`xenotaur/LCATS`'s `lcats/project/audits/`, including a `docs/`
subfolder matching that exact default pattern).

## Not to be confused with scenario audits

`prosoc` has a second, unrelated "audit" concept: `prosoc/scenarios/<name>/audit.md`
and `prosoc/scenarios/AUDIT_SUMMARY.md`, produced by
`/prosoc-scenario-audit` and `/prosoc-scenario-audit-all`. Those check an
individual scenario card's prose/YAML consistency, schema and charter
compliance, and source fidelity — a step in the scenario content lifecycle
(`prosoc/scenarios/workflow.md`), not an engineering report. If you're
looking for scenario-card audit findings, they live there, not here.

## Contents

- [`2026-07-19_scenario_section_renderer_followup.md`](2026-07-19_scenario_section_renderer_followup.md):
  not itself an audit (see its own header) — a synthesis of which
  `prosoc/scenarios/<name>/audit.md` findings were resolved by PR #21/#22's
  section renderer, and what gaps remain for a human to fill in, gathered
  in one place to speed up the follow-up editing pass.
