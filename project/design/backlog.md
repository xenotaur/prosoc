# Design Backlog

Lightweight running list of gaps noticed during normative-card review
sessions that are out of scope for the review itself — things worth doing
later but that shouldn't block or bloat the promotion in progress. Not a
formal LRH artifact (no frontmatter, no lifecycle) — just a durable place
to park findings until someone turns one into a work item.

## Missing forward-referenced cards

Cards sometimes name a `related_contexts` (or similar cross-reference)
entry that doesn't exist yet as an actual card in the corpus. This is
treated as intentional scaffolding, not an audit defect — `prosoc-card-audit`
does not fail a card for it — but it's worth tracking so the gaps get
filled deliberately rather than forgotten.

| Missing id | Referenced by | Noted | Status |
|---|---|---|---|
| `guidance.accessibility_sensitive` | `contexts/guidance_docent` (`related_contexts`) | 2026-08-01 | open |
| `environment.child_centric` | `contexts/public_navigation` (`related_contexts`) | 2026-08-01 | open |
| `environment.dense_crowd` | `contexts/public_navigation` (`related_contexts`) | 2026-08-01 | open |
| `workplace.formalized_service` | `contexts/routine_delivery` (`related_contexts`) | 2026-08-01 | open |
| `package_delivery_office` (scenario) | `tasks/deliver_object` (`example_scenarios`) | 2026-08-01 | open |
| `handoff_to_human_corridor` (scenario) | `tasks/deliver_object` (`example_scenarios`) | 2026-08-01 | open |
| `pickup_and_deliver_shelf_to_desk` (scenario) | `tasks/deliver_object` (`example_scenarios`) | 2026-08-01 | open |

## Tooling

- **Update `prosoc-card-audit`/`prosoc-card-review`/`prosoc-card-review-all`
  to use this backlog directly.** Right now a missing forward reference is
  just prose in that card's `audit.md` (or, before this note, not tracked
  anywhere at all) — the skills should append a row to this file's table
  automatically when they notice one, and consult it rather than relying on
  ad-hoc notes in individual audit reports. Noted 2026-08-01, not yet
  scoped as a work item.
