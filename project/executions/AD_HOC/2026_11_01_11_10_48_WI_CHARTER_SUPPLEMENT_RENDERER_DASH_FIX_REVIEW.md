---
execution_id: 2026_11_01_11_10_48_WI_CHARTER_SUPPLEMENT_RENDERER_DASH_FIX_REVIEW
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_RENDERER_DASH_FIX_REVIEW)[2026-11-01T11:10:30+00:00]
work_item: AD_HOC
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/121
commit: f4e3e7927840b57b01027477f7494e66a5facd82
created_at: 2026-11-01T11:10:48+00:00
agent: claude-code
instruction_source: https://github.com/xenotaur/prosoc/pull/121
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

`/lrh-review-response` pass for PR #121 (new
WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX), addressing one Copilot
review comment
(https://github.com/xenotaur/prosoc/pull/121#discussion_r4435351521).

# Result

Comment: "Adding `\usepackage[T1]{fontenc}` to the template
necessarily changes the assembled `rendered.tex`: `render_paper()`
copies the template and replaces its card placeholders
(`src/prosoc/nca/utils/papers/render.py:248-276`). Pandoc's card
fragments may remain unchanged, but the preamble will differ from the
golden file. Please expect that change and require a human-reviewed
golden update rather than expecting unchanged `.tex` output."

Triage:
- Presence check: present -- the WI's Scope and Acceptance Criteria
  said the fix "shouldn't" change `.tex` output and the golden file
  should be regenerated "only if" it does.
- Validity check: valid -- re-read `render_paper()` directly
  (`src/prosoc/nca/utils/papers/render.py:240-273`): it reads
  `template_file.read_text(...)` wholesale into `rendered`, then only
  substitutes card placeholders via `replace_placeholder`. The
  preamble (everything outside placeholders, including any
  `\usepackage` line) passes through verbatim. Confirmed the WI's
  "shouldn't change .tex output" claim was simply wrong.
- Feasibility check: feasible, doc-only wording fix.

Fix: reworded the Scope bullet, one Acceptance Criteria bullet, and
the matching Acceptance Criteria body bullet to state the golden file
regeneration is expected unconditionally (not "only if"), with human
review confirming the diff is exactly the new preamble line and no
card-content changes.

# Validation

- `lrh validate` -- 0 errors, 20 pre-existing unrelated warnings

# Follow-up

None. Pushed directly to the open PR branch. `/lrh-confirm-fixes` will
re-verify against the new HEAD and resolve the thread before merge.
