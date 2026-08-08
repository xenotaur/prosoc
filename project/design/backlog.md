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
| `food_delivery` (scenario, name unconfirmed) | `scenarios/crash_cart`'s Table 3 entry cites "Food Delivery" as its related scenario, but no such card exists — the card's own `related_scenarios` substitutes `object_handover` instead, and its own Notes section discusses both | 2026-08-02 | open |
| `leave_group` (scenario, name unconfirmed) | `scenarios/join_a_group`'s Table 3 entry cites "Leaving a Group" as its related scenario, but no such card exists — the card's own `related_scenarios` substitutes `crowd_navigation` instead | 2026-08-02 | open |
| `narrow_arch` (scenario, name unconfirmed) | `scenarios/narrow_doorway`'s Table 3 entry cites "Narrow Arch" as its related scenario, but no such card exists — the card's own `related_scenarios` substitutes `blind_corner`/`entering_room`/`exiting_room` instead | 2026-08-02 | open |
| `robot_courier` (scenario, name unconfirmed) | `scenarios/object_handover`'s Table 3 entry cites "Robot Courier" as its related scenario, but no such card exists — the card's own `related_scenarios` substitutes `crash_cart` instead | 2026-08-02 | open |
| `circular_crossing` (scenario) | `scenarios/parallel_traffic`'s Table 3 entry cites "Circular Crossing" as its related scenario — a Figure 7 variant with no implemented scenario directory; the card's own `related_scenarios` substitutes `perpendicular_traffic`/`crowd_navigation` instead | 2026-08-02 | open |
| `down_path` (scenario, name unconfirmed) | `scenarios/pedestrian_overtaking`'s Table 3 entry cites "Down Path" as its related scenario, but no such card exists — the card's own `related_scenarios` substitutes `robot_overtaking` instead | 2026-08-02 | open |
| `accompany_peer` (scenario) | `scenarios/following`'s Table 3 entry cites "Accompany Peer" as its related scenario — a Figure 7 variant with no implemented scenario directory; the card's own `related_scenarios` substitutes `leading` instead | 2026-08-07 | open |
| `tour_guide` (scenario, name unconfirmed) | `scenarios/leading`'s Table 3 entry cites "Tour Guide" as its related scenario, but no such card exists — the card's own `related_scenarios` substitutes `following` instead | 2026-08-07 | open |

`entering_elevator`/`exiting_elevator` are additionally two of the P&G
paper's own Figure 7 scenarios ("doorway variants for elevators") with no
Table 3 metadata — per `.claude/skills/_shared/pg_scenarios.md`'s
"Additional Scenarios (Figure 7, not in Table 3)" section, they'd need to
be extrapolated carefully from the paper's descriptions and Figure 7
directly, not drafted from a Table 3 row the way most other scenarios in
this corpus were.

## Potential new scenario cards: narrow-doorway / intersection cross-pollination

Noted 2026-08-02 (user-directed) while reviewing `scenarios/narrow_doorway`:
the intersection family (`intersection_no_gesture`,
`intersection_gesture_proceed`, and by implication a not-yet-seen
"intersection gesture wait" variant) shares the same core structural
challenge as Narrow Doorway — two agents approaching a shared bottleneck
that only one can occupy at a time, resolved via gesture or its absence.
Worth exploring both:

- **Cross-references**: consider whether `narrow_doorway`'s
  `related_scenarios` should also point to the intersection family (and
  vice versa), even though the geometric layouts differ (room-and-door
  vs. open intersection) — the sequencing/right-of-way logic is
  structurally analogous.
- **New scenario variants**: the intersection family's gesture-based
  distinctions (no gesture / gesture-then-proceed) suggest analogous
  doorway variants not currently in the corpus:
  - `narrow_doorway_no_gesture` — no explicit signal, right-of-way
    resolved implicitly (as the current `narrow_doorway` card already
    models)
  - `narrow_doorway_gesture_proceed` — one party gestures the other
    through
  - `narrow_doorway_gesture_wait` — one party gestures the other to wait
  - `narrow_doorway_hold_the_door` — a distinct social variant where one
    party actively holds the door open for the other, rather than merely
    yielding right-of-way

None of these have Table 3 entries — they'd be corpus-original
extensions by analogy, similar to how Figure 7 scenarios are handled, not
drafted from a Table 3 row. Not yet scoped as a work item.

## APPROVED cards with unresolved should-fix findings

These cards are already `APPROVED` (`scope: 0` — the review-queue engine
can't offer an `APPROVED` card for promotion, so `prosoc-card-review-all`
will never revisit it), but their most recent `audit.md` still carries
should-fix findings from before they were approved. `AUDITED`'s bar is a
passing verdict (`ready`/`ready_with_fixes`), not zero findings, so this
isn't a process violation — but the findings themselves were never
actually fixed, and nothing in the current workflow ever routes back to an
already-`APPROVED` card to clean them up. (`charter` was tracked here
2026-08-02 through 2026-08-06 after reverting from `APPROVED` to `EDITED`
for an unrelated content update; its should-fix findings were fully
resolved by 2026-08-06 and its row removed — see `prosoc/charter/audit.md`
for the current clean-pass report.)

| Card | Findings (from audit.md, date noted) | Noted | Status |
|---|---|---|---|
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
| `scenarios/object_handover` | "avoid collision with the human during approach" — nearest prose item ("startles the human or resembles an unrelated close pass") implies but doesn't name collision risk | 2026-08-02 |
| `scenarios/parallel_traffic` | "avoid collision with any pedestrian in the stream" — closest prose items address pace/weaving/overtake, not collision directly | 2026-08-02 |
| `scenarios/following` | "avoid collision with the human, other pedestrians, and obstacles" — closest prose item ("cutting through obstacles or other pedestrians to preserve following distance") is about cutting through, not collision directly | 2026-08-07 |
| `scenarios/leading` | "avoid collision with the human, other pedestrians, and obstacles" — the other `must` item is covered verbatim in prose, but this one is never stated as its own bullet | 2026-08-07 |

**Task:** once the current `prosoc-card-review-all` pass finishes working
through the cards the review-queue engine currently surfaces as in scope,
do a dedicated backlog-burndown pass across the whole `scenarios` family
checking every card's Normative Expectations section against its
`expected_behaviors.must` list, adding explicit bullets for symmetry with
`should`/`should_not` wherever missing. Noted 2026-08-02 (user-directed),
not yet scoped as a work item.

## Open suggestions on promoted cards (low priority, burndown candidates)

Standing policy (2026-08-02, user-directed): whenever a card is promoted
with open suggestion-level findings still on its audit — even ones that
aren't should-fixes and don't block promotion — record them here, so
they aren't lost once the card's own `audit.md` gets superseded by a
later re-audit. This is the source list for a future comprehensive
backlog-burndown pass across the whole corpus. (The recurring
must-level-prose-gap pattern above has its own dedicated table since it
spans many cards with the same root cause; this table is for
one-off/card-specific suggestions.)

| Card | Suggestion | Noted |
|---|---|---|
| `scenarios/entering_room` | Consider adding P3 (Legibility) to `relevant_principles` — the robot's "waiting" intent arguably needs to be legible to the human, a concern distinct from the already-included P4/P5 politeness/social-competency principles | 2026-08-02 |
| `scenarios/intersection_gesture_proceed` | `expected_behaviors.should`'s "commit promptly to motion after the gesture" has no qualitative anchor for what "prompt" means, which could invite inconsistent labeling across evaluators; optionally clarify in `evaluation_notes` (no numeric threshold) | 2026-08-02 |
| `scenarios/robot_overtaking` | (1) Card specializes P&G Table 3's "Generic" physical environment to "indoor" without noting it's a deliberate narrowing — optionally add a brief note in `evaluation_notes` or Social Navigation Context. (2) `related_scenarios` lists only `pedestrian_overtaking`, but the Notes section names `frontal_approach` and `single_file_hallway` (both implemented) as natural pairings without adding them as formal cross-references | 2026-08-02 |
| `scenarios/frontal_approach` | Missing both optional-but-recommended template sections: "Social Navigation Context" (no dedicated section; `context.social_setting` never narrated in prose) and "Normative Expectations" (rich `expected_behaviors` YAML with no prose restatement) | 2026-08-02 |
| `scenarios/crash_cart` | `agents.humans[0].count: 3` (bystanders) has no prose basis grounding the specific number 3 — unresolved across multiple prior audits; either state an approximate count in prose or note in `evaluation_notes` that it's a reasonable default | 2026-08-02 |
| `scenarios/crowd_navigation` | `related_scenarios` lists `perpendicular_traffic`, but `perpendicular_traffic`'s own `related_scenarios` doesn't reciprocate (only lists `parallel_traffic`/`intersection_no_gesture`) — a one-way reference, inconsistent with the reciprocal-linking pattern every other cross-reference in the corpus follows. Pre-existing on `perpendicular_traffic`'s side, not introduced by `crowd_navigation`'s own promotion; found by independent subagent review on PR #71 | 2026-08-02 |
| `scenarios/exiting_room` | Consider adding P7 (Proactivity) to `relevant_principles` — the scenario names indefinite hesitation/stand-off as an explicit failure mode and unacceptable behavior, a reasonable match for P7's "deadlock or hesitation is the core challenge" criterion, but P7 isn't listed (P3/P5/P6 partially cover related ground) | 2026-08-02 |
| `scenarios/join_a_group` | (1) `agents.humans[0].count: 3` duplicates `attributes.group_size: 3` — redundant, could silently desync on a future edit. (2) Normative Expectations prose omits an explicit bullet for the `must`-level "avoid collision with any group member" (only the O-space-crossing `must` is bulleted). (3) `related_scenarios` lists `crowd_navigation`, but `crowd_navigation` doesn't reciprocate — same one-way-reference pattern as the `crowd_navigation`/`perpendicular_traffic` gap above | 2026-08-02 |
| `scenarios/movable_obstruction` | `evaluation_notes`'s task/context cross-reference names all three contexts (`routine_delivery`, `guidance_docent`, `high_urgency`) as illustrative options, but doesn't carry forward the source paper's (Francis, PRNC, §4.2.2) specific behavioral implication for `emergency.high_urgency` — neither remove nor report, just prioritize timely task completion. Optionally add one clause to `evaluation_notes` for that context. Not a defect; the card doesn't misstate anything, just less specific than the source on this one point | 2026-08-06 |
| `scenarios/pedestrian_overtaking` | (1) Card specializes P&G Table 3's "Generic" physical environment to "indoor" without noting it's a deliberate narrowing — same pattern as `robot_overtaking`. (2) `expected_behaviors.must`'s "avoid impeding the pedestrian's overtaking maneuver" is only loosely paraphrased in prose ("forces the pedestrian to take evasive action"), not explicitly bulleted | 2026-08-02 |

## Tooling

- **Update `prosoc-card-audit`/`prosoc-card-review`/`prosoc-card-review-all`
  to use this backlog directly.** Right now a missing forward reference is
  just prose in that card's `audit.md` (or, before this note, not tracked
  anywhere at all) — the skills should append a row to this file's table
  automatically when they notice one, and consult it rather than relying on
  ad-hoc notes in individual audit reports. Noted 2026-08-01, not yet
  scoped as a work item.

## LRH card-architecture reuse assessment — not yet warranted

**Noted:** 2026-08-03 (user-directed design session), assessing whether
`prosoc/packet/` + `prosoc/literate/` + `prosoc/utils/cards/` +
`prosoc/auditor/` could be split out as a reusable library for a second
consumer — specifically `LogicalRoboticsHarness`, whose own
`project/principles/`/`project/guardrails/` governance is growing as
agent-harness support (Claude Code, Codex, Antigravity) and
`/lrh-execute` autonomy/review-cycle structure deepen.

**Idea:** A full engine survey found most of prosoc's normative-card
machinery already domain-agnostic — `prosoc/literate/`,
`prosoc/packet/gate.py`, `prosoc/packet/manifest.py`,
`prosoc/packet/resolve.py`, and all of `prosoc/auditor/` have zero
family-specific branching. The one genuinely domain-coupled piece is
`prosoc/packet/assemble.py`'s principle-union composition
(`_principle_union`, lines 64-107; `_tensions`, lines 110-126), plus the required
`guidance.principles`/`guidance.tensions` fields it bakes into
`prosoc/packet/schema.json:108-136` — that's the part any second consumer
would need to replace, not reuse. `prosoc/manifests/schema.json:50-59`
also closed-enums prosoc's own five family names directly, a second sharp
coupling point.

LRH was audited as the candidate second consumer. Its current
`project/principles/`+`project/guardrails/` content is small (7 files, 53
guidance units, 188 lines per `wc -l`) and structurally unconsumed by any LRH
tooling — `src/lrh/assist/snapshot_cli.py`'s `summarize_file()` only
treats it as opaque frontmatter-plus-prose, and a same-named
`src/lrh/guardrails/` Python package that looks like it should enforce
these rules is an unconnected no-op skeleton. LRH's real emerging
complexity — autonomy/review-cycle gating for `/lrh-execute` — is already
served by its own working, self-amending `project/memory/decisions/DEC-*.md`
decision-record pattern and per-assistant `kind:`-tagged policy files,
unrelated to this architecture. Harness differentiation is real and
shipped for Claude/Codex (`src/lrh/skills/installer.py`'s `SkillTarget`
enum and per-target renderers), with Antigravity tracked separately as
proposed, not-yet-shipped work — but either way it lives at LRH's
skill-installer layer, not in guidance content.

Checked against best-practice sources: one worked example (prosoc itself)
is short of the usual Rule-of-Three threshold for safely abstracting a
shared interface (Fowler/Roberts); `assemble.py`'s own
`if card.family == "constitutions"` branching is already a live instance
of Sandi Metz's "wrong abstraction" warning sign — *"if you find yourself
passing parameters and adding conditional paths through shared code, the
abstraction is incorrect"* (sandimetz.com, 2016) — worth fixing on its own
terms regardless of any extraction.

**Status:** Not proposing extraction now. Revisit at a future backlog
burndown if LRH's needs firm up — full trigger list recorded in the
sibling `logical_robotics_harness` repo's own `project/design/backlog.md`
§ "Card-architecture reuse assessment (prosoc) — not yet warranted".
Independently of that: worth unifying `prosoc/packet/loader.py`'s
`FAMILIES` dict with `prosoc/utils/cards/validate_status.py`'s separate,
duplicate `Family`/`FAMILIES` dict — that's a real duplication today and
doesn't need a second consumer to justify fixing.

**Related:** `prosoc/packet/assemble.py`, `prosoc/packet/loader.py:69-80`,
`prosoc/packet/schema.json:108-136`, `prosoc/manifests/schema.json:50-59`,
`prosoc/utils/cards/validate_status.py`; mirrored entry in the sibling
`logical_robotics_harness` repo's own `project/design/backlog.md`.
