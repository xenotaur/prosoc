---
execution_id: 2026_08_13_03_47_46_CHARTER_FRONTIERS_SYNC
prompt_id: PROMPT(AD_HOC:CHARTER_FRONTIERS_SYNC)[2026-08-13T03:39:45+00:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/92
commit: f9241ac8d014ac6b33f8c7992e435477363ecedb
created_at: 2026-08-13T03:47:46+00:00
agent: claude_app
instruction_source: project/design/proposals/proposed/charter-frontiers-sync/00_proposal.md
session_transcript: claude-app:6b2ba6cf-e741-4636-96d3-430b7f169c45
---

# Summary

Compared `prosoc/charter/charter.md` (APPROVED) against the submitted,
frozen Frontiers paper "The Prosocial Robot Navigation Charter" (Francis)
principle-by-principle (Section 2 definition plus P0–P9), and captured the
reconciliation decisions as design proposal `PROP-CHARTER-FRONTIERS-SYNC`.

# Result

Wrote `project/design/proposals/proposed/charter-frontiers-sync/00_proposal.md`
with a `## Design Decisions` entry per principle. Resolved: Section 2
definition and P0 (no change, already in sync), P1 (broaden Safety scope
to match paper), P5 (restore "where feasible" hedge), the MUST/SHOULD
modal-verb convention (MUST for P1 only, SHOULD elsewhere, matching the
paper), P6 (keep charter's "accommodate" wording, change modal only), P8
(inline the six-context taxonomy into the normative statement), and P9
(trim the task/context/goals qualifier from the normative statement,
per the paper's post-P0 narrowing, while keeping it in the Section 2
definition). Left as Open Questions, deferred to a follow-up
per-principle walkthrough: P2/P3/P4 wording synchronization, P7's scope,
and the exact severity→modal rule (plus whether any `severity` values
themselves need to change).

# Validation

- `lrh validate` — 0 errors, 0 warnings.
- Prior-art check (duplication + demand search) run per
  `references/prior-art-check.md` — no existing proposal, workstream, or
  work item covers this topic; recommendation was Proceed / No action.
- Slug-based idempotence check (`lrh prompt check-execution --slug
  charter-frontiers-sync --work-item AD_HOC`) found no prior record before
  minting the prompt ID.

# Follow-up

- Walk through P2/P3/P4 wording and P7's scope with the user, and settle
  the severity→modal audit, updating this proposal's Design Decisions
  section with the outcomes.
- Once all decisions are finalized, create a work item via
  `/lrh-work-item` to implement the resulting charter edits (this
  proposal explicitly does not edit `charter.md` itself).
- `session_transcript` above uses the live host session ID; update if a
  more durable pointer becomes available.
