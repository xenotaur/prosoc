---
scenario: narrow_doorway
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-05
---

# Audit: Narrow Doorway

- **Scenario:** `prosoc/scenarios/narrow_doorway/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Ready, no blocking issues found

## Findings

### 1. "Related Scenarios" and "Cited In" are not surfaced in a Scenario Card Summary section — suggestion
- **Section/field:** Scenario Card Summary (absent as a distinct section) vs. Notes for Scenario Designers and Evaluators
- **Issue:** `template.md` calls for a `## Scenario Card Summary` block (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) as "Required for AUDITED scenarios." This card does not include that block as a standalone section; instead, its content is distributed across the Status block, Scenario Overview prose, the YAML block, and a "Notes for Scenario Designers and Evaluators" section (which does cover Related Scenarios informally: Narrow Arch, Blind Corner, Entering/Exiting Room).
- **Recommended fix:** Before final AUDITED promotion, consider adding an explicit "Scenario Card Summary" section consolidating these fields for at-a-glance review, per `template.md`'s structure — though all the underlying content is present elsewhere in the card, so this is a formatting/completeness nit rather than a substantive gap.

### 2. `expected_behaviors.should` mixes a graded/comparative claim ("proceed decisively and without hesitation") — suggestion
- **Section/field:** `expected_behaviors.should` vs. P&G Guideline N6 (over-specification)
- **Issue:** The entries are phrased as kinds of behavior ("recognize... adjust approach speed," "yield clearly," "proceed decisively... without hesitation") rather than exact motions or numeric thresholds, so this is not a blocking over-specification violation. However, "proceed decisively and without hesitation" edges toward prescribing manner/style rather than outcome; it is defensible as legibility guidance but worth a second look.
- **Recommended fix:** No change required; flagging only as a minor style note. If tightened, could be rephrased as "proceed without ambiguity about intent" to keep focus on legibility (the underlying principle, P3) rather than motion style.

## Source Fidelity

SOURCE cites "P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [126]." This matches a real Table 3 entry in `../../../.claude/skills/_shared/pg_scenarios.md`, under Doorway Scenarios → **Narrow Doorway**. Comparison:

| Field | P&G Table 3 (`pg_scenarios.md`) | This scenario | Match? |
|---|---|---|---|
| Description | Robot and human at a narrow doorway (room and door) | Robot and human pedestrian approach a narrow doorway from opposite directions, single-file passage | Yes |
| Physical Env | Indoor | `context.environment.type: indoor` | Yes |
| Geometric Layout | Room and door | `geometric_layout: room and door` | Yes |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Yes |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B through the doorway` | Yes |
| Human Behavior | Navigate B to A | `intended_human_behavior: navigate from B to A through the doorway` | Yes |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot and human sequence through the doorway one at a time without collision or obstruction` | Yes |
| Related Scenarios | Narrow Arch | Noted in "Notes for Scenario Designers and Evaluators" as a related geometric variant | Yes |
| Cited In | [126] | SOURCE field cites [126] | Yes |

**Source fidelity: checked against P&G Table 3 — full match, no mismatches found.** All physical description, purpose, layout, roles, task, and ideal-outcome fields are consistent with the canonical Table 3 entry, and the "Related Scenarios" cross-reference (Narrow Arch) is preserved. The scenario also reasonably extrapolates additional detail (bottleneck sequencing dynamics, comparison to Blind Corner and Frontal Approach) beyond what Table 3 specifies, which is appropriate elaboration rather than a deviation.

## Completeness

Walking `template.md`'s "Required for AUDITED scenarios" fields:

**Scenario Card Summary** (content present, though not consolidated into a single named section — see Finding 1):
- Scenario Name — present ("Narrow Doorway")
- Scenario Description — present (Scenario Overview section + YAML `summary`)
- Scientific Purpose — present (`scientific_purpose: pedestrian interaction`)
- Physical Environment — present (`context.environment.type: indoor`)
- Geometric Layout — present (`geometric_layout: room and door`)
- Robot Role — present (`agents.robot.role: navigating_agent`)
- Robot Task / Human Behavior — present (`intended_robot_task`, `intended_human_behavior`)
- Success Metrics / Quality Metrics — present (`scenario_usage_guide.success_metrics`: SR, NoCollisions; `quality_metrics`: P3, P4)
- Ideal Outcome — present (`ideal_outcome` field)
- Related Scenarios — present, informally, in "Notes for Scenario Designers and Evaluators" (Narrow Arch, Blind Corner, Entering Room, Exiting Room) — reasonably complete, though not in a formal "Related Scenarios:" line
- Cited In — present (SOURCE field: "cited in [126]")

**Scenario Usage Guide:**
- Success Metrics — present (SR, NoCollisions), though only in YAML, not restated as prose under a `### Success Metrics` heading — **reasonably blank** as a prose subsection since the YAML values are clear and unambiguous; low priority to duplicate.
- Quality Metrics — present (P3, P4) — same note as above.
- Ideal Outcome — present (`ideal_outcome` field, echoed in Scenario Overview prose).
- Failure Modes — present (4 detailed entries in YAML), not restated as prose — **reasonably blank** as a prose subsection, values are already clear.
- Labeling Criteria — present (3 entries in YAML) — **reasonably blank** as a prose subsection, same reasoning.

No blank fields were found that are "should probably be filled in now" — all template-required content is present either in prose or in the YAML, and the only gap is a structural/formatting one (no consolidated Scenario Card Summary heading), captured as Finding 1 (suggestion-level, not blocking).

This card is in noticeably better shape than a typical DRAFTED scenario: schema-valid, principle count within guidance (4, within 3–5), no P9/invented-principle issues, dry-run distiller check produced no diff, and full Table 3 fidelity. The main remaining gap before EDITED/AUDITED promotion is cosmetic section consolidation, which is a human editorial choice.
