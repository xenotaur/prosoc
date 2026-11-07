---
family: charter
card: charter
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-11-07
---

# Audit: Prosocial Robot Navigation Charter

- **Card:** `src/prosoc/prnc/charter/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED, no blocking or should-fix issues — one
  low-priority suggestion only.

This is a fresh audit written after `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`
reconciled the Normative Statement/`description` drift the prior 2026-11-07
audit flagged as should-fix (Finding 1). It does not carry forward that
finding's text, since the content it described no longer exists.

## Findings

### Resolved: Normative Statement omitted content the YAML `description` and prose Explanation carried

The prior audit's should-fix Finding 1 (Normative Statement vs. `description`
drift for P1, P2, P4, P5, and P6) is resolved. Re-verified directly against
the current `charter.md`/`charter.yml`:

- **P1 Safety** ([`charter.md:135`](charter.md)): Normative
  Statement now reads "...or themselves. This includes maintaining a safe
  distance unless explicitly invited to approach." — an exact match to
  `description`.
- **P2 Comfort** (`charter.md:166`): Normative Statement now includes "This
  includes refraining from sudden movements or uninvited approaches." — exact
  match to `description`.
- **P4 Politeness** (`charter.md:222`, `:226`, `:232-234`): Normative
  Statement, Explanation, and `description` were all three updated
  consistently, and the previously-unconditional "offering help when asked"
  was hedged to "offering help or at least an acknowledgement when asked" —
  a genuine content correction, not just a backport, since an unconditional
  help obligation conflicted with a robot's actual capability and with P8's
  own crash-cart subordination example (`charter.md:341`). Re-distilled
  (`scripts/distill/charter --dry-run --show-diffs` reports no diff) and
  schema-validated clean.
- **P5 Social Competency** (`charter.md:251`): Normative Statement now
  includes "...avoiding inappropriate behaviors such as interrupting
  conversations or blocking passage." — consistent in substance with
  `description` (Normative Statement retains additional "basic... governing
  shared spaces" framing `description` doesn't carry, a superset, not a
  contradiction).
- **P6 Agent Understanding** (`charter.md:279`): Normative Statement now
  includes "(humans, robots, pets, etc.)" — exact match to `description`.

No new contradiction was introduced by this round of edits; `scripts/distill/charter
--dry-run --show-diffs` (run fresh for this audit, with the correct
`PYTHONPATH` for this checkout) reports no differences.

### Considered and rejected: `principles.md`'s P9 summary row

Unchanged from the prior audit — carried forward since the 2026-11-07 edits
did not touch P9 or `principles.md`. The charter's own P9 Explanation states
the task/context/goals qualifier remains operative ("that bound is expressed
here, in this Explanation, rather than in the statement itself" —
`charter.md`, P9 Explanation); `principles.md`'s retained qualifier is
accurate, not stale. Not a finding.

### 1. P4 and P5 positive examples both illustrate "yielding to people passing" — suggestion
- **Section/field:** P4 Politeness `examples.positive` vs. P5 Social Competency `examples.positive`
- **Issue:** P4's "Robot pauses to let two people pass during their
  conversation" and P5's "Robot waits at the side while people pass in a
  narrow hallway" both depict a robot yielding so people can pass. They are
  not interchangeable on close reading — P4's is about not interrupting a
  conversation (an individual-courtesy angle) while P5's is about following a
  narrow-space queueing norm — but the surface similarity is close enough
  that a reader skimming examples alone could conflate the two principles.
- **Recommended fix:** No action required; optionally sharpen one example's
  wording (e.g., naming the conversational-interruption angle explicitly in
  P4's example) to make the distinction more self-evident without relying on
  the surrounding prose.

## Completeness

- All ten principles (P0–P9) have every schema-required field (`id`, `name`,
  `description`, `severity`, non-empty `examples.positive`/`.negative`) — no
  blanks found. Schema validation (`jsonschema.validate` against
  `schema.json`) passes clean.
- All structural sections required by the checklist are present: `## Status`,
  `## 1. Purpose of This Charter`, `## 2. Definition...`, `## 3. Structure of
  the Principles`, `## 14. Use of This Charter...`, `## Definitions and
  Glossary`, and `## References`.
- Nothing is reasonably-blank or should-fill-in-now — the charter document is
  complete per both the schema and the structural checklist.
