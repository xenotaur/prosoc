---
resolution: "Implemented and merged in PR #65 (commit 0049f6c). Promoted the 5 sample_packet pilot cards to APPROVED and regenerated the golden packet in production mode -- the corpus's first packet produced without the dev-mode escape hatch."
blocked_reason: null
blocked: false
id: WI-CARD-APPROVAL-PILOT
title: Promote the 5 sample_packet pilot cards to APPROVED and produce the corpus's first APPROVED-mode golden packet
type: operation
status: resolved
assigned_agents: []
related_focus:
  - FOCUS-NORMATIVE-PACKET-ASSEMBLY
related_roadmap: []
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/proposed/normative-card-approval/00_proposal.md
depends_on:
  - WI-CARD-APPROVE-SKILLS
blocked_by: []
expected_actions:
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - edit_card_normative_content
  - promote_non_pilot_cards
  - modify_packet_gate_logic
  - modify_packet_envelope_shape
  - remove_allow_unapproved_flag
acceptance:
  - "All 5 pilot cards (charter, asimov_three_laws, intersection_gesture_wait, navigate_lead_agent, high_urgency) reach state: APPROVED in both their fenced YAML and projected Markdown Status/STATUS block"
  - "prosoc/manifests/sample_packet/packet.golden.yml is regenerated via scripts/assemble without --allow-unapproved and contains no escape-hatch notice"
  - ".github/workflows/packet.yml's packet-drift check and tests/packet/cli_test.py's golden-file checks are updated to validate the regenerated production-mode golden file"
  - "lrh validate reports 0 errors after all card and golden-file changes"
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/charter/charter.md
  - prosoc/constitutions/asimov_three_laws/constitution.md
  - prosoc/scenarios/intersection_gesture_wait/scenario.md
  - prosoc/tasks/navigate_lead_agent/task.md
  - prosoc/contexts/high_urgency/context.md
  - prosoc/manifests/sample_packet/packet.golden.yml
  - .github/workflows/packet.yml
  - tests/packet/cli_test.py
---

# WI-CARD-APPROVAL-PILOT

## Summary

Using the `prosoc-card-review` / `prosoc-card-review-all` tooling built in
`WI-CARD-APPROVE-SKILLS`, promote the 5 `sample_packet` manifest cards
(charter, `asimov_three_laws`, `intersection_gesture_wait`,
`navigate_lead_agent`, `high_urgency`) from their current states through
`AUDITED` to `APPROVED`, then regenerate `sample_packet`'s golden packet
without `--allow-unapproved` — the corpus's first production-mode packet.

## Problem / Context

No card in the 32-card prosoc normative corpus has ever been promoted to
`AUDITED` or `APPROVED`. Per `PROP-NORMATIVE-CARD-APPROVAL` Decision 1,
prove the mechanism on a small, already-audited subset before committing to
the full corpus. Current state, re-verified against the live corpus:
charter, `intersection_gesture_wait`, `navigate_lead_agent`, and
`high_urgency` are `DRAFTED`; `asimov_three_laws` is `EDITED`. All 5 already
have `audit.md` with a passing verdict (charter: `ready_with_fixes`;
`asimov_three_laws`: `ready`; `intersection_gesture_wait`: `ready`;
`navigate_lead_agent`: `ready_with_fixes`; `high_urgency`:
`ready_with_fixes`) — none need a fresh audit, and none are blocked by the
`→AUDITED` evidence gate.

### Duplication search
- In-repo: no existing pilot-promotion or golden-packet-regeneration work
  found — `grep` for `sample_packet.*pilot`, `golden.*packet.*approved`
  across `project/work_items/`, `project/design/proposals/`,
  `.claude/skills/`, `prosoc/` returns only the sibling
  `WI-CARD-APPROVE-SKILLS` (the tooling this item depends on) and the
  governing proposal — not duplicates.
- Sibling repos: None identified.
- External libraries: Not applicable.
- Recommendation: Proceed.

### Demand search
- Work items: None found requesting this specific promotion run.
- Proposals: `PROP-NORMATIVE-CARD-APPROVAL` Decision 1 — this item
  implements the pilot; not a duplicate.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

- Promote exactly the 5 named pilot cards through `AUDITED` to `APPROVED`.
- Regenerate `sample_packet`'s golden packet in production mode.
- Update the packet-drift workflow and packet CLI golden-file tests to match
  the new production-mode golden packet.
- Does not touch any of the other 27 corpus cards.

## Required Changes

1. Run `prosoc-card-review-all` (or `prosoc-card-review` per card) against
   the 5 pilot cards. Each promotion is human-attested per
   `PROP-NORMATIVE-CARD-APPROVAL` Decision 2 — the repo owner is the
   approver for every card.
2. For each card: `→AUDITED` (gated on the existing `audit.md` verdict,
   already `ready`/`ready_with_fixes` for all 5), then `→APPROVED` (human
   confirmation, no additional evidence).
3. Regenerate `prosoc/manifests/sample_packet/packet.golden.yml` via
   `scripts/assemble` **without** `--allow-unapproved` — this must be the
   first golden packet in the repo produced under the production
   (`APPROVED`-floor) gate rather than the dev-mode escape hatch.
4. Update the packet-drift workflow
   (`.github/workflows/packet.yml`, from the resolved
   `WI-PACKET-CI-DRIFT-CHECK`) and the packet CLI golden-file tests
   (`tests/packet/cli_test.py`) so they assemble/check `sample_packet`
   in production mode rather than via the dev-mode `--allow-unapproved`
   escape hatch.
5. Re-run the packet-drift workflow logic and packet CLI tests against the
   regenerated golden file and confirm they pass.

## Non-Goals

- Does not promote any of the other 27 corpus cards — deferred, offered
  separately per the proposal's Implementation Plan.
- Does not audit the 4 coverage-gap cards (`asimov_four_laws`,
  `guidance_docent`, `public_navigation`, `routine_delivery`) — none are in
  the pilot.
- Does not change the assembler's gate logic, envelope shape, or
  `--allow-unapproved` semantics — the escape hatch stays permanent per
  the parent proposal (`PROP-NORMATIVE-PACKET-ASSEMBLY` Decision 5).
- Does not resolve the 3 pilot cards' `should_fix` audit findings
  (charter, `navigate_lead_agent`, `high_urgency` all have
  `ready_with_fixes` verdicts) — the evidence gate accepts
  `ready_with_fixes` as-is; fixing those findings is separate editorial
  work, not a precondition of this WI.

## Acceptance Criteria

- All 5 pilot cards reach `state: APPROVED` in both their fenced YAML and
  projected Markdown Status/STATUS block (heading case varies by family —
  e.g. charter uses `## Status`, tasks/contexts use `## STATUS`; either is
  a valid block per the validator).
- `sample_packet`'s golden packet is regenerated without
  `--allow-unapproved` and carries no escape-hatch notice.
- The packet-drift workflow and packet CLI golden-file tests are updated to
  validate the regenerated production-mode golden file, and both pass.
- `lrh validate` reports 0 errors after all changes.

## Validation

- `scripts/version tools`
- `lrh validate`
- `scripts/validate/status --family charter`
- `scripts/validate/status --family constitutions --card asimov_three_laws`
- `scripts/validate/status --family scenarios --card intersection_gesture_wait`
- `scripts/validate/status --family tasks --card navigate_lead_agent`
- `scripts/validate/status --family contexts --card high_urgency`
- `scripts/assemble prosoc/manifests/sample_packet/manifest.yml --check`
- `python -m unittest tests.packet.cli_test`

## Risk Notes

- This item's `depends_on: [WI-CARD-APPROVE-SKILLS]` names a real
  prerequisite: the promotion tooling it uses. (`blocked`/`blocked_reason`
  stay `false`/`null` per the work-item schema, which reserves those fields
  for `status: active` items — `depends_on` is the correct field for a
  `proposed` item's prerequisites.) `WI-CARD-APPROVE-SKILLS`'s creation PR
  has since merged (#62), so this dependency is satisfied at the planning
  level; implementing that tooling is still a separate, not-yet-started
  step this item's own execution depends on. Do not attempt manual
  frontmatter edits as a workaround if the tooling isn't ready when this
  item is picked up — per the governing proposal's Decision 2, unmediated
  manual edits are exactly the error-prone pattern the tooling was built to
  avoid.
- 3 of 5 pilot cards carry unresolved `should_fix` audit findings; approving
  them as-is is a deliberate, in-scope choice per the evidence gate, but the
  human approver should read each `audit.md` before confirming, not just
  the verdict line.
- Regenerating the golden packet in production mode is a one-way proof —
  if the fail-closed gate rejects any card unexpectedly, that is a signal
  to investigate the gate logic (out of scope to fix here) before
  re-attempting, not to reach for `--allow-unapproved` as a workaround.
- Today both `.github/workflows/packet.yml` and
  `tests/packet/cli_test.py` still assume a dev-mode golden assembled with
  `--allow-unapproved`; this WI must update those checks in the same change
  as the regenerated golden file or they will fail/flake on the old
  expectation.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
- Design: `project/design/proposals/proposed/normative-card-approval/00_proposal.md`
  (Decision 1, Implementation Plan)
