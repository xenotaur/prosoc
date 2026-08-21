---
resolution: null
blocked_reason: null
blocked: false
id: WI-SKILL-DOCS-SRC-LAYOUT-REFRESH
title: Refresh stale flat-layout paths in prosoc skill docs after the src/-layout migration
type: operation
status: proposed
owner: anthony
contributors:
  - anthony
assigned_agents: []
related_focus: []
related_roadmap: []
related_workstreams: []
related_design:
  - project/design/proposals/adopted/nca-prnc-package-layout/00_proposal.md
depends_on: []
blocked_by: []
expected_actions:
  - edit_file
forbidden_actions:
  - force_push
  - delete_branch
  - edit_card_normative_content
  - edit_historical_execution_records
acceptance:
  - Every listed file's stale flat prosoc/<family>/... or prosoc.<family> reference is updated to its new src/prosoc/{prnc,nca}/<family>/... (or src/prosoc/constitutions|manifests/...) location
  - grep for the old flat prosoc/<family>/ or prosoc.<family> pattern across .claude/skills/ returns zero matches outside card content and historical project/executions/ records
  - lrh validate passes with 0 errors
required_evidence:
  - lrh_validate
  - manual_review
artifacts_expected:
  - .claude/skills/prosoc-card-audit/SKILL.md
  - .claude/skills/prosoc-card-approve/SKILL.md
  - .claude/skills/prosoc-card-review/SKILL.md
  - .claude/skills/prosoc-card-review-all/SKILL.md
  - .claude/skills/prosoc-card-audit-all/SKILL.md
  - .claude/skills/prosoc-scenario-new/SKILL.md
  - .claude/skills/prosoc-scenario-new/references/schema_guide.md
  - .claude/skills/_shared/principles.md
  - .claude/skills/_shared/pg_scenarios.md
---

# Refresh stale flat-layout paths in prosoc skill docs after the src/-layout migration

## Summary

`WI-NCA-PRNC-PACKAGE-LAYOUT` moved prosoc's package from a flat `prosoc/` layout to `src/prosoc/{nca,prnc,constitutions,manifests}/`, and updated the 6 `.claude/skills/_shared/audit_checklists/*.md` files that work item's Required Changes explicitly named — but several other actively-used skill docs were left out of that scope and still reference nonexistent pre-move paths. Update them to the new paths.

## Problem / Context

`PROP-NCA-PRNC-PACKAGE-LAYOUT` / `WI-NCA-PRNC-PACKAGE-LAYOUT` (implemented in PR #95) deliberately scoped its Required Changes step 6 to only the 6 `_shared/audit_checklists/*.md` files, per its own documented non-goals around scope discipline. A cold-context `/lrh-self-review` subagent, dispatched independently against that same PR during its `/lrh-land` pass, read every `.claude/skills/*.md` file and confirmed (via `git diff` against the pre-move commit) that 9 other files were genuinely untouched by the migration and still contain stale references: `prosoc-card-audit/SKILL.md` (13 matches), `prosoc-card-approve/SKILL.md` (11), `prosoc-card-review/SKILL.md` (2), `prosoc-card-review-all/SKILL.md` (2), `prosoc-card-audit-all/SKILL.md` (5), `prosoc-scenario-new/SKILL.md` (7) and its `references/schema_guide.md` (1), `_shared/principles.md` (2), and `_shared/pg_scenarios.md` (2) — verified fresh again while drafting this work item.

These are live, actively-used Claude Code skill instructions (not historical records or card content) — every one of these skills is enabled in the current session and gets invoked directly by name (`prosoc-card-audit`, `prosoc-card-approve`, etc.). A skill instruction pointing at a path that no longer exists (e.g. "List `prosoc/scenarios/`") will mislead whichever agent follows it next.

### Duplication search
- In-repo: No existing implementation found.
- Sibling repos: None identified.
- External libraries: None identified — this is a documentation path-reference fix, not a library capability.
- Recommendation: Proceed.

### Demand search
- Work items: None found.
- Proposals: None found.
- Backlog: No matching entries.
- Recommendation: No action beyond implementing this fix.

## Scope

- Update the 9 files listed above to reference the new `src/prosoc/...` paths.
- Do not touch any other file category (card content, historical execution records, other already-correct docs).

## Required Changes

1. `.claude/skills/prosoc-card-audit/SKILL.md` — update all 13 stale `prosoc/<family>/...`/`prosoc.<family>` references to their `src/prosoc/{prnc,nca}/<family>/...` equivalents.
2. `.claude/skills/prosoc-card-approve/SKILL.md` — update all 11 stale references.
3. `.claude/skills/prosoc-card-review/SKILL.md` — update both stale references.
4. `.claude/skills/prosoc-card-review-all/SKILL.md` — update both stale references.
5. `.claude/skills/prosoc-card-audit-all/SKILL.md` — update all 5 stale references.
6. `.claude/skills/prosoc-scenario-new/SKILL.md` — update all 7 stale references.
7. `.claude/skills/prosoc-scenario-new/references/schema_guide.md` — update the 1 stale reference.
8. `.claude/skills/_shared/principles.md` — update both stale references.
9. `.claude/skills/_shared/pg_scenarios.md` — update both stale references.

Use the same family→path mapping already applied to `_shared/audit_checklists/*.md` in PR #95: `charter`/`scenarios`/`tasks`/`contexts` move under `src/prosoc/prnc/`; `constitutions`/`manifests` stay top-level under `src/prosoc/`; `literate`/`auditor`/`packet`/`utils` (including `utils/cards`) move under `src/prosoc/nca/`.

## Non-Goals

- Does not touch card content (`scenario.md`, `task.md`, `context.md`, `constitution.md`, `charter.md`, `manifest.md`, `audit.md`) — these are normative documents outside this work item's remit.
- Does not touch historical records under `project/executions/`, `project/work_items/resolved/`, or `project/design/proposals/adopted/` — these are point-in-time records of what was true when authored, not living documentation.
- Does not touch the root `README.md` or `docs/paper-supplements.md` — both were already refreshed as part of `WI-NCA-PRNC-PACKAGE-LAYOUT`.
- Does not change any skill's actual behavior or logic — path-reference text only.

## Acceptance Criteria

- Each of the 9 listed files has zero remaining `prosoc/<family>/...` or `prosoc.<family>` stale references.
- `grep -rEn '\bprosoc/(charter|scenarios|tasks|contexts|constitutions|manifests|packet|literate|auditor|utils)\b' .claude/skills/ | grep -v 'src/prosoc/'` returns no matches outside card-content directories or historical records (there should be none, since skill docs don't embed card content). The `grep -v 'src/prosoc/'` filter is required because `constitutions` and `manifests` stay top-level under `src/prosoc/` — without it, the bare word-boundary match also fires on the already-correct `src/prosoc/constitutions/...`/`src/prosoc/manifests/...` paths (e.g. in `.claude/skills/_shared/audit_checklists/constitutions.md`/`manifests.md`, already migrated by `WI-NCA-PRNC-PACKAGE-LAYOUT`), producing false positives the check could never actually clear.
- `lrh validate` reports 0 errors.

## Validation

- `lrh validate`
- `grep -rEn 'prosoc\.(literate|auditor|packet|utils|charter|scenarios|tasks|contexts)\b' .claude/skills/` (expect no matches)
- `grep -rEn '\bprosoc/(charter|scenarios|tasks|contexts|constitutions|manifests|packet|literate|auditor|utils)\b' .claude/skills/ | grep -v 'src/prosoc/'` (expect no matches; the `-v` filter excludes already-correct `src/prosoc/constitutions/...`/`src/prosoc/manifests/...` references from the bare word-boundary match)

## Risk Notes

- Low risk: pure documentation path-reference updates, no code or behavior change. Main risk is missing an occurrence within one of the 9 files — validate with a final grep sweep across all of `.claude/skills/`, not just the 9 named files, in case the self-review subagent's enumeration missed something.

## Related Workstream and Designs

- Design: `project/design/proposals/adopted/nca-prnc-package-layout/00_proposal.md`
- Related, independently landed: `WI-NCA-PRNC-PACKAGE-LAYOUT` (PR #95) — the source of the layout change this work item's path references need to catch up with.
