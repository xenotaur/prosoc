---
id: PROP-NORMATIVE-PACKET-ASSEMBLY
type: design_proposal
title: Manifest-Driven Normative Packet Assembly
status: proposed
created_on: 2026-07-23
updated_on: 2026-07-23
implementation_status: not_started
implemented_by: []
supersedes: []
superseded_by: null
related_design:
  - prosoc/scenarios/workflow.md
  - prosoc/constitutions/README.md
  - project/focus/current_focus.md
---

# Manifest-Driven Normative Packet Assembly

## Summary

Defines how prosoc assembles normative cards — charter principles,
constitutions, tasks, contexts, and scenarios — into a single
machine-readable guidance packet for a downstream agent. A human-authored,
auditable manifest names the member cards; a deterministic engine resolves,
lifecycle-gates, and composes them into a signing-ready provenance envelope.

## Background / Motivation

The Prosocial Robot Navigation Charter paper specifies that a normative
card's machine-readable portion "should be combinable with other cards into
a single packet that is sent to a downstream intelligent system" (§3.3.3,
"Structurally Composable"), and Figure 5 depicts an assembled machine
payload spanning charter, principles, scenario, and task. No such tooling
exists. Each card family has a distiller (`prosoc/<family>/distill.py`) and
a JSON schema, but only the charter has a runtime loader; `prosoc/__init__.py`
is empty, and no module outside `prosoc/contexts/` or `prosoc/tasks/`
references either family. The corpus has the inputs to a packet and none of
the composition.

Three corpus facts constrain any design, and each is load-bearing below.

**The situation→cards edges are absent.** A scenario card references
`relevant_principles` and `related_scenarios`, but nothing pointing to a task
or a context card. `intended_robot_task` and the inline `context:` block are
free text, not references. The member set of a packet therefore cannot be
inferred by traversal today; it must be stated.

**Lifecycle state lives only in Markdown, in incompatible encodings.** A
card's `STATE` appears in its Markdown STATUS block but never in the
distilled YAML an assembler would read. Worse, the four families encode the
block four different ways (scenarios under `## Status`, tasks/contexts under
`## STATUS` with a `- **STATE:**` line, constitutions with the state fused
into the heading `## STATUS: EDITED <date>` and no `STATE:` line at all, and
the charter with no STATUS block whatsoever). A gate that parses Markdown
needs several parsers and still cannot read the charter.

**"Audited" is overloaded.** Agent-generated `prosoc/scenarios/<name>/audit.md`
files (produced by `/prosoc-scenario-audit`) are unrelated to the `AUDITED`
lifecycle state. Per `prosoc/scenarios/workflow.md` §4, `AUDITED` means "a
human reviewer has examined the scenario and judged it ready" — human
approval. The existence of an `audit.md` says nothing about whether a card is
`AUDITED`. No card in the corpus currently carries human approval, so a
strict gate emits nothing until the corpus is reviewed.

This work needs to be addressed now because it is the pivot between two
halves of the project: everything below the packet (authoring, distillation,
schema validation, agent auditing) is built and tested, and everything above
it (agent consumption, navigation) is blocked on there being a packet to
consume. It is also well-bounded — the schemas, the cross-reference fields,
and the charter loader pattern all already exist to build from.

## Prior Art Check

### Duplication search
- In-repo: No existing implementation found. `grep -rl` for
  `packet`/`manifest`/`provenance` across `prosoc/` and `.claude/skills/`
  returns nothing.
- Sibling repos: None identified. LogicalRoboticsHarness is prosoc's control
  plane, not a normative-artifact consumer.
- External libraries: None adoptable wholesale. in-toto/DSSE and SLSA
  provenance inform the envelope *shape* (Decision 5) but target build
  artifacts, not normative cards; their schemas are borrowed, their tooling
  is not.
- Recommendation: Proceed.

### Demand search
- Work items: None found. `project/work_items/` holds only three resolved
  scenario-tooling items; there is no `proposed/` bucket.
- Proposals: None found. This is the first proposal in the repo.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action. Note that `project/focus/current_focus.md`
  currently scopes the active focus to scenario-corpus maintenance; adopting
  this proposal opens a new front and that focus file likely wants updating.

## Design Decisions

### Decision 1: Lifecycle vocabulary

**Question.** The `AUDITED` state conflates two distinct review events —
agent auditing (already produced, via `audit.md`) and human approval (the
current meaning of `AUDITED`). How should the lifecycle distinguish them?

Options:
- **(A)** Rename `AUDITED` → `APPROVED`, keeping the existing number of
  states. Agent `audit.md` output remains without a lifecycle home.
- **(B)** Insert a distinct `APPROVED` state after `AUDITED`, so `AUDITED`
  becomes the agent-audit stage and `APPROVED` the human-approval stage.

**Chosen: (B).** It gives agent audits a real lifecycle stage, lets state
promotion to `AUDITED` be automated on evidence already produced, and yields
a *graded* packet gate (an `AUDITED` floor for development, `APPROVED` for
production) rather than a binary approved-or-bypassed decision. The cost is
that `AUDITED` narrows in meaning relative to the published Figure 3; since
the paper is in revision, this is a caption edit now rather than a permanent
mismatch. Paper edits required: Figure 3's Production arrow moves from
`AUDITED` to `APPROVED`, and §3.3.5's gating sentence ("cards will not be
used by downstream systems unless they have reached the state AUDITED")
changes `AUDITED` → `APPROVED`.

The resulting chain, using the repo's existing terms plus the new `APPROVED`:

```
SOURCE? → DRAFTED → EDITED → AUDITED → APPROVED → VALIDATED? → DEPRECATED/RETIRED
          (agent audits advance to AUDITED; a human advances to APPROVED)
```

`SOURCE` and `VALIDATED` are optional stages per `workflow.md`. See Open
Questions for the `VALIDATED`/`VERIFIED` naming split that Phase 0a must
resolve.

### Decision 2: Status source of truth

**Question.** Once `status` must appear in the machine-readable YAML (so the
gate can read it uniformly), how do the YAML and the human-facing Markdown
STATUS block stay in agreement?

Options:
- **(i)** Author `status` in the fenced YAML; project it into the Markdown
  STATUS block.
- **(ii)** Author in Markdown; have the distiller parse the prose into YAML.
- **(iii)** Author in both; have a validator enforce equality.

**Chosen: (i), with (iii) as a CI backstop.** Projection makes divergence
structurally impossible rather than merely detected, and follows the existing
precedent in `prosoc/scenarios/render_sections.py`, which already renders
prose sections from the distilled YAML and mechanically stamps the STATUS
block's `EDITED` line. Option (ii) needs a fragile prose parser across four
formats. The validator from (iii) is retained only to catch hand-edits to
generated regions.

Consequence for the packet: `status` lives in the card YAML, but the
assembler **strips it from the agent-facing payload** and relocates it into
the packet's provenance. The paper is explicit that the machine payload is
"deliberately a subset of the card, so that material… that could be
distracting to a downstream agent is excluded" (§3.3.5). The auditor needs
the state; the robot does not.

### Decision 3: Composition strategy

**Question.** How is the member set of a packet determined and combined?

Options:
- **(1)** Packets as a static sixth card family, each hand-authored.
- **(2)** A runtime assembler the caller drives directly with a member list.
- **(3)** Graph traversal that infers the member set from a scenario.
- **(4)** A human-authored manifest naming the members, resolved by a
  runtime engine (i.e. (2) with (1)'s auditable artifact as its input).

**Chosen: (4), with (2) as its engine.** Option (3) is disqualified today —
the scenario→task and scenario→context edges it would traverse do not exist
(Background), and creating them means re-opening 20 cards that have not yet
had a first human approval. Option (1) duplicates card content into every
packet and drifts when a card changes. Option (2) alone produces a build
artifact with no human-approved intermediary, a weaker form of the paper's
"auditable authority" (§3.3.1). Option (4) keeps derivation single-source
(the packet is generated, never hand-maintained) while making the manifest
the human-approved, auditable artifact that stands between the corpus and the
downstream agent. It migrates cleanly to (3) later: once scenario→task/context
edges exist, manifests can be generated instead of authored.

### Decision 4: Card loading

**Question.** How does the assembler load and validate each member card?

Options:
- **(a)** A per-family `loader.py` + `runtime.py` mirroring the charter's,
  for each of scenarios, tasks, contexts, constitutions (~8 modules).
- **(b)** One generic `CardLoader` over a small family registry.

**Chosen: (b).** It returns `LoadedCard(family, id, path, sha256, status,
payload: dict)` with the payload kept opaque. The assembler needs load →
schema-validate → state-check → embed-verbatim, not field-level access. Full
per-family Pydantic models would restate four rich schemas in a second
language and create a permanent drift surface — a hazard `charter/runtime.py`
itself warns about ("This module is NOT the source of truth for the charter
structure"). The generic loader preserves the repo's single-validation-gate
invariant ("This is the *only* place where schema validation should occur at
runtime", `charter/loader.py`) in ~120 lines rather than ~600. Rich models
are deferred until a real consumer needs field access. The charter keeps its
existing loader, which has a genuinely different rooted shape and its own
tests.

### Decision 5: Envelope shape

**Question.** How are the resolved card payloads combined into one artifact?

**Chosen.** A namespaced envelope, **never a deep merge** — `scenario.yml`
already has a top-level `context:` key (inline environment/social setting)
that would silently collide with the context card, and merging erases
provenance. The envelope is structured as an in-toto-style statement
(`_type` / `subject` / `predicate_type` / `predicate`) with a reserved,
DSSE-shaped `signatures: []` slot, so cryptographic signing is an additive
change later rather than a rework. Two audience-split sections:

- `guidance` — what the agent consumes; can be detached and shipped alone to
  a token-constrained planner. `subject.digest` covers the serialized
  `guidance` block only, so a detached copy stays verifiable against the
  envelope.
- `predicate` — what the auditor consumes: builder identity, and each
  resolved card's id, family, path, content hash, and lifecycle state (the
  SLSA "resolved dependencies" idea applied to normative cards).

The escape hatch is recorded **inside the payload**
(`predicate.policy.escape_hatch` plus a minimal `guidance.notice`), not
merely as a CLI flag. If the hatch existed only in the build log, a
development packet would be byte-indistinguishable downstream from a
production one — so a consuming system could not refuse it. The one
status-derived field allowed into the agent's view is this non-production
notice: "this guidance was not human-approved" is safety-relevant, not
distracting. Defaults are fail-closed per Saltzer & Schroeder (least
privilege / fail-safe defaults), and engaging the hatch requires a written
justification so intent is recorded rather than inferred.

The envelope also normalizes the families' differing root keys (constitutions
wrap under `constitution:`, the charter under `principles:`, the rest flat)
at assembly time, rather than re-authoring any card.

### Decision 6: Principle selection

**Question.** Which principles does a packet carry, given three families that
each reference principles?

**Chosen.** The union of `scenario.relevant_principles`,
`task.related_principles`, and `context.principle_emphasis.emphasized` — the
only clean cross-reference edge in the corpus (verified: zero dangling
principle references across all three families against charter P0–P9).
Principles a context marks `deprioritized` are **annotated, never dropped**:
silently removing a principle is a normative act, not a filter — the agent
would never learn the principle exists. Each principle carries an
`emphasis: emphasized | deprioritized | neutral` annotation instead. For the
same reason, `context.principle_emphasis.common_tensions` and
`constitution.conflict_resolution` are two independent mechanisms that may
disagree; the assembler surfaces both and reconciles neither, respecting the
paper's "interpretive locality" property (§3.3.4).

### Decision 7: Audit skill coverage

**Question.** The repo has scenario audit skills but none for constitutions,
contexts, tasks, or the charter. How is that gap filled?

Options:
- **(a)** Four per-family audit skills.
- **(b)** One family-dispatched `prosoc-card-audit` (+ `-audit-all`).

**Chosen: (b).** Per-family checklists live under
`.claude/skills/_shared/audit_checklists/<family>.md`; the shared audit
protocol lives in the skill body. This matches the existing
`prosoc-<noun>-<verb>` skill naming and the `_shared/` convention. Two
wrinkles are called out for the implementing work: the charter is not a
card-per-directory family (ten principles in one document) and needs a
bespoke audit shape, and constitutions have no `audit.md` precedent, so their
checklist is genuinely new. This is a parallel workstream — it gates how fast
the corpus reaches `APPROVED`, not whether the engine works.

## Non-Goals

- Does not implement cryptographic signing — `signatures: []` is a reserved,
  DSSE-shaped slot only.
- Does not add scenario→task or scenario→context reference fields, and does
  not implement Decision 3 Option (3) auto-resolution; both are deferred.
- Does not repair the dangling `example_scenarios` references on task cards
  (7 of 10 resolve to nothing). A validator surfaces them; fixing them is
  corpus work, and a dangling task→scenario link does not make a *packet*
  wrong.
- Does not define agent-side consumption of a packet, or any navigation
  algorithm.
- Does not alter the normative *substance* of any existing card — only the
  encoding of its STATUS block.
- Does not scaffold the `project/` paths `lrh project doctor` reports missing
  (`principles`, `goal`, `roadmap`, `evidence`, `status`); prosoc adds those
  on demand, not preemptively.

## Implementation Plan

Multi-stage; a governing workstream should own the individual work items. The
phases below are the intended delivery order, not a commitment to their
internal granularity.

| Phase | Content |
|---|---|
| 0a | Lifecycle enum (Decision 1); normalize STATUS blocks across all five families; add `status:` to the schemas; project into Markdown (Decision 2); `scripts/validate/status`. Landed **family-by-family, one commit per family** — schema + distiller + regenerated `.yml` together, each independently revertible with `lrh validate` green throughout. |
| 0b | `prosoc-card-audit` / `prosoc-card-audit-all` skills and per-family checklists; charter-specific audit (Decision 7). Parallel to 0a. |
| 1 | Engine: `resolve`, `gate` (fail-closed), generic `CardLoader` (Decision 4), `assemble`, `packet.schema.json`, the envelope (Decision 5). Ships behind `--allow-unapproved`, which stamps the non-production marker. |
| 2 | Manifest as an auditable card family (`manifest.md` + template + distiller + schema), so manifests get STATUS blocks and pass the audit skill. |
| 3 | CI drift check (`scripts/assemble --check`) against checked-in golden packets. |
| 4 | Deferred: signing; Decision 3 auto-resolution, once scenario→task/context edges exist. |

Phase 0a plus human approval of the corpus is what retires the
`--allow-unapproved` flag for production use.

## Open Questions

- **`VALIDATED` vs `VERIFIED` (blocks Phase 0a).** The repo's stage-5 term is
  inconsistent: `scenarios/workflow.md` §5 defines `VALIDATED` (empirical
  evidence — user studies, experiments), while `constitutions/template.md`
  and the paper's Figure 3 use `VERIFIED` (verified in production). These are
  arguably distinct concepts. Phase 0a's normalization must pick one canonical
  enum. Recommendation: keep `VALIDATED` (the term the scenario corpus
  actually uses, and semantically distinct from `APPROVED`), and treat
  `VERIFIED` as either an alias to retire or a separate production stage —
  decided when 0a lands, not here.
- **Paper-revision sequencing.** Decision 1's Figure 3 and §3.3.5 edits should
  land together with the repo change, but the Frontiers revision is externally
  scheduled.
- **Canonical design docs.** LRH's proposals convention assumes
  `project/design/design.md` and `architecture.md` exist as the documents a
  proposal folds into on adoption. Prosoc has neither. Whether to create them
  before proposals reference them is a separate scaffolding question.

## Cross-References

- Charter paper: *The Prosocial Robot Navigation Charter* (Francis), §3.3
  ("The Normative Card Architecture"), Figures 3 and 5.
- Card lifecycle: `prosoc/scenarios/workflow.md`.
- Existing projection precedent: `prosoc/scenarios/render_sections.py`.
- Single-validation-gate invariant: `prosoc/charter/loader.py`,
  `prosoc/charter/runtime.py`.
- Constitution card family: `prosoc/constitutions/README.md`.
- Provenance shape: in-toto Attestation Framework and DSSE; SLSA Provenance
  v1.0 (`buildDefinition` / `runDetails`, resolved dependencies with digests).
- Fail-safe defaults: Saltzer & Schroeder, "The Protection of Information in
  Computer Systems," Proc. IEEE 63(9), 1975.
