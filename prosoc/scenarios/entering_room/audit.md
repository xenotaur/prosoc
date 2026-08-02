---
family: scenarios
card: entering_room
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-08-02
---

# Audit: Entering Room

- **Card:** `prosoc/scenarios/entering_room/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — and is superseded by this
  pass)
- **Verdict:** Ready — no blocking or should-fix issues found; two minor
  suggestions

## Findings

### 1. P3 (Legibility) not included in `relevant_principles` — suggestion
- **Section/field:** `relevant_principles` vs. `.claude/skills/_shared/principles.md` selection guidance
- **Issue:** The scenario's normative core is about the robot recognizing
  and communicating deference at a threshold ("proceed to enter promptly
  once the threshold is clear," avoiding "waiting so far back... entry is
  delayed"). P3 (Legibility) arguably applies, since a human benefits from
  being able to tell the robot is intentionally waiting rather than
  malfunctioning or blocked. The current selection (P1, P4, P5, P6) is
  reasonable and within the 3–5 guidance, so this is not a defect.
- **Recommended fix:** Optional — add P3 if the editor agrees legibility
  of the robot's "waiting" intent is a distinct concern from
  politeness/social-norm compliance; otherwise no change needed.

### 2. "Normative Expectations" prose omits one `must`-level behavior — suggestion
- **Section/field:** Normative Expectations (prose) vs. `expected_behaviors.must`
- **Issue:** The prose's "Unacceptable behavior" list covers "avoid
  blocking the human's exit path" (via "Blocking the human's exit path by
  positioning too close to the door"), but never explicitly states the
  other `must` behavior — "avoid collision with the human at the doorway"
  — as its own bullet. The idea is present elsewhere (the Scenario
  Description's "must defer to the exiting human before entering," and
  safety is implicit throughout), so this is presentation drift, not a
  contradiction or omission of substance. Same pattern independently
  found this session on `intersection_no_gesture`.
- **Recommended fix:** Optionally add an explicit "avoid collision with
  the human at the doorway" bullet under Normative Expectations for
  symmetry with the `must` list — not required for `AUDITED`.

## Source Fidelity

SOURCE cites P&G Table 3 and "Robotics at Google (R@G), internal scenario
reference." Compared against
`.claude/skills/_shared/pg_scenarios.md`'s "Entering Room" entry: Description ("Robot enters a room occupied by a human"),
Physical Environment (Indoor), Geometric Layout (Room and door),
Scientific Purpose (Pedestrian interaction), Robot Task ("Navigate out to
in" / "navigate from outside to inside the room"), Human Behavior
("Navigate in to out" / "navigate from inside to outside the room"),
Ideal Outcome ("Robot lets human exit" / elaborated consistently), and
Cited In ("R@G — Robotics at Google, an internal scenario reference" /
"Robotics at Google (R@G), internal scenario reference") all match.
Table 3 lists "Entering Elevator (R@G)" as the related scenario, which has
no implemented directory under `prosoc/scenarios/` (confirmed — no
`entering_elevator` directory exists); the card's `related_scenarios`
instead references `exiting_room` and `narrow_doorway`, both implemented
and both discussed in the card's own "Notes for Scenario Designers and
Evaluators" section, and `evaluation_notes` explicitly documents this
substitution. Expected divergence per the checklist's `related_scenarios`
convention, not a defect. No mismatches found.

## Completeness

Scenario Card Summary block fully present: Scenario Name, Description,
Scientific Purpose, Physical Environment, Geometric Layout, Robot Role,
Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal
Outcome, Related Scenarios, Cited In. Scenario Usage Guide fully populated
(Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling
Criteria) matching the YAML `scenario_usage_guide` block. No blank
required fields.

`relevant_principles` (P1, P4, P5, P6) — four valid P0–P9 IDs, within the
3–5 guidance, each discussed in the card's own prose (see Finding 1 for
the optional P3 consideration). `scenario_usage_guide.quality_metrics`
(P4, P5) is a consistent subset. `expected_behaviors` entries describe
kinds of behavior ("hold position," "crowd the doorway") rather than exact
motions or numeric thresholds — no over-specification. `scenario.yml`
confirmed in sync with `scenario.md` (`scripts/distill/scenarios --scenario
entering_room --dry-run --show-diffs`, no diff).
