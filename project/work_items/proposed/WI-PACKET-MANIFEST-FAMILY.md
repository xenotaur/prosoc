---
resolution: null
blocked_reason: null
blocked: false
id: WI-PACKET-MANIFEST-FAMILY
title: Manifest as an auditable card family (Phase 2)
type: deliverable
status: proposed
assigned_agents: []
related_focus:
  - FOCUS-NORMATIVE-PACKET-ASSEMBLY
related_roadmap: []
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/proposed/normative-packet-assembly/00_proposal.md
depends_on:
  - WI-PACKET-ASSEMBLER-ENGINE
  - WI-CARD-AUDIT-SKILLS
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
  - add_manifest_to_packet_loader_families
  - implement_ci_drift_check
acceptance:
  - The manifest family (prosoc/manifests/) schema-validates and distills a manifest.md into manifest.yml, following the same literate/schema-validated pattern as every other card family
  - scripts/validate/status covers a sixth family (manifests) alongside the existing five, all consistent
  - prosoc-card-audit produces a findings-only audit.md for a manifest card via a new manifests checklist, without editing the card or promoting its STATE
  - scripts/assemble continues to work unchanged, now pointed at a manifest card's distilled manifest.yml instead of an ad-hoc YAML file
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/manifests/schema.json
  - prosoc/manifests/template.md
  - prosoc/manifests/distill.py
  - prosoc/manifests/sample_packet/manifest.md
  - prosoc/manifests/sample_packet/manifest.yml
  - prosoc/utils/cards/validate_status.py
  - .claude/skills/_shared/audit_checklists/manifests.md
  - .claude/skills/prosoc-card-audit/SKILL.md
  - .claude/skills/prosoc-card-audit-all/SKILL.md
  - prosoc/packet/examples/ (sample_manifest.yml removed, migrated)
---

# WI-PACKET-MANIFEST-FAMILY

## Summary

Turn the manifest from Phase 1's plain YAML input into a sixth, genuinely
auditable card family: `prosoc/manifests/<id>/manifest.md` + `manifest.yml`,
with its own `schema.json`, `template.md`, and `distill.py` — mirroring every
other family (scenarios, tasks, contexts, constitutions, charter). Extends
the Phase 0a lifecycle-state contract and the Phase 0b audit skills to cover
it, per the proposal's Phase 2 line: "the manifest as an auditable card
family... so manifests get STATUS blocks and pass the audit skill."

## Problem / Context

Phase 1's `prosoc/packet/manifest.py` reads a plain YAML manifest (`builder` +
`members[]`) with no `id`, `name`, `state`, schema, or STATUS block — it is
not a card by any of the conventions the other five families follow, and it
cannot be audited by `prosoc-card-audit` or tracked by
`scripts/validate/status`. This WI closes that gap.

Unlike Phases 0b and 1, the governing proposal has **no dedicated numbered
Decision for Phase 2** — it appears only as one row in the Implementation
Plan table. The design questions below are settled here, not inherited from
the proposal.

### Duplication search
- In-repo: No existing manifest-family scaffolding. `prosoc/packet/manifest.py`
  (Phase 1) is the closest precedent and is extended, not duplicated —
  verified its `parse_manifest` already ignores unrecognized top-level keys,
  so adding `id`/`name`/`state` requires zero changes there.
- Sibling repos: None identified.
- External libraries: Not applicable.
- Recommendation: Proceed.

### Demand search
- Work items: None found. `WI-PACKET-ASSEMBLER-ENGINE` (resolved, Phase 1)
  and `WI-CARD-AUDIT-SKILLS` (resolved, Phase 0b) are the predecessors this
  builds on.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` governs this item (Phase 2 row;
  no dedicated Decision).
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

New `prosoc/manifests/` card family plus registrations of that family into
the two existing generic status/audit systems. No `prosoc/packet/` code
changes (verified unnecessary — see Required Change 1).

## Required Changes

1. **`prosoc/manifests/schema.json`** — flat shape (not root-wrapped, like
   tasks/contexts, not constitutions): `id`, `name`, `state` (the canonical
   7-value enum), `builder` (optional string), `members` (non-empty array of
   `{family, id}`). This is exactly Phase 1's `builder`/`members` shape plus
   `id`/`name`/`state` — `prosoc/packet/manifest.py`'s `parse_manifest`
   already tolerates the extra keys, so no engine-side change is needed.
2. **`prosoc/manifests/template.md`** — mirrors the tasks/contexts template
   pattern: a `## STATUS` block with a `- **STATE:**` first bullet (per
   `prosoc/scenarios/workflow.md`'s Status Section Template), Required
   sections for the human-readable fields, and a fenced `## Manifest
   Specification (Machine-Readable)` YAML block matching the schema.
3. **`prosoc/manifests/distill.py`** — directory-layout discoverer
   (`prosoc/manifests/<id>/manifest.md` -> `manifest.yml`), following the
   `discover_directory_layout` pattern from `prosoc/tasks/distill.py` /
   `prosoc/contexts/distill.py`. Uses the generic `compiler.compile_file`
   (top-level, `root_key=None`) since the shape is flat, not aggregating.
4. **`prosoc/manifests/sample_packet/manifest.md`** — migrate
   `prosoc/packet/examples/sample_manifest.yml`'s content into a real,
   first manifest card (human-readable prose plus the fenced YAML payload),
   then remove the old ad-hoc example so there is one manifest concept, not
   two. Regenerate `manifest.yml` via the new distiller.
5. **`prosoc/utils/cards/validate_status.py`**: register `manifests` in the
   `FAMILIES` registry (flat, `yaml_root_key=None`, directory-layout
   discovery) so `scripts/validate/status` covers a sixth family.
6. **`.claude/skills/_shared/audit_checklists/manifests.md`**: new checklist
   — required fields, `members[].family` validity (must be one of the five
   content families, never `manifests` itself — a manifest cannot name
   another manifest as a member), `members[].id` resolvability per-family,
   no duplicate members, completeness.
7. **`.claude/skills/prosoc-card-audit/SKILL.md`** and
   **`prosoc-card-audit-all/SKILL.md`**: add `manifests` to the family
   tables (Reference Knowledge, Step 1's locate table, `-all`'s Step 2
   enumeration table).

## Non-Goals

- Does not add `manifests` to `prosoc/packet/loader.py`'s five-family
  registry — a manifest is the control/input artifact `resolve` consumes
  directly to build a packet; it is never itself embedded as `guidance`
  content inside another packet. The packet loader stays five families.
- Does not implement the CI drift check (`scripts/assemble --check` against
  checked-in golden packets) — that is Phase 3, a separate work item.
- Does not change `prosoc/packet/`'s engine code (`loader.py`, `resolve.py`,
  `gate.py`, `assemble.py`, `cli.py`) — verified unnecessary.
- Does not promote any card's STATE, or edit any existing card's normative
  content.
- Does not build a `prosoc-manifest-new` authoring skill (a
  `prosoc-scenario-new` equivalent) — out of scope for this WI.

## Acceptance Criteria

- The manifest family (`prosoc/manifests/`) schema-validates and distills a
  `manifest.md` into `manifest.yml`, following the same literate/
  schema-validated pattern as every other card family.
- `scripts/validate/status` covers a sixth family (`manifests`) alongside the
  existing five, all consistent.
- `prosoc-card-audit` produces a findings-only `audit.md` for a manifest card
  via the new `manifests` checklist, without editing the card or promoting
  its STATE.
- `scripts/assemble` continues to work unchanged, now pointed at a manifest
  card's distilled `manifest.yml` instead of an ad-hoc YAML file.

## Validation

- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/validate/status` (all 6 families)
- `python -m prosoc.manifests.distill --dry-run --show-diffs`
- Manually invoke `prosoc-card-audit` against `sample_packet` (manifests) and
  confirm a findings-only `audit.md` with no card/STATE mutation.
- `scripts/assemble prosoc/manifests/sample_packet/manifest.yml
  --allow-unapproved "<why>"` still emits a valid packet (corpus is
  currently all-DRAFTED, so the default fail-closed gate is expected to
  emit nothing).

## Risk Notes

- The manifest schema must forbid `members[].family: manifests` — allowing a
  manifest to name another manifest as a member would make `resolve`
  recursive in a way `prosoc/packet/` was never designed for (see Non-Goals).
  Enforce this in the checklist and, if practical, in `schema.json` itself
  (an `enum` on `members[].family` excluding `manifests`).
- Migrating `sample_manifest.yml` into a real card changes its path
  (`prosoc/packet/examples/` -> `prosoc/manifests/sample_packet/`) — update
  the one place that references the old path
  (`prosoc/packet/README.md`'s Usage examples) so the documented command
  still works.
- Keep the distiller genuinely mirroring tasks/contexts (directory-layout,
  flat, `root_key=None`) rather than inventing a new pattern — the whole
  point of this WI is uniformity with the established five families.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
  (Phase 2).
- Design: `project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`
  (Implementation Plan, Phase 2 row).
