---
scenario: single_file_hallway
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-07-21
---

# Audit: Single File Hallway

- **Scenario:** `prosoc/scenarios/single_file_hallway/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready for AUDITED with minor fixes — no blocking issues; only minor
  prose-completeness gaps remain.

## Findings

### 1. `expected_behaviors.must` items not echoed anywhere in prose — should-fix
- **Section/field:** Scenario Overview (prose) vs. `expected_behaviors.must`
- **Issue:** `scenario.md` has no "Normative Expectations" or "Social Navigation
  Context" section (both optional per `template.md`, but recommended). The Scenario
  Overview does summarize the `should` list in natural language ("The robot must
  anticipate the conflict and take initiative—through signaling, yielding, or
  negotiation—to prevent deadlock or discomfort"), but the two safety-critical `must`
  items — "maintain a safe physical distance from the human" and "avoid entering the
  hallway simultaneously with the human" — are not stated anywhere in prose; they
  exist only inside the embedded YAML/`scenario.yml`. This is a one-sided claim per
  the audit checklist (behavior specified in YAML but absent from prose).
- **Recommended fix:** Add a short "Normative Expectations" section (as
  `robot_overtaking`'s card has) that states the required minimum behaviors —
  maintaining safe distance and not entering the hallway simultaneously with the
  human — in natural language, alongside the already-covered `should` guidance.

### 2. "Cited In" gap note's phrasing could be clearer that the gap is permanent — suggestion
- **Section/field:** Scenario Card Summary "Remaining gaps" note vs. Source Fidelity
- **Issue:** The Card Summary block still carries a self-flagged note: "**Remaining
  gaps:** Cited In — should-fill-in-now." Per
  `../../../.claude/skills/_shared/pg_scenarios.md`, `single_file_hallway` corresponds
  to the Figure 7 "Narrow Hallway" sketch, which — unlike full Table 3 entries — has no
  citation-index data available at all ("they do not have full Table 3 metadata"). This
  is a genuine, permanent gap rather than an oversight: there is no P&G Table 3/Figure 7
  citation index to draw from, so no future editing pass can "fill in" this field from
  the available reference material. The current "should-fill-in-now" phrasing reads as
  an actionable to-do, which overstates what's actually possible.
- **Recommended fix:** Either reword the gap note to reflect that Cited In is currently
  unfillable from available sources (e.g. "reasonably blank — no citation index exists
  for Figure-7-derived scenarios"), or remove the note entirely if the omission is
  considered acceptable as a permanent, source-driven limitation for this
  Figure-7-derived scenario.

## Source Fidelity

SOURCE is explicitly cited as "Principles and Guidelines for Evaluating Social Robot
Navigation (P&G paper)" — a checkable source in principle. However, per
`../../../.claude/skills/_shared/pg_scenarios.md`, "Single File Hallway" is **not**
one of the 18 named entries in P&G Table 3. The reference file's "Additional Scenarios
(Figure 7, not in Table 3)" section states:

> The `single_file_hallway` scenario in the repo corresponds to the **Narrow Hallway**
> figure [in Figure 7]... If implementing these, note that they do not have full Table
> 3 metadata and should be extrapolated carefully from the paper's descriptions and
> Figure 7.

Comparing the card against what's available:
- **Correspondence to Narrow Hallway (Figure 7):** The card's description — "a hallway
  that is too narrow for safe and comfortable passing... single-file passage" — is
  consistent with `pg_scenarios.md`'s one-line gloss: "single-file passage in a narrow
  corridor." No contradiction found.
- **No Table 3 metadata to compare against:** Because Narrow Hallway has no full Table
  3 entry (no Scientific Purpose, Robot Task, Human Behavior, Ideal Outcome, or Cited
  In fields listed in `pg_scenarios.md` beyond the one-line description), a
  field-by-field fidelity check like the one possible for Table 3 scenarios cannot be
  performed for `scientific_purpose`, `intended_robot_task`, `intended_human_behavior`,
  `ideal_outcome`, or `cited_in`.

**Source fidelity: partially checkable.** The high-level correspondence to the Figure
7 "Narrow Hallway" concept holds, and the authored fields (scientific_purpose,
geometric_layout, intended_robot_task, intended_human_behavior, ideal_outcome) remain
internally plausible and consistent with the Figure 7 gloss and the card's own
Overview/Discussion prose, but they cannot be verified against Table-3-style ground
truth because none exists for this scenario. Verifying deeper fidelity would require
reading the P&G paper's Figure 7 discussion directly (not provided as `--paper` input
for this audit) — this audit does not fabricate that comparison. In particular,
`cited_in` has no ground-truth citation index available for this scenario at all (see
Finding 2) — this is a permanent, source-driven limitation, not a gap this audit
expects to close on a future pass.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary:** Complete except **Cited In**, which is blank and
  self-flagged in a "Remaining gaps" note (see Finding 2) — reasonably blank, and
  permanently so, given no citation data exists for this Figure-7-derived scenario in
  the available reference material.
- **Scenario Usage Guide — Success Metrics:** Complete (SR, NoCollisions,
  DeadlockFree).
- **Scenario Usage Guide — Quality Metrics:** Complete (P3, P5, P7 — consistent with
  `relevant_principles` [P1, P3, P5, P7]).
- **Scenario Usage Guide — Ideal Outcome:** Complete, present both in the YAML
  `ideal_outcome` field and the Card Summary/Usage Guide prose.
- **Scenario Usage Guide — Failure Modes:** Complete (three concrete failure modes).
- **Scenario Usage Guide — Labeling Criteria:** Complete (three concrete,
  data-recognizable criteria).

No required fields are blank aside from the permanently-unfillable Cited In noted
above. The optional "Normative Expectations" prose section remains absent (see
Finding 1).

## Re-audit Note

This is a fresh point-in-time re-audit (2026-07-21). The scenario was not edited since
the 2026-07-20 audit; `scripts/distill/scenarios --scenario single_file_hallway
--dry-run --show-diffs` reports no diff and no schema errors. Findings, verdict, and
counts are unchanged from the prior audit — the "Cited In" gap remains classified as a
genuine, permanent gap rather than an oversight to be resolved.
