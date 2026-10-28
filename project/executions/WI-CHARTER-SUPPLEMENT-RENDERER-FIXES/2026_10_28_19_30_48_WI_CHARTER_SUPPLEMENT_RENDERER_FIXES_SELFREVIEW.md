---
execution_id: 2026_10_28_19_30_48_WI_CHARTER_SUPPLEMENT_RENDERER_FIXES_SELFREVIEW
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-RENDERER-FIXES:WI_CHARTER_SUPPLEMENT_RENDERER_FIXES_SELFREVIEW)[2026-10-28T19:30:48+00:00]
work_item: WI-CHARTER-SUPPLEMENT-RENDERER-FIXES
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/115
commit: 8e1a84a800de87c28179a9700b87896207e694db
created_at: 2026-10-28T19:30:48+00:00
agent: claude_app
instruction_source: diff-mode review of the WI-CHARTER-SUPPLEMENT-RENDERER-FIXES implementation, run late (after push) per /lrh-implement Step 7.5 -- a process slip, caught and corrected before Step 4 landing
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Diff-mode review of `WI-CHARTER-SUPPLEMENT-RENDERER-FIXES`'s
implementation (PR #115), per `/lrh-implement` Step 7.5. Run as a
cold-context `general-purpose` subagent dispatch, equivalent to
`/lrh-self-review`'s own dispatch procedure. **Process note:** this
review should have run before Step 8's `gh pr create`, per the
skill's own ordering; it ran after the branch was already pushed and
the PR already open. Caught and corrected before proceeding to Step 4
(landing) — no uncommitted/unreviewed work went further than this.

# Result

Verdict: Clean — minor nitpicks only, no blocking issues.

The subagent empirically tested the Lua filter against several edge
cases via raw `pandoc` invocations (not just reasoning about the
code): multi-digit numbers (works), a bare "N." with no following
text (filter's length guard correctly no-ops, doesn't crash), a
double leading number "1. 2. Purpose" (only the first is stripped —
not a real charter pattern), and critically: a bolded or linked
heading number (`## **1.** Purpose`, `## [1.](#x) Purpose`) — the
filter's `el.content[1].t == "Str"` check fails because pandoc parses
these as `Strong`/`Link` wrapping the `Str`, not a bare `Str`, so the
number is **not** stripped in that case.

I independently re-verified this top finding myself (not
re-delegated): ran `pandoc -f markdown -t native` on `## **1.**
Purpose` and confirmed the AST is `[Strong [Str "1."], Space, Str
"Purpose"]` — exactly as reported — then confirmed the filter leaves
it unstripped. Also confirmed via `grep` that no heading in the real
`src/prosoc/prnc/charter/charter.md` is bold/link-wrapped, so this is
a latent fragility, not a currently live bug. Per the project's own
guidance against adding untested handling for scenarios that can't
currently happen, fixed by adding a one-line code comment documenting
the limitation (commit `47a9f41`) rather than adding speculative
Strong/Link-unwrapping logic.

The subagent also confirmed: the `literate=` table's codepoints match
real characters present in the charter-paper sources' fenced YAML
blocks; `render.py`'s `--lua-filter` scoping is correctly CHARTER-only
regardless of what a caller passes for other keys; `render_paper`
correctly omits the flag with no crash when the filter file is
absent; and the new tests exercise all of this except the three edge
cases above (acceptable, since none are live).

# Validation

- Subagent ran `PYTHONPATH="$(pwd)/src" scripts/test` (304 tests, OK),
  `scripts/lint` (passed), and `lrh validate` (0 errors, 20
  pre-existing warnings, none touching this PR's files).
- Subagent ran empirical `pandoc` tests against the real Lua filter
  for 6 edge cases, with AST dumps (`pandoc -f markdown -t native`)
  backing the Strong/Link-wrapping finding.
- I independently re-ran the AST dump and the filter check myself for
  the top finding before accepting it, and confirmed no live charter
  heading triggers it via `grep -n "^## "
  src/prosoc/prnc/charter/charter.md`.

# Follow-up

None blocking. The documented Strong/Link-wrapping limitation is a
latent fragility, not a live bug — no further action unless a future
charter edit bolds or links a heading number, at which point this
filter's comment points at the gap.
