---
resolution: 'Implemented and merged in PR #148 (commit 0544d955a8625da48d35cf1af82d6e42f7e54bdf).'
blocked_reason: null
blocked: false
id: WI-CARD-AUDIT-BACKLOG-SYNC
title: "Teach prosoc-card-audit/-review/-review-all to sync findings into backlog.md"
type: deliverable
status: resolved
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
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - promote_card_state
  - edit_card_normative_content
  - implement_backlog_burndown
acceptance:
  - "Running prosoc-card-audit against a card with a missing forward-referenced related_contexts/related_scenarios/example_scenarios entry appends a row to backlog.md's 'Missing forward-referenced cards' table in addition to (not instead of) noting it in the card's own audit.md"
  - "Running prosoc-card-review or prosoc-card-review-all against a card being promoted to APPROVED with an unresolved should-fix/suggestion finding appends a row to backlog.md's 'APPROVED cards with unresolved findings' table"
  - "Running prosoc-card-review or prosoc-card-review-all against a card promoted with open suggestion-level findings appends a row to backlog.md's 'Open suggestions on promoted cards' table, per the existing 2026-08-02 standing policy"
  - "Re-running prosoc-card-audit against the same card and the same missing-reference finding does not append a duplicate row to the 'Missing forward-referenced cards' table"
  - "Dedup for the two promotion-based tables is verified against an isolated fixture with a matching row pre-seeded before an eligible promotion, not via a literal re-run -- prosoc-card-review's own Step 3 stops immediately on an already-APPROVED card, before any append logic runs"
  - "prosoc-card-audit-all's Step 8 commit step and Quality Checklist are updated to permit project/design/backlog.md among staged files when a per-card prosoc-card-audit run generates a backlog append, so a bulk audit that discovers a trackable finding is not blocked by the wrapper's own 'audit.md and summary files only' contract"
  - "prosoc-card-review-all's Step 7 commit step and Quality Checklist are updated the same way, so a bulk review-and-promote session that triggers Required Change 2 or 3 is not blocked by its own 'nothing swept in from git status' contract"
  - "Existing hand-authored rows in all three tables are preserved verbatim"
  - "Each card's own audit.md remains self-contained -- no Required Change shortens or removes audit.md findings in favor of the backlog.md row"
  - "lrh validate reports 0 errors"
required_evidence:
  - manual_review
  - lrh_validate
  - test_output
artifacts_expected:
  - .claude/skills/prosoc-card-audit/SKILL.md
  - .claude/skills/prosoc-card-audit-all/SKILL.md
  - .claude/skills/prosoc-card-review/SKILL.md
  - .claude/skills/prosoc-card-review-all/SKILL.md
  - project/design/backlog.md
---

# WI-CARD-AUDIT-BACKLOG-SYNC

## Summary

Teach `prosoc-card-audit`, `prosoc-card-review`, and `prosoc-card-review-all`
to append a row to the matching table in `project/design/backlog.md` when
they encounter one of three tracked conditions — a missing
forward-referenced card, an APPROVED card with an unresolved finding, or a
promoted card with an open suggestion — **in addition to** each card's own
self-contained `audit.md`, so cross-card findings are also tracked
centrally instead of only being discoverable one `audit.md` at a time.

## Problem / Context

`project/design/backlog.md` already holds three hand-maintained Markdown
tables that these three skills' findings logically belong in:

- "Missing forward-referenced cards" — cards whose `related_contexts`,
  `related_scenarios`, or `example_scenarios` point at a card that does not
  yet exist.
- "APPROVED cards with unresolved findings" — a card promoted to APPROVED
  while a should-fix/suggestion finding from its review was never
  addressed.
- "Open suggestions on promoted cards" — suggestion-level findings left
  open on a promoted card, per the standing 2026-08-02 policy already
  recorded in backlog.md.

Today, `prosoc-card-audit` records all of this only in the card's own
`audit.md`, and `prosoc-card-review`/`prosoc-card-review-all` only act on
that same per-card file plus whatever lifecycle note they write when
promoting. Nothing currently rolls these up into backlog.md, so seeing the
full set of (for example) all APPROVED cards with an unresolved finding
requires opening every card's `audit.md` by hand. Each card's `audit.md`
is intended to stay self-contained — it must keep describing that card's
findings fully on its own — so this work item is additive only: it never
removes, shortens, or replaces anything in `audit.md` in favor of a
backlog.md row.

**Prior-art check (duplication search):** `src/lrh/control/validator.py`
has zero references to `backlog`, and the full `lrh` CLI surface
(`validate`, `design organize`, `work-items {organize,validate,audit,
readiness}`, etc.) has no subcommand that edits a free-form Markdown table
in a convention file — `backlog.md` is explicitly outside LRH's control
plane by design. No existing prosoc script performs this sync either
(confirmed by listing `scripts/`). No duplication found.

**Prior-art check (demand search):** backlog.md item #7 (the entry this
work item scopes) is the only existing request for this capability; no
other open work item, proposal, or backlog row asks for the same thing.

## Scope

In scope: the three named skills (`prosoc-card-audit`, `prosoc-card-review`,
`prosoc-card-review-all`), the three named backlog.md tables, and the
staging/checklist steps of both bulk-wrapper skills —
`prosoc-card-audit-all` (wraps `prosoc-card-audit` unmodified per card)
and `prosoc-card-review-all` (wraps `prosoc-card-review` unmodified per
card) — to the extent needed to let a wrapped skill's backlog append
reach the PR either wrapper opens. Today, both wrappers' own commit steps
and Quality Checklists restrict staging to card/audit/summary files only
and treat anything else as unrelated — a restriction that would silently
block the backlog appends this work item adds to the skills they wrap.
Out of scope: any other skill, any other backlog.md section, and any
change to `audit.md`'s own format or content.

## Required Changes

1. In `prosoc-card-audit`, when the audit finds a missing
   forward-referenced card, append a row to backlog.md's "Missing
   forward-referenced cards" table in addition to noting it in the card's
   own self-contained `audit.md` — never replacing or removing the
   `audit.md` note.
2. In `prosoc-card-review` and `prosoc-card-review-all`, when a card is
   promoted to APPROVED while a should-fix/suggestion finding remains
   unresolved, append a row to backlog.md's "APPROVED cards with
   unresolved findings" table, in addition to the existing per-card
   record of that finding.
3. In `prosoc-card-review` and `prosoc-card-review-all`, when a card is
   promoted with an open suggestion-level finding, append a row to
   backlog.md's "Open suggestions on promoted cards" table, consistent
   with the existing 2026-08-02 standing policy already described in
   backlog.md.
4. Define and apply one dedupe key per table (card path + finding
   description, or equivalent) so re-running an audit/review against a
   card whose finding is already tracked does not append a duplicate row.
5. In `prosoc-card-audit-all`, update Step 8's commit step and the Quality
   Checklist so `project/design/backlog.md` is permitted (not flagged as
   unrelated) among staged files whenever a per-card `prosoc-card-audit`
   run in its fan-out generated a backlog append — its own commit step
   today reads "Do not stage anything else" and its checklist reads "The
   commit contains only `audit.md` files and the summary file(s)," both of
   which would block or flag a backlog row produced by Required Change 1.
6. In `prosoc-card-review-all`, update Step 7's commit step and the
   Quality Checklist the same way — its own commit step today reads
   "Stage every card file this session actually changed ... Do not stage
   anything else" and its checklist reads "nothing swept in from `git
   status`," both of which would block or flag a backlog row produced by
   Required Change 2 or 3 during a bulk review-and-promote session. This
   is the identical bug class as item 5, on the sibling wrapper skill
   `prosoc-card-review-all` is explicitly named as a direct actor for in
   Required Changes 2 and 3 above.

## Non-Goals

- Does not change `audit.md`'s format, content, or self-contained nature.
- Does not remove or shorten a card's `audit.md` findings in favor of the
  backlog.md row — each card's `audit.md` stays self-contained; the
  backlog row is additive, not a substitute.
- Does not build generic LRH tooling for editing arbitrary Markdown
  tables — this is a scoped, prosoc-local append helper for these three
  specific tables only (see backlog.md's "Tooling" note for why a
  generic primitive is not yet warranted).
- Does not implement a backlog-burndown or auto-resolution mechanism — it
  only appends; removing or resolving a row stays a human/editorial
  decision, as it is today.

## Acceptance Criteria

- Running `prosoc-card-audit` against a card with a missing
  forward-referenced `related_contexts`/`related_scenarios`/
  `example_scenarios` entry appends a row to backlog.md's "Missing
  forward-referenced cards" table in addition to (not instead of) noting
  it in the card's own `audit.md`.
- Running `prosoc-card-review` or `prosoc-card-review-all` against a card
  being promoted to APPROVED with an unresolved should-fix/suggestion
  finding appends a row to backlog.md's "APPROVED cards with unresolved
  findings" table.
- Running `prosoc-card-review` or `prosoc-card-review-all` against a card
  promoted with open suggestion-level findings appends a row to
  backlog.md's "Open suggestions on promoted cards" table, per the
  existing 2026-08-02 standing policy.
- Re-running `prosoc-card-audit` against the same card and the same
  missing-reference finding does not append a duplicate row to the
  "Missing forward-referenced cards" table.
- Dedup for the two promotion-based tables is verified against an
  isolated fixture with a matching row pre-seeded before an eligible
  promotion, not via a literal re-run — `prosoc-card-review`'s own Step 3
  stops immediately on an already-APPROVED card, before any append logic
  runs, so a literal re-run would never actually exercise the dedupe key.
- `prosoc-card-audit-all`'s Step 8 commit step and Quality Checklist are
  updated to permit `project/design/backlog.md` among staged files when a
  per-card `prosoc-card-audit` run generates a backlog append.
- `prosoc-card-review-all`'s Step 7 commit step and Quality Checklist are
  updated the same way, so a bulk review-and-promote session that
  triggers Required Change 2 or 3 is not blocked by its own "nothing
  swept in from `git status`" contract.
- Existing hand-authored rows in all three tables are preserved verbatim.
- Each card's own `audit.md` remains self-contained — no Required Change
  shortens or removes `audit.md` findings in favor of the backlog.md row.
- `lrh validate` reports 0 errors.

## Validation

- `lrh validate`
- Manual run of `prosoc-card-audit` against a card with a known missing
  forward reference; diff backlog.md to confirm the new row and an
  unchanged `audit.md` note.
- Manual run of `prosoc-card-review`/`prosoc-card-review-all` against a
  card with an unresolved finding being promoted; diff backlog.md to
  confirm the new row.
- Re-run `prosoc-card-audit` a second time against the same missing-
  reference finding; diff backlog.md to confirm no duplicate row was
  appended.
- In an isolated fixture copy of backlog.md, pre-seed a matching row in
  the "APPROVED cards with unresolved findings" (or "Open suggestions on
  promoted cards") table, then run the append logic directly against an
  eligible promotion; diff the fixture to confirm no duplicate row was
  appended. This is a fixture-level test, not a literal skill re-run,
  because `prosoc-card-review` stops on an already-APPROVED card before
  reaching the append step.
- Manual run of `prosoc-card-audit-all` across a small fixture batch that
  includes a card with a missing forward reference; confirm its opened
  PR's commit includes the generated backlog.md row alongside the
  audit.md/summary files, and that its Quality Checklist no longer flags
  this as an unrelated change.
- Manual run of `prosoc-card-review-all` across a small fixture queue
  that includes an eligible promotion triggering an unresolved finding
  or open suggestion; confirm its opened PR's commit includes the
  generated backlog.md row alongside the promoted card files, and that
  its Quality Checklist no longer flags this as swept-in.
- Diff backlog.md's pre-existing rows against their post-change state to
  confirm they are unchanged.

## Risk Notes

The main risk is an append that is scoped too loosely and spills into
adjacent hand-written prose in backlog.md, or a dedupe key that is too
loose (silently swallowing a real new finding) or too strict (producing
duplicate rows). Required Change 4 exists specifically to make the dedupe
key an explicit, reviewable design decision rather than an implementation
afterthought.

A second risk, raised in review: because `prosoc-card-review` stops
before any append logic on a card that is already `APPROVED` or later,
the promotion-table dedupe key can never be exercised by literally
re-running the skill against the same card — the Validation section's
fixture-based test exists specifically to close that gap rather than rely
on a test that cannot actually run the code path it claims to check.
