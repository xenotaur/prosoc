---
scenario: single_file_hallway
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-08-06
---

# Audit: Single File Hallway

- **Scenario:** `prosoc/scenarios/single_file_hallway/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-06 (`--paper` = the
  attached PRNC paper PDF)
- **Verdict:** Ready, no issues found — source fidelity is directly
  confirmed, including a near-verbatim match against the paper's own
  published `expected_behaviors` YAML listing.

This closes out the "Cited In" gap-note phrasing suggestion carried since
2026-07-22: the Scenario Card Summary's "Remaining gaps" note now reads
"reasonably blank — this scenario originates in a source paper (§4.2.1)
that is itself still `submitted` and unpublished, so no external
literature yet exists that could cite it. Revisit once the source paper is
published," replacing the prior "should-fill-in-now" phrasing that
overstated what was actually possible. This was the sole open item carried
forward from this session's earlier `SOURCE` correction (from a generic
"P&G paper" attribution to the actual originating document — *The
Prosocial Robot Navigation Charter* (Francis, submitted to Frontiers),
§4.2.1 — with `state` bumped `DRAFTED` → `EDITED`, per the STATUS block's
`## Status` `STATE` bullet and fenced YAML `state:` field in
`scenario.md`; specific line numbers are not cited here since they shift
as the STATUS block grows — the card has since been promoted further to
`AUDITED`).

## Findings

None.

## Prose/YAML Consistency

Unchanged from the prior pass — re-confirmed: Scenario Overview vs.
`intended_robot_task`/`intended_human_behavior`/`context` consistent;
Normative Expectations prose vs. `expected_behaviors.{must,should,should_not}`
consistent (both `must` items stated in prose); `ideal_outcome` prose
matches the YAML field verbatim. The Cited-In-note reword is prose-only,
outside the fenced YAML block.

### Distiller check

`scripts/distill/scenarios --scenario single_file_hallway --dry-run
--show-diffs` reports no diff and no schema validation error — confirmed
both before and after today's gap-note reword, since that edit touches no
fenced YAML block. `scenario.md`'s embedded YAML and `scenario.yml` remain
in sync.

## Schema and Charter Compliance

Unchanged — `scenario.yml` validates; `relevant_principles` (`P1, P3, P5,
P7`) are all valid P0–P9 IDs, count within the 3–5 guideline;
`scenario_usage_guide.quality_metrics` (`P3, P5, P7`) consistent;
`related_scenarios` (`frontal_approach`, `movable_obstruction`) reference
real directories, independently confirmed by the source paper itself (see
Source Fidelity).

## Source Fidelity

**SOURCE** cites *The Prosocial Robot Navigation Charter* (Francis,
submitted), §4.2.1 — corrected this session from a generic, incorrect
"P&G paper" attribution. This scenario is not extrapolated from P&G's
Figure 7 at all; the source paper states it and `movable_obstruction` are
"two scenarios we developed for this paper" (§4.2.1, PDF p. 23).

Comparing the card against the source text directly:

- **Physical setup:** Paper: "a section of hallway too narrow for a human
  and a robot to pass safely and comfortably." Card's `geometric_layout`:
  "narrow hallway"; Scenario Description: "a hallway that is too narrow for
  safe and comfortable passing." **Match.**
- **Core behavior:** Paper: "A robot not following the principle of P7...
  might enter the hallway at the same time as a human, causing a conflict,
  whereas a proactive robot will either signal for the human to go first or
  ask the human to wait." Card's `expected_behaviors.should`: "recognize
  early that the hallway does not permit passing," "signal intent clearly
  (e.g., yielding, requesting priority, or other clear signaling),"
  `should_not`: "enter the hallway and create a stalemate." **Match.**
- **`expected_behaviors` YAML — near-verbatim match.** The paper's Figure 6
  (PDF p. 25) prints the actual final, schema-compliant `expected_behaviors`
  block the authors arrived at after a documented schema-validation failure
  (Listing 1: an unsupported `may` subtype) and revision (Listings 2→3).
  Comparing Listing 3 to the card's current `expected_behaviors` YAML:

  | Paper (Listing 3) | Card (`scenario.md`) |
  |---|---|
  | `must`: maintain a safe physical distance / avoid entering the hallway simultaneously | identical |
  | `should`: recognize early... / resolve without prolonged deadlock / signal intent clearly (e.g., yielding or requesting priority) | identical, reordered; "signal intent clearly" elaborated to "(e.g., yielding, requesting priority, **or other clear signaling**)" |
  | `should_not`: force the human to back up unexpectedly / enter the hallway and create a stalemate / rely on last-moment braking | identical |

  This is as close to a direct-quotation fidelity check as this corpus
  gets — the card's machine-readable payload matches the paper's own
  published, schema-corrected YAML almost word-for-word.
- **Provenance detail corroborated:** The paper states (§4.3, PDF p. 24)
  that "an early draft of this paper was fed into ChatGPT 5.2 to help
  develop the scenarios presented in Section 4.2.1." The card's own
  `DRAFTED` entry (`scenario.md:7`) independently states "ChatGPT 5.2,
  2026-01-16" — consistent with the paper's account of its own drafting
  process.
- **Related scenarios:** The paper pairs this scenario with *Frontal
  Approach* and *Movable Obstruction* as a minimal three-scenario set
  (§4.2.1, PDF p. 23: "Together, Frontal Approach, Single File Hallway, and
  Movable Obstruction form a minimal scenario set"). The card's
  `related_scenarios` (`frontal_approach`, `movable_obstruction`) match
  exactly.

**Source fidelity: high, directly confirmed** — including a near-verbatim
match on the machine-readable `expected_behaviors` payload itself, not just
the descriptive prose.

## Completeness

All Required fields present and consistent. `Cited In` remains blank, now
correctly self-documented as reasonably blank (source paper unpublished)
rather than as an actionable to-do — closing the prior audit's sole
suggestion.

## Re-audit Note

Third audit of this card (2026-07-21 → 2026-07-22 closed the
missing-Normative-Expectations should-fix; 2026-08-06 first pass corrected
`SOURCE` and rewrote Source Fidelity; this pass closes the remaining
gap-note-phrasing suggestion). Zero open findings of any severity. Ready
for `AUDITED`.
