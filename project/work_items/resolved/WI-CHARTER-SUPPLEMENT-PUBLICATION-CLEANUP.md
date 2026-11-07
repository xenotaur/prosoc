---
resolution: 'Implemented and merged in PR #138 (commit cc067a285a5fbb26b5f598b266018c982f40dce9). Fixed the page-one disclaimer (template.tex) and the "Principle 13" reference in charter.md''s history bullet, both verified masked-safe against the audit-currency guard. Investigated the context-history field-ordering question: an initial read of contexts/template.md suggested the order was intentional fixed-schema behavior, but checking high_urgency (the one other context card that went through the original repair, not just a drive-by fix) disproved that -- routine_delivery/guidance_docent were the actual outliers, fixed by moving MODIFIED to its chronologically-correct position. The publication-view-provenance question needed no change -- an adopted decision to retain full provenance already exists. A pre-push self-review caught and fixed 3 documentation-accuracy issues (wrong card count, missing artifacts_expected entry, uninformative instruction_source) in the new WI/execution-record files. A real Copilot review then caught that the recorded PDF visual-inspection coverage (a sample plus automated scans) did not satisfy this WI''s own "every page" acceptance criterion; completed a full individual inspection of all 48 pages in response, finding zero issues. All 32 cards remain APPROVED and consistent throughout.'
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-PUBLICATION-CLEANUP
title: 'Fix the page-one disclaimer, a "Principle 13" reference, and context-history ordering in the charter supplement'
type: deliverable
status: resolved
related_workstreams: []
related_design:
  - 'project/design/proposals/adopted/normative-card-approval/00_proposal.md'
depends_on: []
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, alter_normative_content, create_synthetic_approval_records, hand_edit_generated_latex, redesign_publication_view_policy]
acceptance:
  - 'papers/01_charter/template.tex''s page-one disclaimer no longer contradicts the included cards'' actual AUDITED/APPROVED state, while preserving the not-validated-for-deployment caveat and the existing URLs/attribution prose'
  - 'src/prosoc/prnc/charter/charter.md''s 2026-11-06 WI-CHARTER-SUPPLEMENT-DEFINITIONAL-CONSISTENCY history bullet no longer says "Principle 13" -- it unambiguously names P9 and Section 13'
  - 'scripts/validate/status reports the charter card consistent after the history-bullet correction, confirming the audit-currency guard treats it as masked lifecycle-tracking content and does not demand re-audit'
  - 'The context-history field-ordering question (routine_delivery, guidance_docent) is resolved by moving MODIFIED to its chronologically-correct position (after AUDITED), matching the convention already demonstrated by high_urgency -- a reorder verified safe against the audit-currency guard, not merely assumed safe'
  - 'The publication-view-provenance question is resolved by citing the existing adopted decision in docs/paper-supplements.md (WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER, confirmed 2026-11-06: retain), not by a new editorial policy change'
  - 'papers/01_charter is regenerated exclusively through papers/01_charter/render.py (no hand-edited golden .tex or PDF), with no golden-file drift'
  - 'All 9 included cards (per papers/01_charter/sources.txt) remain APPROVED with current audit evidence; full corpus scripts/validate/status passes'
  - 'Every rendered PDF page is visually inspected for clipping, overlap, broken URLs, orphaned headings, and pagination regressions'
required_evidence: [manual_review, lrh_validate, test_output]
artifacts_expected:
  - papers/01_charter/template.tex
  - papers/01_charter/golden/rendered.tex
  - src/prosoc/prnc/charter/charter.md
  - src/prosoc/prnc/contexts/routine_delivery/context.md
  - src/prosoc/prnc/contexts/guidance_docent/context.md
---

## Summary

A follow-up external review of the regenerated charter supplement (after
`WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY` closed) found two concrete
publication-text defects and two questions worth a documented decision. Fix
the two defects; resolve the two questions by investigation rather than by
unilateral policy change.

## Problem / Context

1. **Page-one disclaimer is now stale.** `papers/01_charter/template.tex:144-145`
   says the included cards are "not ... fully audited normative card content
   suitable for deployment." Every one of the 9 cards the supplement includes
   (per `papers/01_charter/sources.txt`)
   is `APPROVED` (the human-accountability gate per
   `src/prosoc/prnc/scenarios/workflow.md` stage 5) with current audit
   evidence; none is `VALIDATED` (the empirical-evidence stage, per the same
   doc's stage 6). The sentence is now internally contradictory and should
   instead distinguish `AUDITED`/`APPROVED` (achieved) from deployment
   validation (not achieved).
2. **"Principle 13" is ambiguous.** `src/prosoc/prnc/charter/charter.md`'s
   2026-11-06 `WI-CHARTER-SUPPLEMENT-DEFINITIONAL-CONSISTENCY` history bullet
   references "Principle 13's Explanation." The charter has no Principle 13 --
   `## 13. Principle P9 -- Prosocial Behavior` is the actual heading (confirmed
   by reading the file). The intended referent is P9's Explanation, located in
   Section 13.
3. **Context-history field ordering** (`routine_delivery`, `guidance_docent`):
   `MODIFIED` (2026-10-27) appears before `AUDITED` (2026-08-0x) even though
   it postdates it. Initial read of `contexts/template.md` (CREATED, MODIFIED,
   AUDITED as fixed header fields) suggested this was intentional, fixed-order
   schema, not a bug. Checking `high_urgency` -- the one other context card
   that went through this workstream's *original* repair, not just WI-4's
   drive-by fix -- disproved that: its `MODIFIED` bullet sits *after*
   `AUDITED`, in true chronological order, not in the template's default
   position. `routine_delivery`/`guidance_docent` are the actual outliers.
   Fixed by moving `MODIFIED` to its chronologically-correct position,
   verified safe against the audit-currency guard (see Risk Notes).
4. **Publication-view provenance:** already decided.
   `docs/paper-supplements.md`'s "Publication View and Internal Provenance"
   section documents an adopted decision
   (`WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER`, confirmed with the user
   2026-11-06) to retain full provenance deliberately. No action needed.

### Duplication search
- In-repo: No existing work item covers this; `WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES`
  and `WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER` are the closest prior art
  (both resolved, both narrowly scoped text/policy fixes) and this item follows
  the same pattern.
- Recommendation: Proceed.

### Demand search
- No open work item or proposal requests this; it originates from a follow-up
  external review session after `WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY`
  closed.
- Recommendation: No action beyond this item.

## Scope

- Reword `papers/01_charter/template.tex`'s page-one disclaimer.
- Correct `charter.md`'s "Principle 13" reference in place, to name P9 and
  Section 13 unambiguously -- a wording clarification of what the bullet
  already intended, not a change to what happened, so no new history bullet
  is added.
- Move `MODIFIED` to its chronologically-correct position in `routine_delivery`
  and `guidance_docent`, matching `high_urgency`'s established convention.
- Document (not change) the publication-view-provenance finding.
- Regenerate the supplement through the supported pipeline and visually review
  every page.

## Required Changes

1. Reword `papers/01_charter/template.tex:144-145`'s disclaimer so it
   distinguishes `AUDITED`/`APPROVED` (achieved by every included card) from
   deployment validation (not achieved), preserving the URLs and attribution
   prose.
2. Correct `src/prosoc/prnc/charter/charter.md`'s 2026-11-06 history bullet
   to name P9 and Section 13 instead of "Principle 13."
3. Move `MODIFIED` to its chronologically-correct position (after `AUDITED`)
   in `src/prosoc/prnc/contexts/routine_delivery/context.md` and
   `src/prosoc/prnc/contexts/guidance_docent/context.md`, matching
   `high_urgency`'s established convention.
4. Regenerate `papers/01_charter` via `papers/01_charter/render.py --pdf`,
   update the golden `.tex`, and visually review the full PDF.

## Non-Goals

- Does not alter any normative content, YAML, audit verdict, or approval.
- Does not change the publication-view-provenance policy -- resolved by
  citing the existing adopted decision, not by code change.
- Does not pursue PDF/UA or accessibility tagging.

## Acceptance Criteria

(see frontmatter `acceptance`)

## Validation

- `scripts/validate/status`
- `scripts/lint`
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
- `PYTHONPATH="$(pwd)/src" python -m unittest tests.nca.utils.papers.render_test tests.nca.utils.papers.paper_semantics_test`
- `diff -u papers/01_charter/golden/rendered.tex build/papers/01_charter/rendered.tex`
- `lrh validate`

## Risk Notes

- The charter.md edit lands inside an `EDITED:`-labeled history bullet, which
  the audit-currency guard (`_mask_lifecycle_surface`) masks out entirely
  regardless of its text content -- expected to be a no-op for the guard, but
  confirm with `scripts/validate/status` rather than assuming.
- The `MODIFIED` reorder moves an *unmasked* line (`MODIFIED` is not a
  `STATES`-labeled bullet) relative to *masked* ones (`AUDITED`/`EDITED`
  bullets) only -- its position relative to other unmasked lines (`CREATED`,
  `VALIDATED`) is unchanged, so the masked-comparison text is provably
  unaffected. Confirmed empirically with `scripts/validate/status`, not just
  reasoned about.
