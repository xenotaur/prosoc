---
resolution: null
blocked_reason: null
blocked: false
id: WI-CARD-APPROVE-SKILLS
title: Corpus review-queue engine and prosoc-card-approve / prosoc-card-review / prosoc-card-review-all skills
type: deliverable
status: proposed
assigned_agents: []
related_focus:
  - FOCUS-NORMATIVE-PACKET-ASSEMBLY
related_roadmap: []
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/proposed/normative-card-approval/00_proposal.md
depends_on: []
blocked_by: []
expected_actions:
  - create_file
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - promote_card_state
  - edit_card_normative_content
  - modify_packet_gate_logic
  - modify_packet_envelope_shape
acceptance:
  - "scripts/validate/review-queue runs against the full corpus and emits a ranked worklist (JSON + human-readable table) sorted by configurable --sort/--order flags"
  - "prosoc/utils/cards/review_queue.py has passing unit tests covering severity/scope computation and audit-less-card highest-priority sorting"
  - "prosoc-card-approve, prosoc-card-review, prosoc-card-review-all all exist under .claude/skills/ with SKILL.md following the prosoc-<noun>-<verb> pattern"
  - "prosoc-card-approve is confirm-gated and enforces the audit.md verdict gate for ->AUDITED and the AUDITED-state precondition for ->APPROVED"
  - "lrh validate reports 0 errors after all files are written"
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/utils/cards/review_queue.py
  - tests/utils/cards/review_queue_test.py
  - scripts/validate/review-queue
  - .claude/skills/prosoc-card-approve/SKILL.md
  - .claude/skills/prosoc-card-review/SKILL.md
  - .claude/skills/prosoc-card-review-all/SKILL.md
---

# WI-CARD-APPROVE-SKILLS

## Summary

Build a deterministic corpus review-queue engine (`prosoc/utils/cards/review_queue.py`
+ `scripts/validate/review-queue`) and three skills — `prosoc-card-approve`,
`prosoc-card-review`, `prosoc-card-review-all` — that together let a human
reviewer find, review, and promote prosoc normative cards from `AUDITED` to
`APPROVED`.

## Problem / Context

No tooling exists to promote a prosoc normative card's lifecycle state, and
no tooling exists to rank the 32-card corpus by what most needs review.
`WS-NORMATIVE-PACKET-ASSEMBLY`'s second exit criterion requires the corpus
to reach `APPROVED`, but every implementation work item so far explicitly
forbade `promote_card_state`. `PROP-NORMATIVE-CARD-APPROVAL` Decisions 2–4
settle the design this item builds: a three-skill stack following the
project's existing `prosoc-card-audit` / `-all` composition pattern, and a
deterministic ranking engine reusing three already-tested modules rather
than re-deriving corpus scanning.

### Duplication search
- In-repo: no promotion, ranking, or review-queue tooling exists anywhere
  in `scripts/`, `prosoc/`, or `.claude/skills/` — confirmed via `grep` for
  `review_queue`, `prosoc-card-approve`, `prosoc-card-review`.
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed.

### Demand search
- Work items: None found (`WI-SCENARIO-DISTILL-REVIEW-FOLLOWUP` is an
  unrelated distiller-review item).
- Proposals: `PROP-NORMATIVE-CARD-APPROVAL` — this item implements its
  Decisions 2–4; not a duplicate.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

- Implement the review-queue engine as a testable Python module + thin
  bash CLI wrapper, no skill-computed ranking.
- Implement three new skills under `.claude/skills/`.
- Add unit tests for the engine.
- Does not touch any actual card's content or state (see Non-Goals).

## Required Changes

1. **`prosoc/utils/cards/review_queue.py`** — reuses
   `prosoc/utils/cards/validate_status.py`'s `FAMILIES` registry (line 50)
   for cross-family card discovery, `prosoc/utils/cards/status.py`'s
   `read_yaml_state` (line 122) for current state, and
   `prosoc/packet/gate.py`'s `PRODUCTION_ORDER` (line 17) for a
   state-distance-from-`APPROVED` scope signal. Severity is computed from
   `audit.md` frontmatter (`blocking`/`should_fix`/`suggestion` counts); a
   card with no `audit.md` at all sorts as highest-severity. Ranking order
   is a CLI flag (e.g. `--sort severity,scope --order desc,asc`).
2. **`scripts/validate/review-queue`** — thin bash wrapper over
   `python -m prosoc.utils.cards.review_queue`, matching
   `scripts/validate/status`'s shape.
3. **`tests/utils/cards/review_queue_test.py`** — unit tests per the
   precedent at `tests/utils/cards/status_test.py` and
   `tests/packet/gate_test.py`.
4. **`.claude/skills/prosoc-card-approve/SKILL.md`** — mechanical,
   confirm-gated state-transition primitive: edits the fenced-YAML
   `state:`, runs `scripts/validate/status --fix`, regenerates the
   distilled YAML. Requires `audit.md` verdict `ready`/`ready_with_fixes`
   for `→AUDITED`; requires state already `AUDITED` for `→APPROVED` (no
   additional evidence beyond that).
5. **`.claude/skills/prosoc-card-review/SKILL.md`** — single-card human
   loop: loads the card + `audit.md` (runs `prosoc-card-audit` first if
   missing/stale), adds an LLM recommendation/rationale beyond the audit,
   and on explicit human confirmation calls `prosoc-card-approve`.
6. **`.claude/skills/prosoc-card-review-all/SKILL.md`** — corpus
   orchestrator: calls `scripts/validate/review-queue` for the ranked
   worklist, walks it, invoking `prosoc-card-review` per card. May
   optionally write an end-of-session Markdown snapshot mirroring
   `AUDIT_SUMMARY.md`'s point-in-time convention — not a live dashboard.

## Non-Goals

- Does not promote any actual card's state — that is `WI-CARD-APPROVAL-PILOT`
  (the follow-on pilot item), which uses this tooling on 5 real cards.
- Does not audit the 4 coverage-gap cards (`asimov_four_laws`,
  `guidance_docent`, `public_navigation`, `routine_delivery`) — separate
  `prosoc-card-audit` work.
- Does not change the packet assembler's gate logic, envelope shape, or
  `--allow-unapproved` semantics.
- Does not add packet-centrality weighting to the ranking — noted as a
  future refinement in the governing proposal.
- Does not build a continuously-live review-queue dashboard.

## Acceptance Criteria

- `scripts/validate/review-queue` runs against the full corpus and emits a
  ranked worklist (JSON + table) sorted by configurable flags.
- `prosoc/utils/cards/review_queue.py` has passing unit tests covering
  severity/scope computation and audit-less-card highest-priority sorting.
- `prosoc-card-approve`, `prosoc-card-review`, `prosoc-card-review-all` all
  exist under `.claude/skills/` following the `prosoc-<noun>-<verb>` /
  `-all` pattern.
- `prosoc-card-approve` is confirm-gated and enforces the evidence gates
  from `PROP-NORMATIVE-CARD-APPROVAL` Decision 2.
- `lrh validate` reports 0 errors after all files are written.

## Validation

- `scripts/version tools`
- `lrh validate`
- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `scripts/validate/review-queue` (manual invocation against the live corpus)

## Risk Notes

- The review-queue engine's severity/scope weighting is a design choice
  baked into code (per the proposal's Decision 3) — if the ranking proves
  unhelpful in practice during the pilot, revisiting the weighting is
  cheap (it's isolated in one function) but should be flagged rather than
  silently tuned.
- `prosoc-card-review`'s "runs `prosoc-card-audit` first if missing/stale"
  behavior needs a clear staleness definition (e.g. card content hash vs.
  `audit.md`'s `audited:` date) — under-specified in the proposal; resolve
  during implementation rather than guessing.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
- Design: `project/design/proposals/proposed/normative-card-approval/00_proposal.md`
  (Decisions 2, 3, and 4)
