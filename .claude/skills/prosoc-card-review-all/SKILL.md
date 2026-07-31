---
name: prosoc-card-review-all
description: >
  Walk the prosoc normative card corpus in priority order, reviewing and
  optionally promoting each card one lifecycle step. Calls
  scripts/validate/review-queue for a deterministic ranked worklist
  (severity from audit findings, scope from distance to APPROVED — a card
  with no audit.md at all ranks first), then invokes prosoc-card-review per
  card so each promotion gets its own human confirm gate. Branches, commits
  the session's promotions, and opens a PR, mirroring
  prosoc-card-audit-all's git-action pattern. Use when a human wants to
  work through the corpus (or a family within it) in a structured,
  priority-ordered session rather than naming one card at a time.
---

# prosoc-card-review-all Skill

This skill orchestrates `prosoc-card-review` across the corpus (or a
family within it), using the deterministic review-queue engine
(`prosoc/utils/cards/review_queue.py`, exposed via
`scripts/validate/review-queue`) to decide review order instead of leaving
it to ad-hoc human judgment. It does not reimplement or fork any part of
`prosoc-card-review`'s logic — it dispatches to it, one card at a time, and
aggregates the session's outcome.

Like `prosoc-card-audit-all`, this skill does take git actions on its own
(branch, commit, PR) — a review session naturally produces a batch of
related promotions that belong in one reviewable unit, and
`prosoc-card-approve`/`prosoc-card-review` deliberately do not take git
actions themselves so they stay usable standalone inside any existing
branch.

---

## Inputs

Optional:

- **One family name** (`scenarios`, `tasks`, `contexts`, `constitutions`,
  `charter`, `manifests`). If omitted, the queue spans all six.
- **`--limit N`** — review at most the top `N` queued cards this session,
  rather than the whole queue. Recommended for a first run or a short
  session; omit to walk everything the queue returns.
- **`--sort` / `--order`** — passed through to `scripts/validate/review-queue`
  verbatim if the user wants a different priority ordering than the
  engine's default (`severity,scope` both descending). Most sessions
  should use the default.

---

## Reference Knowledge

This skill does not duplicate `prosoc-card-review`'s reference material —
each dispatched review loads that skill's own reference set. Load directly:

1. **`prosoc/utils/cards/review_queue.py`** module docstring / `scripts/validate/review-queue`
   `--help` — the engine's field meanings (`severity`, `scope`, `has_audit`),
   needed to present the queue meaningfully at Step 3.

---

## Execution Steps

### 1. Branch off main

```bash
git checkout main
git pull
git checkout -b <branch-prefix>/review-cards-<YYYY-MM-DD>
```

`<branch-prefix>` follows whatever branch naming convention this repo
already uses (check recent branches with `git branch -r` or `git log --all
--oneline`; not a fixed value). Use today's date to avoid colliding with a
still-open prior review-all branch/PR. If `main` has local uncommitted
changes that would be clobbered, stop and report — do not stash or discard
anything without asking.

### 2. Get the ranked queue

```bash
scripts/validate/review-queue [--family <name>] --format json
```

Parse the JSON worklist. If `--limit` was given, take the top `N` entries
after the engine's own sort (do not re-sort client-side — the engine's
ordering, including its severity/scope weighting and family/id tiebreak,
is the authoritative ranking).

If the queue is empty (e.g. `--family` scoped to a family with zero
cards), report that and stop.

### 3. Present the plan

Show the user the ranked worklist before reviewing anything — family, id,
current state, scope, severity, and whether each card has an audit at all
(a missing-audit card sorts first and is worth calling out explicitly,
since it will trigger `prosoc-card-audit` inside `prosoc-card-review`
before that card's own recommendation can be formed).

This is context, not a blocking confirm gate — the per-card gate lives
inside each `prosoc-card-review` invocation. But if the queue is large,
confirm with the user how many cards they want to work through this
session before starting (this may already be answered by `--limit`).

### 4. Walk the queue

For each `{family, id}` pair in ranked order, invoke `prosoc-card-review`
exactly as it would run standalone — full audit-currency check,
independent recommendation, confirm gate, and (on approval) delegation to
`prosoc-card-approve`. Record each card's outcome: promoted (with the
transition performed), held (with reason), or skipped (audit ineligible —
e.g. `verdict: not_ready` — surfaced by `prosoc-card-review` itself).

**Stop early if the user indicates they want to** (e.g. "that's enough for
today," "stop here") — report progress on the cards reviewed so far rather
than forcing the full queue.

### 5. Aggregate

Build a summary table:

| Family | Card | Before | After | Outcome |
|---|---|---|---|---|

Plus totals: cards reviewed, cards promoted (broken down by transition:
`→AUDITED` vs `→APPROVED`), cards held, cards skipped (with reasons).

### 6. Optional end-of-session snapshot

Offer (do not write automatically) an end-of-session Markdown snapshot at
`project/audits/CARD_REVIEW_SUMMARY.md` (regenerated wholesale each run,
mirroring `AUDIT_SUMMARY.md`'s point-in-time convention — not a
continuously-live queue; see `PROP-NORMATIVE-CARD-APPROVAL` Decision 4).
If the user wants one, write Step 5's table plus the run's scope
(family/limit/sort used) and date.

### 7. Commit

Stage every card file this session actually changed: each promoted card's
Markdown + distilled YAML, any `audit.md` files created or refreshed while
reviewing cards, plus the optional snapshot from Step 6. Do not stage
anything else — if `git status` shows unrelated changes, stop and ask
rather than sweeping them in. Skip the commit/PR steps only if the session
left no file changes at all; if cards were held but audit evidence was
created or refreshed, commit that audit work and open the PR.

### 8. Push and open the PR

Push the branch and open a PR whose body is Step 5's summary table plus
totals, and a test plan confirming: no normative content was edited on any
card (only `state:` fields and their two projections), and every promotion
this session had an explicit human confirmation recorded in the
conversation.

### 9. Report to the user

Tell the user:

- The branch name and PR URL (or, if no card was promoted, that no PR was
  opened and why)
- Total cards reviewed this session, broken down by outcome
- Whether the queue was fully walked or stopped early, and how many cards
  remain unreviewed
- Whether the optional snapshot (Step 6) was written

---

## Quality Checklist

Before reporting completion, verify:

- [ ] The review order came from `scripts/validate/review-queue`'s output,
      not ad-hoc or re-sorted client-side
- [ ] Every card reviewed went through `prosoc-card-review`'s own full
      procedure (audit-currency check, independent recommendation, confirm
      gate) — none were promoted by skipping straight to
      `prosoc-card-approve`
- [ ] No card's normative content was edited anywhere in this session
- [ ] The commit contains only card files actually promoted this session
      plus the optional snapshot — nothing swept in from `git status`
- [ ] A no-promotion session skipped the commit/PR steps rather than
      opening an empty PR
- [ ] The PR body's summary table matches the session's actual outcomes

---

## What This Skill Does Not Do

- Does not reimplement, fork, or bypass `prosoc-card-review`'s or
  `prosoc-card-approve`'s logic — every per-card outcome comes from an
  unmodified invocation of `prosoc-card-review`.
- Does not compute its own ranking — always defers to
  `scripts/validate/review-queue`.
- Does not force a full-queue walk — the user may stop early, and
  `--limit` bounds the session explicitly.
- Does not edit any card's normative content.
- Does not merge or approve the PR it opens — that remains a human
  decision.
- Does not maintain a continuously-live dashboard — the optional Step 6
  snapshot is a point-in-time record, regenerated wholesale on request,
  never auto-updated between sessions.
