---
scenario: movable_obstruction
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-06
---

# Audit: Movable Obstruction

- **Scenario:** `prosoc/scenarios/movable_obstruction/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-06 (`--paper` = the
  attached PRNC paper PDF)
- **Verdict:** Ready — no blocking or should-fix issues; unusually high source
  fidelity now that the true source document is available.

This re-audits the card after its `SOURCE` field was corrected from a
generic "P&G paper" attribution to the actual originating document — *The
Prosocial Robot Navigation Charter* (Francis, submitted to Frontiers),
§4.2.1 — and `state` was bumped `DRAFTED` → `EDITED` to reflect that
correction (the `## Status` `STATE` bullet and the fenced YAML `state:`
field, both in `scenario.md`). The card has since been promoted further to
`AUDITED` (see the STATUS block's `EDITED` history for the dated record of
each step); specific line numbers for these fields are not cited here
since they shift as the STATUS block grows. All findings from the
2026-07-22 audit remain resolved; this pass adds a direct, paragraph-level
source-fidelity
comparison that was not possible before this paper was available.

## Findings

### 1. High Urgency's specific behavioral implication isn't spelled out in `evaluation_notes` — suggestion
- **Section/field:** `evaluation_notes`'s task/context cross-reference
  (`scenario.md:159-166`) vs. the source paper's context discussion
- **Issue:** The source paper (§4.2.2, PDF p. 24) gives a specific
  behavioral implication for each of the three contexts it names for this
  scenario: Routine Delivery → report to management; Guidance Docent →
  remove the obstruction; **High Urgency → do neither** ("not take the time
  to either remove the obstruction or to document it but instead focus on
  making its delivery in as timely a fashion as possible"). The card's
  `evaluation_notes` lists all three context IDs as illustrative options but
  doesn't carry forward this specific High Urgency implication the way it
  implicitly does for the other two contexts via the Discussion section's
  general framing.
- **Recommended fix:** Optionally add one clause to `evaluation_notes`
  noting that under `emergency.high_urgency`, neither removing nor
  reporting may be appropriate — the robot should prioritize timely task
  completion instead. Not required for `AUDITED`: the card doesn't
  misstate anything, it's simply less specific than the source on this one
  point.

## Prose/YAML Consistency

Unchanged from 2026-07-22 — re-confirmed:
- Scenario Overview vs. `intended_robot_task`/`intended_human_behavior`/
  `context`: consistent.
- Normative Expectations content (Discussion + Scenario Usage Guide prose)
  vs. `expected_behaviors.{must,should,should_not}`: consistent, no
  one-sided claims.
- `ideal_outcome` prose matches the YAML field verbatim in both Scenario
  Card Summary and Scenario Usage Guide.

### Distiller check

`scripts/distill/scenarios --scenario movable_obstruction --dry-run
--show-diffs` reports no diff and no schema validation error following the
`SOURCE`/`state` correction — `scenario.md`'s embedded YAML and
`scenario.yml` remain in sync.

## Schema and Charter Compliance

Unchanged from 2026-07-22 — `scenario.yml` validates; `relevant_principles`
(`P0, P1, P3, P5, P7, P9`) are all valid P0–P9 IDs; the above-5 count
remains justified by the Discussion section's explicit discussion of P0
trade-offs; `related_scenarios` (`frontal_approach`, `single_file_hallway`)
reference real directories and are now independently confirmed by the
source paper's own text, not just by directory existence (see Source
Fidelity below).

## Source Fidelity

**SOURCE**, as corrected this session, cites *The Prosocial Robot
Navigation Charter* (Francis, submitted), §4.2.1. This is now directly
checkable — the attached PDF is that paper.

Comparing the card against the source text (§4.2.1, PDF p. 23; §4.2.2, PDF
p. 24):

- **Physical setup:** Paper: "a section of hallway in theory wide enough
  for a human and robot to pass safely and comfortably, but partially
  blocked by a movable obstruction." Card's `geometric_layout`: "passable
  space, partially obstructed"; Scenario Description: "a hallway that is
  partially blocked by a movable obstruction." **Match.**
- **Core behavioral choice:** Paper: "a robot following P9... might either
  remove the obstruction (if physically capable of moving it) or report it
  to management (if not)." Card's `expected_behaviors.should`: "remove the
  obstruction if physically capable and task-appropriate," "report the
  obstruction to facility management when appropriate," "yield or wait if
  intervention is inappropriate." **Match** — the card's third option
  (yield/wait) corresponds to the paper's own framing that a P7-only robot
  "would behave as in Single File Hallway" as the fallback.
- **P0/P9 trade-off:** Paper: "removing the obstruction might not be
  appropriate behavior if it causes the robot to fail at its task. This is
  why the entire ... Charter, with its complementary set of principles -
  including P0: Goal Achievement - is necessary." Card's Discussion:
  "Trade-offs between Goal Achievement (P0) and prosocial action." **Match.**
- **Task/context cross-reference:** Paper's worked example uses exactly
  `navigate_point_to_point` (low P0 priority → prosocially clear the
  obstruction), `deliver_object` (higher P0 priority → judgment call
  between removing, reporting, or ignoring), and the contexts
  `routine_delivery` (report to management), `guidance_docent` (remove
  it), and `high_urgency` (neither — focus on timely delivery). The card's
  `evaluation_notes` (`scenario.md:159-166`) names the same task and
  context IDs, already verified in the 2026-07-22 audit against
  `prosoc/tasks/*/task.yml` and `prosoc/contexts/*/context.yml` — now also
  confirmed to be the paper's own worked example, not just plausible IDs.
  **Match**, with the High Urgency nuance noted in Finding 1.
- **Related scenarios:** The paper explicitly frames *Movable Obstruction*
  as extending *Frontal Approach* ("narrowing the corridor... gives the
  opportunity to test P7 and P9") and pairs it with *Single File Hallway*
  as a minimal three-scenario set. The card's `related_scenarios`
  (`frontal_approach`, `single_file_hallway`) match exactly.

**Source fidelity: high, directly confirmed.** Every checkable claim in the
card matches the source paper's own description of this scenario, with one
minor enrichment opportunity (Finding 1). This supersedes the 2026-07-22
audit's "not checkable against Table 3" finding, which was accurate at the
time but predated the source document actually being available for
comparison.

## Completeness

Unchanged from 2026-07-22: all Required fields present and consistent.
`Cited In` remains blank — reasonably so, and for a slightly different
reason than previously stated: this scenario originates in a paper that is
itself still `submitted` (not yet published), so there is no external
literature that could yet cite it. Revisit once the source paper is
published or another card's `related_scenarios`/`Cited In` references this
one.

## Verdict Rationale

No blocking or should-fix findings. The `SOURCE` correction closes a real
defect (misattribution to the P&G paper, which has no counterpart for this
scenario). Source fidelity is now not just "not contradicted" but
positively confirmed at a paragraph level against the actual originating
document. Ready for `AUDITED`.
