---
execution_id: 2026_11_01_11_16_23_WI_CHARTER_SUPPLEMENT_RENDERER_PDF_VERIFICATION
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION:WI_CHARTER_SUPPLEMENT_RENDERER_PDF_VERIFICATION)[2026-11-01T11:16:17+00:00]
work_item: WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-11-01T11:16:23+00:00
agent: claude-code
instruction_source: WS-CHARTER-SUPPLEMENT-PIPELINE
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Ran the real `pdflatex` + `pdftotext -layout` round trip this WI calls
for, against `papers/01_charter`'s charter supplement. No renderer,
template, or Lua filter code was changed (verification only, per this
WI's own Non-Goals).

# Result

## Environment
- OS: macOS 27.2 (Darwin 27.2.0, arm64), this sandbox had none of the
  required tooling at the start of this WI.
- `pdflatex`: pdfTeX 3.141592653-2.6-1.40.29 (TeX Live 2026), installed
  user-locally (no sudo) via TeX Live's own `install-tl -scheme basic
  -texdir ~/texlive/2026` -- the previously-attempted
  `brew install --cask basictex` path requires interactive `sudo`,
  unavailable in this sandbox, confirmed failing again before falling
  back to the user-local installer.
- `pdftotext`: 26.08.0 (Homebrew/poppler, already present).
- `kpsewhich`: kpathsea 6.4.2 (from the same TeX Live install).
- Frontiers `frontiers_suppmat.cls` (version 2.2, 2017/05/01): supplied
  by the user from their own Overleaf project for the paper. Installed
  into `~/Library/texmf/tex/latex/frontiers-suppmat/` (the user's
  personal `TEXMFHOME` tree) -- **not committed to this repository**,
  per this WI's Non-Goals and `WI-CHARTER-SUPPLEMENT-PDF-BUILD`'s Risk
  Notes (licensing for redistribution still unconfirmed). Additional
  LaTeX packages the class file transitively requires (`crop`,
  `sttools`, `changepage`, `datetime`, `parskip`, `xcolor`, `fmtcount`,
  `xkeyval`, plus the `collection-latexrecommended` /
  `collection-latexextra` / `collection-fontsrecommended` collections)
  were installed via `tlmgr`, same user-local tree, no sudo.

## Required Changes execution
1. `PYTHONPATH="$(pwd)/src" papers/01_charter/render.py --pdf` ran the
   full `build_pdf()` pipeline successfully: pandoc-version check
   (3.10.1), tool/class-file prerequisite checks, semantic checks,
   render, `pdflatex` compile (44 pages per `pdfinfo`; the CLI's own
   page-count report differs slightly at 45 -- not investigated, out
   of this WI's scope), internal text extraction, and
   `check_pdf_text_regressions` (raised nothing).
2. Separately ran `pdftotext -layout build/papers/01_charter/rendered.pdf
   build/papers/01_charter/rendered.txt` to produce the saved,
   inspectable text artifact this WI's Required Changes call for.
3. **Heading-numbering check: PASS.** All 152 numbered headings across
   the Charter and all 9 source cards show their number exactly once
   (e.g. `1.5.2 Explanation`, `4.3.5.4 Task Context`) -- confirmed via
   `grep -E '^[0-9]+(\.[0-9]+)* +[A-Za-z]'` against `rendered.txt`, no
   doubled-number pattern anywhere.
4. **Unicode-survival check: FAILS for 2 of 6 named characters.**
   Checked every actual occurrence of each named character inside the
   golden source's 19 `lstlisting` blocks (re-derived mechanically via
   a Python regex scan of `papers/01_charter/golden/rendered.tex`, not
   eyeballed) against the real extracted PDF text:
   - en dash (–, U+2013): 1 occurrence in source -- **FAILS**,
     extracts as `{` (confirmed byte-for-byte via hexdump: the P0
     principle's YAML block reads `P1–P9` in source but `P1{P9` in
     the extracted text).
   - em dash (—, U+2014): 3 occurrences in source -- **FAILS**,
     extracts as `|` (the movable-obstruction scenario's listing
     block).
   - curly apostrophe (', U+2019): 1 occurrence in source -- PASSES,
     extracts correctly.
   - non-breaking hyphen (‑, U+2011), curly double open/close quote
     (“/”, U+201C/U+201D): 0 occurrences in the current source content
     -- unverifiable, as this WI's own Required Changes step 4 already
     anticipated at drafting time.

   Likely root cause (diagnostic, not fixed -- out of this WI's
   scope): neither `papers/01_charter/template.tex` nor the Frontiers
   class file loads `\usepackage[T1]{fontenc}` or
   `\usepackage{textcomp}` (confirmed via `grep`), so `\textendash`/
   `\textemdash` (used by the `literatecard` `literate=` mapping,
   `template.tex:65-66`) fall back to OT1-encoded glyphs with
   incorrect PDF `ToUnicode` mappings -- a well-documented LaTeX
   pitfall. `\textquoteright` happens to degrade to a glyph with a
   sane mapping even under OT1, which is why only the apostrophe case
   survived.
5. Environment recorded above.
6. **Filed `WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX`** (merged via
   PR #121, commit `f4e3e7927840b57b01027477f7494e66a5facd82`)
   describing the failing en-dash/em-dash check, per this WI's own
   Acceptance Criteria ("Any residual gap found is filed as a new work
   item, not silently left unresolved") -- rather than silently
   reporting a complete pass.

## Verdict against this WI's own Acceptance Criteria
- "Compiled PDF text shows each heading's number exactly once" --
  **met**.
- "Unicode dash/quote characters inside lstlisting blocks survive a
  real pdflatex compile + pdftotext -layout extraction" -- **not met**
  for en dash and em dash (2 of 6 named characters); met for curly
  apostrophe; unverifiable for the remaining 3 (zero occurrences in
  current content).
- "Any residual gap found is filed as a new work item, not silently
  left unresolved" -- **met**: `WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX`
  filed and merged.

This WI's own job -- verify via a real round trip, and ensure any gap
is tracked rather than silently passed -- is complete. The underlying
renderer defect itself is intentionally left to the new WI, per this
WI's Non-Goals ("Does not re-implement or modify the renderer,
template, or Lua filter -- this is verification only").

# Validation
- `lrh validate` -- 0 errors, 20 pre-existing unrelated warnings
- Manual `pdflatex` + `pdftotext -layout` round trip, reported above,
  including a byte-level (hexdump) re-verification of the en-dash
  corruption, not just a grep match.

# Follow-up
`WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX` tracks the confirmed defect.
`WS-CHARTER-SUPPLEMENT-PIPELINE` remains open behind it.
