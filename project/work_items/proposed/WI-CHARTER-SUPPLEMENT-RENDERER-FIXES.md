---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-RENDERER-FIXES
title: "Fix charter heading double-numbering and Unicode loss in the renderer/template"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
depends_on: []
blocked_by: []
expected_actions: [create_file, edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, modify_ci_pipeline]
acceptance:
  - "Generated LaTeX contains no authored heading-number prefix (prefix-free numbered heading commands)"
  - "literatecard lstlisting style's literate= table covers en dash, em dash, non-breaking hyphen, curly double quotes, and the curly apostrophe, verified against pandoc's generated .tex output"
  - "The real pdflatex+pdftotext round-trip check is deferred to WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION (no pdflatex available in this landing session's sandbox; see Risk Notes)"
  - "lrh validate / scripts/test pass"
required_evidence: [manual_review, lrh_validate, test_output]
artifacts_expected:
  - papers/01_charter/template.tex
  - src/prosoc/nca/utils/papers/render.py
  - papers/01_charter/*.lua
---

## Summary
Fix charter heading double-numbering and Unicode punctuation loss in the
Frontiers supplement renderer/template, and normalize machine-identifier
formatting to code spans.

## Problem / Context
Confirmed: `## 1. Purpose...` renders as `\subsection{1. Purpose...}`,
which the Frontiers class numbers again. Separately, the `literatecard`
`lstlisting` style has no `literate=` table, and en/em dashes sit inside
those blocks. See `project/audits/2026-10-26_charter_supplement_pipeline_audit.md`.

### Duplication search
- In-repo: no existing filter/mapping; confirmed by direct inspection of
  `template.tex` and the renderer.
- Recommendation: Proceed.

### Demand search
- None found.
- Recommendation: No action.

## Scope
- Add a small Pandoc Lua filter, scoped to the charter render path, that
  strips a leading authored `N. ` from heading text before LaTeX emission.
- Add `literate=` Unicode mappings to the `literatecard` style for en
  dash, em dash, non-breaking hyphen, curly double quotes, and the curly
  apostrophe `’` (U+2019) — already present inside the fenced YAML at
  `single_file_hallway/scenario.md:154` — and cover all of these in the
  PDF round-trip checks.
- Normalize `Context ID:`/`Applies To Tasks:` prose to code spans (coordinate
  with WI-CHARTER-SUPPLEMENT-SOURCE-FIXES if it already touches these lines).

## Required Changes
1. New Lua filter under `papers/01_charter/` (or `src/prosoc/nca/utils/papers/`),
   wired into the charter's Pandoc invocation only.
2. `papers/01_charter/template.tex:53-60` — add `literate=` to `literatecard`.
3. Renderer change for identifier code-span normalization, if not already
   source-level per WI-CHARTER-SUPPLEMENT-SOURCE-FIXES.

## Non-Goals
- Does not do a broad regex rewrite of arbitrary generated LaTeX.
- Does not regenerate the golden file (see WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN).

## Acceptance Criteria
- Generated LaTeX for the charter contains no authored heading-number
  prefix — the Lua filter strips it before LaTeX emission, so the
  `.tex` source is prefix-free; only the Frontiers class's automatic
  counter (applied at compile time) numbers the heading.
- The `literatecard` `lstlisting` style's `literate=` table covers en
  dash, em dash, non-breaking hyphen, curly double quotes, and the
  curly apostrophe, verified by inspecting pandoc's generated `.tex`
  output directly (not a real `pdflatex` compile — see Risk Notes).
- `lrh validate` / `scripts/test` pass.

## Validation
- `scripts/test`
- `lrh validate`
- `papers/01_charter/render.py`
- Direct inspection of pandoc's generated `.tex` output for the Lua
  filter's heading-prefix stripping and the `literate=` mappings.

## Risk Notes
- A PDF toolchain may not be available in every sandbox (confirmed absent
  in two of the audit's own sessions, and in this WI's own landing
  session — a `brew install --cask basictex` attempt failed because the
  cask's installer requires interactive `sudo`, unavailable here). Per
  explicit user decision, the real `pdflatex`+`pdftotext` round-trip
  check (the compiled PDF showing each heading's number exactly once,
  and the Unicode characters surviving the round trip) is deferred to
  `WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION`, filed as a
  follow-up, rather than blocking this WI or the rest of the workstream
  on TeX-toolchain availability.
