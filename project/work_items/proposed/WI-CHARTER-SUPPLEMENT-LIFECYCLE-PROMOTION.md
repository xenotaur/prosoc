---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION
title: 'Re-promote the 9 refreshed charter-supplement cards to APPROVED and regenerate the PDF'
type: operation
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY
related_design:
  - 'project/design/proposals/adopted/normative-card-approval/00_proposal.md'
depends_on:
  - WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION
  - WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, fabricate_human_approval, skip_confirmation_gate, hand_edit_rendered_tex_or_pdf]
acceptance:
  - 'Each of the 9 cards is promoted EDITED -> AUDITED only after its fresh audit.md (from WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH) has an acceptable verdict'
  - 'Each of the 9 cards is promoted AUDITED -> APPROVED only via an explicit, live human confirmation -- no approval is inferred or batch-applied without that confirmation'
  - 'papers/01_charter is rebuilt solely via its supported render pipeline (no hand-edited rendered.tex or PDF) and visually spot-checked'
  - 'The rebuilt PDF''s extracted text shows STATE/AUDITED/APPROVED dates consistent with this work item''s run, with no card showing APPROVED dated before its most recent AUDITED'
  - 'No new clipping, malformed characters, spacing regressions, or pagination defects appear versus the pre-demotion PDF'
required_evidence: [manual_review, lrh_validate, test_output, validation_output]
artifacts_expected:
  - papers/01_charter/golden/rendered.tex
  - papers/01_charter/rendered.pdf
---

## Summary

Promote the 9 cards refreshed by `WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH`
back through `EDITED -> AUDITED -> APPROVED`, one human-confirmed step at
a time, then regenerate and re-verify the charter-supplement PDF.

## Problem / Context

`prosoc-card-review` (`.claude/skills/prosoc-card-review/SKILL.md:102-104`)
stops immediately on a card that is already `APPROVED` -- "there is
nothing to review toward promotion" -- which is exactly why the demotion
in `WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION` has to happen before
any promotion tooling can run at all. `prosoc-card-approve`
(`.claude/skills/prosoc-card-approve/SKILL.md:27-39`) promotes exactly
one lifecycle step per invocation and requires its own explicit human
confirmation for the `AUDITED -> APPROVED` step specifically, since that
step "is a human accountability attestation... not a second content
review." This work item is therefore two full passes over all 9 cards,
each card individually gated, not a single batch action.

### Duplication search
- In-repo: `prosoc-card-review` already implements this promotion flow
  exactly; no duplicate needed.
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed.

### Demand search
- Work items: None found.
- Proposals: None found.
- Backlog: No matching entries.
- Recommendation: No action.

## Scope

Run `/prosoc-card-review` against each of the 9 cards, twice each
(`EDITED -> AUDITED`, then `AUDITED -> APPROVED`), with the human
confirming every single promotion. After all 9 are back to `APPROVED`,
regenerate the charter-supplement PDF and re-verify it.

## Required Changes

1. For each of the 9 cards, run `/prosoc-card-review` to promote
   `EDITED -> AUDITED` using the fresh audit evidence; this transition
   needs no further human judgment beyond accepting the audit passed.
2. For each of the 9 cards, run `/prosoc-card-review` again to promote
   `AUDITED -> APPROVED`; this step requires the human's live,
   per-card confirmation -- never inferred, never batch-applied.
3. Once all 9 cards are `APPROVED`, regenerate all affected distilled
   YAML and `papers/01_charter/golden/rendered.tex` via `render.py`, then
   a real `--pdf` build.
4. Run `scripts/validate/status`, the full test suite, and `lrh validate`
   against the fully-promoted state.
5. Visually spot-check the rebuilt PDF (render affected pages to PNG via
   `pdftoppm`, as prior work items in this corpus have done) for
   clipping, spacing, or pagination regressions.
6. Extract the PDF text (`pdftotext -layout`) and confirm each of the 9
   cards' STATE/AUDITED/APPROVED history reads consistently -- no
   APPROVED bullet predating the AUDITED bullet it's supposed to follow.

## Non-Goals

- Does not fabricate, infer, or batch-apply human approval for any card
  -- each `AUDITED -> APPROVED` step is its own live confirmation.
- Does not revisit the publication-view/provenance-retention decision --
  already resolved (`docs/paper-supplements.md:372-373`).
- Does not pursue tagged-PDF/accessibility support -- already an
  explicit non-goal of the prior workstream.
- Does not hand-edit `rendered.tex` or the PDF as a substitute for
  re-running the render pipeline.

## Acceptance Criteria

(see frontmatter `acceptance`)

## Validation

- `scripts/validate/status`
- `lrh validate`
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
- `PYTHONPATH="$(pwd)/src" papers/01_charter/render.py --pdf`
- `pdftotext -layout papers/01_charter/rendered.pdf -`

## Risk Notes

- This is 18 individual human-confirmed gates (9 cards x 2 transitions)
  -- expect this to span more than one session; do not try to compress
  it into a single unattended batch.
- If `WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH` surfaced a blocking
  finding on any card (most likely `high_urgency`, given its substantive
  P9 reclassification), that card may need a further content fix and a
  second audit pass before its `EDITED -> AUDITED` step can proceed --
  do not force the promotion through a blocking verdict.

## Dependencies / Order

Must run strictly after both `WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION`
(cards must be `EDITED`, not `APPROVED`, before `prosoc-card-review` will
engage) and `WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH` (each card's
`AUDITED` promotion needs current audit evidence, not the pre-November
audits being replaced).
