---
resolution: "Implemented and merged in PR #129 (commit 53775c6a029708505187d13fe89cdb6ab0175864) -- fixed a malformed quote-mark pair, labeled an unlabeled P&G citation-index list, updated stale submitted/unpublished wording to in press in 3 locations, narrowed an overbroad citation claim, completed the Dragan et al. reference with its full conference name/pages/DOI, defined P&G at its first use, and applied 5 grammar fixes; added a check_stale_supplement_wording regression check (with whitespace-normalization added during review-response) so these fixes can't silently regress."
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES
title: "Copyedit the charter supplement's source cards: quote marks, Cited In labeling, stale submission language, grammar, and citation completeness"
type: deliverable
status: resolved
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PROOFREADING
depends_on: []
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_lifecycle_state_change]
acceptance:
  - "The 'related_scenarios' quotation-mark pair renders with matching open/close marks, not two opening marks"
  - "The Frontal Approach card's 'Cited In: 50, 126, 167' numbers are traced to their authoritative source and either labeled, replaced with real citations, or removed from the publication view, grounded in what they actually are"
  - "No remaining 'submitted'/'unpublished'/'Francis, submitted' language describing the accompanying article, replaced with durable wording"
  - "The 'no external literature yet exists that could cite it' absolute claim is replaced with a narrower, supportable statement"
  - "The Dragan et al. reference has complete bibliographic details (full conference name, year already present; volume/pages if applicable), traced to the canonical citation, not invented"
  - "'P&G' is defined at first use or replaced with an unambiguous reference"
  - "The 5 named grammar/wording issues (pp. 1, 7, 13, 15, 29-32) are corrected, with a corpus-wide search for other occurrences of the same patterns (especially the hand-off/handoff/handed off inconsistency)"
required_evidence: [manual_review, test_output]
artifacts_expected:
  - src/prosoc/prnc/
---

## Summary
Batch of mechanical, low-judgment copyediting fixes to the charter
supplement's canonical source cards, identified by a second-pass external
proofread of the generated PDF: a malformed quote pair, unexplained
citation numbers, stale "submitted"/"unpublished" language (the
accompanying article is now in author proofs), an incomplete reference,
an undefined abbreviation, and five specific grammar/wording issues.

## Problem / Context
Confirmed directly in this session (grep against the actual source
files, not taken on the reviewer's word alone):

- `src/prosoc/prnc/charter/charter.md:15` -- `(Francis, submitted)`.
- `src/prosoc/prnc/scenarios/single_file_hallway/scenario.md:6,10,35` and
  `src/prosoc/prnc/scenarios/movable_obstruction/scenario.md:6,10,35` --
  "submitted to Frontiers", "is unpublished", and the verbatim absolute
  claim "no external literature yet exists that could cite it."
- `src/prosoc/prnc/charter/charter.md:484` -- `Dragan, A. D., Lee, K. C.
  T., & Srinivasa, S. S. (2013). Legibility and predictability of robot
  motion. *HRI*.` -- ends at the venue abbreviation with no volume,
  pages, or full conference name.

The malformed-quote location (p. 15, `evaluation_notes` block showing
`'related_scenarios'` with two opening marks) and the "Cited In: 50, 126,
167" numbers (Frontal Approach card, pp. 13/15) were not independently
re-verified in this planning pass -- the executing session should locate
and confirm both before editing, per this project's standing "verify
claims against the real tree" practice, and should specifically trace the
`Cited In` numbers to their authoritative source (do not assume they are
main-article bibliography numbers without checking -- they may be
internal corpus metadata not meant for a reader-facing view).

Now that the accompanying article is in author proofs rather than merely
submitted, "submitted"/"unpublished" wording is stale. The reviewer's
suggested durable replacement ("the accompanying article" or another
publisher-approved designation) avoids introducing a new status that will
itself go stale again at the next publication milestone.

### Duplication search
- In-repo: no existing work item covers general copyediting of the
  charter supplement cards; `WI-CHARTER-SUPPLEMENT-SOURCE-FIXES` (resolved)
  covered a different, earlier set of defects (stale paths, collapsed
  lists, dangling cross-references) from the original 2026-10-26 audit.
- Recommendation: Proceed.

### Demand search
- Directly requested by the second-pass proofread (this session,
  2026-11-04).
- Recommendation: Proceed.

## Scope
Source-level (canonical Markdown/YAML) copyediting fixes only -- no
renderer, template, or LaTeX changes. Fix the canonical source, not
generated LaTeX, per the reviewer's own instruction for the quote-mark
issue (and consistent with this pipeline's existing convention of never
hand-editing generated fragments).

## Required Changes
1. Locate and fix the malformed `'related_scenarios'` quote pair (p. 15
   equivalent, an `evaluation_notes` block) -- matching quotation marks,
   or Markdown/YAML code-style presentation (backticks) if more
   appropriate for an identifier.
2. Trace the Frontal Approach card's `Cited In: 50, 126, 167` numbers to
   their authoritative source, then apply whichever grounded fix matches
   what they actually are: an explicit label (e.g. "Cited in P&G
   references 50, 126, and 167"), author-year citations, complete
   references, or removal from the publication view if they are internal
   corpus metadata.
3. Replace "submitted"/"unpublished"/"Francis, submitted"/"submitted to
   Frontiers" language describing the accompanying article with durable
   wording (e.g. "the accompanying article"), across all occurrences
   found by a corpus-wide search, not just the cited locations.
4. Replace the "no external literature yet exists that could cite it"
   absolute claim with a narrower, supportable statement (e.g. "No
   external citations are currently recorded for this scenario.") if
   accurate.
5. Complete the Dragan et al. reference with the full conference title
   and standard bibliographic details, consistent with the supplement's
   existing reference style -- trace the canonical citation rather than
   inventing missing metadata.
6. Define "P&G" at first use, or replace the shorthand with an explicit
   author-year/title reference.
7. Apply the five named grammar/wording fixes (p. 1 "fully-audited
   normative card content"; p. 7 P6 explanation's run-on "This
   understanding determines interaction potential..."; p. 13's "Successful
   navigation ... and successful social navigation ..." repetition; p. 15
   "in the conditions for a mild and typical conflict"; pp. 29-32's
   hand-off/handoff/handed off inconsistency), and search the corpus for
   other occurrences of each pattern so corrections are consistent, not
   local to the cited pages.

## Non-Goals
- Does not touch the charter's or any card's normative content, lifecycle
  state, or definitional meaning -- see
  `WI-CHARTER-SUPPLEMENT-DEFINITIONAL-CONSISTENCY` for the two items
  (prosocial-behavior glossary definition, P9 emergency-context framing)
  that do require that kind of judgment call.
- Does not edit generated LaTeX/fragments directly.
- Does not change audit/approval lifecycle evidence -- see
  `WI-CHARTER-SUPPLEMENT-AUDIT-EVIDENCE-BACKFILL`.

## Acceptance Criteria
- All items in Required Changes applied and verified against the
  regenerated PDF (not just the Markdown source).
- Golden file regenerated with human-reviewed diff.
- New regression coverage: no malformed `'identifier'` quote pairs, no
  unexplained `Cited In` numeric lists in the publication view, no stale
  `submitted`/`unpublished` language in the generated supplement.
- `scripts/test` / `lrh validate` pass.

## Validation
- `scripts/test`
- `lrh validate`
- `papers/01_charter/render.py --pdf`, with a text-extraction check
  confirming each corrected phrase appears as intended in the compiled
  PDF.

## Risk Notes
- The `Cited In` numbers specifically carry a real risk of misattribution
  if fixed without tracing their actual source first -- the reviewer
  explicitly warns against assuming they are main-article bibliography
  numbers.

## Dependencies / Order
None. Independent of the other items in this workstream.
