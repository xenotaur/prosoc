---
execution_id: 2026_11_01_11_14_40_WI_CHARTER_SUPPLEMENT_RENDERER_DASH_FIX_CLOSEOUT
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_RENDERER_DASH_FIX_CLOSEOUT)[2026-11-01T11:14:40+00:00]
work_item: AD_HOC
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/121
commit: f4e3e7927840b57b01027477f7494e66a5facd82
created_at: 2026-11-01T11:14:40+00:00
agent: claude-code
instruction_source: https://github.com/xenotaur/prosoc/pull/121
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Backfill primary execution record for PR #121: files
`WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX`, a new planning-only work
item, grounded in a real verification finding from
`WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION`. No primary record
was ever minted for this PR (a WI-creation-only PR, not an
`/lrh-implement` run), so this record is created directly as the
primary, per `/lrh-land`'s no-primary backfill path.

# Result

- Added `WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX` to
  `project/work_items/proposed/`: a confirmed PDF-text corruption of
  en dash and em dash inside the charter supplement's `lstlisting`
  blocks (likely cause: missing `\usepackage[T1]{fontenc}` in
  `papers/01_charter/template.tex`), found during a real `pdflatex` +
  `pdftotext -layout` round trip.
- Added it to `WS-CHARTER-SUPPLEMENT-PIPELINE`'s `work_items:` list.
- `/lrh-review-response` (see
  `2026_11_01_11_10_48_WI_CHARTER_SUPPLEMENT_RENDERER_DASH_FIX_REVIEW.md`):
  addressed 1 real Copilot comment -- the WI's own claim that the
  golden file "shouldn't" need regeneration was wrong, since
  `render_paper()` copies `template.tex`'s preamble verbatim into the
  assembled `.tex` (`render.py:240-273`, independently re-verified).
  Reworded to state regeneration is expected unconditionally.
- `/lrh-confirm-fixes` (see
  `2026_11_01_11_11_56_WI_CHARTER_SUPPLEMENT_RENDERER_DASH_FIX_CONFIRM.md`):
  thread classified Clear-satisfied, resolved. Final merge-readiness
  verdict GREEN, re-verified against the actual final HEAD
  `4727b2f2b5d71858672514935125c2216109eaa6` (written in one pass this
  round -- no repeated HEAD-drift cycle this time, per the lesson from
  PR #120's confirm round).
- Merged via `lrh vcs merge --match-head-commit
  4727b2f2b5d71858672514935125c2216109eaa6 --squash`. Verified
  `state: MERGED`, commit `f4e3e7927840b57b01027477f7494e66a5facd82`.

CHAIN-NOTE: `cycles=1; stops=0; gates=[chain-authorization (skip_if_opted_in auto-applied), confirm_fixes_batch-autopilot]; friction=none; note="Clean round -- one real Copilot finding, fixed and independently re-verified against render.py's actual source. Wrote the confirm-fixes record once with the Step 8 results included rather than in two passes, avoiding the repeated HEAD-drift re-verification cycle hit on PR #120's confirm round."`

# Validation

- `lrh validate` -- 0 errors, 20 pre-existing unrelated warnings
- CI: `lint`/`test` SUCCESS, re-verified against the actual final
  merged HEAD `4727b2f2b5d71858672514935125c2216109eaa6`

# Follow-up

`WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX` stays `proposed` -- this is
a WI-creation-only PR and does not resolve its own WI, per the
planning-only-PR convention. It depends on no other WI and can be
picked up by a future `/lrh-execute WS-CHARTER-SUPPLEMENT-PIPELINE`
once an environment with `pdflatex`/`kpsewhich`/the Frontiers class
file is available (now true in this sandbox, per this session's own
TeX Live install).
