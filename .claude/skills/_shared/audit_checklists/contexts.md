# Prosoc Context Audit Checklist

This is a verification rubric, companion to `prosoc/contexts/schema.json` and
`prosoc/contexts/template.md`. It explains what to check when auditing an
already-drafted context card. Read `../principles.md` for the P0–P9 definitions
referenced below.

## Required Fields (schema.json)

| Field | Check |
|-------|-------|
| `id` | Matches `^[a-z]+(\.[a-z0-9_]+)+$` (dotted, e.g. `emergency.high_urgency`) |
| `name` | Matches the context's title heading in `context.md` |
| `context_class` | `core` or `derived` — matches the STATUS block's `CONTEXT TYPE` line |
| `primary_robot_role` | A social role, not a task description |
| `applies_to_tasks` | Non-empty; task ids or `"*"` |
| `axes.{cultural,diversity,environmental.{geometric,operational},task,interpersonal}` | All five present and non-empty |
| `principle_emphasis.{emphasized,deprioritized,common_tensions}` | All three present |
| `limits.{includes,excludes}` | Both present |

## Prose/YAML Cross-Checks

| Prose section | Cross-check against YAML field(s) |
|---|---|
| Context Summary | `context_class`, `primary_robot_role`, `applies_to_tasks` |
| Context Axes Instantiated (Cultural/Diversity/Environmental/Task/Interpersonal) | `axes.*` — each subsection should map to its matching `axes` key |
| Relationship to Prosocial Navigation Principles | `principle_emphasis.emphasized`, `principle_emphasis.deprioritized`, `principle_emphasis.common_tensions` |
| Applicability and Limits | `limits.includes`, `limits.excludes` |
| Derived and Related Contexts | `related_contexts` |

Flag a **contradiction** when prose and YAML assert incompatible facts (e.g. prose
says a principle is emphasized but it appears in YAML's `deprioritized` list instead,
or vice versa). Flag **drift** when merely inconsistent in emphasis or detail.

## Schema / Charter Compliance

- [ ] `context.yml` validates against `schema.json` (no `additionalProperties`
      violations; `axes.environmental` has only `geometric`/`operational`;
      `principle_emphasis` has only `emphasized`/`deprioritized`/`common_tensions`;
      `limits` has only `includes`/`excludes`)
- [ ] `principle_emphasis.emphasized` and `.deprioritized` — every entry matches
      `^P[0-9]+$` and is P0–P9 (see `../principles.md`)
- [ ] No principle appears in **both** `emphasized` and `deprioritized` —
      contradictory by construction
- [ ] `principle_emphasis.deprioritized` is an **annotation**, not a removal — per
      `PROP-NORMATIVE-PACKET-ASSEMBLY` Decision 6, a deprioritized principle must
      still be discussed as present, not silently dropped from the context's
      normative picture; flag prose that reads as if a deprioritized principle simply
      does not apply
- [ ] `axes.*` fields stay qualitative/descriptive, not numeric weightings —
      per `template.md`'s own instruction ("motivates *why* principle weightings
      shift, without defining the shifts numerically")

## Completeness (template.md "Required" sections)

- [ ] Context Summary (Context ID, Context Name, Context Class, Primary Role of
      Robot, Applies To Tasks)
- [ ] Context Description
- [ ] Normative Significance
- [ ] Context Axes Instantiated (all five subsections)
- [ ] Relationship to Prosocial Navigation Principles
- [ ] Applicability and Limits

Optional-but-recommended sections (`Derived and Related Contexts`, `Example Scenario
Classes`): if blank, decide reasonably blank vs. should probably be filled in now.
