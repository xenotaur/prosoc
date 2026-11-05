# Charter supplement second-pass proofread: external review and verification

An external review session proofread the charter supplement PDF produced by
`WS-CHARTER-SUPPLEMENT-PIPELINE` and reported 13 remaining defect categories,
plus a required-testing list and a verification workflow. This document is
the evidence record for that feedback and for the independent verification
performed before filing work items against it. It does not implement any
fix; see `WS-CHARTER-SUPPLEMENT-PROOFREADING` and its work items for that.

**Run date:** 2026-11-04. **Scope:** the regenerated charter supplement PDF
(`papers/01_charter/`), its 9 source cards, and the lifecycle metadata of
every APPROVED card in `src/prosoc/prnc/tasks/` and `src/prosoc/prnc/
contexts/`.

## Independently verified before filing work items

Per this project's standing practice (claims from outside this repo get
checked against the real tree, not accepted on their own authority), the
most consequential and most novel claims were verified directly rather than
trusted:

### 1. Dash glyphs inside `lstlisting` blocks are still visually wrong (confirmed)

`WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX` (closed via PR #124) verified its
`fontenc` fix only via `pdftotext -layout` text extraction. This review
correctly identifies that as an insufficient check: `pdftotext` reports the
`ToUnicode`-mapped character, which can be correct even when the drawn glyph
is wrong.

Verified directly this session by rendering `build/papers/01_charter/
rendered.pdf` to PNG at 600 DPI (`pdftoppm -png -r 600`) and visually
comparing glyphs:

- Page 3, body prose ("the social principles P1–P9."): renders a correct,
  long en dash.
- Page 3, the *same sentence* inside the P0 principle's embedded YAML
  `lstlisting` block (monospace `\ttfamily`, `literatecard` style): renders
  a visibly short, hyphen-like glyph for the same `P1–P9` text, even though
  `pdftotext` extracts the correct en dash from both locations.
- Page 25, `itself—by` and `obstruction—thereby` inside a scenario's
  `lstlisting` block: same pattern for the em dash.

Conclusion: real defect, confirmed by direct pixel inspection, not merely
restated from the review. Feeds
`WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX`.

### 2. Blank `AUDITED:` bullets despite real audit evidence (confirmed, and broader than reported)

The review named 5 cards (as rendered in the PDF): Navigate from Start to
Goal (p. 26), Deliver an Object (p. 29), Routine Service Delivery (p. 32),
Guidance and Docent Operation (p. 36), Emergency High-Urgency Operation
(p. 40).

Verified directly: all 5 have a real `audit.md` on disk with an acceptable
verdict (`ready` or `ready_with_fixes`), yet their `## STATUS` block's
`AUDITED:` bullet reads `—`. A full corpus scan (every `state: APPROVED`
card under `src/prosoc/prnc/tasks/` and `src/prosoc/prnc/contexts/`) found
the same pattern on 3 additional cards not in the supplement's
`sources.txt` (`navigate_lead_agent`, `navigate_follow_agent`,
`public_navigation`) — **8 of 8 APPROVED task/context cards**, not just the
5 visible in this PDF. No lifecycle state is wrong; this is a
provenance-display gap, not a validity problem — `WI-CARD-LIFECYCLE-
VALIDATOR-AUDIT-CHECK` (resolved) deliberately validates against the real
`audit.md` file rather than this bullet, which is exactly what let the
bullet go stale/blank undetected.

Feeds `WI-CHARTER-SUPPLEMENT-AUDIT-EVIDENCE-BACKFILL`.

### 5 and 9. Stale "submitted" language and the incomplete Dragan reference (confirmed)

Grepped directly against `src/prosoc/prnc/charter/charter.md`,
`src/prosoc/prnc/scenarios/single_file_hallway/scenario.md`, and
`src/prosoc/prnc/scenarios/movable_obstruction/scenario.md`: the
`(Francis, submitted)` / "submitted to Frontiers" / "is unpublished" /
"no external literature yet exists that could cite it" language is present
verbatim as reported. `charter.md:484`'s Dragan et al. reference does end
at `*HRI*.` with no volume, pages, or full conference name. Feeds
`WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES`.

## Not independently re-verified in this pass

The remaining items (malformed quote marks p. 15, the Frontal Approach
card's unexplained `Cited In` numbers, the glossary/formal-definition gap,
the P9 emergency-context mischaracterization, status-block spacing, PDF
metadata, final-page layout) are well-specified and plausible but were not
individually re-checked against the live tree before filing work items.
Each work item below carries an instruction to locate and confirm its own
claim before editing, consistent with this project's practice of verifying
rather than assuming.

## Disposition

Filed as `WS-CHARTER-SUPPLEMENT-PROOFREADING` with six work items, grouped
by required judgment level and technical novelty (not a 1:1 mapping to the
review's 13 numbered items — several mechanical fixes are batched
together, and the two items requiring normative/editorial judgment calls
are kept separate from purely mechanical copyediting):

- `WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX`
- `WI-CHARTER-SUPPLEMENT-AUDIT-EVIDENCE-BACKFILL`
- `WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES`
- `WI-CHARTER-SUPPLEMENT-DEFINITIONAL-CONSISTENCY`
- `WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER`
- `WI-CHARTER-SUPPLEMENT-PUBLICATION-POLISH`

`WS-CHARTER-SUPPLEMENT-PIPELINE` is closed out separately (all 10 of its
original work items resolved; this review's findings are new, distinct
scope rather than unfinished work from that workstream).
