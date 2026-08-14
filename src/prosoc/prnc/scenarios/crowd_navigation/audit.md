---
family: scenarios
card: crowd_navigation
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-08-02
---

# Audit: Crowd Navigation

- **Card:** `prosoc/scenarios/crowd_navigation/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — and is superseded by this
  pass. The prior audit's sole finding, a stale STATUS-block `EDITED`
  provenance line, is a repo-wide artifact of that same mechanical
  migration touching every card without updating each one's provenance
  trail — not re-flagged here, consistent with how this session treated
  the identical pattern on `entering_room`.)
- **Verdict:** Ready, no issues found

## Findings

No findings. `scenario.yml` is in sync with `scenario.md` (confirmed via
`scripts/distill/scenarios --scenario crowd_navigation --dry-run
--show-diffs`, no diff). This card's Normative Expectations prose is
notably thorough: unlike several sibling cards audited this session, both
`expected_behaviors.must` items ("avoid collision with any individual,"
"not become indefinitely stuck") are explicitly covered in the
"Unacceptable behavior" bullets ("Colliding with or forcing evasive
action...," "Freezing indefinitely or taking excessively wide
detours...") — no must-level prose gap here.

Prose/YAML cross-check (Scenario Overview / Social Navigation Context /
Normative Expectations against `intended_robot_task`,
`intended_human_behavior`, `agents`, `expected_behaviors`,
`ideal_outcome`) found no contradictions or drift — all describe the same
many-agent, low-predictability crossing task with 10 milling pedestrians.

`relevant_principles` (P1, P2, P6, P7) — four valid P0–P9 IDs, within the
3–5 guidance, each discussed in the card's own prose (P1/P2 via collision
and comfort-at-scale; P6 via multi-agent trajectory prediction; P7 via
avoiding indefinite freezing). `scenario_usage_guide.quality_metrics`
(P2, P7) is a consistent subset. `expected_behaviors` entries describe
kinds of behavior ("thread through gaps," "maintain reasonable
clearance") rather than exact motions or numeric thresholds — no
over-specification (P&G Guideline N6).

## Source Fidelity

SOURCE cites P&G Table 3, "cited in various." Compared against
`.claude/skills/_shared/pg_scenarios.md`'s "Crowd Navigation" entry:
Description ("A robot navigates through a crowd"), Physical Environment
(Generic), Geometric Layout (Passable space), Scientific Purpose (Crowd
navigation), Robot Task ("Navigate thru" / elaborated), Human Behavior
("Mill about" / elaborated), Ideal Outcome ("No collision/obstruction" /
elaborated with an added "steady progress" clause, not a contradiction),
and Cited In ("Various" / "various") all match. Table 3 lists "Robot
Crowding" as the related scenario, a Figure 7 scenario with no
implemented directory under `prosoc/scenarios/` (confirmed — no
`robot_crowding` directory exists); the card's `related_scenarios`
instead references `parallel_traffic` and `perpendicular_traffic`, both
implemented and both discussed in the card's own Notes section, and
`evaluation_notes` explicitly documents this substitution. Expected
divergence per the checklist's `related_scenarios` convention, not a
defect. No mismatches found.

## Completeness

Scenario Card Summary fully present: Scenario Name, Description,
Scientific Purpose, Physical Environment, Geometric Layout, Robot Role,
Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal
Outcome, Related Scenarios, Cited In. Scenario Usage Guide fully
populated (Success Metrics, Quality Metrics, Ideal Outcome, Failure
Modes, Labeling Criteria) matching the embedded YAML `scenario_usage_guide`
block. No blank required fields.
