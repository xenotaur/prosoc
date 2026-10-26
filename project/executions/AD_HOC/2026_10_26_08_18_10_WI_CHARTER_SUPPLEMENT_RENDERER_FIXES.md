---
execution_id: 2026_10_26_08_18_10_WI_CHARTER_SUPPLEMENT_RENDERER_FIXES
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_RENDERER_FIXES)[2026-10-26T08:17:36+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-10-26T08:18:10+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-RENDERER-FIXES.md
session_transcript: pending
---

# Summary

Create `WI-CHARTER-SUPPLEMENT-RENDERER-FIXES`, planning a Lua filter for
charter heading double-numbering, `literate=` Unicode mappings for the
`literatecard` `lstlisting` style, and identifier code-span normalization.

# Result

Wrote `project/work_items/proposed/WI-CHARTER-SUPPLEMENT-RENDERER-FIXES.md`
(`status: proposed`), citing the exact template/renderer locations
confirmed structurally by the audit (no `literate=` table; headings
manually numbered then renumbered by the Frontiers class). No source
files were edited by this item — it is planning only.

# Validation

- `lrh prompt check-execution --slug wi-charter-supplement-renderer-fixes`
  — no prior record.
- `lrh validate` — 0 errors.

# Follow-up

Implementation is deferred to a later PR against this work item,
including the PDF-level verification the audit flagged as unconfirmable
in a sandbox without `pdflatex`. This item stays `proposed` at this PR's
closeout.
