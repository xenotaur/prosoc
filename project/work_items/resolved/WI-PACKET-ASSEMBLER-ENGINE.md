---
resolution: Implemented and merged in PR #51 (commit 308da1f); the Phase 1 engine (prosoc/packet/ + scripts/assemble) produces a namespaced, fail-closed provenance packet from a manifest, with the --allow-unapproved escape hatch stamped into the payload.
blocked_reason: null
blocked: false
id: WI-PACKET-ASSEMBLER-ENGINE
title: Normative packet assembler engine — resolve, fail-closed gate, generic loader, envelope (Phase 1)
type: deliverable
status: resolved
assigned_agents: []
related_focus:
  - FOCUS-NORMATIVE-PACKET-ASSEMBLY
related_roadmap: []
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/proposed/normative-packet-assembly/00_proposal.md
depends_on:
  - WI-CARD-STATUS-CHARTER
blocked_by: []
expected_actions:
  - create_file
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - implement_cryptographic_signing
  - implement_manifest_card_family
  - implement_ci_drift_check
  - add_scenario_task_context_edges
  - edit_card_normative_content
acceptance:
  - A generic CardLoader loads all five families named in a manifest into LoadedCard(family, id, path, sha256, state, payload) through the single schema-validation gate; constitutions' root-wrapped and the charter's principles-rooted shapes both load
  - scripts/assemble emits a namespaced in-toto-style envelope (guidance + predicate, reserved signatures [], subject.digest over the serialized guidance only) that validates against prosoc/packet/schema.json; state is stripped from guidance and recorded per-card in predicate; principles are the Decision-6 union with emphasis annotations and none dropped
  - The gate is fail-closed by default (emits nothing when any member is below the APPROVED threshold); --allow-unapproved lowers the floor and stamps predicate.policy.escape_hatch plus a guidance.notice into the payload, not just the build log
  - lrh validate, scripts/lint, scripts/test, and scripts/format --check all pass; scripts/assemble is a python -m wrapper; no normative card content changed
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/packet/__init__.py
  - prosoc/packet/loader.py
  - prosoc/packet/resolve.py
  - prosoc/packet/gate.py
  - prosoc/packet/assemble.py
  - prosoc/packet/schema.json
  - scripts/assemble
  - tests/packet/
---

# WI-PACKET-ASSEMBLER-ENGINE

## Summary

Build the Phase 1 assembler engine from `PROP-NORMATIVE-PACKET-ASSEMBLY`: turn a
human-authored manifest into a single machine-readable guidance packet via a
generic `CardLoader`, manifest `resolve`, a fail-closed lifecycle `gate`, and
`assemble` into a namespaced, in-toto-style provenance envelope validated by
`prosoc/packet/schema.json`. Ships behind `--allow-unapproved`. This is the core
deliverable the workstream is built toward; Phase 0a (now complete) supplies the
machine-readable `state` the gate reads uniformly across all five families.

## Problem / Context

The charter paper (§3.3.3, Figure 5) specifies that a card's machine-readable
payload "should be combinable with other cards into a single packet"; no such
tooling exists. Each family has a distiller and a JSON schema, and — after
Phase 0a — a top-level machine-readable `state`. What is missing is the
composition: load → gate → assemble.

The proposal settles the design; this WI implements **Phase 1** of its
Implementation Plan (the engine), leaving Phases 0b/2/3/4 to other work items.
Three corpus facts were re-verified against the distilled YAML before scoping:

- The **`context:` collision is real**: `scenario.yml` has a top-level inline
  `context:` key that would silently collide with a context card — so the
  envelope must be **namespaced, never deep-merged** (Decision 5).
- The **Decision-6 principle edges exist and are clean**: `relevant_principles`
  (scenario), `related_principles` (task), and `principle_emphasis.emphasized`
  / `deprioritized` / `common_tensions` (context) are all present; constitutions
  carry `conflict_resolution` (root-wrapped under `constitution:`).
- Families have **different root shapes**: constitutions wrap under
  `constitution:`, the charter under `principles:`, the rest are flat — the
  loader/envelope must normalize this at assembly time, not by re-authoring.

### Duplication search
- In-repo: No packet/assembler/manifest code (`find prosoc -iname '*assembl*' -o
  -iname '*packet*' -o -iname '*manifest*'` returns nothing). The proposal's
  prior-art check reached the same verdict. Greenfield `prosoc/packet/`.
- Sibling repos: None. LogicalRoboticsHarness is the control plane, not a
  normative-artifact consumer.
- External libraries: in-toto/DSSE and SLSA inform the envelope *shape* only
  (schemas borrowed, tooling not adopted).
- Recommendation: Proceed.

### Demand search
- Work items: None; the resolved Phase 0a `WI-CARD-STATUS-*` items are the
  predecessors this builds on.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` governs this item.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

Phase 1 only, in a new `prosoc/packet/` package plus a `scripts/assemble`
bash wrapper calling `python -m prosoc.packet...` (per the repo's `python -m`
script convention). The parts are one unit: none emits a packet alone, so they
are delivered together rather than sliced.

## Required Changes

1. **`prosoc/packet/loader.py`** — a generic `CardLoader` over a small family
   registry (Decision 4b). Returns `LoadedCard(family, id, path, sha256, state,
   payload: dict)` with the payload kept **opaque** (no per-family Pydantic
   models — avoids restating four schemas and the drift surface
   `charter/runtime.py` warns about). Flow per card: locate → schema-validate
   (reusing each family's existing schema; this stays the single runtime
   validation gate) → read `state` (handling constitutions' `constitution.state`
   and the charter's top-level `state`) → compute `sha256` of the card source.
   The charter keeps its own `loader.py`; the registry adapts its rooted shape.
2. **Minimal manifest input** — a plain YAML file naming members as `family` +
   `id` (and an optional builder identity). The full card-family treatment
   (STATUS block, schema, audit skill) is **Phase 2** and is out of scope here;
   define only what `resolve` needs.
3. **`prosoc/packet/resolve.py`** — `resolve(manifest) -> list[LoadedCard]`,
   preserving manifest order and raising a clear error on a member that does not
   resolve to a card.
4. **`prosoc/packet/gate.py`** — a fail-closed lifecycle gate. Default threshold
   `APPROVED`; if any member is below threshold the assembler **emits nothing**.
   `--allow-unapproved` lowers the floor **and** records the bypass *in the
   payload*: `predicate.policy.escape_hatch` (with the written justification)
   plus a minimal `guidance.notice` ("this guidance was not human-approved"), so
   a development packet is not byte-indistinguishable from a production one
   (Decision 5, Saltzer & Schroeder fail-safe defaults).
5. **`prosoc/packet/assemble.py`** — compose resolved payloads into a
   **namespaced** envelope (never a deep merge). Structure it as an in-toto-style
   statement (`_type` / `subject` / `predicate_type` / `predicate`) with a
   reserved, DSSE-shaped `signatures: []` slot. Two audience-split sections:
   - `guidance` — agent-facing. `state` stripped from every card; family root
     keys normalized; principles are the **union** of
     `scenario.relevant_principles`, `task.related_principles`, and
     `context.principle_emphasis.emphasized`, each annotated
     `emphasis: emphasized | deprioritized | neutral` — a `deprioritized`
     principle is **annotated, never dropped**. `context.common_tensions` and
     `constitution.conflict_resolution` are **both surfaced, reconciled by
     neither** (interpretive locality, §3.3.4). `subject.digest` covers the
     serialized `guidance` block only, so a detached `guidance` stays verifiable.
   - `predicate` — auditor-facing: builder identity and, per resolved card, its
     `id`, `family`, `path`, `sha256`, and lifecycle `state`.
6. **`prosoc/packet/schema.json`** — the packet schema for the envelope;
   `assemble` validates its output against it before writing.
7. **`scripts/assemble`** — bash wrapper → `python -m prosoc.packet.assemble`
   (or a `prosoc.packet.cli`), taking a manifest path and `--allow-unapproved`
   with a required justification string.
8. **`tests/packet/`** — cover loader (all five families, sha256, state read,
   schema-invalid rejection), resolve (order, dangling member), gate (fail-closed
   default, escape-hatch stamping), assemble (namespacing/no-collision on the
   `scenario.context:` case, state stripped from guidance and present in
   predicate, principle union + emphasis annotations, both tension mechanisms
   surfaced, `subject.digest` over guidance), and schema validity — with a
   checked-in sample manifest as a golden input.

## Non-Goals

- No cryptographic signing — `signatures: []` is a reserved DSSE-shaped slot
  only.
- No manifest **card family** (`manifest.md` + template + distiller + schema) —
  that is Phase 2; this WI uses a minimal manifest input.
- No CI drift check against golden packets — Phase 3.
- No scenario->task or scenario->context reference fields, and no Decision-3
  auto-resolution of the member set — deferred.
- Does not repair the dangling `example_scenarios` task references; a validator
  may surface them, but a dangling task->scenario link does not make a *packet*
  wrong.
- No agent-side consumption or navigation algorithm.
- Does not change the normative substance of any card — only reads distilled
  payloads.

## Acceptance Criteria

- A generic `CardLoader` loads all five families named in a manifest into
  `LoadedCard(family, id, path, sha256, state, payload)` through the single
  schema-validation gate; constitutions' root-wrapped and the charter's
  `principles:`-rooted shapes both load.
- `scripts/assemble` emits a namespaced in-toto-style envelope (`guidance` +
  `predicate`, reserved `signatures: []`, `subject.digest` over the serialized
  `guidance` only) that validates against `prosoc/packet/schema.json`; `state` is
  stripped from `guidance` and recorded per-card in `predicate`; principles are
  the Decision-6 union with emphasis annotations and none dropped.
- The gate is fail-closed by default (emits nothing when any member is below the
  `APPROVED` threshold); `--allow-unapproved` lowers the floor and stamps
  `predicate.policy.escape_hatch` plus a `guidance.notice` into the payload,
  not just the build log.
- `lrh validate`, `scripts/lint`, `scripts/test`, and `scripts/format --check`
  all pass; `scripts/assemble` is a `python -m` wrapper; no normative card
  content changed.

## Validation

- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/validate/status`
- `scripts/assemble <sample-manifest>` (fail-closed: emits nothing on the
  current all-DRAFTED corpus)
- `scripts/assemble <sample-manifest> --allow-unapproved "<justification>"`
  (emits an envelope; verify the escape-hatch marker is in the payload)
- `python -m prosoc.packet.assemble --help`

## Risk Notes

- **Fail-closed by construction.** No card in the corpus is `APPROVED` yet, so
  the default gate emits nothing — tests must drive the happy path via
  `--allow-unapproved` or fixture cards at a higher state. This is expected, not
  a bug.
- **Namespacing is load-bearing.** The `scenario.context:` collision means a
  deep merge silently corrupts the packet; assemble must namespace by
  family/id. A regression test on that exact collision is required.
- **Single validation gate.** Keep schema validation in the loader only; do not
  add a second parallel validation path (`charter/loader.py` invariant).
- **Charter shape.** The charter is one document with `principles:` at the top
  and now a top-level `state`; the loader must read it without assuming the
  card-per-directory `<id>.yml` layout the other families use.
- **State encodings.** After Phase 0a, state is top-level for scenarios/tasks/
  contexts/charter but nested under `constitution.state` for constitutions;
  reuse `prosoc/utils/cards/status.read_yaml_state(..., root_key=...)` rather
  than re-implementing.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
  (Phase 1).
- Design: `project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`
  (Decisions 2, 4, 5, 6; Implementation Plan Phase 1).
