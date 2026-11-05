---
execution_id: 2026_11_05_04_26_13_WI_CHARTER_SUPPLEMENT_LISTING_DASH_GLYPH_FIX
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX:WI_CHARTER_SUPPLEMENT_LISTING_DASH_GLYPH_FIX)[2026-11-05T04:07:43+00:00]
work_item: WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/127
commit:
created_at: 2026-11-05T04:26:13+00:00
agent: claude-code
instruction_source: WS-CHARTER-SUPPLEMENT-PROOFREADING
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Fixed the visually-short en/em dash glyphs inside the charter
supplement's `lstlisting` blocks, found by a second-pass external
proofread: `WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX` (PR #124) fixed
`pdftotext` extraction but not the actual drawn glyph.

# Result

- Root-caused the defect via isolated `pdflatex`+`pdftoppm` comparisons
  against three monospace fonts (Latin Modern Mono, TeX Gyre Cursor,
  DejaVu Sans Mono): Latin Modern Mono's own `\textendash`/`\textemdash`
  glyphs are drawn short by genuine font design, not a mapping bug (TeX
  Gyre Cursor reproduces the same short rendering with its own distinct
  glyphs). DejaVu Sans Mono renders visually longer, but its TeX Live T1
  encoding vector substitutes `/hyphen` for `/endash` at that slot
  (confirmed via the font's own `.enc` file) and extracts as a plain
  hyphen -- not a usable drop-in fix.
- Added `\newcommand{\dashstretch}[1]{\scalebox{1.8}[1]{#1}}` to
  `papers/01_charter/template.tex` and wrapped the `literatecard`
  style's `literate=` mapping's `\textendash`/`\textemdash` replacements
  with it. `\scalebox` only transforms how the already-selected real
  glyph is drawn, not which glyph/character it is, so the correct
  `ToUnicode` mapping from `WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX` is
  untouched.
- Verified with a real `pdflatex`+`pdftoppm` round trip at 600 DPI
  against the actual compiled PDF: both the en dash (P0 principle's
  embedded YAML `lstlisting` block) and em dash (movable-obstruction
  scenario's listing block) now render visibly long, correct dashes.
  `pdftotext` extraction counts unchanged (en dash 8, em dash 75 -- no
  regression on the prior fix).
- Added `TestListingDashGlyphVisualWidth`
  (`tests/nca/utils/papers/render_test.py`): renders the real
  `literatecard` style's mapped en-dash output (reusing `template.tex`'s
  own literal preamble text, so it can't drift from the real style) to a
  raster image via `pdftoppm`, parses the resulting PGM with a small
  pure-Python helper (no new dependency -- PIL/Pillow isn't part of this
  project's environment), and asserts the drawn stroke is meaningfully
  wider than a plain hyphen's. Confirmed by temporarily reverting the fix
  that this test fails against the old mapping (15px vs 15px, zero
  difference) and passes against the fix -- a genuine, working regression
  check for a defect class `pdftotext`-only validation cannot catch.
- Regenerated `papers/01_charter/golden/rendered.tex`; diff reviewed and
  approved by the human as exactly the new preamble content (the
  `graphicx` import, the `\dashstretch` macro, two `literate=` lines), no
  card-content changes.
- Diff-mode self-review (cold `general-purpose` subagent, before this
  PR's first push): no blocking findings. Independently re-verified its
  top finding myself directly: confirmed the WI's acceptance criteria do
  literally say "renders representative pages," and confirmed the new
  test renders a synthetic two-page reproduction rather than the real
  card pages -- accepted as a documented tradeoff (the real pages were
  independently visually verified earlier in this session; see the
  `_SELFREVIEW` record for the full finding and rationale). Fixed one
  trivial nitpick (missing `capture_output` on the test's `pdftoppm`
  calls) before pushing.

# Validation

- `python -m unittest discover tests '*_test.py'` -- 339/339 pass
  (skipped=1, the environment-conditional real-tool-availability case)
- `scripts/lint` -- clean
- `lrh validate` -- 0 errors, 20 pre-existing unrelated warnings
- Manual `pdflatex` + `pdftoppm` round trip at 600 DPI, direct visual
  inspection of both affected pages, reported above
- New regression test confirmed to fail against the pre-fix mapping and
  pass against the fix, verified before landing either

# Follow-up

None blocking. This resolves the highest-priority item in
`WS-CHARTER-SUPPLEMENT-PROOFREADING`, pending this PR landing.
