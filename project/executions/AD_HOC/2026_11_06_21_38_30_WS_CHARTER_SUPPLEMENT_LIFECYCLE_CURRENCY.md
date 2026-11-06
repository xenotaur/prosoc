---
execution_id: 2026_11_06_21_38_30_WS_CHARTER_SUPPLEMENT_LIFECYCLE_CURRENCY
prompt_id: PROMPT(AD_HOC:WS_CHARTER_SUPPLEMENT_LIFECYCLE_CURRENCY)[2026-11-06T20:48:45+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/133
commit:
created_at: 2026-11-06T21:38:30+00:00
agent: claude_app
instruction_source: project/workstreams/proposed/WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Files `WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY`, a new workstream to
repair the 9 normative cards whose embedded `state: APPROVED` postdates
their last real `audit.md`.

# Result

Created `project/workstreams/proposed/WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY.md`
with `status: proposed`, `stage: planned`, and its 4 constituent work
items listed in `work_items:`. Grounded the 9-card finding in a
corpus-wide git-history sweep (32 cards across all 6 families) that
independently confirmed the 7 cards an external paper-review pass
flagged, surfaced 2 more (`navigate_follow_agent`, `navigate_lead_agent`)
that review had no visibility into, and confirmed 3 cards the naive
date-check also flags (`routine_delivery`, `guidance_docent`,
`public_navigation`) are not actually stale -- their only post-audit
touch was a metadata backfill matching their own audit's pre-existing
date, not a new content edit. Linked the workstream to
`PROP-NORMATIVE-CARD-APPROVAL` Decision 5
(`project/design/proposals/adopted/normative-card-approval/00_proposal.md:213`),
which named this exact failure mode as an acknowledged, unsolved Open
Question.

# Validation

- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- Prior-art duplication and demand search run per
  `references/prior-art-check.md`: no duplicate implementation or
  existing request found; recorded in the workstream's own `## Prior Art
  Check` section.

# Follow-up

The 4 work items this workstream lists are being filed in the same PR
(see their own execution records); the heaviest remaining step is
`WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`'s 18 individual
human-confirmed promotion gates, which this record does not cover.
