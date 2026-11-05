---
execution_id: 2026_11_05_04_24_20_WI_CHARTER_SUPPLEMENT_LISTING_DASH_GLYPH_FIX_SELFREVIEW
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_LISTING_DASH_GLYPH_FIX_SELFREVIEW)[2026-11-05T04:24:16+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-11-05T04:24:20+00:00
agent: claude-code
instruction_source: WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Diff-mode `/lrh-self-review`, run before this PR's first push, against the
3-file diff (`papers/01_charter/template.tex`,
`papers/01_charter/golden/rendered.tex`,
`tests/nca/utils/papers/render_test.py`) implementing
WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX.

# Result

Dispatched a cold `general-purpose` subagent (no session memory) with
only the diff and the target WI's full content. Findings: no blocking
issues; 3 nitpicks:

1. The new `TestListingDashGlyphVisualWidth` regression test renders a
   synthetic minimal reproduction (an isolated hyphen vs. an isolated en
   dash through the shared `literatecard` style), not literally the WI's
   named "page 3"/"page 25" content -- correctly flagged against the WI's
   literal acceptance-criteria wording ("renders representative pages").
   Non-blocking: the real pages 3 and 25 of the actual compiled PDF were
   independently visually verified earlier in this session (600 DPI
   renders, direct pixel inspection, before this test was written), and
   the synthetic reproduction reuses `template.tex`'s own literal
   preamble text (not a hand-duplicated copy), so it validates the real
   fix mechanism and cannot silently drift from it. A full page-level
   automated visual check was judged disproportionate (slower, tied to
   exact page numbers that shift as corpus content changes) versus a
   driftproof, isolated glyph-width check plus the one-time manual page
   verification already performed.
2. The two `pdftoppm` `subprocess.run` calls lacked `capture_output=True,
   text=True` (unlike the `pdflatex` call just above, which wraps
   failure with a helpful message). Fixed: both calls now wrapped in the
   same try/except-with-diagnostics pattern as the `pdflatex` call.
3. `_darkest_row_run_length`'s pure-Python nested loop over a full 300
   DPI page (~8M iterations x2) is slow but not a bug -- accepted as-is,
   since no image library (PIL/Pillow) is part of this project's
   environment.

Independently re-verified the subagent's top finding (#1) myself,
directly against the live repo (not re-delegated): confirmed
`project/work_items/proposed/WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX.md:18`
does say "renders representative pages to PNG/image," and confirmed the
new test indeed renders a synthetic two-page reproduction, not the real
card pages. The finding held up exactly as reported; applied fix #2
immediately (trivial and clearly correct), accepted #1 and #3 as
documented tradeoffs rather than defects.

Also independently verified several of the subagent's other specific
claims were themselves checkable and correct: the golden-file diff is
identical to the `template.tex` diff (header lines aside), the
documentclass-swap regex matches the real `template.tex:10` line exactly,
and `re` was already imported at the top of `render_test.py`.

# Validation

Re-ran the full suite after applying fix #2:
- `python -m unittest discover tests '*_test.py'` -- 339/339 pass
  (skipped=1, the environment-conditional `TestPdfBuildRealEnvironment`
  case)
- `scripts/lint` -- clean
- `lrh validate` -- 0 errors, 20 pre-existing unrelated warnings

# Follow-up

None blocking. `/lrh-implement` Step 8 (commit/push) proceeds regardless
of this clean-with-nitpicks result, per this skill's own design.
