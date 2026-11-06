---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD
title: 'Add a git-history audit-currency check to scripts/validate/status'
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY
related_design:
  - 'project/design/proposals/adopted/normative-card-approval/00_proposal.md'
depends_on: []
blocked_by: []
expected_actions: [create_file, edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, redesign_audit_evidence_format, run_prosoc_card_review]
acceptance:
  - 'scripts/validate/status fails (not just warns) for an AUDITED/APPROVED card whose Markdown or distilled YAML was committed after its audit.md'
  - 'The check compares git commit timestamps (or an equivalent durable signal), not the optional human-authored AUDITED: provenance bullet'
  - 'A card whose only post-audit commit is a backfill of pre-existing audit-evidence content (matching this workstream''s routine_delivery/guidance_docent/public_navigation precedent) does not false-positive'
  - 'New test coverage exercises both the stale-flagged and the backfill-not-flagged cases'
  - 'All 9 cards promoted by WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION pass the new check once landed'
required_evidence: [manual_review, lrh_validate, test_output]
artifacts_expected:
  - src/prosoc/nca/utils/cards/status.py
  - tests/nca/utils/cards/status_test.py
---

## Summary

Extend `check_audit_evidence`
(`src/prosoc/nca/utils/cards/status.py:201-237`) or add a sibling check
so `scripts/validate/status` automatically flags an `AUDITED`/`APPROVED`
card whose source is newer than its audit evidence, closing the gap that
let 9 cards drift silently in this workstream.

## Problem / Context

`check_audit_evidence` currently only checks that an `audit.md` exists
next to an `AUDITED`/`APPROVED` card with an acceptable verdict
(`ready`/`ready_with_fixes`); it never compares commit timestamps between
the card and its audit, so it could not have caught any of the 9 cards
this workstream repairs. `PROP-NORMATIVE-CARD-APPROVAL` Decision 5
(`project/design/proposals/adopted/normative-card-approval/00_proposal.md:213`)
names this exact failure mode -- "State-staleness/auto-regression on
later content edits... is an acknowledged gap, deferred as an Open
Question, not solved here" -- and the originating review for this
workstream explicitly asked that a regression guard be proposed as its
own work item rather than bundled into the repair itself.

A naive "last commit touching the card is newer than the last commit
touching `audit.md`" check is insufficient on its own: this session's own
investigation found 3 cards (`routine_delivery`, `guidance_docent`,
`public_navigation`) that fail that naive test but are not actually
stale -- their only post-audit commit (PR #128) backfilled a previously
blank `AUDITED:` provenance bullet with a date **copied from their own
pre-existing `audit.md`**, not a new edit. Any implementation must
distinguish a true content edit from this kind of metadata backfill, or
it will false-positive on cards that are genuinely current.

### Duplication search
- In-repo: No existing staleness check. Related: `check_audit_evidence`
  (same file) is the natural extension point rather than a new module.
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed -- extend the existing function/module rather
  than create a parallel one.

### Demand search
- Work items: None found requesting this specifically (the broader gap
  is named in the adopted proposal above, but no work item exists for
  it).
- Proposals: `PROP-NORMATIVE-CARD-APPROVAL` Decision 5 defers exactly
  this as an Open Question -- this work item is its resolution, worth
  linking back to that proposal rather than treating as unrelated new
  scope.
- Backlog: No matching entries.
- Recommendation: No action beyond the cross-link above.

## Scope

Design and implement a git-history-based (or equivalent durable-signal)
staleness check in `scripts/validate/status`'s Python implementation,
distinguishing a true post-audit content edit from a metadata-only
backfill, with test coverage for both cases.

## Required Changes

1. Investigate how to reliably distinguish "content changed after audit"
   from "a backfill commit added provenance text matching the audit's
   own pre-existing date" -- a pure git-commit-timestamp comparison is
   not sufficient on its own (see Problem/Context); consider comparing
   against content hashes recorded at audit time, or restricting the
   check to specific sections/fields, and document the chosen approach's
   tradeoffs before implementing.
2. Implement the check in `src/prosoc/nca/utils/cards/status.py`,
   following `check_audit_evidence`'s existing pattern (directory vs.
   flat layout handling, `ConsistencyResult` return type).
3. Wire the new check into `scripts/validate/status`'s existing
   validation pass.
4. Add test coverage in `tests/nca/utils/cards/status_test.py` (or the
   project's equivalent test module) for: a genuinely stale card, a
   current card, and a backfill-only card that must not false-positive.
5. Run the new check against the full corpus (post-
   `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`) and confirm it passes
   cleanly.

## Non-Goals

- Does not redesign the `audit.md` evidence format (e.g. to a
  content-hash scheme) as part of this item unless that turns out to be
  the only reliable implementation -- if so, surface that as a decision
  to confirm before building it, not something to implement silently.
- Does not re-run `/prosoc-card-review` or change any card's lifecycle
  state -- validator code only.
- Does not retroactively re-check history prior to this workstream's own
  cards -- scoped to catching future drift.

## Acceptance Criteria

(see frontmatter `acceptance`)

## Validation

- `scripts/validate/status`
- `lrh validate`
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
- `scripts/lint`

## Risk Notes

- The backfill-vs-stale distinction is the hard part of this item and
  the most likely source of either false positives (blocking legitimate
  provenance backfills) or false negatives (missing real drift) --
  budget investigation time before committing to an implementation
  approach, and confirm the approach with the user before writing it if
  it requires anything beyond a straightforward timestamp comparison.
