---
execution_id: 2026_11_07_08_37_32_CHARTER_SUPPLEMENT_PUBLICATION_CLEANUP
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-PUBLICATION-CLEANUP:CHARTER_SUPPLEMENT_PUBLICATION_CLEANUP)[2026-11-07T08:37:32+00:00]
work_item: WI-CHARTER-SUPPLEMENT-PUBLICATION-CLEANUP
status: in_progress
rerun_of: null
pr: https://github.com/xenotaur/prosoc/pull/138
commit: null
created_at: 2026-11-07T08:37:32+00:00
agent: claude_app
instruction_source: ad hoc — follow-up publication cleanup requested in a review session after WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY closed; WI created in this same session, so no prior WI file to point to
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Follow-up publication cleanup for the charter supplement, from an external
review session after `WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY` closed. Fixed
three concrete defects and resolved two investigation questions.

# Result

1. **Page-one disclaimer** (`papers/01_charter/template.tex:144-145`) --
   reworded to distinguish `AUDITED`/`APPROVED` (achieved by all 9 included
   cards, per `papers/01_charter/sources.txt`) from deployment validation (not achieved), replacing the now-stale
   "not ... fully audited" wording. URLs and attribution prose preserved.
2. **"Principle 13" reference** (`src/prosoc/prnc/charter/charter.md`) --
   corrected the 2026-11-06 history bullet to read "P9's Explanation in
   Section 13" instead of "Principle 13's Explanation." Verified `## 13.
   Principle P9` is the actual heading before editing. Edited in place (a
   wording clarification of the original intent, not a change to what
   happened) rather than adding a new history bullet, since the edit lands
   entirely inside an existing `EDITED:`-labeled bullet already masked by
   the audit-currency guard.
3. **Context-history field ordering** (`routine_delivery`, `guidance_docent`)
   -- moved `MODIFIED: 2026-10-27` to after `AUDITED` in both cards, matching
   the chronological convention already demonstrated by `high_urgency` (the
   one other context card that went through this workstream's original
   repair, not just WI-4's drive-by fix). Initial investigation assumed the
   out-of-order appearance was intentional fixed-schema behavior per
   `contexts/template.md`; checking `high_urgency` disproved that --
   `routine_delivery`/`guidance_docent` were the actual outliers. Verified
   the reorder is masked-comparison-safe before and after editing (`MODIFIED`
   is not a `STATES`-labeled bullet, so it is unmasked; its position relative
   to other unmasked lines -- `CREATED`, `VALIDATED` -- is unchanged by moving
   it past masked `AUDITED`/`EDITED` bullets).
4. **Publication-view provenance** -- investigated, no change made. An
   adopted decision already exists (`docs/paper-supplements.md`'s
   "Publication View and Internal Provenance" section,
   `WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER`, confirmed with the user
   2026-11-06): retain full provenance deliberately, as part of the
   supplement's "transparent, auditable snapshot" purpose. No action needed.

All 32 cards remain consistent and `APPROVED` after all three edits --
confirmed via `scripts/validate/status`, not assumed. The supplement was
regenerated exclusively through `papers/01_charter/render.py --pdf`; the
golden `.tex` was updated to match, with the diff scoped exactly to the
three intended changes each time. All 48 PDF pages were checked
programmatically (blank-page scan, broken-URL scan, malformed-quote scan,
footer consistency) and every page was individually visually inspected (not
a sample -- a Copilot review of an earlier commit on this PR correctly
flagged that the sample-plus-scans approach did not actually satisfy the
WI's own "every page" acceptance criterion; completed the full inspection
in response).

# Validation

- `scripts/validate/status` -- all 32 cards consistent, `APPROVED`, both
  before and after the context-card reorder.
- `PYTHONPATH="$(pwd)/src" scripts/distill/charter --dry-run --show-diffs`
  and `python -m prosoc.prnc.contexts.distill --dry-run --show-diffs` -- no
  drift from either content edit.
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"` --
  390 tests, 0 failures, 1 pre-existing skip.
- `PYTHONPATH="$(pwd)/src" python -m unittest tests.nca.utils.papers.render_test
  tests.nca.utils.papers.paper_semantics_test` -- 68 tests, 0 failures,
  1 pre-existing skip.
- `diff -u papers/01_charter/golden/rendered.tex build/papers/01_charter/rendered.tex`
  -- clean after golden update.
- `scripts/lint` -- all checks passed.
- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- PDF: 48 pages, no blank pages, no broken/malformed URLs, no malformed
  quotes, consistent odd/even footer convention (pre-existing Frontiers
  template behavior, unchanged). All 48 pages individually visually
  inspected -- no clipping, overlap, orphaned headings, malformed code
  blocks, or pagination regressions found anywhere.

# Follow-up

None blocking.
