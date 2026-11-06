---
resolution: "Implemented and merged in PR #131 (commit 0d7294e44ef90904ef7a3e82952b1af01a4a5086) -- cataloged actual instances of internal-development content in the compiled PDF and presented the retain-vs-filter choice to the user, who chose retain: the corpus's own stated purpose is a transparent, auditable snapshot, not a polished publication-only artifact. Documented this decision and its rationale durably in docs/paper-supplements.md. Regardless of the decision, reworded 3 specific phrases that referenced internal development context meaninglessly to an external reader."
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER
title: "Decide and implement how much internal development/provenance history belongs in the publication-facing charter supplement"
type: investigation
status: resolved
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PROOFREADING
depends_on: []
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_lifecycle_state_change]
acceptance:
  - "An explicit decision is recorded: either retain internal development metadata in the publication view intentionally (with stated rationale), or add a paper-specific filter/marker mechanism that omits it from the supplement while preserving it in the repository"
  - "No provenance is deleted from the canonical cards themselves -- any suppression is publication-view-only"
  - "Any renderer-level filtering mechanism stays generic/reusable, with paper-specific suppression rules living in the paper-specific layer (papers/01_charter/), not hardcoded into the shared renderer"
  - "At minimum, development commentary meaningless to a publication reader (e.g. references to something having been 'previously guessed in internal scenario-sourcing notes' or 'not a source-fidelity gap') is addressed by whichever option is chosen"
required_evidence: [manual_review, test_output]
artifacts_expected:
  - src/prosoc/nca/utils/papers/render.py
  - papers/01_charter/
---

## Summary
The charter supplement PDF exposes substantial repository-development
metadata to a reader who has no context for it: model names (Claude,
ChatGPT), work-item identifiers, PR numbers, script filenames
(`render_sections.py`), audit-checklist filenames, internal corrective
history, and repository file paths embedded in reader-facing prose. A
second-pass external proofread flagged this as needing an explicit
publication-view decision, not a silent fix in either direction.

## Problem / Context
This is an investigation/decision item, not yet a scoped implementation
-- the right answer depends on a design choice this project hasn't made
yet: whether the charter supplement is meant to read as a clean,
standalone publication artifact (favoring suppression of internal
provenance) or as a transparent, auditable snapshot of a living
normative-card corpus (favoring retention, since the cards' own stated
purpose per `template.tex`'s intro text is to "show the expressiveness
and scope of the system," not present polished, publication-only prose).

Specific instances were not independently re-verified page-by-page in
this planning pass; the executing session should locate concrete examples
in the regenerated PDF (model names, WI/PR identifiers, script/filenames,
internal corrective-history language, repo paths) before deciding.

### Duplication search
- In-repo: no existing proposal or work item addresses a publication-view
  filtering layer for the paper-supplement renderer
  (`src/prosoc/nca/utils/papers/render.py`); `docs/paper-supplements.md`
  documents the renderer as generic/reusable across future papers, which
  is directly relevant to keeping any filter mechanism paper-specific
  rather than baked into the shared renderer.
- Recommendation: Proceed.

### Demand search
- Directly requested by the second-pass proofread (this session,
  2026-11-04).
- Recommendation: Proceed.

## Scope
First, make the retain-vs-filter decision explicitly (with the user's
input, since this affects the supplement's editorial character, not just
its correctness). Then implement whichever option is chosen.

## Required Changes
1. Catalog concrete instances of internal-only content in the current
   regenerated PDF (model names, WI/PR identifiers, script filenames,
   internal corrective-history language, repo paths in prose) -- ground
   the decision in what's actually present, not the proofread's summary
   alone.
2. Present the retain-vs-filter choice to the user with the cataloged
   instances, and record the decision (and its rationale) in this work
   item's execution record regardless of which way it goes.
3. If retaining: document why in a durable location (e.g. a short note in
   `docs/paper-supplements.md` or the charter supplement's own intro
   text), so this doesn't get re-litigated as a "bug" in a future
   proofread.
4. If filtering: design and implement a paper-specific suppression
   mechanism -- e.g. a marker convention in the source Markdown/YAML that
   a paper-specific post-processing step in `papers/01_charter/` (not the
   shared `prosoc.nca.utils.papers.render` module) can act on. Preserve
   the underlying content in the canonical cards unconditionally; only
   the publication view is affected.
5. At minimum, regardless of which option is chosen, replace development
   commentary that is meaningless to a publication reader (the reviewer's
   examples: something "previously guessed in internal scenario-sourcing
   notes," or "not a source-fidelity gap") with reader-appropriate
   wording or omit it from the view.

## Non-Goals
- Does not delete any provenance from the canonical cards in the
  repository -- whatever is decided, the repository's own copy stays
  complete.
- Does not generalize paper-specific suppression logic into the shared
  renderer (`prosoc.nca.utils.papers.render`) -- keep it in the
  paper-specific layer, consistent with `docs/paper-supplements.md`'s own
  stated design ("The template remains paper-specific. Do not generalize
  publisher-specific formatting into the shared renderer until more than
  one paper needs the same behavior").

## Acceptance Criteria
- A recorded, explicit decision with rationale.
- If filtering was chosen: a working, paper-specific suppression
  mechanism, verified against the regenerated PDF, with the canonical
  cards' own content unchanged.
- If retaining was chosen: durable documentation of why, so it isn't
  re-flagged as an unreviewed bug later.
- Golden file regenerated with human-reviewed diff if supplement content
  or the renderer changed.
- `scripts/test` / `lrh validate` pass.

## Validation
- `scripts/test`
- `lrh validate`
- Manual review of the regenerated PDF against the catalog from step 1.

## Risk Notes
- Genuinely ambiguous without the user's input -- do not default to
  either retain or filter without presenting the catalog and getting an
  explicit decision first.

## Dependencies / Order
None technically, but the decision made here may inform wording choices
in `WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES` and
`WI-CHARTER-SUPPLEMENT-DEFINITIONAL-CONSISTENCY` -- recommended to run
this one's decision step early, even if full implementation lands later.
