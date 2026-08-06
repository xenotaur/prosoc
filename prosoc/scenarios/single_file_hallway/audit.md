---
family: scenarios
card: single_file_hallway
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-02
---

# Audit: Single File Hallway

- **Card:** `prosoc/scenarios/single_file_hallway/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — finding carries forward
  unchanged since no content changed)
- **Verdict:** Ready for `AUDITED`, no blocking or should-fix issues found

## Findings

### 1. "Cited In" gap note's phrasing could be clearer that the gap is permanent — suggestion (carried forward from 2026-07-22)
- **Section/field:** Scenario Card Summary "Remaining gaps" note vs.
  Source Fidelity
- **Issue:** The Card Summary carries a self-flagged note: "**Remaining
  gaps:** Cited In — should-fill-in-now." Per
  `.claude/skills/_shared/pg_scenarios.md`, `single_file_hallway`
  corresponds to the Figure 7 "Narrow Hallway" sketch, which — unlike
  full Table 3 entries — has no citation-index data available at all. This
  is a genuine, permanent gap, not an oversight: no future editing pass
  can "fill in" this field from available reference material. The
  "should-fill-in-now" phrasing reads as an actionable to-do, overstating
  what's actually possible.
- **Recommended fix:** Reword the gap note to reflect that Cited In is
  currently unfillable from available sources, or remove the note
  entirely as a permanent, source-driven limitation. Not required for
  `AUDITED`.

No other findings. Both `must`-level behaviors are already explicitly
stated in the "Normative Expectations" prose (no must-level-prose-gap
pattern here — this was closed by PR #31, per the 2026-07-22 audit's
Re-audit Note). Both `related_scenarios` entries (`frontal_approach`,
`movable_obstruction`) reciprocate the link back to `single_file_hallway`
— no one-way cross-reference gap.

## Source Fidelity

SOURCE cites "Principles and Guidelines for Evaluating Social Robot
Navigation (P&G paper)" generically — this scenario is **not** one of
the 18 named entries in P&G Table 3. Per
`.claude/skills/_shared/pg_scenarios.md`'s "Additional Scenarios (Figure
7, not in Table 3)" section, `single_file_hallway` corresponds to the
**Narrow Hallway** figure, which has no full Table 3 metadata.

The card's description ("a hallway too narrow for safe and comfortable
passing... single-file passage") is consistent with `pg_scenarios.md`'s
one-line gloss ("single-file passage in a narrow corridor"). No
contradiction found. A field-by-field fidelity check (as done for
Table-3-sourced cards) is not possible here since Figure 7 entries carry
no Scientific Purpose / Robot Task / Human Behavior / Ideal Outcome /
Cited In ground truth to compare against — this audit does not fabricate
that comparison. `cited_in` is absent from the YAML entirely (not even a
placeholder), which is correct given no citation index exists for this
scenario.

## Completeness

Scenario Card Summary: complete except **Cited In**, which is blank and
self-flagged (Finding 1) — reasonably and permanently blank, given no
citation data exists for this Figure-7-derived scenario.

Scenario Usage Guide: Success Metrics (SR, NoCollisions, DeadlockFree),
Quality Metrics (P3, P5, P7 — consistent with `relevant_principles` [P1,
P3, P5, P7]), Ideal Outcome, Failure Modes, and Labeling Criteria all
present and non-trivial.

No required fields are blank aside from the permanently-unfillable Cited
In. `scripts/distill/scenarios --scenario single_file_hallway --dry-run
--show-diffs` reported no diff, confirming `scenario.md` and
`scenario.yml` are in sync.
