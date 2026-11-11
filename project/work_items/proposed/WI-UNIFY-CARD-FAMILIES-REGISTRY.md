---
resolution: null
blocked_reason: null
blocked: false
id: WI-UNIFY-CARD-FAMILIES-REGISTRY
title: "Unify the duplicate card-families registry in loader.py and validate_status.py"
type: operation
status: proposed
owner: anthony
contributors:
  - anthony
assigned_agents: []
related_focus: []
related_roadmap: []
related_workstreams: []
related_design: []
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
  - add_new_card_family
  - change_card_lifecycle_validation_behavior
  - modify_schema_json
acceptance:
  - "A single shared definition of each card family's common fields (name, default root, yaml_root_key, single/layout-support) exists, and both src/prosoc/nca/packet/loader.py's FAMILIES and src/prosoc/nca/utils/cards/validate_status.py's FAMILIES are built from it rather than independently hardcoded"
  - "No behavioral change: scripts/validate/status and scripts/assemble src/prosoc/manifests/sample_packet/manifest.yml produce identical output before and after, for every family scripts/validate/status covers"
  - "scripts/test passes with no new failures"
  - "lrh validate reports 0 errors"
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - src/prosoc/nca/packet/loader.py
  - src/prosoc/nca/utils/cards/validate_status.py
---

# WI-UNIFY-CARD-FAMILIES-REGISTRY

## Summary

Replace the two independently-maintained `FAMILIES` registries in
`src/prosoc/nca/packet/loader.py` (`PacketFamily`) and
`src/prosoc/nca/utils/cards/validate_status.py` (`Family`) with a single
shared source of truth for each card family's common identity (name,
default root directory, `yaml_root_key`, single-document/layout flags),
so the two consumer-specific fields (`schema_path`/`card_filename` for
the packet loader; `discover`/`supports_flat`/`label_by_stem` for the
status validator) are the only parts still defined per-consumer.

## Problem / Context

Both modules hardcode the same five card families (`scenarios`, `tasks`,
`contexts`, `constitutions`, `charter`), import the same `*_distill`
modules to derive each family's root, and separately encode the same two
special cases (`constitutions`'s root-wrapped YAML via `yaml_root_key`,
`charter`'s single-document layout). Nothing enforces the two registries
stay in sync — adding a family or changing one of these special cases
today means remembering to update both files. Flagged in
`project/design/backlog.md`'s "LRH card-architecture reuse assessment —
not yet warranted" section as "a real duplication today [that] doesn't
need a second consumer to justify fixing."

### Duplication search
- In-repo: Related: the duplication itself is
  `src/prosoc/nca/packet/loader.py:37-89` vs.
  `src/prosoc/nca/utils/cards/validate_status.py:40-111` — confirmed by
  direct reading, no third copy found elsewhere.
- Sibling repos: None identified.
- External libraries: None identified (domain-specific registry logic).
- Recommendation: Proceed.

### Demand search
- Work items: None found (checked all `WI-*FAMIL*` matches; only
  `WI-PACKET-MANIFEST-FAMILY`, unrelated).
- Proposals: None found.
- Backlog: Found — `project/design/backlog.md` § "LRH card-architecture
  reuse assessment — not yet warranted," closing "Related" bullet.
- Recommendation: Offer to remove that backlog bullet once this work
  item exists.

## Scope

- Extract the common per-family fields (name, default root,
  `yaml_root_key`, single-document/layout treatment) into one shared
  definition both modules consume.
- Keep each consumer's own specific fields (`schema_path`,
  `card_filename` for the loader; `discover`, `supports_flat`,
  `label_by_stem` for the status validator) defined per-consumer,
  layered on top of the shared base.
- Cover all families both registries already know about today (the five
  shared ones; `validate_status.py`'s extra `manifests` entry is
  unaffected since `loader.py` has no equivalent).

## Required Changes

1. Design and add a shared family-identity module (exact
   location/shape left to the implementor — see Open Questions) covering
   `name`, default root resolution (currently
   `pathlib.Path(<distill_module>.__file__).parent` in both places),
   `yaml_root_key`, and the single-document/charter special case.
2. Refactor `src/prosoc/nca/packet/loader.py`'s `_family()`/`FAMILIES` to
   build `PacketFamily` from the shared definition plus
   `schema_path`/`card_filename`.
3. Refactor `src/prosoc/nca/utils/cards/validate_status.py`'s `FAMILIES`
   to build `Family` from the shared definition plus
   `discover`/`supports_flat`/`label_by_stem`.
4. Remove the now-redundant hardcoded family lists from both files.

## Non-Goals

- Do not add a sixth family to `loader.py` (e.g. `manifests`) — out of
  scope.
- Do not change any card's lifecycle-validation behavior or schema.
- Do not pursue the broader LRH-reuse/extraction question from the same
  backlog section — this item is explicitly the piece the backlog note
  says doesn't need that larger question resolved first.

## Open Questions

- Where the shared definition should live (a new small module under
  `src/prosoc/nca/` vs. one of the two existing files importing from the
  other) is left to the implementor's judgment at implementation time.

## Acceptance Criteria

- A single shared definition of each family's common fields exists;
  both `FAMILIES` dicts are built from it.
- `scripts/validate/status` produces identical output before and after,
  for every family it covers.
- `scripts/assemble src/prosoc/manifests/sample_packet/manifest.yml`
  produces an identical assembled packet before and after (the only
  manifest currently in the repo).
- `scripts/test` passes with no new failures.
- `lrh validate` reports 0 errors.

## Validation

- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/validate/status` (before and after, diffed)
- `scripts/assemble src/prosoc/manifests/sample_packet/manifest.yml`
  (before and after, diffed)

## Risk Notes

- The two registries' special-case fields (`yaml_root_key`,
  single-document handling) must map identically after the refactor — a
  subtle mismatch here would silently break schema validation or status
  checking for `constitutions`/`charter` only, the two non-default cases.
