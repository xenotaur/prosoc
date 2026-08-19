---
execution_id: 2026_08_14_01_21_24_WI_NCA_PRNC_PACKAGE_LAYOUT
prompt_id: PROMPT(WI-NCA-PRNC-PACKAGE-LAYOUT:WI_NCA_PRNC_PACKAGE_LAYOUT)[2026-08-14T01:21:10+00:00]
work_item: WI-NCA-PRNC-PACKAGE-LAYOUT
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/95
commit: a9ea0c35c59e4907a60d552b673add3147533533
created_at: 2026-08-14T01:21:24+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-NCA-PRNC-PACKAGE-LAYOUT.md
session_transcript: claude-app:f087f2be-5992-4711-b12b-40cebb7e8305
---

# Summary

Implements `WI-NCA-PRNC-PACKAGE-LAYOUT` (implementing `PROP-NCA-PRNC-PACKAGE-LAYOUT`,
merged via PR #85/#91): restructures prosoc's flat `prosoc/{packet,literate,
auditor,utils,charter,scenarios,tasks,contexts,constitutions,manifests}/`
layout into a `src/`-layout single top-level package, separating verified
domain-agnostic engine code (`prosoc.nca`) from PRNC-specific data
(`prosoc.prnc`/`prosoc.constitutions`/`prosoc.manifests`), with
`pyproject.toml` rewired to build a complete single-wheel distribution.

# Result

Executed all 8 Required Changes from the work item:

1-2. `git mv` moved engine code into `src/prosoc/nca/{literate,auditor,
   packet,utils}/` (utils/ wholesale, including `utils/experiments/` and
   `utils/papers/`) and PRNC data into `src/prosoc/prnc/{charter,scenarios,
   tasks,contexts}/`, `src/prosoc/constitutions/`, `src/prosoc/manifests/`.
   No `src/prosoc/experiments/` was created (correctly distinct from the
   unrelated root-level `<root>/experiments/`, left untouched).
3. Fixed `packet/loader.py`'s imports and `REPO_ROOT` depth
   (`parents[2]` → `parents[4]`), and `utils/cards/validate_status.py`'s
   matching imports — plus a much larger scope than the work item
   anticipated: a comprehensive grep found ~20 additional files with
   stale `prosoc.X` absolute imports or self-referencing sibling imports
   (including 5 function-local imports a first pass missed, caught by
   actually running the test suite and by this PR's own self-review).
4. Rewrote `pyproject.toml`: `package-dir`, `packages.find.where`,
   `include-package-data`, and per-subpackage `package-data` globs for
   all six families (previously only `charter`'s 3 files shipped) —
   verified via a real `python -m build --wheel` whose file list was
   diffed against `git ls-files` for zero missing/extraneous files.
5. Restructured `tests/` to mirror the new layout; running the suite
   surfaced and fixed 3 real test-side path bugs (a doubled
   `tests/tests/` path from a depth-miscount, and two hardcoded
   old-flat-layout fixture paths) plus one real source bug (a stale
   golden fixture whose card `path` fields needed regenerating after the
   move — sha256 hashes unchanged, confirming only paths moved).
6. Updated `.github/workflows/packet.yml`/`charter.yml` path triggers
   (and switched their install step to `pip install -e .`, since the old
   flat layout made `prosoc` importable via bare cwd-on-path with no
   install needed — that assumption breaks under `src/`); `scripts/
   distill/*`, `scripts/validate/*`, `scripts/lint`, `scripts/format`,
   `scripts/check`, `scripts/clean`, `scripts/assemble` module/path
   references; the 6 `.claude/skills/_shared/audit_checklists/*.md`
   files.
7. Updated `papers/01_charter/sources.txt`'s 9 paths and `render.py`'s
   `sys.path` hack for the new layout; re-ran the renderer and confirmed
   **byte-identical** output against `papers/01_charter/golden/
   rendered.tex`.
8. Full validation green (see below) before every push.

Additionally fixed `README.md` and `docs/paper-supplements.md` (the
latter landed on `main` via PR #93 after this branch started, requiring a
rebase to pick up) — both document this exact package layout and were
squarely on-topic, unlike the many other stale-path references
deliberately left untouched (card content, historical `project/`
execution records, and skill docs not named in Required Changes step 6 —
out of scope and, for card content, explicitly forbidden to edit).

A `/lrh-self-review` diff-mode pass (cold-context subagent + mandatory
independent re-verification of its top finding) ran the full validation
suite itself and found one real, confirmed class of issue: ~13 files with
stale `prosoc.<family>` path references left in docstrings/comments
(not live imports) that the earlier import-fixing pass missed since it
only searched live `from`/`import` statements. All fixed; one
pre-existing, unrelated issue (`utils/cards/validator.py`'s header
comment, already wrong on `main`) was correctly left alone per the
subagent's own recommendation. See
`project/executions/AD_HOC/2026_08_14_01_18_39_WI_NCA_PRNC_PACKAGE_LAYOUT_SELFREVIEW.md`.

One known, pre-existing gap unrelated to this move: `openai`/
`python-dotenv` aren't declared as dependencies, so 2 test modules fail
to import in a bare venv — confirmed this already fails identically on
`main` before this branch.

# Validation

- `lrh validate` — 0 errors, 0 warnings
- `scripts/test` (`python -m unittest discover tests "*_test.py"`) —
  259/259 passing
- `scripts/lint` — all checks passed
- `scripts/format --check --diff` — 22 pre-existing files flagged, exact
  same count/files as `main` (confirmed via direct comparison); zero new
  formatting issues from this branch's own edits (2 were caught and
  fixed during implementation)
- `scripts/build` — wheel contains all six families' data (161 files),
  verified against `git ls-files`
- `scripts/assemble` against `src/prosoc/manifests/sample_packet/
  manifest.yml --check` — exit 0, confirming the regenerated golden
  matches (member card `sha256` hashes unchanged, only `path` fields
  updated)
- `papers/01_charter/render.py` — output byte-identical to
  `papers/01_charter/golden/rendered.tex`
- Content-hash diff of all 161 old-path files vs. new-path files — only
  the 19 intentionally-edited files (18 import-path fixes + 1 regenerated
  golden fixture) differ; zero drift in any card `.md`/`.yml`/`.json`
- `/lrh-self-review` diff-mode pass — see the linked `_SELFREVIEW` record
  above for its own independently-run validation suite

# Follow-up

- `/lrh-review-response` and `/lrh-confirm-fixes` as PR #95 collects
  review activity; continue honoring the fleet-wide no-manual-Codex/
  Copilot-retrigger policy (self-review substitution) for any further
  verification rounds.
- `/lrh-closeout` once PR #95 merges.
- Possible follow-up (not filed, flagged for the user to decide): many
  `.md` files across `project/` execution history, other `.claude/
  skills/*.md` not named in this work item's Required Changes, and card
  `audit.md`/prose still reference the old flat `prosoc/...` paths in
  incidental prose. None were touched here — out of this work item's
  explicit scope, and several (card content, historical records) are
  inappropriate to edit regardless.
