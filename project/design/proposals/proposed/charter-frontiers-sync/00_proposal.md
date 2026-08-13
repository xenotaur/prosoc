---
id: PROP-CHARTER-FRONTIERS-SYNC
type: design_proposal
title: Reconciling the Prosoc Charter with the Frontiers Paper
status: proposed
created_on: 2026-08-12
updated_on: 2026-08-12
implementation_status: not_started
implemented_by: []
supersedes: []
superseded_by: null
related_design:
  - prosoc/charter/charter.md
  - prosoc/charter/audit.md
---

## Summary

This proposal captures the reconciliation decisions between `prosoc/charter/charter.md`
(APPROVED) and the Frontiers paper "The Prosocial Robot Navigation Charter"
(Francis, submitted — frozen, no longer editable). The paper is now the
external reference point but the charter is the only artifact that can
change; each principle P0–P9 (plus the Section 2 prosocial-navigation
definition) is reviewed and a decision recorded, either resolved here or
flagged as an Open Question for further per-principle review before a
work item implements the edits.

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
6. Principles needing closer, not-yet-final review (P2/P3/P4 wording,
   P7).

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
Paper's §3.4.2 list uses MUST only for P1 (severity: critical) and SHOULD
for every other principle (P0, P2–P9), including P6 (severity: high) and
P8 (severity: medium). The charter currently uses MUST for P0, P1, P2,
P3, P4, P5, P6, P8, and SHOULD only for P7 and P9 — a blanket-MUST
pattern that also does not consistently track its own `severity` field
(P3/P4/P5/P8 are all `severity: medium`, yet P7 — also `severity:
medium` — already uses "should" while the other three use "must").
**Chosen: MUST for P1 only; SHOULD for P0 and P2–P9**, matching the
paper's convention. This also requires an explicit audit of the
charter's `severity` field per principle, since the current mapping is
internally inconsistent independent of what the paper says — a
consistent severity→modal rule (e.g. critical/high → MUST, medium →
SHOULD, optional → MAY/SHOULD) should be adopted and applied uniformly.
Rationale: the paper explicitly frames MUST/SHOULD as RFC 2119/8174-style
vocabulary carrying real normative weight (paper §3.2.2, §3.3.4); the
charter's blanket-MUST pattern undercuts that design intent.

**Open Question:** what is the exact severity→modal rule, and does every
principle's current `severity` value survive the audit unchanged, or do
some need to be re-leveled as part of this pass? Deferred to the
per-principle walkthrough that follows this proposal.

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

### Decision: P2, P3, P4 — wording synchronization
Paper and charter differ in wording for all three (e.g. "anxiety or
distress" vs. "stress, fear, or annoyance" for P2; "goals" vs. "goals and
intentions" for P3; scope of "in its presence" vs. "in shared social
spaces" for P4) beyond the shared modal-verb pattern.
**Open Question:** not yet decided — needs line-by-line review, one
principle at a time, deferred to the walkthrough following this
proposal.

### Decision: P7 — Proactivity, scope
Charter: "anticipate potential issues and take initiative to avoid or
resolve them" (broader — any potential issue, avoid-or-resolve). Paper:
"proactively act to resolve conflicts before they happen" (narrower —
conflicts only, resolve-only).
**Open Question:** not yet decided — needs closer review, deferred to the
walkthrough following this proposal.

## Non-Goals

- Does not edit `prosoc/charter/charter.md` — this proposal is a decision
  record only; implementation happens in a follow-on work item.
- Does not edit the Frontiers paper — it is submitted and frozen; the
  charter is the sole artifact that changes going forward.
- Does not finalize P2/P3/P4 wording or P7's scope — those remain Open
  Questions pending a closer per-principle walkthrough.
- Does not re-open Section 2's prosocial-navigation definition or P0 —
  both are already in sync between charter and paper.
- Does not re-derive or re-litigate the 2026-08-05/06 prior sync — this
  proposal picks up from the charter's current state as of 2026-08-12.

## Implementation Plan

Small scope, single work item once all decisions (including the three
remaining Open Questions) are finalized:

1. Finish the per-principle walkthrough for P2/P3/P4 wording, P7 scope,
   and the severity→modal audit for all ten principles — update this
   proposal's Design Decisions section with the outcomes.
2. Create a work item (`/lrh-work-item`) to implement the resulting
   charter edits: P1, P5, P6 (modal only), P8, P9, plus whatever P2/P3/P4/P7
   changes and severity re-leveling the walkthrough settles on.
3. The work item reverts the charter from APPROVED to EDITED for the
   content update, per the precedent set by the 2026-08-05 edit, and
   carries it back through AUDITED → APPROVED.

## Cross-References

- `prosoc/charter/charter.md` — the artifact being reconciled.
- `prosoc/charter/audit.md` — prior audit history, including the
  2026-08-05/06 partial sync this proposal continues.
- Frontiers paper "The Prosocial Robot Navigation Charter" (Francis,
  submitted) — external, not tracked in this repo.
