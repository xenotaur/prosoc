---
execution_id: 2026_11_01_10_05_13_WI_CHARTER_SUPPLEMENT_RENDERER_PDF_VERIFICATION_READINESS_REVIEW
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_RENDERER_PDF_VERIFICATION_READINESS_REVIEW)[2026-11-01T10:03:14+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/120
commit:
created_at: 2026-11-01T10:05:13+00:00
agent: claude-code
instruction_source: https://github.com/xenotaur/prosoc/pull/120
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

`/lrh-review-response` pass for PR #120 (readiness-patch for
WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION), addressing 2 Copilot
review comments.

# Result

1. (https://github.com/xenotaur/prosoc/pull/120#discussion_r4435136226)
   "`render.py --pdf` does not save or print the extracted PDF text ...
   Add an explicit `pdftotext -layout` command that writes a text file
   before the manual checks."
   - Presence: present -- Required Change #1 relied on `build_pdf()`'s
     internal extraction, which the CLI never surfaces.
   - Validity: valid -- leaves no artifact for the manual inspection
     steps #2-#3 to actually read.
   - Feasibility: feasible, doc-only fix.
   - Fix: split step 1 into "run `render.py --pdf`" (internal pipeline,
     pandoc/tool/class-file checks, compile) and a new step 2: run
     `pdftotext -layout build/papers/01_charter/rendered.pdf
     build/papers/01_charter/rendered.txt` explicitly, producing a saved
     text file. Steps 3-4 (renumbered from 2-3) now reference
     `rendered.txt` instead of "the extracted PDF text."

2. (https://github.com/xenotaur/prosoc/pull/120#discussion_r4435136237)
   "The 19 listing blocks in `papers/01_charter/golden/rendered.tex`
   contain no non-breaking hyphens (U+2011) or curly double quotes
   (U+201C/U+201D) ... Require an explicit coverage check for each named
   character, and record absent characters as unverified gaps."
   - Presence check (verified directly, not just accepted from the
     comment): parsed the 19 `lstlisting` blocks in
     `papers/01_charter/golden/rendered.tex` and counted occurrences of
     each named character. Confirmed exactly as claimed: en dash
     (U+2013) 1, em dash (U+2014) 3, non-breaking hyphen (U+2011) 0,
     curly double open quote (U+201C) 0, curly double close quote
     (U+201D) 0, curly apostrophe (U+2019) 1.
   - Validity: valid -- a round trip against this source cannot verify
     3 of the 6 named characters as written today.
   - Feasibility: feasible, doc-only fix.
   - Fix: reworded step 4 (was step 3) to require a per-character
     coverage check against `rendered.txt` for each of the 6 named
     characters individually, and to record any character with zero
     occurrences in the source as an unverified gap in the renumbered
     step 6 (file-a-new-WI step), never as a passing check.

# Validation

- `scripts/lint` -- clean
- `scripts/format --check --diff` -- 22 pre-existing, unrelated
  reformats (none touching this change, which is Markdown-only)
- `lrh work-items readiness WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION
  --format md` -- still `prompt_ready: yes` after the edit
- `lrh validate` -- 0 errors, 20 pre-existing unrelated warnings

# Follow-up

None. Pushed directly to the open PR branch. `/lrh-confirm-fixes` will
re-verify against the new HEAD and resolve the two threads before merge.
