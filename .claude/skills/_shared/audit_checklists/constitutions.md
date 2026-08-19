# Prosoc Constitution Audit Checklist

This is a verification rubric, companion to `src/prosoc/constitutions/schema.json` and
`src/prosoc/constitutions/template.md`. It explains what to check when auditing an
already-drafted constitution card. Unlike scenarios/tasks/contexts, no prior
`audit.md` precedent exists for constitutions — this checklist is new, grounded
directly in the schema and template. Read `../principles.md` for the P0–P9
definitions referenced below.

## Structural Shape (unique to this family)

Constitutions are **root-wrapped**: the fenced YAML is `{constitution: {...}}`, not
a top-level mapping. Before checking anything else:

- [ ] The fenced YAML block's top-level (and only) key is `constitution`
- [ ] `constitution.yml` mirrors the same root-wrapped shape (confirm with
      `prosoc.nca.utils.cards.status.read_yaml_state(path, root_key="constitution")` if
      in doubt, rather than assuming top-level `state`)

## Required Fields (schema.json, inside `constitution:`)

| Field | Check |
|-------|-------|
| `id` | Matches the directory name |
| `name` | Matches the card's title heading (`# Constitution Card: <TITLE>`) |
| `rules` | Non-empty array |
| `rules[].id` | Stable, referenced consistently (e.g. `L1`, `C1`) — check for
  duplicate ids within the same constitution |
| `rules[].text` | A single, testable normative statement — flag a rule that bundles
  multiple distinct obligations into one `text` |
| `rules[].type` | One of `must`, `must_not`, `should` — matches the rule's actual
  phrasing (a `text` phrased as prohibition but typed `must` is a mismatch) |
| `rules[].priority` | One of `high`, `medium`, `low` |

## Prose/YAML Cross-Checks

| Prose section | Cross-check against YAML field(s) |
|---|---|
| Overview | `constitution.name`, `constitution.scope` (if present) |
| Provenance | `constitution.id` naming, STATUS block's `SOURCE` |
| Normative Payload (the fenced YAML itself, embedded in prose) | must match `constitution.yml` exactly (re-distill and diff, as in the scenario checklist's dry-run pattern, rather than comparing embedded YAML to prose narrative) |
| Discussion | not machine-checked; scan for stated ambiguities/assumptions/tradeoffs that should instead be reflected as a rule, scope exclusion, or `conflict_resolution` note |

## Schema Compliance

- [ ] `constitution.yml` validates against `schema.json`
- [ ] `scope.domain`/`scope.contexts`/`scope.exclusions`, if present, don't
      contradict any individual rule's `text` (e.g. a rule addressing
      `emergency_medical_response` when `scope.exclusions` lists it)
- [ ] `rules[].examples.positive`/`.negative`, if present, actually illustrate the
      rule's `text` — flag an example that reads as generic or unrelated
- [ ] `rules[].evaluation_tags`, if present, are consistent in naming style across
      rules in the same constitution (not blocking; a should-fix)
- [ ] `conflict_resolution`, if present, actually resolves conflicts implied by the
      rules' `priority` values — flag if two `high`-priority rules could plausibly
      conflict and `conflict_resolution` doesn't address the ordering

## Normative Coherence (constitution-specific)

Unlike a scenario or task, a constitution's primary risk is **internal
contradiction between rules**, not prose/YAML drift:

- [ ] No two rules directly contradict (one `must` and another `must_not` covering
      the same concrete action)
- [ ] `must_not` rules read as genuine prohibitions, not restated `must` rules with
      inverted phrasing
- [ ] Rule `priority` roughly tracks the charter principles a rule traces to, if the
      `rationale` cites one (e.g. a rule the `rationale` ties to P1 Safety should not
      be `priority: low` without explicit justification)

## Completeness (template.md "Normative Payload" required content)

- [ ] `id`, `name`, `state` present in the fenced YAML
- [ ] At least one rule with `id`/`text`/`type`/`priority`
- [ ] STATUS block present with a `- **STATE:**` first bullet (see
      `src/prosoc/prnc/scenarios/workflow.md`'s Status Section Template)

Optional-but-recommended (`scope`, `rules[].rationale`/`.examples`/`.evaluation_tags`,
`conflict_resolution`, `## Discussion`): if blank, decide reasonably blank vs. should
probably be filled in now — a constitution with rules but no `rationale` anywhere is
usually a should-fix, since traceability to charter principles is part of what makes
a constitution auditable.
