---
execution_id: 2026_11_01_21_16_16_WI_CHARTER_SUPPLEMENT_RENDERER_DASH_FIX
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX:WI_CHARTER_SUPPLEMENT_RENDERER_DASH_FIX)[2026-11-01T11:35:23+00:00]
work_item: WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/124
commit: 9a701396fdb6e7325f254266048013d75a1a96f0
created_at: 2026-11-01T21:16:16+00:00
agent: claude-code
instruction_source: WS-CHARTER-SUPPLEMENT-PIPELINE
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Fixed the confirmed PDF-text corruption of en dash and em dash inside
the charter supplement's `lstlisting` blocks, found by
`WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION`.

# Result

- Added `\usepackage[T1]{fontenc}` to `papers/01_charter/template.tex`,
  right after `\documentclass` and before `\usepackage{lmodern}` --
  without T1 encoding, `\textendash`/`\textemdash` (used by the
  `literatecard` style's `literate=` mapping, `template.tex:71-73`)
  fall back to OT1-encoded glyphs with incorrect PDF `ToUnicode`
  mappings.
- Re-ran the real `pdflatex` + `pdftotext -layout` round trip (same
  user-local TeX Live install and user-supplied Frontiers class file
  from earlier in this session). Both previously-corrupted phrases now
  extract correctly: `P1–P9` (was `P1{P9`) and
  `itself—by removing or reporting the obstruction—thereby` / `apply — it is`
  (was `|`). Total character counts in the extracted text confirm this
  exactly: en dash 7 -> 8 (+1), em dash 72 -> 75 (+3) -- each delta
  matching the previously-corrupted occurrence count precisely, with no
  other count changes.
- Regenerated `papers/01_charter/golden/rendered.tex`. Diff reviewed
  and approved by the user before regenerating: exactly the new
  preamble block (6 lines, comment + `\usepackage[T1]{fontenc}`), no
  card-content changes -- as predicted, since `render_paper()` copies
  `template.tex`'s preamble verbatim
  (`src/prosoc/nca/utils/papers/render.py:248`).
- Diff-mode self-review (cold `general-purpose` subagent, before this
  PR's first push): no findings. Independently re-verified its two key
  claims myself directly: the `fontenc` line's placement (confirmed via
  `sed`) and the repo-wide `grep -rln fontenc` result (confirmed only
  the two changed files match).

# Validation

- `scripts/test` -- 338/338 pass (the "FAIL ..." lines in its output
  are expected stdout from the card-validator CLI under test, not
  actual test failures -- confirmed by the final "OK (skipped=1)")
- `scripts/lint` -- clean
- `scripts/format --check --diff` -- 22 pre-existing, unrelated
  reformats (none touching this change, which is `.tex`-only)
- `lrh validate` -- 0 errors, 20 pre-existing unrelated warnings
- Manual `pdflatex` + `pdftotext -layout` round trip, before/after
  character-level comparison, reported above

# Follow-up

None. This resolves the last open item in
`WS-CHARTER-SUPPLEMENT-PIPELINE`'s original work-items list, pending
this PR landing.
