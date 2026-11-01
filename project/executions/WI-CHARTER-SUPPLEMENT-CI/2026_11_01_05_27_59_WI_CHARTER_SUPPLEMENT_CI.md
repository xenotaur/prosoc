---
execution_id: 2026_11_01_05_27_59_WI_CHARTER_SUPPLEMENT_CI
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-CI:WI_CHARTER_SUPPLEMENT_CI)[2026-11-01T03:49:05+00:00]
work_item: WI-CHARTER-SUPPLEMENT-CI
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/119
commit: d6084d1f8da4ba3e817d239d7f6414c20599e9c9
created_at: 2026-11-01T05:27:59+00:00
agent: claude-code
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-CI.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implements WI-CHARTER-SUPPLEMENT-CI: adds CI coverage for the charter
supplement pipeline, resolved as the next ready work item under
WS-CHARTER-SUPPLEMENT-PIPELINE via /lrh-execute
(RENDERER-PDF-VERIFICATION skipped again -- still not prompt_ready,
missing Required Changes).

# Result

Added `.github/workflows/charter-supplement.yml` (new file; existing
`.github/workflows/charter.yml` untouched per this WI's Non-Goals).
Steps: install the pinned Pandoc version (read dynamically from
`PANDOC_PINNED_VERSION` in `prosoc.nca.utils.papers.render`, avoiding a
second hardcoded copy) -> check it via `check_pandoc_version()` (a real,
job-failing step) -> run the renderer/semantic regression suite -> render
the supplement -> fail the job on a golden-file diff (meaningful now that
WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN has landed, PR #118) -> best-effort
attempt a PDF build via `render.py --pdf`, reporting clearly via
`::notice::` (never silently) when it can't complete, and uploading the
PDF + diagnostics as artifacts only on success. Triggers on
`papers/01_charter/**`, all 9 source cards in `sources.txt`, the renderer
module, its tests, and `pyproject.toml`.

A diff-mode `/lrh-self-review` pass (see
`project/executions/AD_HOC/2026_11_01_05_26_49_WI_CHARTER_SUPPLEMENT_CI_SELFREVIEW.md`)
found 0 issues; the subagent additionally reproduced the PDF-stage's
`set +e`/capture-exit-code behavior locally against this sandbox's real
missing-`pdflatex` state, verified the `actions/upload-artifact` SHA pin
live against GitHub's API, and ran the full pipeline locally confirming
the golden file is genuinely non-stale.

**Real test-PR run (this WI's own Validation requirement):** the new
workflow ran on PR #119 itself immediately after the first push --
run 41277094772, conclusion `success`. Pandoc 3.10.1 installed and
matched the pin; the renderer/semantic test suite passed; render +
golden-diff check passed with no drift; the PDF stage correctly did
not complete (`pdflatex` unavailable on the runner, as expected) and
reported this via a GitHub Actions `::notice::` rather than failing or
silently skipping -- exactly the designed behavior. Reported in the PR
description.

# Validation

- `lrh validate` -- 0 errors, 20 pre-existing unrelated warnings
- Diff-mode self-review: 0 findings, full local pipeline run clean
- Real workflow run on PR #119 (run 41277094772): success, behaved as
  designed on every stage (see above)

# Follow-up

- `WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION` remains the only
  other open item in WS-CHARTER-SUPPLEMENT-PIPELINE, still blocked on
  its own missing Required Changes section.
- Once this WI merges, WS-CHARTER-SUPPLEMENT-PIPELINE's remaining exit
  criteria depend only on that one item.
