---
scenario: leading
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-21
---

# Audit: Leading

- **Scenario:** `prosoc/scenarios/leading/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready, no blocking or should-fix issues found

## Findings

### 1. `related_scenarios` omits Table 3's stated related scenario — suggestion
- **Section/field:** `related_scenarios` (YAML) vs. P&G Table 3 "Related Scenarios" and the card's own "Notes for Scenario Designers and Evaluators" section
- **Issue:** `related_scenarios` now lists only `following`. Table 3 lists "Tour Guide" as Leading's related scenario, and the card's Notes/`evaluation_notes` also discuss *Tour Guide* as "a specialized, extended variant... not separately defined in Table 3." `following` is a reasonable and schema-correct choice — `related_scenarios` must reference an implemented scenario directory per `schema.json`'s description, and `tour_guide` does not exist as a directory under `prosoc/scenarios/` (confirmed by directory listing) — but this is worth noting since Table 3's own related-scenario pointer isn't yet represented.
- **Recommended fix:** No action required now. If/when a `tour_guide` scenario is drafted, add it to `related_scenarios`.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Leading" (cited in [50]), which matches the entry in `.claude/skills/_shared/pg_scenarios.md`:

| Table 3 field | Reference value | Scenario card |
|---|---|---|
| Description | A robot leads a person | Matches — Overview: "a robot in a leader role whose task is to guide a human through a walking space" |
| Physical Env | Generic | Matches — `context.environment.type: generic` |
| Geometric Layout | Walking space | Matches — `geometric_layout: walking space` |
| Scientific Purpose | Joint navigation | Matches — `scientific_purpose: joint navigation` |
| Robot Role | Leader | Matches — `agents.robot.role: leader` |
| Robot Task | Lead human | Matches — `intended_robot_task: lead the human to a destination` |
| Human Behavior | Follow robot | Matches — `intended_human_behavior: follow the robot, tracking its path and pace` |
| Ideal Outcome | Person follows robot | Matches — `ideal_outcome: person follows the robot to the destination, with the robot adapting pace and signaling turns so the human stays with it` |
| Related Scenarios | Tour Guide | Partial — formal `related_scenarios` field now populated but lists `following` rather than Tour Guide, since the latter is not yet an implemented scenario directory (see Finding 1) |
| Cited In | [50] | Matches — formal `cited_in: ["50"]` now present, matching the Status block's SOURCE line and Table 3 |

No mismatches found beyond the related_scenarios note above. Source fidelity: confirmed against Table 3.

## Completeness

`scripts/distill/scenarios --scenario leading --dry-run --show-diffs` produced no diff and no schema errors — `scenario.yml` is in sync with the embedded YAML and validates against `schema.json`.

Walking the fields `template.md` marks "Required for AUDITED scenarios":

- **Scenario Card Summary block** — present and complete (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In). Related Scenarios / Cited In — previously flagged as the sole gap — are now filled in (`following`; `50`).
- **Scenario Usage Guide — Success Metrics** — present (`SR`, `NoCollisions`, `TTG`), matches YAML.
- **Scenario Usage Guide — Quality Metrics** — present (`P3`, `P6`), matches YAML and is a sensible subset of `relevant_principles` (`P1`, `P3`, `P6`, `P8`).
- **Scenario Usage Guide — Ideal Outcome** — present, matches YAML `ideal_outcome`.
- **Scenario Usage Guide — Failure Modes** — present, four modes, matches YAML.
- **Scenario Usage Guide — Labeling Criteria** — present, three criteria, matches YAML.

No blank required fields remain. Prose (Scenario Overview, Social Navigation Context, Normative Expectations) is internally consistent with the YAML's `intended_robot_task`, `intended_human_behavior`, `agents` (leader/follower roles, count 1), `expected_behaviors`, and `ideal_outcome` — no contradictions or drift found. `relevant_principles` (4 entries, all P0–P9) and `quality_metrics` are within the recommended 3–5 range. `expected_behaviors` entries describe kinds of behavior ("choose a pace appropriate to the human's demonstrated walking speed," "signal upcoming turns with enough lead time") rather than exact motions or numeric thresholds — no over-specification per P&G Guideline N6.

`initial_conditions` contains only `robot_position` and `human_position` (situational starting conditions), with no duplicate fields restating other YAML values — no redundancy findings for this scenario.
