---
execution_id: 2026_07_29_22_08_40_WI_CARD_AUDIT_SKILLS
prompt_id: PROMPT(WI-CARD-AUDIT-SKILLS:WI_CARD_AUDIT_SKILLS)[2026-07-29T21:51:00-04:00]
work_item: WI-CARD-AUDIT-SKILLS
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/54
commit: cf36b88b424f63201712ccb072fee9a4217d8560
created_at: 2026-07-29T22:08:40-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-AUDIT-SKILLS.md
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Implemented WI-CARD-AUDIT-SKILLS — Phase 0b's family-dispatched card audit
skills. Builds `prosoc-card-audit` (single card) and `prosoc-card-audit-all`
(fan-out), generalizing the retired `prosoc-scenario-audit(-all)` to all five
card families per `PROP-NORMATIVE-PACKET-ASSEMBLY` Decision 7.

# Result

- `.claude/skills/_shared/audit_checklists/`: `scenarios.md` migrated
  verbatim from `prosoc-scenario-audit/references/audit_checklist.md` (paths
  fixed for the new location); `tasks.md` and `contexts.md` new, derived from
  each family's `schema.json` + `template.md`; `constitutions.md` new — no
  prior `audit.md` precedent, grounded in the root-wrapped `constitution:`
  shape; `charter.md` new and bespoke — audits all ten principles
  collectively in one document, not per-card.
- `prosoc-card-audit/SKILL.md`: family-dispatched. Resolves family from the
  named card id (or explicit family name); locates the card; dry-run
  distills for freshness (only scenarios has per-card `--scenario` scoping —
  tasks/contexts/constitutions dry-run necessarily re-validates the whole
  family, documented explicitly so an auditor doesn't fold unrelated drift
  into this audit's verdict); runs the resolved checklist; writes a
  findings-only `audit.md` (or `prosoc/charter/audit.md` for the charter, no
  id). Never edits a card or promotes STATE — same contract as the retired
  skill.
- `prosoc-card-audit-all/SKILL.md`: fans out across one family, several, or
  the whole corpus; batches of 2; aggregates verdicts/findings into a table;
  detects recurring patterns via exact-match finding-title normalization
  (case-fold, strip numbering/severity) at a configurable card-count
  threshold (default 3); writes `AUDIT_SUMMARY.md` — per-family for a
  single-family run (mirrors today's scenario behavior exactly), plus one
  aggregate `project/audits/CARD_AUDIT_SUMMARY.md` for multi-family/corpus
  runs (a settled design decision from the confirm-gate plan).
- Retired `prosoc-scenario-audit(-all)` (`git rm -r`); updated cross-references
  in `prosoc/scenarios/workflow.md`, `prosoc-scenario-new/SKILL.md`,
  `project/audits/README.md`, and `project/focus/current_focus.md`. Left
  card/report content (scenario.md prose citations, existing audit.md
  provenance lines) deliberately untouched — editing those would violate
  `forbidden_actions: edit_card_normative_content`.

Manually validated per the WI's own `## Validation` section (see below) rather
than relying on inspection alone — audited one real card per family, plus a
full-family `prosoc-card-audit-all` run on tasks (the smallest corpus) to
exercise aggregation and recurring-pattern detection against genuine content.
That run surfaced two real cross-card patterns in the tasks family (a Common
Failure Modes fidelity gap in 4/4 cards, dangling `example_scenarios` in 3/4),
correctly detected by the exact-title-match logic. The charter audit
independently found a genuine structural gap: 6 of 10 principles are missing
the `### Explanation` subsection the charter's own Section 3 promises every
principle has — a real finding from dogfooding the new skill, not scaffolding.

Design decisions settled at implement time (per the confirmed plan): family
dispatch by natural-language card-id resolution, not CLI flags; the
per-family vs. multi-family `AUDIT_SUMMARY.md` location split; card/report
content left untouched by design. Prior-art check present in the WI. No
`prosoc/` Python, schema, or distiller changes; no normative card content
changed.

# Validation

- `scripts/test`: 190 passed (no Python touched — confirms no regression).
- `scripts/lint`: All checks passed.
- `scripts/format --check` (black 25.12.0): clean (68 files unchanged).
- `lrh validate`: 0 errors, 0 warnings.
- Manual: `prosoc-card-audit` run against `blind_corner` (scenarios), all 4
  task cards (tasks), `high_urgency` (contexts), `asimov_three_laws`
  (constitutions), and the charter — `git diff` on every audited card's
  Markdown/YAML confirmed empty (zero mutation) in every case.
- Manual: `prosoc-card-audit-all` logic exercised on the tasks family —
  `prosoc/tasks/AUDIT_SUMMARY.md` aggregates all 4 verdicts correctly and
  both recurring patterns cross-checked by hand against the threshold.
- Repo-wide `grep` scan: zero leftover `/prosoc-scenario-audit` references
  outside intentionally-untouched card/report content and immutable
  execution-record history.

# Follow-up

- At closeout, resolve WI-CARD-AUDIT-SKILLS (Phase 0b's engine is done). The
  workstream stays open for Phase 2 (manifest card family) and Phase 3 (CI
  drift check).
- The findings surfaced in this run's audits (charter's missing Explanation
  subsections; tasks' Common Failure Modes / example_scenarios patterns;
  contexts' two should-fix items) are real corpus findings for a human editor
  to act on — not addressed here, per the audit skills' own findings-only
  contract.
