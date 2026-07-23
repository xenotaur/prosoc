---
scenario: object_handover
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-22
---

# Audit: Object Handover

- **Scenario:** `prosoc/scenarios/object_handover/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready, no blocking or should-fix issues found — Card Summary, YAML, and Usage Guide are complete and internally consistent. This re-audit reflects the PR #30 addition of an explicit "Related Scenarios note" to `evaluation_notes` documenting the `related_scenarios`/Table 3 divergence; that note is itself the expected self-documentation the audit checklist calls for, not a defect.

## Findings

### 1. Normative Expectations prose doesn't mirror the must/should/should_not split — suggestion
- **Section/field:** Normative Expectations vs. `expected_behaviors.{must,should,should_not}`
- **Issue:** The prose "Normative Expectations" section presents two flat lists ("Acceptable robot behavior includes" / "Unacceptable behavior includes") without distinguishing `must` (strictly required) from `should`/`should_not` (preferred). For example, "Waiting for a clear indication of grip before releasing the object" reads like a strict requirement and correctly maps to `must` ("not release the object before the human has a secure grip"), while "Approaching the human at a moderate, predictable pace" maps to `should` — but a reader relying only on the prose can't tell the two apart. Content matches the YAML; this is drift in emphasis, not a contradiction. (Carried forward unchanged across prior audits — not addressed by the related_scenarios/cited_in backfill or the new PR #30 evaluation_notes addition, both of which are orthogonal to this section.)
- **Recommended fix:** Optionally annotate the prose list (e.g., "(required)" / "(preferred)" tags) or group must-items first, so a prose-only reader gets the same required/preferred signal as the YAML.

## Source Fidelity

SOURCE cites "P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [161]." Compared against `.claude/skills/_shared/pg_scenarios.md`'s Object Handover entry (Specialized Scenarios section):

| Field | P&G Table 3 | Scenario card | Result |
|---|---|---|---|
| Description | "A robot hands an object to a human" | Servant robot navigates to human, hands over object, recognizes receipt | Match (elaborated) |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Passable space | `geometric_layout: passable space` | Match |
| Scientific Purpose | Interactive navigation | `scientific_purpose: interactive navigation` | Match |
| Robot Role | Servant | `agents.robot.role: servant` | Match |
| Robot Task | Deliver object | `intended_robot_task: deliver the object to the human` | Match |
| Human Behavior | Receive object | `intended_human_behavior: receive the object` | Match |
| Ideal Outcome | Human takes object | "human takes the object from the robot without awkwardness, collision, or dropped object" | Match (elaborated) |
| Related Scenarios | Robot Courier | Card lists `crash_cart` (not `robot_courier`) | Expected divergence — see note below |
| Cited In | [161] | `cited_in: ["161"]`, and Card Summary "Cited In: 161" | Match |

**Note on Related Scenarios divergence:** P&G Table 3 names "Robot Courier" as Object Handover's related scenario, but the card's `related_scenarios` field (and Card Summary) list `crash_cart` instead. `robot_courier` does not exist as an implemented scenario directory in this repo (confirmed — only `crash_cart` is present under `prosoc/scenarios/`), which is the first of the three expected-divergence cases in `prosoc-scenario-audit`'s `audit_checklist.md`: Table 3 names an unimplemented sibling and the card substitutes an implemented scenario it actually discusses in its own prose. As of PR #30, `evaluation_notes` now includes an explicit "Related Scenarios note" paragraph stating exactly this rationale, so the card self-documents the divergence rather than leaving it implicit. Per the checklist, this is expected and not a source-fidelity defect — no mismatch flagged.

## Schema and Charter Compliance

- Single-scenario dry-run distill (`scripts/distill/scenarios --scenario object_handover --dry-run --show-diffs`) reported no diff and no schema validation error (exit 0) — `scenario.yml` is in sync with the embedded YAML in `scenario.md` and validates against `schema.json`.
- `relevant_principles: [P1, P2, P4, P6]` — 4 entries, all valid P0–P9, within the recommended 3–5 range.
- `scenario_usage_guide.quality_metrics: [P2, P4]` — valid P0–P9.
- `expected_behaviors` entries describe kinds of behavior (e.g., "approach at a moderate, predictable pace," "stop at a distance and orientation suitable for a comfortable handover") rather than exact motions or numeric thresholds — no P&G Guideline N6 over-specification found.
- `related_scenarios: [crash_cart]` and `cited_in: ["161"]` are both present in `scenario.yml`, reference an existing scenario directory, and are schema-valid (arrays of strings).

## Completeness

**Scenario Card Summary** (template.md: required for AUDITED):
- Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In — all present and consistent with the YAML and P&G source.

**Scenario Usage Guide** (template.md: required for AUDITED):
- Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria — all present and consistent with the YAML's `scenario_usage_guide` block.

No required fields are blank.
