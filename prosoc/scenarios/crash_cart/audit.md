---
scenario: crash_cart
verdict: ready_with_fixes
blocking: 0
should_fix: 3
suggestion: 1
audited: 2026-07-05
---

# Audit: Crash Cart

- **Scenario:** `prosoc/scenarios/crash_cart/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Missing "Scenario Card Summary" section — should-fix
- **Section/field:** `scenario.md` structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Card Summary block
- **Issue:** `scenario.md` has no `## Scenario Card Summary` section (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In). The equivalent content exists only inside the embedded YAML block and prose narrative, not as the dedicated summary the template structures for AUDITED scenarios.
- **Recommended fix:** Add a `## Scenario Card Summary` section populated from existing values (Robot Role: Leader; Robot Task: deliver medical product urgently; Human Behavior: bystanders yield / recipient receives; Ideal Outcome; Related Scenarios: Food Delivery, Object Handover; Cited In: this article).

### 2. Missing standalone "Scenario Usage Guide" prose section — should-fix
- **Section/field:** `scenario.md` structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Usage Guide section
- **Issue:** Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria exist only inside the YAML's `scenario_usage_guide` block, not as the dedicated prose section template.md requires for AUDITED readiness.
- **Recommended fix:** Add a `## Scenario Usage Guide` section with `### Success Metrics`, `### Quality Metrics`, `### Ideal Outcome`, `### Failure Modes`, `### Labeling Criteria` subsections, restating the YAML content in prose form.

### 3. Bystander awareness stated inconsistently across fields — should-fix
- **Section/field:** `initial_conditions.human_positions` vs. `intended_human_behavior` / `expected_behaviors` / Normative Expectations
- **Issue:** `initial_conditions.human_positions` states bystanders are "unaware of the specific urgency," yet `intended_human_behavior` assumes "bystanders yield to the passing robot," and both the prose Normative Expectations and `expected_behaviors.should` ("signal urgent status clearly to bystanders...so they can accommodate it") presuppose bystanders can and do perceive the robot's signaled urgency and respond accordingly. As written, it's ambiguous whether "unaware of the specific urgency" means bystanders start out unaware (and are expected to become aware via the robot's signaling, which is consistent) or that they remain unaware throughout (which would contradict the yield expectation). Likely just an underspecified initial condition rather than an outright contradiction.
- **Recommended fix:** Clarify `initial_conditions.human_positions` to state bystanders begin unaware of the *specific* delivery's urgency but are expected to update upon perceiving the robot's signaling — this is probably the intended meaning but should be made explicit to avoid ambiguity.

### 4. Bystander count is an unstated elaboration — suggestion
- **Section/field:** Scenario Overview / Social Navigation Context prose vs. `agents.humans[0].count: 3`
- **Issue:** Prose never states a specific bystander count (uses "bystanders," "pedestrians" generically); YAML picks `count: 3`. This is drift rather than contradiction — a reasonable concretization for simulation setup, but worth a human sanity check since prose gives no basis to confirm 3 specifically (vs. 1, 2, or more).
- **Recommended fix:** Either state an approximate bystander count in prose (e.g., "a small number of bystanders (2–3)") to ground the YAML's `count: 3`, or note in `evaluation_notes` that the count is a reasonable default subject to variation.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Crash Cart" entry, cited in "this article." Compared against `../../../.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | scenario.yml / scenario.md | Match? |
|---|---|---|---|
| Description | Robot delivering a medical product indoors | Overview: robot delivers urgent medical product indoors | Yes |
| Physical Env | Indoor | `context.environment.type: indoor` | Yes |
| Geometric Layout | Passable space | `geometric_layout: passable space` | Yes |
| Scientific Purpose | Interactive navigation | `scientific_purpose: interactive navigation` | Yes |
| Robot Role | Leader | `agents.robot.role: leader` | Yes |
| Robot Task | Deliver object | `intended_robot_task: deliver the medical product urgently` | Yes (elaborated with urgency, consistent with description) |
| Human Behavior | Receive object | `intended_human_behavior: ...recipient receives the medical product upon arrival` | Yes |
| Ideal Outcome | Delivery of medicine | `ideal_outcome: delivery of medicine to the recipient promptly and without collision or unsafe maneuvers` | Yes (elaborated, consistent) |
| Related Scenarios | Food Delivery | Notes section: "related to Object Handover... and to Food Delivery" | Yes |
| Cited In | this article | Status block: "cited in this article" | Yes |

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

- **Scenario Card Summary fields** — should-fill-in-now. No dedicated section exists in `scenario.md`, but every underlying value (name, description, scientific purpose, physical environment, geometric layout, robot role, robot task, human behavior, ideal outcome, related scenarios, cited-in) is already present in prose or YAML. See Finding 1.
- **Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)** — should-fill-in-now as a prose section. All content already exists in the YAML's `scenario_usage_guide` block (SR, NoCollisions, TTG; P3, P8; failure modes list; labeling criteria list). See Finding 2.
- **Related Scenarios / Cited In** — should-fill-in-now once Finding 1's summary section is added; content (Food Delivery, Object Handover, "this article") is already written in the Notes and Status sections and just needs to be surfaced in the summary block.
