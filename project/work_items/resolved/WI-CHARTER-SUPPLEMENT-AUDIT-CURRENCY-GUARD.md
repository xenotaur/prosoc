---
resolution: 'Implemented and merged in PR #137 (commit 70c51fba846ca319731bcde2d48f461018814564) -- added a mask-and-compare audit-currency check to scripts/validate/status, confirmed with the user before implementing per the work item''s own risk notes. Validated the design against two real historical cases before writing code (PR #128''s provenance backfill, this workstream''s own promotion diff). Running it against the full corpus surfaced and fixed 2 genuinely stale pre-existing cards outside this workstream''s original 9 (routine_delivery, guidance_docent). A subsequent real Copilot review round found and all fixes verified 6 further issues, including a severe shallow-clone boundary bug that could have silently defeated the guard entirely; all reproduced against real data (including a real git clone --depth 1) before fixing. 26 new regression tests; full corpus scripts/validate/status passes clean (32/32 cards).'
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD
title: 'Add a git-history audit-currency check to scripts/validate/status'
type: deliverable
status: resolved
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY
related_design:
  - 'project/design/proposals/adopted/normative-card-approval/00_proposal.md'
depends_on: []
blocked_by: []
expected_actions: [create_file, edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, redesign_audit_evidence_format, run_prosoc_card_review]
acceptance:
  - 'scripts/validate/status fails (not just warns) for an AUDITED/APPROVED card whose Markdown or distilled YAML carries a post-audit change outside the lifecycle-tracking surface (state:, its Markdown projections, and STATUS-block history bullets)'
  - 'The check compares git commit timestamps (or an equivalent durable signal), not the optional human-authored AUDITED: provenance bullet'
  - 'A card whose only post-audit commit(s) touch only the lifecycle-tracking surface -- a provenance backfill (this workstream''s routine_delivery/guidance_docent/public_navigation precedent) or a legitimate prosoc-card-approve promotion/approval commit -- does not false-positive'
  - 'New test coverage exercises all three cases: a genuinely stale card, a backfill-only card, and a card whose only post-audit commit is a lifecycle promotion'
  - 'All 9 cards promoted by WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION pass the new check once landed -- including immediately after each of their own 18 promotion commits, not just at the end'
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
touching `audit.md`" check is insufficient on its own, and confirmed in
review to fail in **two** distinct ways, not one:

1. This session's own investigation found 3 cards (`routine_delivery`,
   `guidance_docent`, `public_navigation`) that fail the naive test but
   are not actually stale -- their only post-audit commit (PR #128)
   backfilled a previously blank `AUDITED:` provenance bullet with a
   date **copied from their own pre-existing `audit.md`**, not a new
   edit.
2. **Confirmed in review of this very workstream's PR:** a naive rule
   also rejects *every* ordinary lifecycle promotion. A successful
   `prosoc-card-approve` run commits a change to the card's Markdown and
   distilled YAML strictly *after* the audit it is promoting from (that
   is the whole point of the transition) -- without content changing at
   all. `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`'s own 18 promotion
   commits would each immediately re-trip a naive version of this guard
   the moment they land, making the 9 repaired cards permanently
   unable to pass it.

Both failure modes share one root cause: the naive rule treats *any*
post-audit commit as evidence of staleness, when what actually
invalidates an audit is a change to **normative content** -- not a
change confined to the card's lifecycle-tracking surface (the `state:`
field, its Markdown `STATE`/`Status:` projections, and the STATUS-block's
own history bullets, including the one that very backfill or promotion
writes). Reframing the check around that distinction -- flag only when
something *outside* the lifecycle-tracking surface changed since the
audit -- naturally covers both the backfill case and the promotion case
with one rule, rather than special-casing each separately.

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
distinguishing a true post-audit normative-content change from a
post-audit change confined to the card's lifecycle-tracking surface
(covers both the backfill case and the ordinary-promotion case), with
test coverage for all cases.

## Required Changes

1. Investigate how to reliably distinguish "normative content changed
   after audit" from "only the lifecycle-tracking surface changed after
   audit" -- a pure git-commit-timestamp comparison is not sufficient on
   its own (see Problem/Context); consider diffing each post-audit
   commit's changed lines against a known pattern for the `state:`
   field, the Markdown `STATE`/`Status:` line(s), and `**AUDITED:**`/
   `**APPROVED:**`/`**EDITED:**` history bullets, or comparing content
   hashes recorded at audit time restricted to the non-lifecycle
   portions of the card. Document the chosen approach's tradeoffs before
   implementing, and confirm it with the user if it requires anything
   beyond that.
2. Implement the check in `src/prosoc/nca/utils/cards/status.py`,
   following `check_audit_evidence`'s existing pattern (directory vs.
   flat layout handling, `ConsistencyResult` return type).
3. Wire the new check into `scripts/validate/status`'s existing
   validation pass.
4. Add test coverage in `tests/nca/utils/cards/status_test.py` (or the
   project's equivalent test module) for: a genuinely stale card (real
   content change after audit), a current card, a backfill-only card
   that must not false-positive, and -- confirmed in review as a
   distinct, easily-missed case -- a card whose only post-audit commit
   is a legitimate `prosoc-card-approve` promotion (state + projections
   + one new history bullet, no content change), which must also not
   false-positive.
5. Run the new check against the full corpus (post-
   `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`) and confirm it passes
   cleanly, including immediately after each of that work item's own 18
   promotion commits -- not only once at the very end.

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

- The lifecycle-tracking-surface-vs-content distinction is the hard part
  of this item and the most likely source of either false positives
  (blocking legitimate provenance backfills *or* ordinary promotions) or
  false negatives (missing real drift) -- budget investigation time
  before committing to an implementation approach, and confirm the
  approach with the user before writing it if it requires anything
  beyond a straightforward timestamp comparison.
- Getting this wrong in the false-positive direction is not merely
  theoretical here: if this guard lands and is misimplemented as a bare
  timestamp check, it would immediately and permanently fail for all 9
  cards the moment `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION` promotes
  them, since every promotion commit postdates its audit by
  construction -- confirmed as a real review finding on this very
  workstream's own planning PR, not a hypothetical.
