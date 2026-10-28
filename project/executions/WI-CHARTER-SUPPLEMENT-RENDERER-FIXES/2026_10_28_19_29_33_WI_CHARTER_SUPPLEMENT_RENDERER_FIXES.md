---
execution_id: 2026_10_28_19_29_33_WI_CHARTER_SUPPLEMENT_RENDERER_FIXES
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-RENDERER-FIXES:WI_CHARTER_SUPPLEMENT_RENDERER_FIXES)[2026-10-28T19:03:09+00:00]
work_item: WI-CHARTER-SUPPLEMENT-RENDERER-FIXES
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/115
commit: 8e1a84a800de87c28179a9700b87896207e694db
created_at: 2026-10-28T19:29:33+00:00
agent: claude_app
instruction_source: user /lrh-execute WS-CHARTER-SUPPLEMENT-PIPELINE invocation, resolved to WI-CHARTER-SUPPLEMENT-RENDERER-FIXES
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Resolved via `/lrh-execute WS-CHARTER-SUPPLEMENT-PIPELINE` to the next
ready work item. Fixes the charter supplement renderer's heading
double-numbering and Unicode dash/quote loss inside `lstlisting`
blocks, per the 2026-10-26 charter supplement pipeline audit.

# Result

1. Added `papers/01_charter/strip_heading_numbers.lua`, a Pandoc Lua
   filter that strips a leading authored `N. ` token from heading
   text before LaTeX emission. Wired into the charter's own Pandoc
   invocation only, via a new optional `lua_filter` parameter threaded
   through `build_pandoc_args` → `render_fragment` → `render_paper` in
   `src/prosoc/nca/utils/papers/render.py` (`render_paper` looks for
   the filter file by a fixed name in `paper_dir` and only passes it
   through when present; `build_pandoc_args` only ever applies it for
   `key == "CHARTER"`).
2. Added a `literate=` table to the `literatecard` `lstlisting` style
   in `papers/01_charter/template.tex`, covering en dash, em dash,
   non-breaking hyphen, curly double quotes, and the curly apostrophe
   — verified the exact codepoints (U+2013, U+2014, U+2011, U+201C,
   U+201D, U+2019) against the actual characters used.
3. Confirmed (via `git grep` and a Python scan of every in-paper
   source's fenced YAML blocks) that `WI-CHARTER-SUPPLEMENT-SOURCE-FIXES`
   already code-span-normalized every `Context ID:`/`Applies To Tasks:`
   line for cards actually included in this paper — no further
   action needed.
4. Per explicit user decision (`pdflatex` unavailable in this sandbox;
   a `brew install --cask basictex` attempt failed because the cask's
   installer needs interactive `sudo`), narrowed this WI's own
   acceptance criteria to what's verifiable at the pandoc/`.tex`-source
   level and filed the real `pdflatex`+`pdftotext` round-trip check as
   a new backlog item, `WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION`
   (`depends_on` this WI). Both the narrowed acceptance criteria and
   the new backlog WI already landed on `main` directly (pure planning
   edits, via the detached-HEAD-from-origin/main workaround since
   `main` is locked in the primary worktree) before this WI's own
   implementation commit.

# Validation

- Ran the actual Lua filter against representative headings via raw
  `pandoc` invocations before wiring it in: confirmed it strips
  single/double-digit `N. ` prefixes, leaves unnumbered headings
  (`### Normative Statement`) untouched, and leaves a dotted
  sub-number (`4.1`, which doesn't occur in the real charter but was
  tested defensively) untouched.
- Ran the real end-to-end charter paper render
  (`python3 papers/01_charter/render.py`, real `pandoc`, no `pdflatex`
  needed for this step) and inspected the generated
  `build/papers/01_charter/fragments/charter.tex`: every `## N. ...`
  heading renders prefix-free (`\subsection{Purpose of This
  Charter}`, not `\subsection{1. Purpose...}`).
- Scanned every in-paper source's fenced YAML blocks for the target
  Unicode characters and confirmed they survive verbatim into the
  pandoc-generated `.tex` fragments: en dash in `charter.md`, em dash
  (×3) in `movable_obstruction/scenario.md`, curly apostrophe in
  `single_file_hallway/scenario.md`.
- `PYTHONPATH="$(pwd)/src" scripts/test` — 304 tests, OK.
- `scripts/lint` — all checks passed.
- `lrh validate` — 0 errors, 20 pre-existing warnings.
- New tests added: `TestLuaFilterIntegration` (3 tests against real
  `pandoc`, skip-guarded if `pandoc`/the filter file are absent),
  `test_charter_adds_lua_filter_when_given`,
  `test_charter_omits_lua_filter_when_not_given`,
  `test_non_charter_never_gets_lua_filter_even_if_given`,
  `test_render_paper_passes_lua_filter_only_for_charter_when_present`,
  `test_render_paper_omits_lua_filter_when_file_absent`.

# Follow-up

The real `pdflatex`+`pdftotext` compile-and-extract round trip is
deferred to `WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION` (already
filed on `main`), which needs an environment with a working `pdflatex`
(with outline fonts) — not available in this sandbox.
