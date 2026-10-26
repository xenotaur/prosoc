---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-SOURCE-FIXES
title: "Fix text-level defects in the charter supplement's 9 source cards"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
depends_on: []
blocked_by: []
expected_actions: [create_file, edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, modify_ci_pipeline]
acceptance:
  - "No prosoc/<family>/ pre-restructure path remains in the 9 included source cards"
  - "No .claude/skills/... path remains in any included source card"
  - "papers/01_charter/README.md's import path matches the actual module path"
  - "lrh validate reports 0 errors"
required_evidence: [manual_review, lrh_validate, test_output]
artifacts_expected:
  - src/prosoc/prnc/charter/charter.md
  - src/prosoc/prnc/scenarios/frontal_approach/scenario.md
  - src/prosoc/prnc/scenarios/single_file_hallway/scenario.md
  - src/prosoc/prnc/scenarios/movable_obstruction/scenario.md
  - src/prosoc/prnc/tasks/navigate_point_to_point/task.md
  - src/prosoc/prnc/tasks/deliver_object/task.md
  - src/prosoc/prnc/contexts/routine_delivery/context.md
  - src/prosoc/prnc/contexts/guidance_docent/context.md
  - src/prosoc/prnc/contexts/high_urgency/context.md
  - papers/01_charter/README.md
---

## Summary
Fix text-level defects across the 9 source cards included in the Frontiers
charter supplement: collapsed-list formatting, stale pre-restructure paths,
a leaked internal-tooling path, an internal AI-attribution string, a
dangling cross-reference, Task/Context-ID formatting inconsistency, and a
stale README import path.

## Problem / Context
`project/audits/2026-10-26_charter_supplement_pipeline_audit.md` found these
defects by direct inspection of the current tree. They're independent of
the renderer/template fixes (WI-CHARTER-SUPPLEMENT-RENDERER-FIXES) and the
lifecycle display fix (WI-CHARTER-LIFECYCLE-DISPLAY-FIX) — pure source-text
edits.

### Duplication search
- In-repo: no existing fix for these; confirmed by direct inspection.
- Sibling repos / external libraries: not applicable.
- Recommendation: Proceed.

### Demand search
- Work items / proposals / backlog: none found requesting this.
- Recommendation: No action.

## Scope
- Insert blank lines before Markdown lists after bold labels (`Includes`,
  `Excludes`, `Geometric Factors`, `Operational Factors`, "frequently
  interacts with", and unbolded `include:` variants) across the 9 sources.
- Fix stale `prosoc/<family>/...` paths to the current `src/prosoc/prnc/...`
  form.
- Remove or replace the `.claude/skills/...` internal-tooling reference.
- Reword the `SOURCE: Prompt to ChatGPT 5.2` string for publication.
- Resolve the dangling `blind_corner` Related-Scenario reference.
- Normalize `Context ID:`/`Applies To Tasks:` to code spans, matching
  `Task ID:`'s existing convention.
- Fix `papers/01_charter/README.md`'s stale import-path claim.

## Required Changes
1. `src/prosoc/prnc/charter/charter.md:28` — fix `` `prosoc/scenarios/workflow.md` ``.
2. `src/prosoc/prnc/scenarios/frontal_approach/scenario.md:145` — fix stale path; line 6 — reword SOURCE string; lines 28/110/146 — resolve `blind_corner` reference.
3. `src/prosoc/prnc/scenarios/movable_obstruction/scenario.md:164` — fix stale paths.
4. `src/prosoc/prnc/scenarios/single_file_hallway/scenario.md:9` — remove/replace `.claude/skills/...` reference.
5. Blank-line fixes at each collapsed-list location catalogued in the audit doc (across all 9 sources).
6. `src/prosoc/prnc/contexts/*/context.md` — code-span the `Context ID:`/`Applies To Tasks:` values.
7. `papers/01_charter/README.md:37` — correct the import path.

## Non-Goals
- Does not touch any card's lifecycle state — the `state:` field or the
  `STATE:`/`AUDITED:`/`APPROVED:` provenance bullets. (This does not
  prohibit the `frontal_approach/scenario.md:6` `SOURCE:` reword this item
  requires, which is a different field in the same `## STATUS` block.)
- Does not change renderer/template code (see WI-CHARTER-SUPPLEMENT-RENDERER-FIXES).
- Does not regenerate the golden file (see WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN).

## Acceptance Criteria
- No `prosoc/<family>/` pre-restructure path remains in the 9 source cards.
- No `.claude/skills/...` path remains in any included source card.
- `README.md`'s import path matches the actual module path.
- `lrh validate` reports 0 errors.

## Validation
- `lrh validate`
- `grep -rn "prosoc/\(charter\|scenarios\|tasks\|contexts\|constitutions\|manifests\)/" <9 files>` returns nothing
- `grep -rn "\.claude/skills" <9 files>` returns nothing
- `scripts/test`
