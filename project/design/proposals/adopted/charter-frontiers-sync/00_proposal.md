---
id: PROP-CHARTER-FRONTIERS-SYNC
type: design_proposal
title: Reconciling the Prosoc Charter with the Frontiers Paper
status: adopted
created_on: 2026-08-12
updated_on: 2026-08-21
implementation_status: implemented
implemented_by:
  - WI-CHARTER-FRONTIERS-SYNC
supersedes: []
superseded_by: null
related_design:
  - src/prosoc/prnc/charter/charter.md
  - src/prosoc/prnc/charter/audit.md
---

# Reconciling the Prosoc Charter with the Frontiers Paper

## Summary

This proposal captures the reconciliation decisions between `prosoc/charter/charter.md`
(APPROVED) and the Frontiers paper "The Prosocial Robot Navigation Charter"
(Francis, submitted — frozen, no longer editable). The paper is now the
external reference point but the charter is the only artifact that can
change; each principle P0–P9 (plus the Section 2 prosocial-navigation
definition) is reviewed and a decision recorded. All decisions are now
finalized — Section 2, P0–P9, the MUST/SHOULD modal-verb convention, and
the severity ladder — and the proposal is ready for a follow-on work item.

## Background / Motivation

The charter's own Status section documents at least one prior sync attempt
(2026-08-05/06) that updated Section 2's prosocial-navigation definition
and P9 to match the paper. Since then, further drift has accumulated
between the two documents, and the paper has now been submitted — freezing
it as a reconciliation target rather than a moving one.

A side-by-side comparison (this session) of `prosoc/charter/charter.md`
against the submitted paper draft surfaced several categories of
difference:

1. Places where the charter should adopt paper wording it currently lacks
   (P1's broader damage scope, P5's feasibility hedge).
2. A systematic modal-verb (MUST/SHOULD) convention mismatch, compounded
   by an internal inconsistency in the charter's own severity-to-modal
   mapping independent of the paper.
3. Places where the charter's current wording is judged better than the
   paper's and should be *kept* (P6's "accommodate" framing).
4. A structural choice about where a taxonomy lives (P8: normative
   statement vs. Explanation).
5. A case where the paper deliberately narrowed a principle's scope after
   P0 was introduced, and the charter should follow that narrowing (P9).
6. Principles where neither version wins outright and a merged wording
   was drafted, combining charter content with paper phrasing (P2, P3,
   P4, P7).

This project's standing norm is that genuinely contested content
judgment calls get surfaced for human decision rather than resolved
unilaterally by an agent (see `prosoc/charter/audit.md` history and the
2026-08-05/06 Status entries for precedent). This proposal is that
surfacing mechanism, and the record of the decisions once made.

## Prior Art Check

### Duplication search
- In-repo: No existing proposal, workstream, or work item addresses
  charter/paper reconciliation. `project/design/proposals/proposed/nca-prnc-package-layout/00_proposal.md`
  references `charter` only in the context of Python package layout
  (`prosoc/charter/` as a data subpackage) — unrelated to this proposal's
  normative-content scope.
- Sibling repos: None identified — the paper is maintained in Overleaf,
  outside any repo.
- External libraries: Not applicable — this is a content-authoring
  decision, not a build-vs-buy question.
- Recommendation: Proceed.

### Demand search
- Work items: None found under `project/work_items/proposed/`.
- Proposals: None found under `project/design/proposals/proposed/` other
  than the unrelated package-layout proposal above.
- Backlog: `project/design/backlog.md` references `charter` only for the
  now-resolved 2026-08-02–08-06 should-fix tracking entry (already
  removed) — no open backlog entry matches this topic.
- Recommendation: No action.

## Design Decisions

### Decision: Section 2 — Prosocial-navigation definition
Charter and paper (§3.4.1) are word-for-word identical.
**Chosen: No change.**

### Decision: P0 — Goal Achievement
Charter and paper (§3.4.2) are identical.
**Chosen: No change.**

### Decision: P1 — Safety, scope of protected parties
Paper: "must not cause damage to pedestrians, other robots, its
environment, or itself." Charter: "must not cause harm to humans or
damage environments" — narrower, omitting other-robots and self-damage
protection.
**Chosen: Upgrade the charter to match the paper's broader scope.**
Rationale: the narrower charter wording appears to be an unintentional
gap rather than a deliberate scope decision; multi-robot and
robot-self-preservation concerns are legitimately safety-relevant.

### Decision: P5 — Social Competency, feasibility hedge
Paper: "should follow local social norms **where feasible**." Charter:
"must follow basic social norms governing shared spaces" — hedge
dropped, "basic" qualifier added.
**Chosen: Restore the "where feasible" hedge.**
Rationale: P5's own Explanation section discusses norms that vary by
locale (e.g. driving-side convention) and describes following the
applicable local norm as reducing conflict — language that assumes norms
can be infeasible or contradictory across contexts. Dropping the hedge
removed the escape valve the Explanation itself depends on.

### Decision: Modal-verb convention (MUST vs. SHOULD) across all principles
**Correction (2026-08-13):** an earlier draft of this decision claimed the
paper uses MUST only for P1. That was a misreading — the paper's §3.4.2
text for P0 reads "Robots **must** attempt to achieve their assigned
navigation or task objectives..." — P0 is MUST in the paper too. The
decision below reflects the corrected reading.

Paper's §3.4.2 list uses MUST for P0 and P1 and SHOULD for every other
principle (P2–P9), including P2 and P6 (severity: high) and P8
(severity: medium) — so the paper's modal choice does not track its own
severity tiers at all (P0 and P2 are both `high` but get different
modals). The charter currently uses MUST for P0, P1, P2, P3, P4, P5, P6,
P8, and SHOULD only for P7 and P9 — a blanket-MUST pattern that also does
not consistently track its own `severity` field (P3/P4/P5/P8 are all
`severity: medium`, yet P7 — also `severity: medium` — already uses
"should" while the other three use "must").
**Chosen: MUST for P0 and P1; SHOULD for P2–P9**, matching the paper's
actual convention. This also requires an explicit audit of the charter's
`severity` field per principle, since the current mapping is internally
inconsistent independent of what the paper says.
Rationale: the paper explicitly frames MUST/SHOULD as RFC 2119/8174-style
vocabulary carrying real normative weight (paper §3.2.2, §3.3.4); the
charter's blanket-MUST pattern undercuts that design intent. P0 keeping
MUST (rather than being reconsidered as SHOULD) also matches the
charter's own Explanation for P0, which frames goal achievement as
equally load-bearing to safety in preventing "paralysis or
over-cautiousness."

**Severity audit outcome:** the severity ladder (P1 `critical`; P0, P2,
P6 `high`; P3, P4, P5, P7, P8 `medium`; P9 `optional`) was reviewed
against the modal-verb decision above and confirmed as-is — no
re-leveling. `severity` and the MUST/SHOULD modal are deliberately
decoupled: `severity` continues to rank principles against each other for
conflict resolution, while the modal verb is now MUST-for-P0-and-P1,
SHOULD-elsewhere, independent of a principle's severity tier.

### Decision: P6 — Agent Understanding, wording
Paper: "should be aware of and predict the behavior of nearby agents..."
(epistemic — an input to planning). Charter: "must predict and
accommodate the behavior of other agents" (adds a behavioral duty).
**Chosen: Keep the charter's "accommodate" wording; change the modal to
SHOULD** per the modal-verb decision above.
Rationale: the charter's own Explanation ("interaction potential...
should sometimes be minimized and sometimes maximized") supports
"accommodate" as the intentional and stronger framing; the paper's
purely epistemic phrasing is the one judged to have room for
improvement, not the charter's.

### Decision: P8 — Contextual Appropriateness, taxonomy placement
Paper's §3.4.2 summary line inlines the six context axes (cultural,
diversity, geometric/operational environmental, task, interpersonal)
directly into the normative statement. Charter's normative statement is
generic ("adapt their behavior to the social and situational context"),
with the taxonomy currently living only in the Explanation section.
**Chosen: Inline the six-context taxonomy into the charter's normative
statement**, matching the paper's structure.

### Decision: P9 — Prosocial Behavior, qualifier scope
The paper deliberately removed the "in ways appropriate to task/context
and without sacrificing own goals" qualifier from P9's normative
statement once P0 (goal preservation) and P8 (contextual
appropriateness) were introduced as separate principles that already
cover that ground — keeping P9 itself focused purely on the prosociality
behavior. The charter's P9 normative statement still carries that
trailing qualifier.
**Chosen: Trim the qualifier from the charter's P9 normative statement**,
to match the paper's narrower framing. The qualifier remains correctly
present in the Section 2 prosocial-navigation *definition* (unchanged —
see above), which is the right place for it now that P0/P8 exist as
separate principles.

### Decision: P2 — Comfort, wording
Paper: "should not cause anxiety or distress in nearby navigating
pedestrians." Charter: "must avoid causing stress, fear, or annoyance"
(unscoped audience).
**Chosen (merged):** *"Robots must avoid causing stress, fear, or
annoyance in nearby humans."*
Rationale: keeps the charter's existing three-item emotion list — "fear"
and "anxiety" were judged too close to synonyms to justify adding
"anxiety" separately, and "anxiety" carries psychological-diagnosis
overtones "fear" avoids. Adopts the paper's move of naming an audience,
but generalized to "nearby humans" rather than the paper's narrower
"navigating pedestrians," since P2's own Explanation is not limited to
people who are themselves navigating (a stationary bystander can be
discomforted too).

### Decision: P3 — Legibility, wording
Paper: "should navigate in such a way that the robot's goals are clear
from its behavior" (goals only). Charter: "must act in ways that make
their goals and intentions easy to understand" (goals + intentions).
**Chosen (merged):** *"Robots must act in ways that make their goals and
intentions clear from their behavior."*
Rationale: keeps the charter's broader "goals and intentions" (the
paper's "goals" is a subset). Adopts the paper's "clear from its
behavior" framing over the vaguer "easy to understand" — ties legibility
to observable behavior specifically, consistent with the Dragan et al.
(2013) legibility citation already in the charter's References.

### Decision: P4 — Politeness, wording
Paper: "should act in a way that shows respect for other navigating
agents in its presence" (narrow, generic). Charter: "must be respectful
and considerate in shared social spaces," with a richer YAML description
(offering help, avoiding dismissive behavior) added in the 2026-08-06
sync.
**Chosen (merged):** *"Robots must be respectful and considerate toward
other agents in shared social spaces."*
Rationale: keeps the charter's broader "shared social spaces" (the
paper's "in its presence" is narrower) and its richer description/
Explanation content from the 2026-08-06 sync. Adds explicit "other
agents" as the object, borrowed from the paper, making explicit what was
previously only implicit in the Explanation (including robot-robot
politeness).

### Decision: P7 — Proactivity, scope
Charter: "anticipate potential issues and take initiative to avoid or
resolve them" (broader — any potential issue, avoid-or-resolve). Paper:
"proactively act to resolve conflicts before they happen" (narrower —
conflicts only, resolve-only).
**Chosen (merged):** *"Robots should proactively anticipate potential
issues or conflicts and take initiative to avoid or resolve them."*
Rationale: keeps the charter's broader "avoid or resolve" — the paper's
preventive-only "before they happen" framing doesn't fit the charter's
own deadlock-breaking example (resolving an already-occurring conflict,
not preventing one). Adds "proactively" and names "conflicts" explicitly
alongside the broader "issues," both borrowed from the paper.

## Non-Goals

- Does not edit `prosoc/charter/charter.md` — this proposal is a decision
  record only; implementation happens in a follow-on work item.
- Does not edit the Frontiers paper — it is submitted and frozen; the
  charter is the sole artifact that changes going forward.
- Does not re-open Section 2's prosocial-navigation definition or P0 —
  both are already in sync between charter and paper.
- Does not re-derive or re-litigate the 2026-08-05/06 prior sync — this
  proposal picks up from the charter's current state as of 2026-08-12.

## Implementation Plan

Small scope, single work item. All decisions above are finalized:

1. Create a work item (`/lrh-work-item`) to implement the resulting
   charter edits:
   - P1: broaden Safety scope (other robots, self-damage).
   - P2, P3, P4, P7: adopt the merged normative-statement wording above.
   - P5: restore the "where feasible" hedge.
   - Modal verbs: MUST for P0 and P1, SHOULD for P2–P9 across every
     principle's normative statement and YAML `description`.
   - P6: modal only (MUST → SHOULD); wording unchanged.
   - P8: inline the six-context taxonomy into the normative statement.
   - P9: trim the task/context/goals qualifier from the normative
     statement (Section 2's definition keeps it, unchanged).
   - Severity fields: no change (audit confirmed the existing ladder).
2. The work item reverts the charter from APPROVED to EDITED for the
   content update, per the precedent set by the 2026-08-05 edit, and
   carries it back through AUDITED → APPROVED.

## Cross-References

- `prosoc/charter/charter.md` — the artifact being reconciled.
- `prosoc/charter/audit.md` — prior audit history, including the
  2026-08-05/06 partial sync this proposal continues.
- Frontiers paper "The Prosocial Robot Navigation Charter" (Francis,
  submitted) — external, not tracked in this repo.
