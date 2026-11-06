---
execution_id: 2026_11_06_02_30_12_WI_CHARTER_SUPPLEMENT_PUBLICATION_POLISH
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-PUBLICATION-POLISH:WI_CHARTER_SUPPLEMENT_PUBLICATION_POLISH)[2026-11-06T02:29:44+00:00]
work_item: WI-CHARTER-SUPPLEMENT-PUBLICATION-POLISH
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/132
commit: 71009327ca63460813aa0c58f3dfcbc29845aec7
created_at: 2026-11-06T02:30:12+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-PUBLICATION-POLISH.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implements `WI-CHARTER-SUPPLEMENT-PUBLICATION-POLISH`: two independent
proofreading-pass findings, a visible spacing inconsistency in the
rendered PDF and missing PDF document-properties metadata. Both are
mechanical, low-risk fixes with no normative-content changes.

# Result

1. **Status-block spacing fix.** Investigated the reported visible
   spacing mismatch between task-card and scenario-card STATUS blocks
   in the rendered PDF. Root cause, found by diffing the generated
   LaTeX fragments byte-for-byte
   (`build/papers/01_charter/fragments/navigate_point_to_point.tex` vs.
   `.../frontal_approach.tex`): task cards' STATUS bullets end their
   Markdown source lines with a trailing double space (a Markdown hard
   line break), which Pandoc renders as a trailing `\\` inside the
   LaTeX `\item` -- scenario cards' bullets carry no such trailing
   whitespace. Not a "tight list vs. loose list" issue as the WI's own
   prose first suggested (both families already use `\tightlist`);
   confirmed via `grep -c '  $'` that only the task family had the
   defect, not the context family. Stripped the trailing `  ` from all
   6 STATUS-block bullets in all 4 task cards (`navigate_point_to_point`,
   `deliver_object`, `navigate_follow_agent`, `navigate_lead_agent` --
   all 4 for corpus-wide consistency, even though only the first two are
   members of this paper's `sources.txt`), and added a matching new
   `**EDITED:**` bullet to each documenting the fix. Visually confirmed
   via a `pdftoppm`-rendered PNG of PDF page 27
   (`navigate_point_to_point`'s STATUS block) that spacing now matches
   the scenario-card style.
2. **PDF metadata.** Added a `\hypersetup{pdftitle=...,pdfauthor=...,
   pdfsubject=...,pdfkeywords=...,pdflang=...}` block to
   `papers/01_charter/template.tex`, placed immediately before
   `\begin{document}` -- `hyperref` is already loaded earlier in that
   file (line 22), so no new package was needed. Kept distinct from the
   Frontiers template's own separate guidance (near `\maketitle`) to
   omit the *typeset* title/author block, which concerns visible
   content, not invisible PDF document properties. Verified via
   `pdfinfo` on a real `--pdf` build that Title/Subject/Keywords/Author
   are now populated; `pdflang` (`/Lang`) could not be independently
   confirmed with the tooling available in this environment (no
   `pypdf`/`qpdf`/`pdftk`), though no hyperref warning about the
   `pdflang` key appeared in the build log.

Checked whether `navigate_lead_agent`'s `sample_packet` manifest
membership required `packet.golden.yml` regeneration (per this
session's own `feedback_packet_manifest_golden_cascade.md` lesson from
an earlier WI this session): `python -m prosoc.nca.packet.cli
.../manifest.yml --check` exits 0 with no drift, since STATUS-block
prose isn't part of the packet's distilled YAML content -- no
regeneration needed. Regenerated `papers/01_charter/golden/rendered.tex`
via `render.py` (no `--pdf`) and hand-reviewed the diff: exactly the
intended `\hypersetup` block plus the trailing-`\\` removals and new
EDITED bullets in the two in-sources.txt task cards -- nothing else
changed.

# Validation

- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
  -- 344 tests, `OK (skipped=1)`.
- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- `scripts/lint` -- all checks passed.
- `PYTHONPATH="$(pwd)/src" scripts/distill/tasks --dry-run --show-diffs`
  -- no diff output; STATUS-block prose isn't part of distilled task
  YAML.
- `PYTHONPATH="$(pwd)/src" python -m prosoc.nca.packet.cli
  src/prosoc/manifests/sample_packet/manifest.yml --check` -- exits 0
  silently, confirming the packet golden file is genuinely unaffected
  despite `navigate_lead_agent` being a manifest member.
- Ran the specific pre-existing regression test the WI's own Risk Notes
  named by class
  (`tests.nca.utils.papers.render_test.TestListCollapseRegression.test_no_collapsed_list_after_known_labels`)
  directly, not just via the full suite -- still passes, confirming this
  fix did not reintroduce the prior collapsed-list defect.
- A real `PYTHONPATH="$(pwd)/src" papers/01_charter/render.py --pdf`
  build succeeded; `pdfinfo` confirmed Title/Subject/Keywords/Author
  populated as expected.
- `pdftoppm -png -r 150 -f 27 -l 27 ...` rendered PDF page 27
  directly to a PNG for visual spacing confirmation.
- `papers/01_charter/render.py` (no `--pdf`) regenerate, diffed against
  the accepted golden file before acceptance -- confirmed the diff
  maps exactly to the intended source changes, nothing else.
- Diff-mode `/lrh-self-review` dispatched before this PR was opened
  (see the companion `_SELFREVIEW` record): clean result, no blocking
  findings, independently re-verified.

# Follow-up

None blocking. `pdflang`/`/Lang` could not be independently verified
with the tooling available in this environment (no
`pypdf`/`qpdf`/`pdftk`); the `hypersetup` key was set correctly and no
hyperref warning appeared in the build log, but this is a known,
disclosed verification gap rather than a confirmed pass.
