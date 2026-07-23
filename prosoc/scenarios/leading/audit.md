---
scenario: leading
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-07-22
---

# Audit: Leading

- **Scenario:** `prosoc/scenarios/leading/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready, no issues found

## Findings

No blocking, should-fix, or suggestion findings.

The single-scenario dry-run distiller (`scripts/distill/scenarios --scenario leading
--dry-run --show-diffs`) reported no diff and no schema validation error; `scenario.yml`
also validates cleanly against `schema.json` directly. Prose and embedded YAML are
consistent throughout:

- **Scenario Overview / Social Navigation Context** vs. `intended_robot_task`,
  `intended_human_behavior`, `agents`, `context.social_setting`: robot role
  (`leader`), single following human (`role: follower`, `count: 1`), and the
  pace-matching/turn-signaling/monitoring discussion all agree with the prose
  description of a robot proactively guiding a human through a walking space.
- **Normative Expectations** vs. `expected_behaviors`: every acceptable/unacceptable
  behavior described in prose has a corresponding `must`/`should`/`should_not` entry
  and vice versa (pace matching, turn signaling with lead time, pausing when the
  human falls behind, avoiding fixed-pace/oblivious navigation, avoiding sudden
  turns).
- **`ideal_outcome`** ("person follows the robot to the destination, with the robot
  adapting pace and signaling turns so the human stays with it") matches the prose's
  described good ending.

`expected_behaviors` entries describe kinds of behavior (e.g. "choose a pace
appropriate to the human's demonstrated walking speed," "signal upcoming turns with
enough lead time for the human to follow") rather than exact motions or numeric
thresholds — no over-specification (P&G Guideline N6) concerns.

`relevant_principles` (P1, P3, P6, P8) is a count of 4, all valid P0–P9 IDs, and each
is discussed or clearly implicated in the prose (collision risk, legible route/turn
signaling, monitoring whether the human is keeping up, adapting to the human's
demonstrated capability). `scenario_usage_guide.quality_metrics` (P3, P6) is a valid
subset. `initial_conditions` contains only situational starting values
(`robot_position`, `human_position`) with no duplicate fields restating other YAML
values.

`related_scenarios` (`following`) diverges from P&G Table 3's own citation ("Tour
Guide") because Tour Guide has no implemented scenario directory — this is the
expected, documented divergence pattern per `audit_checklist.md`'s
`related_scenarios` guidance, not a source-fidelity defect. The card's own
`evaluation_notes` explicitly calls this out with a "Related Scenarios note"
paragraph, which is good practice.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Leading" (cited in [50]), which matches the entry in
`.claude/skills/_shared/pg_scenarios.md`:

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
| Related Scenarios | Tour Guide | `related_scenarios` lists `following` rather than Tour Guide, because Tour Guide has no implemented scenario directory under `prosoc/scenarios/`. This is the expected, documented `related_scenarios`/Table 3 divergence pattern (see `audit_checklist.md`), not a source-fidelity defect — the card's own `evaluation_notes` "Related Scenarios note" paragraph (added in PR #30) explicitly explains the substitution. |
| Cited In | [50] | Matches — `cited_in: ["50"]` |

No mismatches found. Source fidelity: confirmed against Table 3.

## Completeness

`scripts/distill/scenarios --scenario leading --dry-run --show-diffs` produced no diff
and no schema errors — `scenario.yml` is in sync with the embedded YAML block and
validates against `schema.json` (confirmed independently with `jsonschema.validate`).

Walking the fields `template.md` marks "Required for AUDITED scenarios":

- **Scenario Card Summary block** — present and complete (Scenario Name, Description,
  Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task,
  Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios,
  Cited In).
- **Scenario Usage Guide — Success Metrics** — present (`SR`, `NoCollisions`, `TTG`),
  matches YAML.
- **Scenario Usage Guide — Quality Metrics** — present (`P3`, `P6`), matches YAML and
  is a sensible subset of `relevant_principles` (`P1`, `P3`, `P6`, `P8`).
- **Scenario Usage Guide — Ideal Outcome** — present, matches YAML `ideal_outcome`.
- **Scenario Usage Guide — Failure Modes** — present, four modes, matches YAML.
- **Scenario Usage Guide — Labeling Criteria** — present, three criteria, matches
  YAML.

No blank required fields remain. Prose (Scenario Overview, Social Navigation Context,
Normative Expectations) is internally consistent with the YAML's
`intended_robot_task`, `intended_human_behavior`, `agents` (leader/follower roles,
count 1), `expected_behaviors`, and `ideal_outcome` — no contradictions or drift
found. `relevant_principles` (4 entries, all P0–P9) and `quality_metrics` are within
the recommended 3–5 range. `expected_behaviors` entries describe kinds of behavior
rather than exact motions or numeric thresholds — no over-specification per P&G
Guideline N6.
