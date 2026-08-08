---
family: scenarios
card: following
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-07
---

# Audit: Following

- **Card:** `prosoc/scenarios/following/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-07 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — this pass adds the
  must-level-prose-gap finding and resolves the Table 3 erratum question)
- **Verdict:** Ready for `AUDITED`, no blocking or should-fix issues found

## Findings

### 1. "Normative Expectations" prose omits a `must`-level item — suggestion
- **Section/field:** `expected_behaviors.must` ("avoid collision with the
  human, other pedestrians, and obstacles", "not lose track of the human
  during turns or brief occlusions") vs. the prose "Unacceptable
  behavior" list
- **Issue:** The second `must` item is covered ("Following at a distance
  so far that the robot loses the human at a turn or in a crowd"), but
  the first ("avoid collision") is never stated as its own bullet — the
  closest prose item ("Cutting through obstacles or other pedestrians to
  preserve following distance") is about cutting through, not collision
  directly. Matches the recurring must-level-prose-gap pattern already
  tracked in `project/design/backlog.md`.
- **Recommended fix:** Add an explicit "Colliding with the human, other
  pedestrians, or obstacles while following" bullet to Unacceptable
  behavior. Not required for `AUDITED`; deferred to the dedicated
  backlog-burndown pass.

No other findings. `related_scenarios: [leading]` reciprocates — `leading`'s
own `related_scenarios` lists `following` back. No one-way
cross-reference gap.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Following" entry (cited in [50]).
Compared against `.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | A robot follows a person | Overview: "robot in a servant role follows a human who leads their own navigation" | Match |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Walking space | `geometric_layout: walking space` | Match |
| Scientific Purpose | Joint navigation | `scientific_purpose: joint navigation` | Match |
| Robot Role | Servant | `agents.robot.role: servant` | Match |
| Robot Task | Follow lead robot | `intended_robot_task: follow the lead human` | Erratum — resolved below |
| Human Behavior | Lead human | `intended_human_behavior: lead, navigating freely...` | Match |
| Ideal Outcome | Robot follows person | `ideal_outcome: robot follows the person continuously...` | Match |
| Related Scenarios | Accompany Peer | `related_scenarios: [leading]` — Accompany Peer has no implemented scenario directory; card's own `evaluation_notes` documents the substitution | Consistent — expected divergence per convention, not a fidelity gap |
| Cited In | [50] | `cited_in: ["50"]` | Match |

**Robot Task erratum — confirmed by the user directly (2026-08-07), who
is the P&G paper's lead author.** Table 3 as transcribed literally reads
"Follow lead robot" for this scenario's Robot Task field, which
contradicts the scenario's own Description ("A robot follows a person")
and Human Behavior ("Lead human") — a robot cannot simultaneously be the
one following and the one being followed within the same row. The user
confirmed this is a genuine erratum in the source paper and should be
read as "Follow lead human." The card's `intended_robot_task: follow the
lead human` already reflects this correct reading; the `evaluation_notes`
"Ambiguity note" should be updated to state this is a confirmed erratum
rather than an unverified suspicion, but this is optional polish, not a
fidelity defect — the card's own interpretive call was already correct.

"Accompany Peer" is not yet tracked in `project/design/backlog.md`'s
"Missing forward-referenced cards" table — adding it as part of this
review.

## Completeness

Scenario Card Summary: all fields present and rendered — Scenario Name,
Description, Scientific Purpose, Physical Environment, Geometric Layout,
Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics,
Ideal Outcome, Related Scenarios (`leading`), Cited In (`50`).

Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome,
Failure Modes, and Labeling Criteria all present and non-trivial.
`quality_metrics` (P2, P6) is a sensible subset of `relevant_principles`
(P1, P2, P6, P8).

No required fields are blank. `scripts/distill/scenarios --scenario
following --dry-run --show-diffs` reported no diff, confirming
`scenario.md` and `scenario.yml` are in sync.
