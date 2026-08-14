---
family: constitutions
card: asimov_three_laws
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-29
---

# Audit: Asimov's Three Laws of Robotics

- **Card:** `prosoc/constitutions/asimov_three_laws/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-07-29
- **Verdict:** Ready, one minor suggestion

## Findings

### 1. L3's text says "must" but is typed `should` — suggestion
- **Section/field:** `rules[2]` (L3): `text` vs. `type`
- **Issue:** L3's `text` reads "A robot **must** protect its own existence..."
  (a direct quote of Asimov's original 1942 phrasing), but `type: should` and
  `priority: low`. Taken in isolation, the wording suggests an obligation
  stronger than `should`.
- **Recommended fix:** No change needed for historical fidelity — the
  `should`/`low` classification correctly captures L3's subordination to L1
  and L2 (per `conflict_resolution`'s stated ordering), and rewriting the
  quoted text would break fidelity to the source. Noted only so a future
  reader isn't confused by the literal word "must" alongside `type: should`.

## Prose/YAML Consistency

The Overview and Provenance sections match the card's Asimov/`Generating
Robot Constitutions` sourcing. The embedded Normative Payload YAML matches
`constitution.yml` exactly (re-distilled, see below). Discussion's stated
ambiguities (harm definition, inaction-clause edge cases) and ethical
tradeoffs are consistent with, and do not contradict, the rules themselves.

## Schema and Structural Compliance

- `scripts/distill/constitutions --dry-run --show-diffs` produced no diff and
  no schema validation error (whole-family dry-run; the corpus's other
  constitution showed no drift either).
- Root-wrapped shape confirmed: the fenced YAML's only top-level key is
  `constitution`, matching `constitution.yml`.
- `rules[].id` values (L1, L2, L3) are unique, no duplicates.
- `rules[].type` matches each rule's phrasing: L1 (`must_not`) is a genuine
  prohibition, L2 (`must`, with an explicit First-Law exception clause) is a
  genuine obligation. See Finding 1 for L3.
- `rules[].priority` (high, medium, low for L1/L2/L3) tracks
  `conflict_resolution`'s stated ordering ("L1 overrides L2 and L3; L2
  overrides L3") exactly.
- `rules[].examples.{positive,negative}` are present for all three rules and
  each concretely illustrates its own rule's `text` — no generic or
  unrelated examples.
- No two rules directly contradict; `must_not` (L1) and `must` (L2, with its
  own built-in exception) coexist without conflict, and `conflict_resolution`
  resolves the only case where a conflict is plausible (L1 vs. L2's
  exception).

## Completeness

`id`, `name`, `state` present in the fenced YAML; STATUS block present with a
`- **STATE:**` first bullet. All three rules have `id`/`text`/`type`/
`priority`, plus `rationale`, `examples`, and `evaluation_tags` (all
optional-but-recommended fields are populated, not blank). `scope` and
`conflict_resolution` are both present. `## Discussion` is populated with
known ambiguities, environmental assumptions, and ethical tradeoffs.
