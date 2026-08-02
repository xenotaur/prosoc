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
| `guidance.accessibility_sensitive` | `contexts/guidance_docent` (`related_contexts`; added to YAML 2026-08-02 to match prose, per PR #68 code review) | 2026-08-01 | open |
| `environment.child_centric` | `contexts/public_navigation` (`related_contexts`) | 2026-08-01 | open |
| `environment.dense_crowd` | `contexts/public_navigation` (`related_contexts`) | 2026-08-01 | open |
| `workplace.formalized_service` | `contexts/routine_delivery` (`related_contexts`) | 2026-08-01 | open |
| `package_delivery_office` (scenario) | `tasks/deliver_object` (`example_scenarios`) | 2026-08-01 | open |
| `handoff_to_human_corridor` (scenario) | `tasks/deliver_object` (`example_scenarios`) | 2026-08-01 | open |
| `pickup_and_deliver_shelf_to_desk` (scenario) | `tasks/deliver_object` (`example_scenarios`) | 2026-08-01 | open |
| `group_following_open_space` (scenario) | `tasks/navigate_follow_agent` (`example_scenarios`; sibling entry `human_following_corridor` swapped for the real `following` scenario 2026-08-02) | 2026-08-02 | open |
| `entering_elevator` (scenario) | `scenarios/entering_room`'s Table 3 entry cites this as its related scenario, but no such card exists — the card's own `related_scenarios` substitutes `exiting_room`/`narrow_doorway` instead | 2026-08-02 | open |
| `exiting_elevator` (scenario) | `scenarios/exiting_room`'s Table 3 entry cites this as its related scenario, same gap as above | 2026-08-02 | open |
| `ped_obstruct` (scenario, name unconfirmed) | `scenarios/frontal_approach`'s Table 3 entry cites "Ped. Obstruct" as its related scenario, but no such card exists — the card's own `related_scenarios` substitutes `blind_corner`/`movable_obstruction`/`single_file_hallway` instead | 2026-08-02 | open |

`entering_elevator`/`exiting_elevator` are additionally two of the P&G
paper's own Figure 7 scenarios ("doorway variants for elevators") with no
Table 3 metadata — per `.claude/skills/_shared/pg_scenarios.md`'s
"Additional Scenarios (Figure 7, not in Table 3)" section, they'd need to
be extrapolated carefully from the paper's descriptions and Figure 7
directly, not drafted from a Table 3 row the way most other scenarios in
this corpus were.

## APPROVED cards with unresolved should-fix findings

These cards are already `APPROVED` (`scope: 0` — the review-queue engine
can't offer them for promotion, so `prosoc-card-review-all` will never
visit them again), but their most recent `audit.md` still carries
should-fix findings from before they were approved. `AUDITED`'s bar is a
passing verdict (`ready`/`ready_with_fixes`), not zero findings, so this
isn't a process violation — but the findings themselves were never
actually fixed, and nothing in the current workflow ever routes back to
an already-`APPROVED` card to clean them up.

| Card | Findings (from audit.md, 2026-07-29) | Noted | Status |
|---|---|---|---|
| `charter` | 1. Six of ten principles lack a "### Explanation" subsection. 2. Some principles' YAML `description` states content absent from prose. | 2026-08-02 | open |
| `contexts/high_urgency` | 1. Common tension wording drift. 2. `related_contexts` prose/YAML mismatch. | 2026-08-02 | open |
| `tasks/navigate_lead_agent` | 1. Common failure mode omitted or softened in YAML. 2. Dangling `example_scenarios` entries. | 2026-08-02 | open |

## Scenario `cited_in` fields are bare reference numbers

Every scenario card's `cited_in` field (and its "Cited In" prose bullet)
carries bare numeric indices copied verbatim from the P&G paper's own
citation list (e.g. `intersection_no_gesture`'s `[27, 50, 167]`) rather
than resolvable bibliographic references. `.claude/skills/_shared/pg_scenarios.md`
shows the same pattern is corpus-wide — every scenario sourced from P&G
Table 3 has this. A couple of entries additionally use non-numeric
placeholders ("R@G — Robotics at Google, an internal scenario reference,"
"Various," "this article") that would need their own handling, not just a
number-to-citation lookup.

**Task:** go through every scenario card and replace each bare number with
a full reference (BibTeX entry or equivalent structured citation),
resolved against the P&G paper's own bibliography. Noted 2026-08-02
(user-directed, while reviewing `intersection_no_gesture`), not yet scoped
as a work item. Affects the `scenarios` family only — no other family has
a `cited_in`-equivalent field.

## Recurring: "Normative Expectations" prose omits `must`-level behaviors

A systemic pattern across scenario cards, first noticed 2026-08-02 and
confirmed on four cards so far: the YAML `expected_behaviors.must` list
has 2–3 entries, but the prose "Normative Expectations" ("Acceptable robot
behavior...") section only explicitly bullets the `should` entries plus
one `must` entry — never all of them. The missing `must` items aren't
contradicted or actually absent from the card (the substance usually
shows up elsewhere — in the Overview, `ideal_outcome`, or a failure mode),
but a reader who only skims the prose section and never opens the YAML
would come away without seeing that specific expectation stated as its
own item. Suggestion-level in each individual card's audit (not required
for `AUDITED`), but the recurrence across independently-drafted cards
suggests a systemic drafting habit worth a dedicated pass rather than
one-off mentions.

| Card | Missing `must` item(s) in prose | Noted |
|---|---|---|
| `scenarios/intersection_no_gesture` | "avoid collision with the human at the intersection," "behave conservatively when right-of-way is ambiguous" | 2026-08-02 |
| `scenarios/entering_room` | "avoid collision with the human at the doorway" | 2026-08-02 |
| `scenarios/intersection_gesture_proceed` | "enter and traverse the intersection safely," "avoid collision with the human" | 2026-08-02 |
| `scenarios/robot_overtaking` | "avoid colliding with or startling the pedestrian," "maintain a safe and respectful distance during approach and passing" (only loosely paraphrased, not explicitly bulleted) | 2026-08-02 |

**Task:** once the current `prosoc-card-review-all` pass finishes working
through the cards the review-queue engine currently surfaces as in scope,
do a dedicated backlog-burndown pass across the whole `scenarios` family
checking every card's Normative Expectations section against its
`expected_behaviors.must` list, adding explicit bullets for symmetry with
`should`/`should_not` wherever missing. Noted 2026-08-02 (user-directed),
not yet scoped as a work item.

## Optional principle-selection suggestions (single-card, low priority)

Individual audits sometimes surface an optional "consider adding principle
X" suggestion that isn't a defect (the current `relevant_principles`
selection is already valid and within the 3–5 guidance) but is worth a
human editor's judgment call. Tracked here so they aren't lost once the
card's own audit.md gets superseded by a later re-audit.

| Card | Suggestion | Noted |
|---|---|---|
| `scenarios/entering_room` | Consider adding P3 (Legibility) to `relevant_principles` — the robot's "waiting" intent arguably needs to be legible to the human, a concern distinct from the already-included P4/P5 politeness/social-competency principles | 2026-08-02 |

## Tooling

- **Update `prosoc-card-audit`/`prosoc-card-review`/`prosoc-card-review-all`
  to use this backlog directly.** Right now a missing forward reference is
  just prose in that card's `audit.md` (or, before this note, not tracked
  anywhere at all) — the skills should append a row to this file's table
  automatically when they notice one, and consult it rather than relying on
  ad-hoc notes in individual audit reports. Noted 2026-08-01, not yet
  scoped as a work item.
