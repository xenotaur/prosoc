---
execution_id: 2026_10_26_08_18_10_WI_CHARTER_SUPPLEMENT_PDF_BUILD
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_PDF_BUILD)[2026-10-26T08:17:37+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-10-26T08:18:10+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-PDF-BUILD.md
session_transcript: pending
---

# Summary

Create `WI-CHARTER-SUPPLEMENT-PDF-BUILD`, planning a reproducible PDF
build entry point (fail-fast `pdflatex`, outline fonts, `pdftotext`
checks, pinned/checked Pandoc version) for the charter supplement.

# Result

Wrote `project/work_items/proposed/WI-CHARTER-SUPPLEMENT-PDF-BUILD.md`
(`status: proposed`), grounded in the audit's confirmation that
`render.py`'s `main()` currently rejects any arguments and that Pandoc
version drift (3.10.1 vs. 2.9.2 observed across two sandboxes) is a live
reproducibility risk. No source files were edited by this item — it is
planning only.

# Validation

- `lrh prompt check-execution --slug wi-charter-supplement-pdf-build` —
  no prior record.
- `lrh validate` — 0 errors.

# Follow-up

Implementation is deferred to a later PR against this work item,
including the licensing question on Frontiers publisher class files. This
item stays `proposed` at this PR's closeout.
