# Workstreams

Workstreams are LRH planning nodes for meaningful streams of work: they group
design, planning, work items, execution, review, and closeout for an effort
substantial enough that its context and sequencing should stay visible in
`project/`. Trivial fixes and obvious maintenance do not need one.

This is LRH's own convention, not a prosoc invention. The directory layout,
lifecycle vocabulary, and `WS-*` frontmatter schema come from LRH's own
`project/workstreams/`, and `lrh validate` and `lrh workstreams organize`
understand this structure. As with `project/design/proposals/`,
`lrh project init` does *not* scaffold it — the tree is created by hand when a
project first needs it, which is why it appeared in prosoc only when the first
workstream was written.

## The model

```text
Project → Workstream → Work Item
```

A workstream is a planning node; a work item is an executable leaf. A
workstream lists its work items in `work_items:`; each work item points back
via `related_workstreams:`. Bucket placement is a navigational projection, not
the source of truth — the frontmatter `status` is authoritative.

## Status buckets

`status` determines the subdirectory:

| `status` | Directory | Meaning |
|---|---|---|
| `proposed` | `proposed/` | being considered or designed |
| `active` | `active/` | currently being executed or reviewed |
| `resolved` | `resolved/` | completed and closed out |
| `abandoned` | `abandoned/` | intentionally stopped, rejected, or superseded |

`lrh validate` warns on a bucket/status mismatch; `lrh workstreams organize
--apply` moves files into the right bucket. Buckets are created on demand
rather than pre-created empty.

## Stage vs status

Two axes, like design proposals:

- **`status`** answers which bucket the workstream lives in (above).
- **`stage`** gives the fine-grained position within that status:
  `conceived` → `assessed` → `designed` → `planned` → `executing` →
  `reviewing` → `closed` (or `abandoned`).

A newly created workstream defaults to `stage: conceived`; use a later stage
only when it is already established (e.g. `designed` when a reviewed proposal
governs the work).

## Required frontmatter

`id` (must start with `WS-`, and the filename stem must match it), `kind:
planning_node`, `title`, `status`, and `stage`. List fields — `work_items`,
`related_design`, `related_focus`, `related_roadmap`, `exit_criteria`,
`children`, `execution_records`, `evidence` — must be lists when present, and
`lrh validate` enforces the schema.

## Relationship to the other lifecycles

A workstream's `status`/`stage` govern an engineering effort's progress. Keep
this separate from a design proposal's `status` (whether a design decision
governs — see [`../design/proposals/README.md`](../design/proposals/README.md))
and from a normative card's `STATE` (whether card content is fit for
downstream use — see `prosoc/scenarios/workflow.md`). A workstream can be
`active` while the proposal it implements is still `proposed` and the cards it
touches are still `DRAFTED`.

## Contents

- [`proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`](proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md)
  — implementation of the manifest-driven normative packet assembler
  (governed by
  [`../design/proposals/proposed/normative-packet-assembly/00_proposal.md`](../design/proposals/proposed/normative-packet-assembly/00_proposal.md)).
