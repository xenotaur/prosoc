---
resolution: 'Implemented and merged in PR #136 (commit 4c7ab6c486dec48747b4d6fe69920278277f49a5) -- promoted all 9 refreshed cards through 18 individually human-confirmed EDITED -> AUDITED -> APPROVED transitions, none batched. Fixed a real Normative Statement/description drift in the charter (P1, P2, P4, P5, P6) and should-fix findings on 5 other cards along the way, rather than carrying them forward; two of those (navigate_lead_agent, high_urgency) had sat open in project/design/backlog.md since 2026-08-02 and were resolved and removed from that table. Discovered and fixed a pre-existing history-bullet ordering bug in 5 cards, caught by this work item''s own PDF-text history-ordering acceptance check. Regenerated papers/01_charter/golden/rendered.tex and src/prosoc/manifests/sample_packet/packet.golden.yml via their supported pipelines. All 344 tests pass (0 failures) -- the 6 packet-related failures WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION left as a disclosed consequence are now gone.'
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION
title: 'Re-promote the 9 refreshed charter-supplement cards to APPROVED and regenerate the PDF'
type: operation
status: resolved
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
  - 'Each promotion (18 total) adds its own dated AUDITED:/APPROVED: history bullet by hand -- prosoc-card-approve never writes one itself -- preserving every existing bullet verbatim'
  - 'After each of the charter''s 2 promotions, its separate free-text Status: header is hand-synced to match -- prosoc-card-approve/--fix never touches that header'
  - 'papers/01_charter is rebuilt solely via its supported render pipeline (no hand-edited rendered.tex or PDF) and visually spot-checked'
  - 'For the 7 cards in papers/01_charter/sources.txt, the rebuilt PDF''s extracted text shows STATE/AUDITED/APPROVED dates consistent with this work item''s run, with no card showing APPROVED dated before its most recent AUDITED; for navigate_follow_agent and navigate_lead_agent (not in sources.txt), the same check is made directly against their task.md files instead of the PDF'
  - 'No new clipping, malformed characters, spacing regressions, or pagination defects appear versus the pre-demotion PDF'
required_evidence: [manual_review, lrh_validate, test_output, validation_output]
artifacts_expected:
  - papers/01_charter/golden/rendered.tex
  - build/papers/01_charter/rendered.pdf
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

**Two confirmed gaps in `prosoc-card-approve`'s own documented Step 5**
(`.claude/skills/prosoc-card-approve/SKILL.md`, read in full during
review): it edits only the fenced `state:` field plus its two
projections (distilled YAML, Markdown `STATE` line) -- it never writes a
dated `**AUDITED:**`/`**APPROVED:**` history bullet, unlike the
convention every existing promoted card in this corpus already follows
(e.g. the charter's own `**APPROVED:** Claude, 2026-08-19 (PR #97) --
re-audited and promoted...` bullets). And for the charter specifically,
nothing in its Step 5 touches the separate free-text `**Status:**`
header -- confirmed independently against `validate_status.py`'s own
comment that `--fix` "never addresses" that header. Both are explicit
hand-edit steps in this work item below, not assumptions about what the
skill does automatically.

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
   Immediately after each promotion, hand-add a dated `**AUDITED:**`
   history bullet (auditor + date, matching this card family's existing
   convention) -- `prosoc-card-approve` does not add one itself. For the
   charter specifically, also hand-sync its separate `**Status:**`
   header to `Audited (Normative)` and re-run
   `scripts/validate/status --family charter` (no `--fix`) to confirm.
2. For each of the 9 cards, run `/prosoc-card-review` again to promote
   `AUDITED -> APPROVED`; this step requires the human's live,
   per-card confirmation -- never inferred, never batch-applied.
   Immediately after each promotion, hand-add a dated `**APPROVED:**`
   history bullet, same convention. For the charter specifically, again
   hand-sync its `**Status:**` header, this time to `Approved
   (Normative)`, and re-run `scripts/validate/status --family charter`
   (no `--fix`) to confirm.
3. Once all 9 cards are `APPROVED`, regenerate all affected distilled
   YAML and `papers/01_charter/golden/rendered.tex` via `render.py`, then
   a real `--pdf` build (output lands at
   `build/papers/01_charter/rendered.pdf` -- `render.py`'s own
   `BUILD_DIR`, not `papers/01_charter/`).
4. Run `scripts/validate/status`, the full test suite, and `lrh validate`
   against the fully-promoted state -- confirm the 6 packet-related test
   failures `WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION` introduced
   (verified during its implementation; its own Required Changes step 6
   names all 6) are gone now that `charter`/`navigate_lead_agent`/`high_urgency`
   are `APPROVED` again, and `scripts/assemble
   src/prosoc/manifests/sample_packet/manifest.yml --check` passes with
   no golden drift (no regeneration should be needed, since member
   content never changed, only its lifecycle state round-tripped).
5. Visually spot-check the rebuilt PDF (render affected pages to PNG via
   `pdftoppm`, as prior work items in this corpus have done) for
   clipping, spacing, or pagination regressions.
6. Extract the PDF text (`pdftotext -layout build/papers/01_charter/rendered.pdf -`)
   and confirm, **for the 7 of the 9 cards actually in
   `papers/01_charter/sources.txt`** (`charter`, `frontal_approach`,
   `single_file_hallway`, `movable_obstruction`, `navigate_point_to_point`,
   `deliver_object`, `high_urgency`), that STATE/AUDITED/APPROVED history
   reads consistently -- no `APPROVED` bullet predating the `AUDITED`
   bullet it's supposed to follow. `navigate_follow_agent` and
   `navigate_lead_agent` are not in `sources.txt` and cannot be checked
   through this PDF at all -- verify those two directly against their
   own `task.md` files instead.

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
- `pdftotext -layout build/papers/01_charter/rendered.pdf -`
- `scripts/assemble src/prosoc/manifests/sample_packet/manifest.yml --check`

## Risk Notes

- This is 18 individual human-confirmed gates (9 cards x 2 transitions)
  -- expect this to span more than one session; do not try to compress
  it into a single unattended batch.
- The hand-added history bullet and (for the charter) the header sync
  are easy to forget across 18 gates since `prosoc-card-approve` does
  neither automatically -- re-run `scripts/validate/status` after each
  charter promotion specifically to catch a missed header sync before
  moving to the next card, rather than discovering it only at the end.
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
