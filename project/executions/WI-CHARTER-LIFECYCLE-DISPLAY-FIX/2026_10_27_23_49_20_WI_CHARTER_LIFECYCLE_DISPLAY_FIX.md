---
execution_id: 2026_10_27_23_49_20_WI_CHARTER_LIFECYCLE_DISPLAY_FIX
prompt_id: PROMPT(WI-CHARTER-LIFECYCLE-DISPLAY-FIX:WI_CHARTER_LIFECYCLE_DISPLAY_FIX)[2026-10-27T23:37:54+00:00]
work_item: WI-CHARTER-LIFECYCLE-DISPLAY-FIX
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/113
commit: 84bc040f12e6832c139c9e745d9abfc4091879b5
created_at: 2026-10-27T23:49:20+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-LIFECYCLE-DISPLAY-FIX.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implement `WI-CHARTER-LIFECYCLE-DISPLAY-FIX`: fix the charter's stale
`Status:` header and add the missing closing re-approval history
bullets — display/provenance-bookkeeping only, no `state:` change.

# Result

Changed `charter.md:4`'s `**Status:**` line from "Draft (Normative)" to
"Approved (Normative)", matching the authoritative `STATE: APPROVED`
bullet and embedded YAML. Added two closing history bullets (2026-08-07,
PR #79; 2026-08-19, PR #97) documenting the re-audit/re-approval that
closed out each "reverted from APPROVED pending re-audit" entry.

A pre-push diff-mode self-review independently verified both new
bullets' factual claims against real repo evidence (PR #79's
squash-merge commit title "Promote charter EDITED -> AUDITED ->
APPROVED", and PR #97's own execution record plus `audit.md` dated
2026-08-19) rather than trusting the WI's own assertions — both held
up. One nuance it surfaced and I independently re-verified: the PR #97
bullet cites 2026-08-19 (when the re-audit/approval activity actually
happened, per `audit.md` and the execution record's `created_at`), not
2026-08-20 (when that PR actually merged to GitHub, delayed by an
unrelated merge-conflict fix) — a deliberate, evidenced choice of the
more meaningful date, not an inconsistency.

`charter.yml`'s `state:` field and the embedded fenced YAML inside
`charter.md` are untouched; no principle's content was changed. Opened
PR #113.

# Validation

- `lrh validate`: 0 errors, 20 pre-existing unrelated warnings.
- `scripts/validate/status --family charter --card charter`: consistent.
- `scripts/test`: 259 tests, OK.
- `scripts/lint`: all checks passed.

# Follow-up

None outstanding for this item.
