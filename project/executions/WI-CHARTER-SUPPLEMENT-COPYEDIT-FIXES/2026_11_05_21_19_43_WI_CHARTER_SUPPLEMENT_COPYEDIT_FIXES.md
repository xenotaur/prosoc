---
execution_id: 2026_11_05_21_19_43_WI_CHARTER_SUPPLEMENT_COPYEDIT_FIXES
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES:WI_CHARTER_SUPPLEMENT_COPYEDIT_FIXES)[2026-11-05T21:05:24+00:00]
work_item: WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/129
commit:
created_at: 2026-11-05T21:19:43+00:00
agent: claude-code
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES.md
session_transcript: pending
---

# Summary

Implements `WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES`: 7 mechanical copyedit
fixes to the charter supplement's canonical source cards, identified by a
second-pass external proofread. Source-level fixes only, per the WI's own
Scope -- one exception noted below.

# Result

1. **Malformed quote pair**: `frontal_approach/scenario.md`'s
   `evaluation_notes` block had a backtick-quoted `` `related_scenarios` ``
   inside a raw `lstlisting`-rendered block, which renders as two
   opening-style marks (backtick has no closing counterpart glyph), not a
   matching pair -- confirmed by direct inspection of the golden LaTeX
   output's `lstlisting` content before editing. Switched to straight
   double quotes, matching the adjacent sentence's own `"Ped. Obstruct"`
   convention in the same paragraph.
2. **Unlabeled Cited In list**: traced `cited_in: [50, 126, 167]` to
   `.claude/skills/_shared/pg_scenarios.md:23` (`Cited In: [50, 126, 167]`
   for Frontal Approach, verbatim from P&G paper Table 3) and
   `schema.json`'s own field description ("external works... e.g., P&G
   paper citation numbers") -- confirmed these are the P&G paper's own
   bibliography-index numbers, not internal corpus metadata. Labeled the
   rendered "Scenario Card Summary" bullet explicitly: "P&G references 50,
   126, and 167". Left the underlying `cited_in:` YAML array untouched.
3. **Stale submitted/unpublished language**: `charter.md`'s SOURCE line
   ("Francis, submitted)" -> "Francis, in press)"), and
   `single_file_hallway`/`movable_obstruction`'s SOURCE lines ("submitted
   to Frontiers" -> "in press at Frontiers").
4. **Overbroad absolute claim**: the same two scenario cards' "Cited In
   -- reasonably blank" notes narrowed "no external literature yet exists
   that could cite it" to "no external citations are currently recorded
   for this scenario."
5. **Incomplete Dragan et al. reference**: completed with the full
   conference name, pages, and DOI -- verified via a live web search
   against the real HRI 2013 proceedings (CMU RI publication page,
   DBLP), not invented: "In Proceedings of the 8th ACM/IEEE International
   Conference on Human-Robot Interaction (HRI '13), 301-308.
   https://doi.org/10.1109/HRI.2013.6483603".
6. **Undefined "P&G"**: defined at its first in-body use in `charter.md`
   ("Following the Principles and Guidelines (P&G) paper (Francis et al.,
   2025), we define...").
7. **Five grammar/wording fixes**: un-hyphenated "fully-audited" ->
   "fully audited" in `template.tex` (the one exception to source-only
   scope -- this specific prose lives only in the hand-authored LaTeX
   template, not in any card); split a run-on sentence in `charter.md`'s
   P6 explanation; reduced a repeated "navigation...navigation" in
   `frontal_approach`'s Scenario Overview; reworded an awkward "in the
   conditions for a mild and typical conflict" phrase; standardized
   `deliver_object/task.md`'s "hand-off" (3 noun-form occurrences) to
   "handoff", matching the dominant corpus convention already used in
   `object_handover`/`crash_cart` -- left the verb-form "handed off" and
   the `handoff_to_human_corridor` identifier untouched.

Added `check_stale_supplement_wording()` to
`src/prosoc/nca/utils/papers/render.py` (mirroring the existing
`check_pdf_text_regressions()` pattern), wired into `build_pdf()`, to
catch any of these wording fixes silently regressing. Regenerated
`frontal_approach/scenario.yml` and `deliver_object/task.yml` via their
distillers (the quote-pair/phrasing fix and the handoff fix each live
inside an embedded fenced-YAML field, not just rendered prose).
Regenerated `papers/01_charter/golden/rendered.tex`, hand-reviewed the
diff (exactly the 7 intended hunks plus 5 new EDITED-history bullets,
nothing else), and confirmed it with a real `pdflatex` build.

**Self-inflicted false-positive caught and fixed during implementation**:
my first attempt at the new EDITED-history bullets quoted the *old*
stale text verbatim as documentation (e.g. `the stale "(Francis,
submitted)" SOURCE attribution`), which is itself part of the rendered
PDF -- this immediately tripped my own new
`check_stale_supplement_wording` check on the first `--pdf` build
attempt. Reworded the bullets to describe the fix generically instead of
quoting the exact flagged substrings, then re-built clean.

# Validation

- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
  -- 343 tests, `OK (skipped=1)` (4 new tests for the regression check).
- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- `scripts/lint` -- all checks passed.
- `PYTHONPATH="$(pwd)/src" scripts/distill/scenarios`/`scripts/distill/tasks
  --dry-run --show-diffs` -- confirmed the exact expected single-field
  diff before applying each; 0 differences after.
- A real `PYTHONPATH="$(pwd)/src" papers/01_charter/render.py --pdf`
  build succeeded (45 pages); `pdftotext -layout` extraction directly
  confirms every corrected phrase appears as intended and all 5
  `KNOWN_STALE_SUPPLEMENT_WORDING` substrings have zero matches.
- `papers/01_charter/render.py` (no `--pdf`) regenerate, diffed against
  the accepted golden file -- empty, byte-identical.
- Diff-mode `/lrh-self-review` dispatched before this PR was opened (see
  the companion `_SELFREVIEW` record): clean result, no blocking
  findings, independently re-verified.

# Follow-up

None blocking. **Noted for future awareness** (out of scope for this
WI, per its own Non-Goals): the same backtick-quote-pair pattern this PR
fixes in `frontal_approach` also exists in ~12 other scenario cards not
currently in `papers/01_charter/sources.txt` (confirmed by the self-review
subagent). If a future WI brings any of those cards into the charter
supplement, the same fix should be applied there too.
