---
execution_id: 2026_10_29_15_41_54_WI_CHARTER_SUPPLEMENT_PDF_BUILD
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-PDF-BUILD:WI_CHARTER_SUPPLEMENT_PDF_BUILD)[2026-10-29T15:26:04+00:00]
work_item: WI-CHARTER-SUPPLEMENT-PDF-BUILD
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/117
commit: 1e3e7f8b38fe5d47af199d72353b9bd1faa26ef7
created_at: 2026-10-29T15:41:54+00:00
agent: claude-code
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-PDF-BUILD.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implements WI-CHARTER-SUPPLEMENT-PDF-BUILD: a reproducible PDF build entry
point for the charter supplement (`render.py --pdf`), resolved as the next
ready work item under WS-CHARTER-SUPPLEMENT-PIPELINE via `/lrh-execute`
(RENDERER-PDF-VERIFICATION skipped — not `prompt_ready`, missing Required
Changes).

# Result

Added to `src/prosoc/nca/utils/papers/render.py`: `PANDOC_PINNED_VERSION`,
`FRONTIERS_TEX_CLASS`, `SEMANTIC_CHECK_MODULES`,
`KNOWN_PDF_TEXT_CORRUPTIONS` constants; `parse_tool_version`,
`check_pandoc_version`, `get_tex_engine_version`, `require_tool`,
`check_class_file`, `run_semantic_checks`, `compile_pdf`,
`extract_pdf_text`, `count_pdf_pages`, `check_pdf_text_regressions`,
`build_pdf` functions; and a `--pdf` flag on `main()`. `build_pdf`
orchestrates: pin-checked Pandoc version -> required-tool presence
(`pdflatex`, `pdftotext`) -> Frontiers class-file presence via
`kpsewhich` -> the semantic/LaTeX regression suite
(`WI-CHARTER-SUPPLEMENT-TEST-COVERAGE`'s tests) -> render -> fail-fast
`pdflatex` compile -> `pdftotext -layout` extraction -> known-corruption
regression check -> a report (Pandoc version, TeX engine version, PDF
path, page count).

`papers/01_charter/template.tex` now loads `lmodern` (outline/scalable
fonts) so `pdftotext` extraction doesn't silently drop dashes/quotes, per
the 2026-10-26 audit's finding that the class's default bitmap Computer
Modern fonts do exactly that.

`docs/paper-supplements.md` documents the new command and its 7-step
pipeline.

**Not done, by the WI's own Non-Goals:** no Frontiers `frontiers_suppmat`
class file committed (licensing not confirmed for redistribution --
`--pdf` fails clearly with a "supply it locally" message instead); golden
file not regenerated (`WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN`); no CI wiring
(`WI-CHARTER-SUPPLEMENT-CI`).

**Verification caveat:** this sandbox has no `pdflatex`/`kpsewhich`/class
file, so the compile -> extract -> regression-check path is validated via
injected fake runners in unit tests, not an end-to-end real PDF compile.
The fail-fast paths are exercised for real wherever possible, including
one test (`TestPdfBuildRealEnvironment`) against this sandbox's actual
missing-`pdflatex` state.

A diff-mode `/lrh-self-review` pass (see
`project/executions/AD_HOC/2026_10_29_15_40_25_WI_CHARTER_SUPPLEMENT_PDF_BUILD_SELFREVIEW.md`)
found and fixed one should-fix issue before this push:
`check_pandoc_version`/`get_tex_engine_version` didn't wrap
`CalledProcessError` into a clear error, unlike the file's other
subprocess-calling functions.

# Validation

- `black --check` clean
- `scripts/lint` clean
- `PYTHONPATH="$(pwd)/src" python3 -m unittest tests.nca.utils.papers.render_test -v` -- 59/59 pass
- `PYTHONPATH="$(pwd)/src" scripts/test` -- 337/337 pass
- `lrh validate` -- 0 errors, 20 pre-existing unrelated warnings

# Follow-up

- Deferred PDF-level/end-to-end verification against a real `pdflatex` +
  committed/supplied Frontiers class file remains tracked under
  `WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION` (currently blocked on
  its own missing Required Changes section) and, more directly, under this
  WI's own acceptance criteria once a sandbox or CI with `pdflatex` and the
  class file available can exercise it.
- `WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN` and `WI-CHARTER-SUPPLEMENT-CI` remain
  open in `WS-CHARTER-SUPPLEMENT-PIPELINE`.
