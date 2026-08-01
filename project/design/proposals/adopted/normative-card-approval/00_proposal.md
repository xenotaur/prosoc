---
id: PROP-NORMATIVE-CARD-APPROVAL
type: design_proposal
title: Normative Card Corpus Approval — Human Review Pass to APPROVED
status: proposed
created_on: 2026-07-30
updated_on: 2026-07-30
implementation_status: not_started
implemented_by: []
supersedes: []
superseded_by: null
related_design:
  - project/design/proposals/adopted/normative-packet-assembly/00_proposal.md
  - project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md
  - prosoc/scenarios/workflow.md
  - .claude/skills/prosoc-card-audit/SKILL.md
  - .claude/skills/prosoc-card-audit-all/SKILL.md
---

# Normative Card Corpus Approval — Human Review Pass to APPROVED

## Summary

Defines how a human reviewer promotes prosoc normative cards from `AUDITED`
to `APPROVED` — the accountability gate `prosoc/scenarios/workflow.md`
requires for production packet use — via a deterministic corpus
review-queue engine and a three-skill stack (`prosoc-card-approve`,
`prosoc-card-review`, `prosoc-card-review-all`), piloted on the 5
`sample_packet` cards before any full-corpus commitment.

## Background / Motivation

`WS-NORMATIVE-PACKET-ASSEMBLY`'s second exit criterion requires the corpus
to reach `APPROVED`, but no card has ever been promoted past
`DRAFTED`/`EDITED`, and no tooling exists to do it — every implementation
work item so far explicitly forbade `promote_card_state`.
`scripts/validate/status --fix` only projects an already-edited YAML
`state:` into Markdown; it doesn't perform the transition, enforce evidence
gates, or help a human decide *what to review next* out of 32 cards. Doing
this by hand — 4 different YAML root shapes (parent proposal Decision 2)
plus no visibility into which cards most need attention — is exactly the
error-prone, unscalable pattern the corpus's existing tooling was built to
avoid. A deterministic review-queue engine turns "review the corpus" from
unstructured triage into a ranked, resumable worklist, reusing modules
(`prosoc/utils/cards/validate_status.py`, `prosoc/packet/gate.py`) that
already exist and are already unit-tested.

Grounding facts, verified against the live corpus at authoring time:

- 32 cards across 6 families: charter 1, constitutions 2, contexts 4,
  manifests 1, scenarios 20, tasks 4.
- Lifecycle today: all `DRAFTED` except the 2 constitutions (`EDITED`). No
  card has ever been promoted to `AUDITED` or `APPROVED`.
- `audit.md` coverage: all 20 scenarios and all 4 tasks have one;
  `asimov_four_laws` (constitutions) and 3 of 4 contexts
  (`guidance_docent`, `public_navigation`, `routine_delivery`) do not. The
  5 pilot cards (charter, `asimov_three_laws`, `intersection_gesture_wait`,
  `navigate_lead_agent`, `high_urgency`) all already have `audit.md`.
- Per `PROP-NORMATIVE-PACKET-ASSEMBLY` Decision 1: `AUDITED` = agent audit
  produced; `APPROVED` = human review. `prosoc-card-audit`/`-all`
  (`WI-CARD-AUDIT-SKILLS`) already produce the `AUDITED`-track evidence;
  nothing currently promotes card `state` itself.

## Prior Art Check

### Duplication search

- In-repo: no promotion, ranking, or review-queue tooling exists anywhere
  in `scripts/`, `prosoc/`, or `.claude/skills/`. The closest precedent,
  `prosoc-card-audit-all`'s aggregation step
  (`.claude/skills/prosoc-card-audit-all/SKILL.md:125`), re-derives a
  summary via LLM file reads each run rather than a persisted/testable
  module — related but not a duplicate of a ranking engine.
- Sibling repos: None identified — LogicalRoboticsHarness is prosoc's
  control plane, not a normative-artifact consumer (established in the
  parent proposal).
- External libraries: None identified.
- Recommendation: Proceed.

### Demand search

- Work items: None found requesting this (`project/work_items/` holds only
  resolved Phase 0a–3 items).
- Proposals: None found — `PROP-NORMATIVE-PACKET-ASSEMBLY` Decision 7
  anticipated review/approval as future parallel work but didn't design it.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action — net-new, no closeout opportunity.

## Design Decisions

### Decision 1: Pilot vs. full corpus

**Question.** Promote the full 32-card corpus to `APPROVED` in one pass, or
prove the mechanism on a subset first?

**Chosen: pilot first.** Promote only the 5 `sample_packet` manifest cards
initially (charter, `asimov_three_laws`, `intersection_gesture_wait`,
`navigate_lead_agent`, `high_urgency` — all 5 already have `audit.md`,
independently verified). No card has ever reached `AUDITED` or `APPROVED`
before, so both the tooling and the human process are unproven; a small,
already-audited set bounds risk and produces the corpus's first
APPROVED-mode golden packet as a concrete, end-to-end proof. Full-corpus
promotion is offered follow-on work, not committed here.

### Decision 2: Skill stack, approver, and evidence gate

**Question.** Who approves, what evidence is required, and what tooling
performs the promotion?

**Chosen.** You (repo owner) are the sole approver — matches the
single-owner project and `workflow.md`'s "human accountability gate"
framing; no multi-reviewer process is invented. Evidence: `→AUDITED`
requires an `audit.md` with `verdict: ready` or `ready_with_fixes`
(`.claude/skills/prosoc-card-audit/SKILL.md:199-208`); `→APPROVED` requires
the card already be `AUDITED` and adds nothing evidentiary beyond it —
approval is an attestation, not a second content review.

Mechanism: three skills, following the project's established
`prosoc-<noun>-<verb>` / `-all` composition pattern (`prosoc-card-audit` /
`prosoc-card-audit-all`):

- **`prosoc-card-approve`** — mechanical, confirm-gated state-transition
  primitive: edits the fenced-YAML `state:`, runs
  `scripts/validate/status --fix`, regenerates the distilled YAML.
- **`prosoc-card-review`** — single-card human loop: loads the card +
  `audit.md` (runs `prosoc-card-audit` first if missing/stale), adds LLM
  recommendation/rationale beyond the audit, and on explicit human
  confirmation calls `prosoc-card-approve`.
- **`prosoc-card-review-all`** — corpus orchestrator: calls the Decision 3
  review-queue engine for the ranked worklist, walks it, invoking
  `prosoc-card-review` per card.

Options considered and rejected:

- Folding promotion into `prosoc-card-audit-all` — that skill explicitly
  states "Does not promote any card's STATE"
  (`.claude/skills/prosoc-card-audit-all/SKILL.md:239`), a boundary that
  exists because `workflow.md` Design Principle 4 ("Authorship, review, and
  empirical validation are distinct stages and should not be conflated,"
  `prosoc/scenarios/workflow.md:34-35`) is the same principle that split
  `AUDITED` from `APPROVED` in the first place — conflating them here would
  undo that split.
- A single monolithic review+approve skill — couples "give a
  recommendation" to "commit the promotion" with no reusable mechanical
  primitive for a human who's already decided and just wants to promote.

### Decision 3: Corpus review-queue engine

**Question.** How does a human find the next card to review, in what
order, and does the ordering also surface cards missing `audit.md`
entirely?

**Chosen: a deterministic script, not a skill-computed queue.** A new
`prosoc/utils/cards/review_queue.py` behind `scripts/validate/review-queue`
(same bash-wrapper-over-`python -m`-module shape as
`scripts/validate/status`), reusing three already-tested modules rather
than re-deriving corpus scanning:

- Cross-family discovery: the `FAMILIES` registry
  (`prosoc/utils/cards/validate_status.py:50`).
- Current state per card: `status.read_yaml_state`
  (`prosoc/utils/cards/status.py:122`).
- A numeric state-distance-from-`APPROVED` scope signal:
  `gate.PRODUCTION_ORDER` (`prosoc/packet/gate.py:17`).

Severity comes from `audit.md`'s existing frontmatter (`blocking` /
`should_fix` / `suggestion` counts); a card with **no** `audit.md` at all
sorts as highest-severity, which subsumes the coverage-gap question (4
cards) into the same ranked list rather than a separate manual decision.
Ranking order is a CLI flag (e.g. `--sort severity,scope --order
desc,asc`) — the tunable "simple knob." No hard dependency ordering (e.g.,
blocking scenario review until charter/constitutions are `APPROVED`) is
enforced — the engine informs priority, it doesn't gate.

Options considered and rejected:

- Skill-only re-derivation (the LLM re-scans the corpus each run, as
  `prosoc-card-audit-all` does today for aggregation) — non-deterministic,
  non-testable, re-parses the whole corpus every run at LLM cost, and
  duplicates already-tested modules for no benefit.
- No tooling — manual human triage — doesn't scale as the corpus grows and
  discards the severity/scope prioritization entirely.

### Decision 4: Viewer / worklist artifact form

**Question.** What form does the ranked worklist take — a live display, a
committed artifact, or a dashboard?

**Chosen: ephemeral, not a committed dashboard.** The engine emits JSON
(for skills) and a formatted table (for human display) live within a
`prosoc-card-review-all` run; nothing is committed by default. A review
queue is operational state that changes the instant one card is promoted —
unlike `AUDIT_SUMMARY.md`, a point-in-time record worth version-controlling,
a committed queue file would go stale mid-session with no CI backstop
(unlike the packet golden-file check in `.github/workflows/packet.yml`).
`prosoc-card-review-all` may optionally write an end-of-session Markdown
snapshot, mirroring `AUDIT_SUMMARY.md`'s point-in-time convention, not a
live dashboard.

Rejected: a rendered HTML dashboard — no repo precedent, disproportionate
for a 32-card corpus.

### Decision 5: Governance for new cards going forward

**Question.** What keeps future `DRAFTED` cards, or edits to already
`APPROVED` cards, from silently entering production packets?

**Chosen: unchanged from the parent proposal.** `--allow-unapproved` stays
the permanent dev-mode escape hatch (`PROP-NORMATIVE-PACKET-ASSEMBLY`
Decision 5) — it was already designed as permanent, not a bridge.
State-staleness/auto-regression on later content edits (an `APPROVED` card
silently re-edited without dropping its state) is an acknowledged gap,
deferred as an Open Question, not solved here.

## Non-Goals

- Does not itself audit the 4 coverage-gap cards (`asimov_four_laws`,
  `guidance_docent`, `public_navigation`, `routine_delivery`) — the engine
  surfaces them as highest priority; running `/prosoc-card-audit` against
  them is separate, deferred work.
- Does not promote the full 32-card corpus — pilot + reusable mechanism
  only.
- Does not change the assembler's gate logic, envelope shape, or
  `--allow-unapproved` semantics (already implemented).
- Does not build state-staleness/auto-regression detection.
- Does not edit `WS-NORMATIVE-PACKET-ASSEMBLY`'s exit-criterion wording or
  `project/focus/current_focus.md`.
- Does not add a multi-approver workflow.
- Does not enforce hard dependency ordering between families — ranking
  informs, doesn't gate.
- Does not add packet-centrality weighting to the initial ranking — noted
  as a future refinement once more manifests exist.
- Does not persist a continuously-live review-queue dashboard — only an
  optional end-of-session snapshot.

## Implementation Plan

Offered as work items against the existing, still-open
`WS-NORMATIVE-PACKET-ASSEMBLY`:

| WI | Content |
|---|---|
| WI 1 (tooling) | Build the review-queue engine (`prosoc/utils/cards/review_queue.py` + `scripts/validate/review-queue`, unit-tested per `tests/utils/cards/status_test.py` / `tests/packet/gate_test.py` precedent) and the three skills (`prosoc-card-approve`, `prosoc-card-review`, `prosoc-card-review-all`). |
| WI 2 (pilot) | Use `prosoc-card-review-all` to walk the 5 `sample_packet` cards `AUDITED`→`APPROVED`, regenerate `sample_packet`'s golden packet without `--allow-unapproved`. |
| Deferred, not committed | Audit the 4 gap cards (surfaced automatically at the top of the engine's ranking) and promote the remaining 27. |

## Open Questions

- Whether WI 1+2 alone satisfy `WS-NORMATIVE-PACKET-ASSEMBLY`'s exit
  criterion #2, or whether it requires full-corpus promotion — left to the
  user, possibly via editing the WS.
- State-staleness/auto-regression on edit — future work.
- Whether `project/focus/current_focus.md` and the WS prose need updating
  once this lands — deferred.
- Packet-centrality weighting in the ranking engine — deferred until more
  manifests exist to make it meaningful.

## Cross-References

- Governing parent proposal:
  `project/design/proposals/adopted/normative-packet-assembly/00_proposal.md`
  (`PROP-NORMATIVE-PACKET-ASSEMBLY`, adopted 2026-07-30).
- Governing workstream:
  `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
  (`WS-NORMATIVE-PACKET-ASSEMBLY`).
- Card lifecycle: `prosoc/scenarios/workflow.md`.
- Existing audit tooling: `.claude/skills/prosoc-card-audit/SKILL.md`,
  `.claude/skills/prosoc-card-audit-all/SKILL.md`.
- Reused modules: `prosoc/utils/cards/validate_status.py`,
  `prosoc/utils/cards/status.py`, `prosoc/packet/gate.py`.
