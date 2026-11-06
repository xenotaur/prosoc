---
id: WS-CHARTER-SUPPLEMENT-PROOFREADING
kind: planning_node
title: "Charter Supplementary-Material Second-Pass Proofreading"
status: resolved
stage: closed
origin: follow_up
summary: "Resolve the defects found by a second-pass external proofread of the charter supplement PDF produced by WS-CHARTER-SUPPLEMENT-PIPELINE: a visually-incorrect dash glyph regression inside lstlisting blocks, blank audit-evidence bullets, stale/incomplete citation and status language, charter definitional inconsistencies, a publication-view provenance decision, and remaining layout/metadata polish."
related_focus: []
related_roadmap: []
related_design: []
work_items:
  - WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX
  - WI-CHARTER-SUPPLEMENT-AUDIT-EVIDENCE-BACKFILL
  - WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES
  - WI-CHARTER-SUPPLEMENT-DEFINITIONAL-CONSISTENCY
  - WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER
  - WI-CHARTER-SUPPLEMENT-PUBLICATION-POLISH
evidence:
  - project/audits/2026-11-04_charter_supplement_second_pass_proofread.md
exit_criteria:
  - "The lstlisting-block en/em dash glyphs render correctly when the PDF is visually inspected (image-rendered, not pdftotext-only), with a regression check that can catch a visually-wrong-but-correctly-mapped glyph"
  - "Every APPROVED task/context card's AUDITED: bullet reflects its real audit.md evidence, and scripts/validate/status fails (not warns) on APPROVED without acceptable audit evidence"
  - "No remaining malformed quote marks, unexplained Cited In numbers, or stale submitted/unpublished language describing the accompanying article in the generated supplement"
  - "The glossary definition of prosocial behavior and the high-urgency context's P9 framing are each internally consistent with the charter's own formal definitions"
  - "An explicit, documented decision governs how much internal development/provenance history appears in the publication view, with no provenance deleted from the canonical cards themselves"
  - "Status-block spacing is consistent across card families, and the compiled PDF carries author-controlled Title/Author/Subject/Keywords/language metadata where the Frontiers template supports it"
---

# Charter Supplementary-Material Second-Pass Proofreading

## Purpose

Coordinates the resolution of a second-pass external proofread's findings
against the charter supplement PDF that `WS-CHARTER-SUPPLEMENT-PIPELINE`
produced and closed out. That workstream's own exit criteria (rendering
correctness, build reproducibility, CI coverage) are fully met and it is
closed separately; this workstream covers a distinct, newly-surfaced
concern -- publication content readiness -- including one genuine
regression in previously-closed renderer work (the dash-glyph defect) that
this workstream's own evidence record verified directly rather than taking
on the reviewer's word alone.

## Scope

Six work items, grouped by required judgment level rather than a 1:1
mapping to the proofread's 13 numbered findings:

1. **Listing dash-glyph fix** -- the highest-priority item: a real,
   independently-verified regression in `WI-CHARTER-SUPPLEMENT-RENDERER-
   DASH-FIX`'s closed-out fix, needing real investigation (not just a
   mapping tweak) and a new image-based regression check.
2. **Audit-evidence backfill** -- mechanical once scoped: project real,
   already-passing audit evidence into blank `AUDITED:` bullets across all
   8 affected cards (not just the 5 visible in this supplement), plus
   confirm/close any remaining validator gap.
3. **Copyedit fixes** -- mechanical, low-judgment source-text corrections:
   quote marks, citation labeling, stale submission-status language,
   grammar, reference completeness.
4. **Definitional consistency** -- two items needing charter-semantic
   judgment (glossary vs. formal prosocial-behavior definition; P9's role
   in emergency contexts), kept separate from the mechanical copyedit item
   so the resulting wording gets explicit review.
5. **Publication-view filter decision** -- an investigation/decision item:
   how much internal repository-development metadata belongs in a
   publication-facing supplement, with no deletion from the canonical
   cards either way.
6. **Remaining polish** -- status-block spacing normalization and
   author-controlled PDF metadata; explicitly *not* forcing a final-page
   layout change, per the reviewer's own guidance.

## Non-Goals

- Does not reopen or modify `WS-CHARTER-SUPPLEMENT-PIPELINE`'s own closed
  scope (rendering correctness, CI, build reproducibility) -- that
  workstream's exit criteria were independently confirmed met before this
  one was filed.
- Does not distort the final page's typography merely to eliminate its
  roughly-half-empty layout.
- Does not undertake a risky Frontiers-template rewrite for tagged-PDF/
  accessibility support if that is a publisher-controlled production step.

## Dependencies / Order

No hard dependencies between the six work items. Recommended order:
listing dash-glyph fix and audit-evidence backfill first (both already
fully scoped by direct verification); then copyedit fixes and definitional
consistency; then the publication-view filter decision (its outcome may
inform wording choices in the earlier text-editing items, but doesn't
block them); then remaining polish last, as the lowest-risk, most
independent item.
