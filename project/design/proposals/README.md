# Design Proposals

This directory holds longer-form design proposals: architecture choices,
feature directions, and design decisions that need to be reviewed as a
coherent document rather than captured as a work item.

This is LRH's own convention, not a prosoc invention. The canonical
directory layout, lifecycle vocabulary, and frontmatter schema come from
LRH's own `project/design/proposals/`, and `lrh validate` and
`lrh design organize` both understand this structure. Note that
`lrh project init` does *not* scaffold it at any profile (`minimal`,
`prompt-workflow`, or `full`) — the directory is created by hand when a
project first needs it, which is why it appeared in prosoc only when the
first proposal was written.

Prosoc adapts rather than mirrors LRH's version. LRH's proposals README
refers throughout to `project/design/design.md`,
`project/design/architecture.md`, and `project/design/repository_spec.md`
as the canonical documents a proposal is measured against and eventually
folded into. Prosoc has none of those yet. Until it does, proposals here
stand on their own, and "adopting" a proposal means its decisions govern
future work directly rather than being merged into a canonical design doc.

## Proposal sets

A proposal set is a directory containing one or more design documents that
share an `id:` prefix and a single umbrella document:

```text
project/design/proposals/<bucket>/<slug>/
  00_proposal.md      # umbrella; no `parent:` field
  01_<topic>.md       # optional sub-proposal; `parent: PROP-<SLUG>`
  appendix_<x>.md     # optional appendix; `parent: PROP-<SLUG>`
  README.md           # optional reading-order index (ignored by the validator)
```

The slug should be stable and descriptive (`normative-packet-assembly`,
not `proposal-001`). Every document carries `type: design_proposal` in its
YAML frontmatter. IDs use the `PROP-*` prefix.

## Two lifecycle axes

Proposals track two independent things, and conflating them is the most
common authoring error:

- **`status`** — does this design decision govern the project?
  One of `proposed`, `adopted`, `superseded`, `rejected`. (`accepted` is a
  legacy spelling of `adopted`; the validator warns on it.)
- **`implementation_status`** — has the governed design been delivered?
  One of `not_started`, `partial`, `implemented`, `deferred`, `obsolete`.
  When `implemented`, back it with `implemented_by` work items and/or
  `evidence` links.

An adopted proposal governs future work even when nothing has been built
yet, so `status: adopted` with `implementation_status: not_started` is a
normal and meaningful combination.

## Buckets

`status` determines which subdirectory a proposal lives in:

| `status` | Directory |
|---|---|
| `proposed` | `proposed/` |
| `adopted` (or legacy `accepted`) | `adopted/` |
| `superseded` | `superseded/` |
| `rejected` | `rejected/` |

`lrh validate` warns on a bucket/status mismatch; `lrh design organize --apply`
moves files into the right bucket. Buckets are created when first needed
rather than pre-created empty — LRH's own repo carries only `proposed/` and
`adopted/` for the same reason.

## Not to be confused with the normative card lifecycle

Prosoc has a second, unrelated lifecycle. Normative cards — scenarios,
tasks, contexts, constitutions, and the charter — carry a `STATE` in their
Markdown STATUS block drawn from the workflow in
[`prosoc/scenarios/workflow.md`](../../../prosoc/scenarios/workflow.md)
(optional `SOURCE`, then `DRAFTED`, `EDITED`, `AUDITED`, optional
`VALIDATED`, and the terminal `DEPRECATED` / `RETIRED`). That axis governs
whether a *card's normative content* is fit to be used by a downstream
system.

The `status` field here governs whether an *engineering design decision*
about prosoc governs future work. The two never interact: a proposal can be
`adopted` while every card it describes is still `DRAFTED`, and a card can
be `AUDITED` with no proposal mentioning it at all. Keep the vocabularies
separate — in particular, "audited" in the card lifecycle means human
review of normative content, and has nothing to do with a proposal's state
or with the engineering reports in [`project/audits/`](../../audits/README.md).

## Contents

No proposals have landed yet. This README establishes the convention; the
first proposal set follows in a separate change.
