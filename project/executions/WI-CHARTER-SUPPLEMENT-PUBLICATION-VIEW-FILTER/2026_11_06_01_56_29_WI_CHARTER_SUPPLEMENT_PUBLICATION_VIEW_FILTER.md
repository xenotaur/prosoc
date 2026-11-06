---
execution_id: 2026_11_06_01_56_29_WI_CHARTER_SUPPLEMENT_PUBLICATION_VIEW_FILTER
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER:WI_CHARTER_SUPPLEMENT_PUBLICATION_VIEW_FILTER)[2026-11-06T01:47:17+00:00]
work_item: WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/131
commit: 0d7294e44ef90904ef7a3e82952b1af01a4a5086
created_at: 2026-11-06T01:56:29+00:00
agent: claude-code
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implements `WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER`: an
investigation/decision item, not mechanical copyediting. Per this
WI's own Risk Notes ("Genuinely ambiguous without the user's input --
do not default to either retain or filter without presenting the
catalog and getting an explicit decision first"), the catalog was
built and presented before any implementation choice was made.

# Result

1. **Cataloged concrete instances** in a freshly regenerated PDF
   (not the proofread's summary alone): 31 model-name mentions, 11
   WI/PR identifiers (e.g. `(WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES)`,
   `(PR #79)`), 3 `render_sections.py` mentions, 3 `src/prosoc/...`
   repo-path mentions, and 3 specific internal-session-only phrases
   (quoted in the PR body and this record's Follow-up section).
2. **Presented the retain-vs-filter choice to the user** with the full
   catalog, as two concrete options with their respective trade-offs.
   **User's decision: retain.** Rationale given and confirmed: the
   normative-card corpus's own stated purpose (per
   `papers/01_charter/template.tex`'s intro prose, "show the
   expressiveness and scope of the system") is a transparent,
   auditable snapshot, not a polished publication-only artifact;
   suppressing provenance would also contradict the renderer's own
   reproducibility goal.
3. **Documented the decision durably** in `docs/paper-supplements.md`,
   as a new "## Publication View and Internal Provenance" section
   between "## Golden Comparison" and "## Validation" -- including the
   standing rule that any future paper-specific suppression mechanism
   must stay in that paper's own directory, never generalized into the
   shared `prosoc.nca.utils.papers.render` module (consistent with
   that document's existing "Renderer Shim" boundary and this WI's own
   Non-Goals).
4. **Reworded the 3 reader-meaningless phrases regardless of the
   decision** (Required Change #5, which applies "regardless of which
   option is chosen"):
   - `frontal_approach/scenario.md`: dropped an EDITED bullet's
     internal "(was an internal-tooling attribution string, 'Prompt
     to ChatGPT 5.2')" detail -> "for publication clarity".
   - `frontal_approach/scenario.md`'s `evaluation_notes` (an embedded
     fenced-YAML field rendered verbatim into the PDF as a literatecard
     listing): "This is expected per the related_scenarios convention
     (prosoc-scenario-audit's audit_checklist.md), not a
     source-fidelity gap." -> "This reflects a deliberate divergence
     from P&G Table 3's single-citation convention, consistent with how
     this corpus treats closely related scenario variants, not an
     inconsistency." -- more self-contained than the original, not
     just shorter.
   - `single_file_hallway/scenario.md`: dropped an EDITED bullet's "as
     previously guessed in internal scenario-sourcing notes" clause,
     keeping the substantive correction ("not extrapolated from P&G's
     Figure 7").

Regenerated `frontal_approach/scenario.yml` via `scripts/distill/scenarios`
(the `evaluation_notes` fix lives inside an embedded fenced-YAML
field). Confirmed neither touched scenario is a member of
`src/prosoc/manifests/sample_packet/manifest.yml` (its only scenario
member is `intersection_gesture_wait`, unaffected), so no packet
golden-file regeneration was needed this time. Regenerated
`papers/01_charter/golden/rendered.tex` via `render.py`, hand-reviewed
(exactly the 4 intended hunks: 1 doc section + 3 wording fixes + their
2 new EDITED bullets), and confirmed with a real `pdflatex` build.

# Validation

- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
  -- 344 tests, `OK (skipped=1)`.
- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- `scripts/lint` -- all checks passed.
- `PYTHONPATH="$(pwd)/src" scripts/distill/scenarios --dry-run
  --show-diffs` -- confirmed the exact expected single-field diff
  before applying; 0 differences after.
- `PYTHONPATH="$(pwd)/src" python -m prosoc.nca.packet.cli
  src/prosoc/manifests/sample_packet/manifest.yml --check` -- exits 0
  silently, confirming the packet golden file is genuinely unaffected
  (applying the lesson from a prior WI's own packet-golden-file
  cascade miss).
- A real `PYTHONPATH="$(pwd)/src" papers/01_charter/render.py --pdf`
  build succeeded (46 pages); whitespace-normalized `pdftotext -layout`
  extraction directly confirms all 3 old phrases have zero matches and
  both new replacement sentences are present.
- `papers/01_charter/render.py` (no `--pdf`) regenerate, diffed against
  the accepted golden file -- empty, byte-identical.
- Diff-mode `/lrh-self-review` dispatched before this PR was opened
  (see the companion `_SELFREVIEW` record): clean result, no blocking
  findings, independently re-verified.

# Follow-up

None blocking. The 3 reader-meaningless phrases cataloged, quoted
verbatim for the record:
1. `"(was an internal-tooling attribution string, "Prompt to ChatGPT 5.2")"`
2. `"per the related_scenarios convention (prosoc-scenario-audit's audit_checklist.md), not a source-fidelity gap."`
3. `"as previously guessed in internal scenario-sourcing notes"`

**Noted for future awareness** (out of scope for this WI, per its own
scope being `papers/01_charter` specifically): the self-review
subagent found the phrase "source-fidelity gap" still present in ~12
other scenario cards not currently in `papers/01_charter/sources.txt`.
If a future paper ever pulls any of those cards in, the same rewording
should be applied there too.
